import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: ["@mediapipe/hands", "@mediapipe/camera_utils"],
  },
  build: {
    commonjsOptions: {
      include: [/mediapipe/, /node_modules/],
    },
  },
});
