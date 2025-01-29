// export default {
//   modules: ["@nuxtjs/tailwindcss"],

//   server: {
//       host: '0.0.0.0',
//       port: 3000
//   },

//   compatibilityDate: "2024-11-29"
// };

import { defineNuxtConfig } from 'nuxt/config'; 

export default defineNuxtConfig({
  modules: ["@nuxtjs/tailwindcss", "@pinia/nuxt"],
  devServer: {
    port: 3000,
    host: "0.0.0.0"
  },
  compatibilityDate: "2024-11-29"
}); 