const fs = require('fs');
const path = require('path');
const axios = require('axios');
const fetch = require('node-fetch');

function vulnerablePathTraversal(userPath, uploadPath, content) {
    fs.readFileSync(userPath);
    fs.writeFileSync(uploadPath, content);
    fs.createReadStream(userPath);
    fs.unlinkSync(userPath);
    path.join('/app/uploads', userPath);
}

async function vulnerableSSRF(userUrl) {
    await axios.get(userUrl);
    await fetch(userUrl);
    const http = require('http');
    http.get(userUrl);
}

function vulnerableXXE(xmlString) {
    const libxmljs = require('libxmljs');
    const doc = libxmljs.parseXml(xmlString);
    return doc;
}

function vulnerableDeserialization(userInput) {
    const obj = eval(userInput);
    const fn = new Function(userInput);
    return obj;
}

const express = require('express');
const app = express();

app.get('/admin', (req, res) => {
    res.render('admin');
});

app.post('/admin/users', (req, res) => {
    res.json({ success: true });
});

function vulnerableXSS(userInput) {
    const div = document.createElement('div');
    div.innerHTML = userInput;
    document.write(userInput);
}

function vulnerableSQLi(conn, userId) {
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    conn.query(query);
}

function vulnerableCmdExec(userCmd) {
    const { exec } = require('child_process');
    exec(userCmd);
}

const API_KEY = "sk_live_1234567890abcdef";
const PASSWORD = "MySecretPassword123";
