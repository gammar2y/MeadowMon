const path = require('path');
const Dotenv = require('dotenv-webpack');

module.exports = {
  entry: {
      backend: './server/static/js/plugins.js',
      frontend: './frontend/src/index.js' // Adjust the path as needed
  },
  output: {
      filename: '[name].bundle.js',
      path: path.resolve(__dirname, 'dist')
  },
  module: {
      rules: [
          {
              test: /\.js$/,
              exclude: /node_modules/,
              use: {
                  loader: 'babel-loader',
                  options: {
                      presets: ['@babel/preset-env']
                  }
              }
          }
      ]
  },
  plugins: [
    new Dotenv({
      path: path.resolve(__dirname, '../.env'), // Path to .env file
      safe: false // Load .env.example (defaults to "false" which does not use dotenv-safe)
    })
  ]
};