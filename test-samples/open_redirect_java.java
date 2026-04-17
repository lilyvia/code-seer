import javax.servlet.http.HttpServletResponse;
import org.springframework.web.servlet.view.RedirectView;
import org.springframework.web.servlet.ModelAndView;

public class OpenRedirectJava {
    public void vulnerable(HttpServletResponse response, String user_url) throws Exception {
        response.sendRedirect(user_url);
    }

    public RedirectView vulnerableView(String user_url) {
        return new RedirectView(user_url);
    }

    public ModelAndView vulnerableModel(String user_url) {
        return new ModelAndView("redirect:" + user_url);
    }
}
