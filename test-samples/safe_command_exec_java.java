import java.util.Arrays;
import java.util.List;

class SafeJavaCmdExec {
    public String validateAgainstAllowlist(String userCmd) {
        List<String> allowed = Arrays.asList("date", "whoami", "uptime");
        if (!allowed.contains(userCmd)) {
            return "拒绝执行";
        }
        return "允许的业务动作: " + userCmd;
    }

    public ProcessBuilder buildTrustedCommand() {
        ProcessBuilder builder = new ProcessBuilder();
        builder.redirectErrorStream(true);
        return builder;
    }

    public ProcessBuilder buildFixedCommand() throws java.io.IOException {
        ProcessBuilder builder = new ProcessBuilder("date");
        builder.redirectErrorStream(true);
        return builder;
    }
}
