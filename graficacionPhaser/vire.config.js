import { defineConfig } from 'vite';

export default defineConfig({
    resolve: {
        alias: {
            'phaser': path.resolve(__dirname, 'node_modules/phaser-ce/build/phaser.min.js'),
            'pixi.js': path.resolve(__dirname, 'node_modules/pixi.js/dist/browser/pixi.min.js'),
            'p2': path.resolve(__dirname, 'node_modules/p2/build/p2.min.js')
        },
    },
});
