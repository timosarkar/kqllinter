using System;
using System.Collections.Generic;
using System.Linq;
using Kusto.Language;
using Kusto.Language.Symbols;
using Kusto.Language.Syntax;

class Program
{
    static void Main()
    {
var globals = GlobalState.Default.WithDatabase(
    new DatabaseSymbol("Sentinel",
        new TableSymbol("SigninLogs", "(TimeGenerated: datetime, UserPrincipalName: string, LocationDetails: dynamic, RiskLevelDuringSignIn: string)"),
        new TableSymbol("SecurityEvent", "(TimeGenerated: datetime, Account: string, EventID: int, Computer: string)")
    )
);

var query = @"
SigninLogs
| where RiskLevelDuringSignIn == 'none' and TimeGenerated >= ago(7d)
| sort by RiskLevelDuringSignIn desc
| take 5";

var code = KustoCode.ParseAndAnalyze(query, globals);


        var diagnostics = code.GetDiagnostics();

        if (diagnostics.Count == 0) {
            Console.WriteLine("✅ No issues found in the query.");
        } else {
            Console.WriteLine("❌ Diagnostics:");
            foreach (var diagnostic in diagnostics) {
                var (line, column) = GetLineColumn(query, diagnostic.Start);
                Console.WriteLine($"{diagnostic.Severity}: {diagnostic.Message} at line {line}, column {column}");
            }
        }
    }

    static (int line, int column) GetLineColumn(string query, int position)
    {
        var lines = query.Split('\n');
        int total = 0;

        for (int i = 0; i < lines.Length; i++)
        {
            if (total + lines[i].Length >= position)
            {
                return (i + 1, position - total + 1);
            }
            total += lines[i].Length + 1; // +1 for newline
        }

        return (-1, -1); // fallback
    }
}
