import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;

class JavaCmdExec {
    public void vulnerableRuntime(String userCmd) throws IOException {
        Runtime.getRuntime().exec(userCmd);
    }

    public void vulnerableRuntimeVar(String userCmd) throws IOException {
        java.lang.Runtime r = Runtime.getRuntime();
        r.exec(userCmd);
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

    public void vulnerableBuilderCommandChain(String userCmd) throws IOException {
        ProcessBuilder pb = new ProcessBuilder();
        pb.command("sh", "-c", userCmd).start();
    }

    public void vulnerableBuilderCommandChainWindows(String userCmd) throws IOException {
        ProcessBuilder pb = new ProcessBuilder();
        pb.command("cmd", "/c", userCmd).start();
    }

    public void vulnerableBuilderStart(String userCmd) throws IOException {
        ProcessBuilder pb = new ProcessBuilder("sh", "-c", userCmd);
        pb.start();
    }

    public String safe(String userCmd) {
        List<String> allowed = Arrays.asList("date", "whoami");
        if (allowed.contains(userCmd)) {
            return "允许执行: " + userCmd;
        }
        return "拒绝执行";
    }

    public void falseNegativeExpansionScripting(ScriptEngine engine, String userInput, String userCode) throws Exception {
        engine.eval(userInput);
        new ScriptEngineManager().getEngineByName("nashorn").eval(userCode);
        new GroovyShell().evaluate(userCode);
        Ognl.getValue(userInput, new Object(), new Object());
    }
}

class GroovyShell { Object evaluate(String code) { return null; } }
class Ognl { static Object getValue(String expr, Object context, Object root) { return null; } static void setValue(String expr, Object context, Object root, Object value) {} }
