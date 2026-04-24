using System.Collections.Generic;
using System.Diagnostics;

public class CSharpCmdExecSample
{
    public void VulnerableStart(string userCmd)
    {
        Process.Start(userCmd);
    }

    public void VulnerableCmd(string userInput)
    {
        Process.Start("cmd.exe", "/c " + userInput);
    }

    public void Safe(string userCmd)
    {
        var allowed = new HashSet<string> { "whoami", "hostname" };
        if (allowed.Contains(userCmd))
        {
            var message = "允许执行: " + userCmd;
            _ = message;
        }
    }
}

class FalseNegativeExpansionCommandCSharp {
    void FalseNegativeExpansion(string userCmd, string userArgs) {
        var psi = new ProcessStartInfo();
        psi.FileName = userCmd;
        psi.Arguments = userArgs;
        System.Diagnostics.Process.Start(userCmd);
        PowerShell.Create().AddScript(userCmd);
        var process = new Process();
        process.StartInfo.FileName = userCmd;
    }
}

class PowerShell {
    public static PowerShell Create() { return new PowerShell(); }
    public PowerShell AddScript(string script) { return this; }
}
