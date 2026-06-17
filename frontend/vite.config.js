import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';

// Vite config with React and Tailwind CSS v4 plugins
export default defineConfig({
  plugins: [react(), tailwindcss()],
});
