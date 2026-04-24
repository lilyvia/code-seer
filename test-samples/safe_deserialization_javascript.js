// Safe: Use JSON.parse for untrusted data
function safeParse(data) {
    return JSON.parse(data);
}

function safeParseWithoutReviver(data) {
    return JSON.parse(data);
}

// Safe: Validate schema before using parsed data
function safeParseUser(data) {
    const obj = JSON.parse(data);
    if (typeof obj.name !== 'string' || typeof obj.age !== 'number') {
        throw new Error('Invalid schema');
    }
    return obj;
}
