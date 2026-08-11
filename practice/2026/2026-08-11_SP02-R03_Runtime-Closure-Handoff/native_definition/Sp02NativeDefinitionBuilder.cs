using System.Drawing;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Special;
using Grasshopper.Kernel.Types;

namespace Oleander.Sp02;

public static class Sp02NativeDefinitionBuilder
{
    public static string Build(string outputPath)
    {
        if (string.IsNullOrWhiteSpace(outputPath)) throw new ArgumentException("outputPath required");
        if (!outputPath.EndsWith(".ghx", StringComparison.OrdinalIgnoreCase))
            throw new ArgumentException("v1.3 builder intentionally emits GHX for auditable native serialization.");

        using var doc = new GH_Document();

        var baseParam = AddNumberParam(doc, "SP02_BASE", 40, 80);
        baseParam.SetPersistentData(BuildNominalTree());

        var graft = AddNumberParam(doc, "SP02_GRAFT", 210, 40);
        graft.DataMapping = GH_DataMapping.Graft;
        graft.AddSource(baseParam);

        var flatten = AddNumberParam(doc, "SP02_FLATTEN", 210, 125);
        flatten.DataMapping = GH_DataMapping.Flatten;
        flatten.AddSource(baseParam);

        var mapper = AddPathMapper(doc, "SP02_PATH_MAPPER", 360, 40, graft);
        var transpose = AddNumberParam(doc, "SP02_TRANSPOSE", 520, 40);
        transpose.AddSource(mapper);

        var adverseBase = AddNumberParam(doc, "SP02_ADVERSE_BASE", 40, 220);
        adverseBase.SetPersistentData(BuildAdverseTree());

        var adverseGraft = AddNumberParam(doc, "SP02_ADVERSE_GRAFT", 210, 220);
        adverseGraft.DataMapping = GH_DataMapping.Graft;
        adverseGraft.AddSource(adverseBase);

        var adverseMapper = AddPathMapper(doc, "SP02_ADVERSE_PATH_MAPPER", 360, 220, adverseGraft);
        var adverse = AddNumberParam(doc, "SP02_ADVERSE_TRANSPOSE", 520, 220);
        adverse.AddSource(adverseMapper);

        AddViewer(doc, baseParam, "PV_BASE", 680, 20);
        AddViewer(doc, graft, "PV_GRAFT", 680, 80);
        AddViewer(doc, flatten, "PV_FLATTEN", 680, 140);
        AddViewer(doc, transpose, "PV_TRANSPOSE", 680, 200);
        AddViewer(doc, adverse, "PV_ADVERSE", 680, 260);

        Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(outputPath))!);
        var io = new GH_DocumentIO(doc);
        if (!io.SaveQuiet(outputPath))
            throw new IOException("GH_DocumentIO.SaveQuiet returned false.");

        var reload = new GH_DocumentIO();
        if (!reload.Open(outputPath) || reload.Document is null)
            throw new IOException("GH_DocumentIO.Open failed to reload newly saved GHX.");

        var required = new []{
            "SP02_BASE","SP02_GRAFT","SP02_FLATTEN","SP02_TRANSPOSE","SP02_ADVERSE_TRANSPOSE",
            "PV_BASE","PV_GRAFT","PV_FLATTEN","PV_TRANSPOSE","PV_ADVERSE"
        };
        var counts = required.ToDictionary(
            n => n,
            n => reload.Document.Objects.Count(o => string.Equals(o.NickName, n, StringComparison.Ordinal))
        );
        if (counts.Any(kv => kv.Value != 1))
            throw new InvalidOperationException("Reloaded definition nickname inventory invalid: " + JsonSerializer.Serialize(counts));

        var receipt = new {
            exercise = "SP02-R03 v1.3 Native Definition",
            runtime_state = "REAL_GRASSHOPPER_SERIALIZE_AND_RELOAD",
            extension = ".ghx",
            save_mechanism = "GH_DocumentIO.SaveQuiet",
            load_mechanism = "GH_DocumentIO.Open",
            save_success = true,
            load_success = true,
            sha256 = Sha256(outputPath),
            object_count = reload.Document.Objects.Count,
            nickname_inventory = counts,
            definition_path = Path.GetFullPath(outputPath),
            note = "Legitimate only when Build() ran inside a real Rhino/Grasshopper-capable process."
        };
        var receiptPath = Path.Combine(Path.GetDirectoryName(Path.GetFullPath(outputPath))!, "definition_receipt.json");
        File.WriteAllText(receiptPath, JsonSerializer.Serialize(receipt, new JsonSerializerOptions{WriteIndented=true}), Encoding.UTF8);
        return receiptPath;
    }

    private static Param_Number AddNumberParam(GH_Document doc, string nickname, float x, float y)
    {
        var p = new Param_Number { NickName = nickname, Access = GH_ParamAccess.tree };
        AddAt(doc, p, x, y);
        return p;
    }

    private static GH_PathMapper AddPathMapper(GH_Document doc, string nickname, float x, float y, IGH_Param source)
    {
        var mapper = new GH_PathMapper { NickName = nickname };
        mapper.Lexers.Clear();
        mapper.Lexers.Add(new GH_LexerCombo("{A;B}", "{B}"));
        mapper.AddSource(source);
        AddAt(doc, mapper, x, y);
        return mapper;
    }

    private static void AddViewer(GH_Document doc, IGH_Param source, string nickname, float x, float y)
    {
        var viewer = new GH_ParamViewer { NickName = nickname, DisplayGraph = false };
        viewer.AddSource(source);
        AddAt(doc, viewer, x, y);
    }

    private static void AddAt(GH_Document doc, IGH_DocumentObject obj, float x, float y)
    {
        obj.CreateAttributes();
        if (obj.Attributes is not null) obj.Attributes.Pivot = new PointF(x, y);
        if (!doc.AddObject(obj, false))
            throw new InvalidOperationException("GH_Document.AddObject failed for " + obj.NickName);
    }

    private static GH_Structure<GH_Number> BuildNominalTree()
    {
        var t = new GH_Structure<GH_Number>();
        for (int z=0; z<4; z++)
            for (int i=0; i<6; i++)
                t.Append(new GH_Number(z*100+i), new GH_Path(z));
        return t;
    }

    private static GH_Structure<GH_Number> BuildAdverseTree()
    {
        var t = new GH_Structure<GH_Number>();
        for (int z=0; z<4; z++)
        {
            int count = z==2 ? 5 : 6;
            for (int i=0; i<count; i++)
                t.Append(new GH_Number(z*100+i), new GH_Path(z));
        }
        return t;
    }

    private static string Sha256(string path)
    {
        using var sha=SHA256.Create();
        using var fs=File.OpenRead(path);
        return Convert.ToHexString(sha.ComputeHash(fs)).ToLowerInvariant();
    }
}
