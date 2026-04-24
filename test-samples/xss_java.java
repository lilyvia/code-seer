import java.io.PrintWriter;

public class xss_java {
    public void vulnerable(PrintWriter out, Object response, String userInput) throws Exception {
        out.println("<div>" + userInput + "</div>");
        out.print(userInput);
    }
}

class FalseNegativeExpansionXssJava {
    void false_negative_expansion(HttpServletResponse response, String userInput) throws Exception {
        response.getOutputStream().write(userInput.getBytes());
    }
}
