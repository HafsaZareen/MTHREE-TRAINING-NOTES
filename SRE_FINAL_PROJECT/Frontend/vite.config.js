import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // Ensure it runs on 5173
    host: '0.0.0.0', // Allows access from outside the container
  }
})
