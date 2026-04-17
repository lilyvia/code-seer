import java.util.Set;

public class SafeOpenRedirectJava {
    public String safe(String target) throws Exception {
        Set<String> allowed = Set.of("/home", "/dashboard");
        if (allowed.contains(target)) {
            return target;
        }
        return "/";
    }

    public String safeView() {
        String view = "redirect:/dashboard";
        return view;
    }

    public String safeModelAndView() {
        return "redirect:/home";
    }
}
