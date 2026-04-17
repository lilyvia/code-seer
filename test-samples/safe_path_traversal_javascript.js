const fs = require('fs');

async function safePathTraversal(baseDir, userPath, content) {
    const sanitizedName = userPath.replace(/\.\./g, '').replace(/[\\/]/g, '');
    const targetPath = `${baseDir}/${sanitizedName}`;

    if (sanitizedName.length === 0) {
        throw new Error('invalid path');
    }

    await fs.promises.access(targetPath, fs.constants.R_OK | fs.constants.W_OK);
    return { targetPath, contentLength: content.length };
}
