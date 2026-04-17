import java.nio.file.*;

// Safe: Validate paths using Path API without FileInputStream/FileOutputStream
public class SafePathTraversalJava {
    public byte[] safeRead(String baseDir, String userPath) throws Exception {
        Path base = Paths.get(baseDir).toRealPath();
        Path target = base.resolve(userPath).normalize();
        if (!target.startsWith(base)) {
            throw new IllegalArgumentException("Path traversal detected");
        }
        return Files.readAllBytes(target);
    }

    public void safeWrite(String baseDir, String userPath, byte[] data) throws Exception {
        Path base = Paths.get(baseDir).toRealPath();
        Path target = base.resolve(userPath).normalize();
        if (!target.startsWith(base)) {
            throw new IllegalArgumentException("Invalid path");
        }
        Files.write(target, data);
    }
}
