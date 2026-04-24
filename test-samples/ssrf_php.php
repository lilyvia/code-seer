<?php

function vulnerable($userUrl) {
    file_get_contents($userUrl);
    file_get_contents("http://169.254.169.254/latest/meta-data/");

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $userUrl);
    curl_exec($ch);
}

function false_negative_expansion_http_clients($client, $userUrl) {
    $client->get($userUrl);
    HttpClient::create()->get($userUrl);
}
