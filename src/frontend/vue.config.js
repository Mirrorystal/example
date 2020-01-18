var webpack = require('webpack')
const debug = process.env.NODE_ENV !== 'production'

module.exports = {
  publicPath: '',
  configureWebpack: config => {
    if (debug) {
        config.devtool = 'source-map'
    }
  },
  devServer: {
    proxy: {
      '/api': {
        target: 'http://106.12.31.181',
        changeOrigin: true,
        pathRewrite: {
          '/api': '/api'
        }
      }
    }
  },
  configureWebpack: {
    plugins: [
      new webpack.ProvidePlugin({
        '$': 'jquery',
        'jQuery': 'jquery',
        'window.jQuery': 'jquery',
        'window.$': 'jquery'
      })
    ]
  }
}
