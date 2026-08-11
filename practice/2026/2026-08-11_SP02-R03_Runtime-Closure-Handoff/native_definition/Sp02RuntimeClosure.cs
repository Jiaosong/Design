using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Data;
using Rhino;

namespace Oleander.Sp02;

public static class Sp02RuntimeClosure
{
    private sealed record TreeState(
        string[] paths,
        int branch_count,
        int data_count,
        int[] branch_lengths,
        string topology
    );

    public static string Run(string evidenceDir, string providerId)
    {
        if (string.IsNullOrWhiteSpace(evidenceDir)) throw new ArgumentException("evidenceDir required");
        if (string.IsNullOrWhiteSpace(providerId)) throw new ArgumentException("providerId required");
        Directory.CreateDirectory(evidenceDir);

        var evidenceRoot = Path.GetFullPath(evidenceDir);
        var ghx = Path.Combine(evidenceRoot, "SP02_R03_native.ghx");

        // ND02—ND04: build, native serialize, immediate native reload and identity audit.
        var definitionReceipt = Sp02NativeDefinitionBuilder.Build(ghx);
        var definitionHash = Sha256(ghx);

        var io = new GH_DocumentIO();
        if (!io.Open(ghx) || io.Document is null)
            throw new IOException("Runtime closure could not reopen native GHX.");
        var doc = io.Document;

        // SG00: provider authority receipt. A valid Rhino license is required to claim authority.
        var providerReceipt = new
        {
            provider_id = providerId,
            execution_id = Guid.NewGuid().ToString("D"),
            runtime_authority_verified = RhinoApp.IsLicenseValidated,
            rhino_version = RhinoApp.Version.ToString(),
            rhino_is_evaluation = RhinoApp.IsEvaluation,
            rhino_is_running_automated = RhinoApp.IsRunningAutomated,
            rhino_is_running_headless = RhinoApp.IsRunningHeadless,
            machine = Environment.MachineName,
            timestamp_utc = DateTime.UtcNow.ToString("O"),
            truth_state = "REAL_RHINO_GRASSHOPPER_RUNTIME"
        };
        WriteJson(Path.Combine(evidenceRoot, "provider_receipt.json"), providerReceipt);

        int solutionStarts = 0;
        int solutionEnds = 0;
        var durationsMs = new List<double>();
        doc.SolutionStart += (_, e) => solutionStarts++;
        doc.SolutionEnd += (_, e) =>
        {
            solutionEnds++;
            durationsMs.Add(e.Duration.TotalMilliseconds);
        };

        var run1 = SolveAndExtract(doc);
        var errors1 = CollectErrors(doc);
        var signature1 = StructureSignature(run1);

        var run2 = SolveAndExtract(doc);
        var errors2 = CollectErrors(doc);
        var signature2 = StructureSignature(run2);

        var allErrors = errors1.Concat(errors2).Distinct().OrderBy(x => x).ToArray();

        WriteJson(Path.Combine(evidenceRoot, "tree_runtime.json"), new
        {
            source_definition = ghx,
            definition_sha256 = definitionHash,
            states = run1
        });
        WriteJson(Path.Combine(evidenceRoot, "tree_runtime_repeat.json"), new
        {
            source_definition = ghx,
            definition_sha256 = definitionHash,
            states = run2
        });

        WriteJson(Path.Combine(evidenceRoot, "solve_receipt.json"), new
        {
            request_observed = solutionStarts >= 2,
            completion_observed = solutionEnds >= 2,
            mechanism = "GH_Document.NewSolution(true, GH_SolutionMode.Silent)",
            solution_start_count = solutionStarts,
            solution_end_count = solutionEnds,
            solution_durations_ms = durationsMs,
            errors = allErrors,
            output_fingerprint = signature1,
            note = "SolutionStart records requested solutions; SolutionEnd records handled solution requests."
        });

        WriteJson(Path.Combine(evidenceRoot, "reproduction_receipt.json"), new
        {
            run_count = 2,
            definition_sha256 = definitionHash,
            definition_hash_same = Sha256(ghx) == definitionHash,
            run1_structure_signature = signature1,
            run2_structure_signature = signature2,
            structure_signature_match = signature1 == signature2
        });

        var solvedPath = Path.Combine(evidenceRoot, "SP02_R03_runtime_solved.ghx");
        var solvedIo = new GH_DocumentIO(doc);
        if (!solvedIo.SaveQuiet(solvedPath))
            throw new IOException("Could not save solved GHX evidence.");

        var summary = new
        {
            exercise = "SP02-R03 v1.4 One-Run CP2 Closure",
            provider_receipt = "provider_receipt.json",
            definition_receipt = Path.GetFileName(definitionReceipt),
            solve_receipt = "solve_receipt.json",
            tree_runtime = "tree_runtime.json",
            reproduction_receipt = "reproduction_receipt.json",
            definition_sha256 = definitionHash,
            solved_definition = Path.GetFileName(solvedPath),
            runtime_errors = allErrors,
            intended_result = "SG00—SG07 can be validated from this single real Rhino execution; CP4 remains separate GUI provenance."
        };
        var summaryPath = Path.Combine(evidenceRoot, "ONE_RUN_CP2_SUMMARY.json");
        WriteJson(summaryPath, summary);
        return summaryPath;
    }

