using System;
using System.Diagnostics;

internal static class AgentApiShim
{
    private const string LanguageServer = @"C:\Users\PC\AppData\Local\Programs\antigravity\resources\bin\language_server.exe";

    private static string Quote(string value)
    {
        if (value.Length == 0) return "\"\"";
        if (value.IndexOfAny(new[] { ' ', '\t', '\"' }) < 0) return value;
        return "\"" + value.Replace("\\", "\\\\").Replace("\"", "\\\"") + "\"";
    }

    private static int Main(string[] args)
    {
        var start = new ProcessStartInfo
        {
            FileName = LanguageServer,
            UseShellExecute = false,
            Arguments = "agentapi" + (args.Length == 0 ? "" : " " + string.Join(" ", Array.ConvertAll(args, Quote)))
        };

        using (var process = Process.Start(start))
        {
            process.WaitForExit();
            return process.ExitCode;
        }
    }
}
