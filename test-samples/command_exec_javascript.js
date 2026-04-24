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
