function vulnerableCmdExec(userCmd) {
    const child_process = require('child_process');
    child_process.exec(userCmd);
}

function false_negative_expansion_command_exec(cp, vm, userCmd, userCode) {
    require("child_process").execSync(userCmd);
    cp.fork(userCmd);
    vm.runInThisContext(userCode);
    vm.runInNewContext(userCode, {});
    new vm.Script(userCode);
}

function false_negative_expansion_shelljs(shell, userInput, request) {
    const { spawn } = require('child_process');

    // Vulnerable: user-controlled strings are passed to shell execution sinks.
    shell.exec(userInput);
    shell.exec(request.body.command);
    spawn('sh -c ' + userInput, { shell: true });
}
