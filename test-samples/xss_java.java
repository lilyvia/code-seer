import java.io.PrintWriter;

class xss_java {
    public void vulnerable(PrintWriter out, Object response, String userInput) throws Exception {
        out.println("<div>" + userInput + "</div>");
        out.print(userInput);
    }
}

class FalseNegativeExpansionXssJava {
    void false_negative_expansion(HttpServletResponse response, String userInput) throws Exception {
        response.getOutputStream().write(userInput.getBytes());
    }

    // <%= request.getParameter("q") %>
    // <c:out value="${param.name}" escapeXml="false"/>
}

class HttpServletResponse { ServletOutputStream getOutputStream() { return new ServletOutputStream(); } }
class ServletOutputStream { void write(byte[] bytes) {} }
