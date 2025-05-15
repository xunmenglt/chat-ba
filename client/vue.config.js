const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  configureWebpack: {
    watchOptions: {
      poll: 1000,
      ignored: ['**/node_modules/**', '**/dist/**', '**/.git/**']
    }
  },
  devServer: {
    open: true,
    port: 8088
  },
  pages: {
    index: {
      entry: 'src/main.js',
      title: '智核问答系统'
    }
  },
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: './'
})
