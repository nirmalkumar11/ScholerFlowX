import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // lets `npm run dev` (hot-reload frontend) still hit the Flask API
      // without a CORS dance, while developing.
      "/format-paper": "http://localhost:5002",
      "/download": "http://localhost:5002",
      "/health": "http://localhost:5002"
    }
  },
  build: {
    // build straight into research-paper-ai/frontend_dist, which app.py serves
    outDir: resolve(__dirname, "../frontend_dist"),
    emptyOutDir: true
  }
});
