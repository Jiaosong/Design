using System.Text.Json;
using Mono.Cecil;

const string version = "8.32.26160.13001";
var userProfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
var packageRoot = Path.Combine(userProfile, ".nuget", "packages", "grasshopper", version);
if (!Directory.Exists(packageRoot)) throw new DirectoryNotFoundException(packageRoot);
var candidates = Directory.GetFiles(packageRoot, "Grasshopper.dll", SearchOption.AllDirectories);
if (candidates.Length == 0) throw new FileNotFoundException("Grasshopper.dll not found in restored NuGet package.");
var dll = candidates.OrderByDescending(p => new FileInfo(p).Length).First();

using var asm = AssemblyDefinition.ReadAssembly(dll, new ReaderParameters { ReadSymbols = false });
var filters = new[] { "PathMapper", "Path_Mapping", "Param_Number", "ParamViewer", "Param_Viewer", "Graft", "Flatten" };

bool Match(TypeDefinition t) => filters.Any(f =>
    t.FullName.Contains(f, StringComparison.OrdinalIgnoreCase) ||
    t.Name.Contains(f, StringComparison.OrdinalIgnoreCase));

object Describe(TypeDefinition t) => new {
    t.FullName,
    BaseType = t.BaseType?.FullName,
    Interfaces = t.Interfaces.Select(i => i.InterfaceType.FullName).OrderBy(x => x).ToArray(),
    Constructors = t.Methods.Where(m => m.IsConstructor && m.IsPublic).Select(Signature).ToArray(),
    Properties = t.Properties.Select(p => new {
        p.Name,
        Type = p.PropertyType.FullName,
        CanRead = p.GetMethod is not null,
        CanWrite = p.SetMethod is not null,
        GetterPublic = p.GetMethod?.IsPublic ?? false,
        SetterPublic = p.SetMethod?.IsPublic ?? false
    }).OrderBy(p => p.Name).ToArray(),
    Methods = t.Methods.Where(m => m.IsPublic && !m.IsConstructor).Select(Signature).OrderBy(x => x).ToArray()
};

string Signature(MethodDefinition m) =>
    $"{m.ReturnType.FullName} {m.Name}({string.Join(", ", m.Parameters.Select(p => p.ParameterType.FullName + " " + p.Name))})";

TypeDefinition RequireType(string fullName) => asm.MainModule.Types.FirstOrDefault(t => t.FullName == fullName)
    ?? throw new InvalidOperationException("Required API type missing from assembly metadata: " + fullName);

var interesting = asm.MainModule.Types.Where(Match).OrderBy(t => t.FullName).Select(Describe).ToArray();
var componentServer = RequireType("Grasshopper.Kernel.GH_ComponentServer");
var document = RequireType("Grasshopper.Kernel.GH_Document");
var documentIo = RequireType("Grasshopper.Kernel.GH_DocumentIO");
var param = RequireType("Grasshopper.Kernel.IGH_Param");

var api = new {
    ProbeMode = "PE_IL_METADATA_ONLY_NO_GRASSHOPPER_RUNTIME_LOAD",
    Package = "Grasshopper " + version,
    Assembly = asm.Name.FullName,
    AssemblyLocation = dll,
    Types = interesting,
    KnownApis = new {
        FindObjectByName = componentServer.Methods.Where(m => m.Name == "FindObjectByName").Select(Signature).ToArray(),
        EmitObject = componentServer.Methods.Where(m => m.Name == "EmitObject").Select(Signature).ToArray(),
        AddObject = document.Methods.Where(m => m.Name == "AddObject").Select(Signature).ToArray(),
        DocumentIO = documentIo.Methods.Where(m => m.Name is "Open" or "SaveQuiet").Select(Signature).ToArray(),
        DocumentIOConstructors = documentIo.Methods.Where(m => m.IsConstructor).Select(Signature).ToArray(),
        ParamAddSource = param.Methods.Where(m => m.Name == "AddSource").Select(Signature).ToArray(),
        ParamDataMapping = param.Properties.Where(p => p.Name == "DataMapping").Select(p => new { p.Name, Type=p.PropertyType.FullName }).ToArray()
    }
};

Directory.CreateDirectory("sdk_probe_output");
var json = JsonSerializer.Serialize(api, new JsonSerializerOptions { WriteIndented = true });
File.WriteAllText("sdk_probe_output/grasshopper_sdk_metadata.json", json);
Console.WriteLine(json);
