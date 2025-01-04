const express = require('express');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
app.use(cors());

app.use('/', createProxyMiddleware({
  target: 'https://apigatewaywithmicroservice-ikm8168fy-github-pratiks-projects.vercel.app',
  changeOrigin: true
}));

app.listen(3001); 