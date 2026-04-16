import java.io.PrintWriter;

public class xss_java {
    public void vulnerable(PrintWriter out, Object response, String userInput) throws Exception {
        out.println("<div>" + userInput + "</div>");
        out.print(userInput);
    }
}
