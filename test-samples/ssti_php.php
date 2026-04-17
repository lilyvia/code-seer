<?php

class SstiPhp {
    private $smarty;
    private $twig;

    public function vulnerableSmartyFetch($userTemplate) {
        return $this->smarty->fetch("string:" . $userTemplate);
    }

    public function vulnerableTwigRender($userTemplate, $data) {
        return $this->twig->render($userTemplate, $data);
    }

    public function vulnerableViewRender($userTemplate, $data) {
        return view($userTemplate, $data);
    }
}
