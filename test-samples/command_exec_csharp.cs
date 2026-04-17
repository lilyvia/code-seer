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
