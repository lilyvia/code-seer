import java.io.PrintWriter;
import org.springframework.web.util.HtmlUtils;

// Safe: Escape HTML output before writing to response
public class SafeXssJava {
    public void safeOutput(PrintWriter out, String userInput) {
        String escaped = HtmlUtils.htmlEscape(userInput);
        out.println("<div>" + escaped + "</div>");
    }

    public String safeScript(String userInput) {
        String safe = HtmlUtils.htmlEscape(userInput);
        return "<script>var name = '" + safe + "';</script>";
    }
}
