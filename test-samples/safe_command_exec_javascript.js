const { execFile } = require('child_process');

// Safe: Use execFile with argument array
function safeLs() {
    return execFile('ls', ['-la'], (err, stdout) => {
        if (err) return;
        console.log(stdout);
    });
}

// Safe: Whitelist allowed commands
const allowed = new Set(['date', 'whoami', 'pwd']);

function safeRun(cmd) {
    if (!allowed.has(cmd)) {
        throw new Error('Command not allowed');
    }
    return execFile(cmd, [], (err, stdout) => {
        if (err) return;
        console.log(stdout);
    });
}
