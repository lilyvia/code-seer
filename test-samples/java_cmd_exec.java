import java.io.IOException;
import java.util.Arrays;
import java.util.List;

class JavaCmdExec {
    public void vulnerableRuntime(String userCmd) throws IOException {
        Runtime.getRuntime().exec(userCmd);
    }

    public void vulnerableProcessBuilder(String userCmd) throws IOException {
        new ProcessBuilder("sh", "-c", userCmd).start();
    }

    public void vulnerableBuilderCommand(String userCmd) throws IOException {
        new ProcessBuilder().command("sh", "-c", userCmd).start();
    }

    public void vulnerableBuilderCommandOnWindows(String userCmd) throws IOException {
        new ProcessBuilder().command("cmd", "/c", userCmd).start();
    }

    public String safe(String userCmd) {
        List<String> allowed = Arrays.asList("date", "whoami");
        if (allowed.contains(userCmd)) {
            return "允许执行: " + userCmd;
        }
        return "拒绝执行";
    }
}
