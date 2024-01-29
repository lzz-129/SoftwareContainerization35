import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],

  //server
  server: {
      port: 3000, // Guest port in VM
      host: '0.0.0.0'
  },
})
