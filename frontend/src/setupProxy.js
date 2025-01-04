const { createProxyMiddleware } = require('http-proxy-middleware');

const TARGET_URL = 'https://apigatewaywithmicroservice-ikm8168fy-github-pratiks-projects.vercel.app';

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: TARGET_URL,
      changeOrigin: true,
      pathRewrite: {
        '^/api': ''  // Remove /api prefix when forwarding to target
      }
    })
  );
};