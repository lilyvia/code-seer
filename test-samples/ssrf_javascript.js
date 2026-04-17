const axios = require('axios');
const fetch = require('node-fetch');
const got = require('got');

async function vulnerableSSRF(userUrl, userHost) {
    await axios.get(userUrl);
    await fetch(userUrl);
    const http = require('http');
    http.get(userUrl);

    await axios({url: userUrl});
    await axios.request({url: userUrl});
    await got(userUrl);
    http.request({hostname: userHost}, res => {});
    const https = require('https');
    https.request({hostname: userHost}, res => {});
}

function webhookHandler(req, res) {
    const callbackUrl = req.body.callbackUrl;
    axios({url: callbackUrl});
    got.post(callbackUrl, {json: {status: 'ok'}});
    http.request({host: req.query.target}, res => {});
    https.get({hostname: req.headers['x-internal-host']}, res => {});
}

function callbackSSRF(req) {
    const hook = req.body.webhook;
    fetch(hook);
    axios.request({url: hook});
    got.stream(hook);
}

function pathBasedSSRF(req) {
    const targetPath = req.query.path;
    http.request({path: targetPath}, res => {});
    https.request({path: targetPath}, res => {});
}
