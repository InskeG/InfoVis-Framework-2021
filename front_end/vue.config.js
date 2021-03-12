const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')

module.exports = {
  publicPath: '/',
  configureWebpack: {
    plugins: [
      new VuetifyLoaderPlugin()
    ],
  },
}
