const path = require('path');

module.exports = {
	mode: 'development',
	entry: './src/react/index.tsx',
	output: {
		path: path.resolve(__dirname, 'react-dist'),
		filename: 'bundle.js',
	},
	module: {
		rules: [
			{
				test: /\.(ts|tsx)$/,
				use: 'ts-loader',
				exclude: /node_modules/,
			},
			{
				test: /\.(?:js|mjs|cjs)$/,
				exclude: /node_modules/,
				use: {
					loader: 'babel-loader',
					options: {
						targets: 'defaults',
						presets: [
							['@babel/preset-env', { modules: false }],
							'@babel/preset-react',
						],
					},
				},
			},
		],
	},
};
