import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],

  //server
  server: {
      port: 80, // Guest port in VM
      host: '0.0.0.0'
  },

})

// vue.config.js
// export default defineConfig({
//     plugins: [vue()],
//
//     server: {
//         proxy: {
//             port: 3000, // Guest port in VM
//             host: '0.0.0.0',
//             // 使用 "/api" 作为前缀来代理所有请求
//             // '/api': {
//             //     target: 'http://127.0.0.1:12345', // 后端服务的地址
//             //     changeOrigin: true,
//             //     rewrite: (path) => path.replace(/^\/api/, '') // 重写路径，去掉 `/api` 前缀
//             // }
//         }
//     }
// });
