using System;
using System.IO;

public class PathTraversalCSharp
{
    public void ReadFile(string userPath)
    {
        var text = File.ReadAllText(userPath);
        var bytes = File.ReadAllBytes(userPath);
    }

    public void WriteFile(string uploadPath, byte[] content)
    {
        File.WriteAllBytes(uploadPath, content);
        File.WriteAllText(uploadPath, "content");
    }

    public void DeleteFile(string userPath)
    {
        File.Delete(userPath);
    }

    public string JoinPath(string baseDir, string userPath)
    {
        return Path.Combine(baseDir, userPath);
    }

    public void ParentOps(string userPath, byte[] content)
    {
        var text = File.ReadAllText("../" + userPath);
        File.WriteAllBytes("../" + userPath, content);
        File.Delete("../" + userPath);
    }
}
