const fs = require('fs');
const path = require('path');

function vulnerablePathTraversal(userPath, uploadPath, content) {
    fs.readFileSync(userPath);
    fs.writeFileSync(uploadPath, content);
    fs.createReadStream(userPath);
    fs.unlinkSync(userPath);
    path.join('/app/uploads', userPath);
}

async function vulnerableAsyncPathTraversal(userPath, content) {
    await fs.promises.readFile(userPath);
    await fs.promises.writeFile(userPath, content);
    await fs.promises.unlink(userPath);
}

function vulnerablePathTraversalMore(userPath, uploadPath) {
    fs.readFile(userPath, (err, data) => {});
    fs.writeFile(uploadPath, 'data', (err) => {});
    fs.createWriteStream(uploadPath);
    fs.unlink(userPath, (err) => {});
    fs.open(userPath, 'r', (err, fd) => {});
    fs.openSync(userPath, 'r');
    path.resolve('/app/uploads', userPath);
}
