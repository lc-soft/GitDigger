module.exports = {
  files: [
    '../../../node_modules/octicons/build/svg/*.svg'
  ],
  fontName: 'octicons',
  templateOptions: {
    src: 'url("/static/fonts/octicons.eot?#iefix") format("embedded-opentype"), url("/static/fonts/octicons.woff") format("woff"), url("/static/fonts/octicons.woff2") format("woff2"), url("/static/fonts/octicons.ttf") format("truetype"), url("/static/fonts/octicons.svg#octicons") format("svg")',
    classPrefix: 'octicon-',
    baseSelector: '.octicon'
  },
  types: ['eot', 'woff', 'woff2', 'ttf', 'svg'],
  fileName: '../fonts/[fontname].[ext]'
};
