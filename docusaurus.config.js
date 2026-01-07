// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'ARC Protocol',
  tagline: 'Agent Remote Communication Protocol',
  favicon: 'img/favicon.ico',

  url: 'https://arc-protocol.org',
  baseUrl: '/',

  organizationName: 'arcprotocol',
  projectName: 'arcprotocol',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/arcprotocol/arcprotocol/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themes: [
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      {
        hashed: true,
        language: ["en"],
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
        indexDocs: true,
        indexBlog: false,
        indexPages: true,
        docsRouteBasePath: "/docs",
        searchResultLimits: 8,
        searchResultContextMaxLength: 50,
        useAllContextsWithNoSearchContext: false,
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/arc-social-card.jpg',
      colorMode: {
        defaultMode: 'light',
        disableSwitch: true,
        respectPrefersColorScheme: false,
      },
      navbar: {
        title: 'ARC Protocol',
        logo: {
          alt: 'ARC Protocol Logo',
          src: 'img/arc_logo.jpeg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docs',
            position: 'left',
            label: 'Documentation',
          },
          {
            to: '/docs/guides/multi-agent-system',
            label: 'Guides',
            position: 'left',
          },
          {
            to: '/docs/spec/overview',
            label: 'Specification',
            position: 'left',
          },
          {
            href: 'https://github.com/arcprotocol/arcprotocol',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentation',
            items: [
              {
                label: 'Getting Started',
                to: '/docs/getting-started',
              },
              {
                label: 'Guides',
                to: '/docs/guides/multi-agent-system',
              },
              {
                label: 'Python SDK',
                to: '/docs/sdk/python',
              },
              {
                label: 'Specification',
                to: '/docs/spec/overview',
              },
            ],
          },
          {
            title: 'Concepts',
            items: [
              {
                label: 'Protocol Design',
                to: '/docs/concepts/protocol-design',
              },
              {
                label: 'Architecture',
                to: '/docs/concepts/architecture',
              },
              {
                label: 'Security',
                to: '/docs/concepts/security',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/arcprotocol',
              },
              {
                label: 'Contributing',
                href: 'https://github.com/arcprotocol/arcprotocol/blob/main/CONTRIBUTING.md',
              },
              {
                label: 'Security',
                href: 'https://github.com/arcprotocol/arcprotocol/blob/main/SECURITY.md',
              },
            ],
          },
        ],
        copyright: `© ${new Date().getFullYear()} ARC Protocol`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'typescript', 'bash', 'json', 'yaml'],
      },
    }),
};

export default config;

