import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.nio.file.Paths;

public class path_traversal_java {

    public void readFile(String userPath) throws Exception {
        File file = new File(userPath);
        FileInputStream fis = new FileInputStream(userPath);
    }

    public void writeFile(String uploadPath) throws Exception {
        FileOutputStream fos = new FileOutputStream(uploadPath);
    }

    public void deleteFile(String userPath) {
        new File(userPath).delete();
    }

    public void joinPath(String baseDir, String userPath) {
        Paths.get(baseDir, userPath);
    }

    public void readParent(String rest) throws Exception {
        File f = new File("../" + rest);
        FileInputStream fis = new FileInputStream("../" + rest);
        FileOutputStream fos = new FileOutputStream("../" + rest);
    }
}
