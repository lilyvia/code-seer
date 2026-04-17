const { URL } = require('url');

const ALLOWED_HOSTS = new Set(['api.example.com', 'files.example.com']);

// Safe: Validate URL before fetching
function isSafeUrl(target) {
    try {
        const parsed = new URL(target);
        return parsed.protocol === 'https:' && ALLOWED_HOSTS.has(parsed.hostname);
    } catch {
        return false;
    }
}

async function safeFetch(url) {
    if (!isSafeUrl(url)) {
        throw new Error('URL not allowed');
    }
    return `fetching ${url}`;
}
