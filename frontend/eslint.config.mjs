// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs';

export default withNuxt(
  {
    rules: {
      'indent': ['error', 2],
      'semi': 'off',
      'comma-dangle': 'off',
      'no-trailing-spaces': 'off',
      'eol-last': 'off',
      'no-multiple-empty-lines': 'off',
      'space-before-function-paren': 'off',
      'no-console': 'off',
      'arrow-parens': 'off',
      'vue/singleline-html-element-content-newline': 'off',
      'vue/max-attributes-per-line': 'off',
      '@stylistic/semi': ['error', 'always', { omitLastInOneLineBlock: true }],
      '@stylistic/brace-style': ['error', '1tbs', { allowSingleLine: true }],
      'vue/no-v-html': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
    },
  },
);
