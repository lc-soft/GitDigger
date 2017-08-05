var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
  context: path.join(__dirname, '../app/assets/javascripts'),
  entry: {
    vendor: './vendor.js',
    app: './main.coffee'
  },

  output: {
    path: path.join(__dirname, '../static/javascripts'),
    filename: '[name].js'
  },
  resolve: {
    extensions: ['.js', '.coffee']
  },
  module: {
    rules: [
      {
        test: require.resolve('jquery'),
        use: [{
          loader: 'expose-loader',
          options: 'jQuery'
        },{
          loader: 'expose-loader',
          options: '$'
        }]
      }, {
        test: require.resolve('tether'),
        use: [{
          loader: 'expose-loader',
          options: 'Tether'
        }]
      }, {
        test: /\.coffee$/,
        use: 'coffee-loader'
      }, {
        test: /\.(sass|scss)?$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          //resolve-url-loader may be chained before sass-loader if necessary
          use: ['css-loader', 'sass-loader']
        })
      }, {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }, {
        test: /\.font\.js/,
        loader: ExtractTextPlugin.extract({
          use: [
            'css-loader',
            'webfonts-loader'
          ]
        })
      }
    ]
  },

  plugins: [
    new ExtractTextPlugin('../stylesheets/[name].css')
  ]
};
