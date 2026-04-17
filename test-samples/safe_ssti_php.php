<?php

class SafeSstiPhp {
    private $smarty;
    private $twig;

    public function safeSmartyDisplay() {
        return $this->smarty->display("safe_template.tpl");
    }

    public function safeTwigRender($data) {
        $result = $this->twig->load("safe_template.html");
        return $result->display($data);
    }

    public function safeViewRender($data) {
        return render_view("safe_template", $data);
    }
}
