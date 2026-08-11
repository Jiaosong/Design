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
var filters = new[] { "PathMapper", "Param_Number", "ParamViewer", "Graft", "Flatten", "Lexer" };

bool Match(TypeDefinition t) => filters.Any(f =>
    t.FullName.Contains(f, StringComparison.OrdinalIgnoreCase) ||
    t.Name.Contains(f, StringComparison.OrdinalIgnoreCase));

string Signature(MethodDefinition m) =>
    $"{m.ReturnType.FullName} {m.Name}({string.Join(", ", m.Parameters.Select(p => p.ParameterType.FullName + " " + p.Name))})";

object Describe(TypeDefinition t) => new {
    t.FullName,
    BaseType = t.BaseType?.FullName,
    Interfaces = t.Interfaces.Select(i => i.InterfaceType.FullName).OrderBy(x => x).ToArray(),
    Constructors = t.Methods.Where(m => m.IsConstructor).Select(m => new { Signature=Signature(m), m.IsPublic, m.IsFamily, m.IsAssembly }).ToArray(),
    Fields = t.Fields.Select(f => new { f.Name, Type=f.FieldType.FullName, f.IsPublic, f.IsInitOnly, f.IsStatic }).OrderBy(f => f.Name).ToArray(),
    Properties = t.Properties.Select(p => new {
        p.Name,
        Type = p.PropertyType.FullName,
        CanRead = p.GetMethod is not null,
        CanWrite = p.SetMethod is not null,
        GetterPublic = p.GetMethod?.IsPublic ?? false,
        SetterPublic = p.SetMethod?.IsPublic ?? false
    }).OrderBy(p => p.Name).ToArray(),
    Methods = t.Methods.Where(m => !m.IsConstructor).Select(m => new { Signature=Signature(m), m.IsPublic, m.IsFamily, m.IsAssembly }).OrderBy(x => x.Signature).ToArray()
};

TypeDefinition RequireType(string fullName) => asm.MainModule.Types.FirstOrDefault(t => t.FullName == fullName)
    ?? throw new InvalidOperationException("Required API type missing from assembly metadata: " + fullName);

var interesting = asm.MainModule.Types.Where(Match).OrderBy(t => t.FullName).Select(Describe).ToArray();
var componentServer = RequireType("Grasshopper.Kernel.GH_ComponentServer");
var document = RequireType("Grasshopper.Kernel.GH_Document");
var documentIo = RequireType("Grasshopper.Kernel.GH_DocumentIO");
var param = RequireType("Grasshopper.Kernel.IGH_Param");
var mapper = RequireType("Grasshopper.Kernel.Special.GH_PathMapper");
var lexerCombo = RequireType("Grasshopper.Kernel.Data.GH_LexerCombo");

var api = new {
    ProbeMode = "PE_IL_METADATA_ONLY_NO_GRASSHOPPER_RUNTIME_LOAD",
    Package = "Grasshopper " + version,
    Assembly = asm.Name.FullName,
    AssemblyLocation = dll,
    Types = interesting,
    PathMapper = Describe(mapper),
    LexerCombo = Describe(lexerCombo),
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
