import java.io.IOException;
import java.util.Arrays;
import java.util.List;

public class JavaCmdExecSample {
    public void vulnerableRuntime(String userCmd) throws IOException {
        Runtime.getRuntime().exec(userCmd);
    }

    public void vulnerableProcessBuilder(String userCmd) throws IOException {
        new ProcessBuilder("sh", "-c", userCmd).start();
    }

    public String safe(String userCmd) {
        List<String> allowed = Arrays.asList("date", "whoami");
        if (allowed.contains(userCmd)) {
            return "允许执行: " + userCmd;
        }
        return "拒绝执行";
    }
}
