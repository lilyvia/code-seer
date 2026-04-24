import java.io.PrintWriter;

// Safe: Escape HTML output before writing to response
class SafeXssJava {
    public void safeOutput(PrintWriter out, String userInput) {
        String escaped = HtmlUtils.htmlEscape(userInput);
        out.println("<div>" + escaped + "</div>");
    }

    public String safeScript(String userInput) {
        String safe = HtmlUtils.htmlEscape(userInput);
        return "<script>var name = '" + safe + "';</script>";
    }

    // <c:out value="${param.name}" escapeXml="true"/>
}

class HtmlUtils { static String htmlEscape(String value) { return value; } }
