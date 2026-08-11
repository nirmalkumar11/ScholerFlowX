import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],

    server: {
        port: 5173,
        proxy: {
            "/format-paper": "http://localhost:5002",
            "/download": "http://localhost:5002",
            "/health": "http://localhost:5002",
        },
    },

    build: {
        outDir: "dist",
        emptyOutDir: true,
    },
});