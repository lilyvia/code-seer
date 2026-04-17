const fs = require('fs');
const path = require('path');

async function safePathTraversal(baseDir, userPath, content) {
    const sanitizedName = userPath.replace(/\.\./g, '').replace(/[\\/]/g, '');
    const targetPath = path.join(baseDir, sanitizedName);
    const resolvedPath = path.resolve(baseDir, sanitizedName);

    if (sanitizedName.length === 0) {
        throw new Error('invalid path');
    }

    const baseResolved = path.resolve(baseDir);
    if (!resolvedPath.startsWith(baseResolved + path.sep)) {
        throw new Error('path traversal detected');
    }

    await fs.promises.access(targetPath, fs.constants.R_OK | fs.constants.W_OK);
    return { targetPath, contentLength: content.length };
}
