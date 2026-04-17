const axios = require('axios');
const fetch = require('node-fetch');
const got = require('got');
const http = require('http');
const https = require('https');
const { URL } = require('url');

const SAFE_URL = 'https://api.example.com/webhook';
const SAFE_HOST = 'api.example.com';

async function safeRequests() {
    await axios.get(SAFE_URL, {headers: {'X-Api-Key': 'secret'}});
    await fetch(SAFE_URL, {method: 'POST'});
    await axios({baseURL: SAFE_URL, url: '/path'});
    await axios.request({baseURL: SAFE_URL, url: '/path'});
    await got.get(SAFE_URL);
    http.request({host: SAFE_HOST, path: '/'});
    https.request({host: SAFE_HOST, path: '/'});
}

function safeWebhookHandler() {
    const callbackUrl = SAFE_URL;
    axios({baseURL: callbackUrl, url: '/notify'});
}
