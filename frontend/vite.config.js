import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  root: 'frontend',  // your frontend folder
  plugins: [react()],
  build: {
    outDir: 'dist', // output directory after build
    rollupOptions: {
      input: 'frontend/src/index.jsx',  // entry point file
    },
  },
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx'],  // allow importing these without extensions
  },
});
