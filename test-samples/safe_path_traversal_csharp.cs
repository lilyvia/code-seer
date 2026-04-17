using System;
using System.IO;

// Safe: Validate path within base directory
public class SafePathTraversal
{
    public string SafePath(string baseDir, string userPath)
    {
        var baseFull = Path.GetFullPath(baseDir);
        var target = Path.GetFullPath(baseFull + "/" + userPath);
        if (!target.StartsWith(baseFull + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase))
        {
            throw new InvalidOperationException("Path traversal detected");
        }
        return target;
    }
}
