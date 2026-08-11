using System.Text.Json;
using Oleander.Sp02;

var evidence = Path.GetFullPath("native_ci_evidence");
Directory.CreateDirectory(evidence);
var ghx = Path.Combine(evidence, "SP02_R03_native.ghx");

var receipt = Sp02NativeDefinitionBuilder.Build(ghx);
var output = new {
    gate = "SG01",
    execution_class = "GRASSHOPPER_SDK_NATIVE_SERIALIZATION_NOT_RHINO_SOLVE",
    builder_receipt = Path.GetFullPath(receipt),
    ghx = Path.GetFullPath(ghx),
    note = "This can close native definition serialization/reload only. It cannot close SG00 runtime authority, SG02 solve request, or CP2."
};
File.WriteAllText(Path.Combine(evidence, "sdk_native_execution_receipt.json"), JsonSerializer.Serialize(output, new JsonSerializerOptions{WriteIndented=true}));
Console.WriteLine(JsonSerializer.Serialize(output, new JsonSerializerOptions{WriteIndented=true}));
