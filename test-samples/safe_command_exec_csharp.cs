using System;
using System.Diagnostics;

// Safe: Use .NET built-in APIs instead of shell commands
public class SafeCmdExec
{
    public DateTime SafeDate()
    {
        return DateTime.UtcNow;
    }

    public string SafeReadFile(string path)
    {
        return System.IO.File.ReadAllText(path);
    }

    public void SafeProcessStart()
    {
        var startInfo = new ProcessStartInfo { FileName = "notepad.exe" };
        var process = new Process { StartInfo = startInfo };
        process.Start();
    }
}
