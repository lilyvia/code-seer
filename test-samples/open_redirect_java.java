import javax.servlet.http.HttpServletResponse;
import org.springframework.web.servlet.view.RedirectView;
import org.springframework.web.servlet.ModelAndView;

public class OpenRedirectJava {
    public void vulnerable(HttpServletResponse response, String userUrl) throws Exception {
        response.sendRedirect(userUrl);
    }

    public RedirectView vulnerableView(String userUrl) {
        return new RedirectView(userUrl);
    }

    public ModelAndView vulnerableModel(String userUrl) {
        return new ModelAndView("redirect:" + userUrl);
    }
}
