const HtmlWebPackPlugin = require("html-webpack-plugin");
const path = require('path');
const webpack = require('webpack');

const CSS_RULE = {
    test: /\.(sa|sc|c)ss$/,
    use: [
        'style-loader',
        'css-loader',
        'sass-loader',
    ],
};

const JS_RULES = {
    test: /\.js$/,
    exclude: /node_modules/,
    use: [
        'babel-loader',
    ],
};

const RULES = [
    JS_RULES,
    CSS_RULE,
];

const PLUGINS = [
    new HtmlWebPackPlugin({
        template: './index.html',
    }),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.DefinePlugin({
        'process.env': {
            NODE_ENV: JSON.stringify('development'),
        },
    }),
];

module.exports = {
    mode: 'development',
    context: path.join(__dirname, '../'),
    entry: {
        main: [
            './src/index.js',
        ],
    },
    output: {
        path: path.join(__dirname, './dist'),
        filename: 'index_bundle.js'
    },
    devtool: 'inline-source-map',
    module: {
        rules: RULES,
    },
    resolve: {
        extensions: ['.js'],
        modules: [
            './src',
            './node_modules',
        ],
    },
    plugins: PLUGINS,
    devServer: {
        // without the following watchOptions setting, node would not
        // re-compile frontend changes on some workstations unless the
        // docker container was restarted.
        // With the setting, it re-compiles whenever changes are saved.
        watchOptions: { aggregateTimeout: 300, poll: 1000 },
        inline: true,
        headers: { 'Access-Control-Allow-Origin': '*' },
        historyApiFallback: true,
        host: '0.0.0.0',
        hot: true,
        port: 3000,
        stats: 'errors-only',
    },
};