    private static Dictionary<string, TreeState> SolveAndExtract(GH_Document doc)
    {
        doc.NewSolution(true, GH_SolutionMode.Silent);
        return new Dictionary<string, TreeState>
        {
            ["BASE"] = ReadState(doc, "SP02_BASE"),
            ["GRAFT"] = ReadState(doc, "SP02_GRAFT"),
            ["FLATTEN"] = ReadState(doc, "SP02_FLATTEN"),
            ["TRANSPOSE"] = ReadState(doc, "SP02_TRANSPOSE"),
            ["ADVERSE_TRANSPOSE"] = ReadState(doc, "SP02_ADVERSE_TRANSPOSE")
        };
    }

    private static TreeState ReadState(GH_Document doc, string nickname)
    {
        var hits = doc.Objects.Where(o => string.Equals(o.NickName, nickname, StringComparison.Ordinal)).ToArray();
        if (hits.Length != 1)
            throw new InvalidOperationException($"Expected one object {nickname}, got {hits.Length}.");
        if (hits[0] is not IGH_Param p)
            throw new InvalidOperationException($"{nickname} is not an IGH_Param.");

        IGH_Structure s = p.VolatileData;
        var paths = s.Paths.Select(path => path.ToString()).ToArray();
        var lengths = new int[s.PathCount];
        for (int i = 0; i < s.PathCount; i++)
            lengths[i] = s.get_Branch(i).Count;

        return new TreeState(paths, s.PathCount, s.DataCount, lengths, s.TopologyDescription);
    }

    private static string[] CollectErrors(GH_Document doc)
    {
        return doc.Objects
            .OfType<IGH_ActiveObject>()
            .SelectMany(o => o.RuntimeMessages(GH_RuntimeMessageLevel.Error)
                .Select(m => $"{o.NickName} [{o.GetType().FullName}]: {m}"))
            .Distinct()
            .OrderBy(x => x)
            .ToArray();
    }

    private static string StructureSignature(Dictionary<string, TreeState> states)
    {
        var ordered = states.OrderBy(kv => kv.Key).ToDictionary(kv => kv.Key, kv => kv.Value);
        var json = JsonSerializer.Serialize(ordered);
        using var sha = SHA256.Create();
        return Convert.ToHexString(sha.ComputeHash(Encoding.UTF8.GetBytes(json))).ToLowerInvariant();
    }

    private static string Sha256(string path)
    {
        using var sha = SHA256.Create();
        using var fs = File.OpenRead(path);
        return Convert.ToHexString(sha.ComputeHash(fs)).ToLowerInvariant();
    }

    private static void WriteJson(string path, object value)
    {
        File.WriteAllText(path, JsonSerializer.Serialize(value, new JsonSerializerOptions { WriteIndented = true }), Encoding.UTF8);
    }
}
