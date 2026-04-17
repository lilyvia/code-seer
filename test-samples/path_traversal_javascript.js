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
