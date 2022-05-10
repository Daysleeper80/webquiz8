/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
    root: true,
    extends: [
        "plugin:vue/vue3-essential",
        "eslint:recommended",
    ],
    env: {
        "vue/setup-compiler-macros": true,
        node: true,
        es2022: true,
    },
    globals: {
        globalThis: false, // means it is not writeable
        document: true,
        window: true,
        _: true,
    },
    parserOptions: {
        ecmaVersion: 2022,
        sourceType: "module"
    },
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        indent: [
            "warn",
            4,
            {MemberExpression: 1}
        ],
        semi: [
            "error",
            "always"
        ],
        "no-unused-vars": "warn",
        "linebreak-style": [
            "error",
            "unix"
        ],
    }
};
