const axios = require('axios');
const fetch = require('node-fetch');

async function vulnerableSSRF(userUrl) {
    await axios.get(userUrl);
    await fetch(userUrl);
    const http = require('http');
    http.get(userUrl);
}
