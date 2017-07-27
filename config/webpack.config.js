var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
  context: path.join(__dirname, '../app/assets/javascripts'),
  entry: {
    vendor: './vendor.js',
    app: './main.js'
  },

  output: {
    path: path.join(__dirname, '../static/javascripts'),
    filename: '[name].js'
  },

  module: {
    rules: [
      {
        test: /\.(scss|css)$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          //resolve-url-loader may be chained before sass-loader if necessary
          use: ['css-loader', 'sass-loader']
        })
      }
    ],
    loaders: [
      {
        test: /\.(sass|scss)?$/,
        loader: 'css-loader!sass-loader'
      }, {
        test: /\.css$/,
        loader: 'style-loader!css-loader'
      }
    ]
  },

  plugins: [
    new ExtractTextPlugin('../stylesheets/[name].css'),
    new webpack.ProvidePlugin({   
        jQuery: 'jquery',
        Tether: 'tether',
        $: 'jquery',
        jquery: 'jquery'
    })
  ]
};
