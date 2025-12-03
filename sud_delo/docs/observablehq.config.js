export default {
  title: "Frdus",
  pages: [
    { name: "Сайты судов",
      pages: [
        {name: "Что там внутри?", path: "./sud-delo-files"},
        {name: "Как их получили?", path: "./sud-delo-process"},
      ]
    }
  ],

  root: "src",

  theme: "air", // try "light", "dark", "slate", etc.
  // header: "", // what to show in the header (HTML)
  footer: "<h2>♡</h2>", // what to show in the footer (HTML)
  // sidebar: true, // whether to show the sidebar
  // toc: true, // whether to show the table of contents
  pager: false, // whether to show previous & next links in the footer
  // output: "dist", // path to the output root for build
  search: false, // activate search
  // linkify: true, // convert URLs in Markdown to links
  // typographer: false, // smart quotes and other typographic improvements
  // preserveExtension: false, // drop .html from URLs
  // preserveIndex: false, // drop /index from URLs
};
