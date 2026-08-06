import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/search': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        bypass: (req, _res, _options) => {
          // Do not proxy if the request wants an HTML page (like going to /search in browser)
          if (req.headers.accept?.includes('text/html')) {
            return '/index.html';
          }
        }
      },
      '/cve': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        bypass: (req, _res, _options) => {
          if (req.headers.accept?.includes('text/html')) {
            return '/index.html';
          }
        }
      },
      '/ask': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        bypass: (req, _res, _options) => {
          if (req.headers.accept?.includes('text/html')) {
            return '/index.html';
          }
        }
      }
    }
  }
})
