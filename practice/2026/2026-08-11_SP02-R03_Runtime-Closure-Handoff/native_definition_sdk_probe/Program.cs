using System.Reflection;
using System.Text.Json;
using Grasshopper.Kernel;

var asm = typeof(GH_Document).Assembly;
var filters = new[] { "PathMapper", "Path Mapper", "Param_Number", "ParamViewer", "Param_Viewer", "Graft", "Flatten" };

var hits = asm.GetTypes()
    .Where(t => filters.Any(f => t.FullName?.Contains(f.Replace(" ", ""), StringComparison.OrdinalIgnoreCase) == true
                              || t.Name.Contains(f.Replace(" ", ""), StringComparison.OrdinalIgnoreCase)))
    .OrderBy(t => t.FullName)
    .Select(t => new {
        t.FullName,
        BaseType = t.BaseType?.FullName,
        Interfaces = t.GetInterfaces().Select(i => i.FullName).OrderBy(x => x).ToArray(),
        Constructors = t.GetConstructors(BindingFlags.Public|BindingFlags.Instance)
            .Select(c => c.ToString()).ToArray(),
        Properties = t.GetProperties(BindingFlags.Public|BindingFlags.Instance|BindingFlags.Static)
            .Select(p => new { p.Name, Type = p.PropertyType.FullName, p.CanRead, p.CanWrite })
            .OrderBy(p => p.Name).ToArray(),
        Methods = t.GetMethods(BindingFlags.Public|BindingFlags.Instance|BindingFlags.Static|BindingFlags.DeclaredOnly)
            .Select(m => m.ToString()).OrderBy(x => x).ToArray()
    }).ToArray();

var componentServer = typeof(GH_ComponentServer);
var api = new {
    Package = "Grasshopper 8.32.26160.13001",
    Assembly = asm.FullName,
    AssemblyLocation = asm.Location,
    Types = hits,
    KnownApis = new {
        FindObjectByName = componentServer.GetMethods().Where(m => m.Name == "FindObjectByName").Select(m => m.ToString()).ToArray(),
        EmitObject = componentServer.GetMethods().Where(m => m.Name == "EmitObject").Select(m => m.ToString()).ToArray(),
        AddObject = typeof(GH_Document).GetMethods().Where(m => m.Name == "AddObject").Select(m => m.ToString()).ToArray(),
        DocumentIO = typeof(GH_DocumentIO).GetMethods(BindingFlags.Public|BindingFlags.Instance).Where(m => m.Name is "Open" or "SaveQuiet").Select(m => m.ToString()).ToArray(),
        DocumentIOConstructors = typeof(GH_DocumentIO).GetConstructors().Select(c => c.ToString()).ToArray()
    }
};

Directory.CreateDirectory("sdk_probe_output");
File.WriteAllText("sdk_probe_output/grasshopper_sdk_metadata.json", JsonSerializer.Serialize(api, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine(JsonSerializer.Serialize(api, new JsonSerializerOptions { WriteIndented = true }));
