import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/search',
    component: ComponentCreator('/search', '822'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '661'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'ee5'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'f96'),
            routes: [
              {
                path: '/docs/',
                component: ComponentCreator('/docs/', '56e'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/architecture/',
                component: ComponentCreator('/docs/concepts/architecture/', 'edd'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/architecture/multi-agent',
                component: ComponentCreator('/docs/concepts/architecture/multi-agent', 'c21'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/architecture/supervisor-router',
                component: ComponentCreator('/docs/concepts/architecture/supervisor-router', '112'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/architecture/workflow-composition',
                component: ComponentCreator('/docs/concepts/architecture/workflow-composition', '195'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/protocol-design/',
                component: ComponentCreator('/docs/concepts/protocol-design/', '592'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/protocol-design/error-codes',
                component: ComponentCreator('/docs/concepts/protocol-design/error-codes', '549'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/protocol-design/single-endpoint',
                component: ComponentCreator('/docs/concepts/protocol-design/single-endpoint', 'caf'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/protocol-design/stateless-rpc',
                component: ComponentCreator('/docs/concepts/protocol-design/stateless-rpc', 'f53'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/security/',
                component: ComponentCreator('/docs/concepts/security/', '1bd'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/security/authentication',
                component: ComponentCreator('/docs/concepts/security/authentication', '7bc'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/security/authorization',
                component: ComponentCreator('/docs/concepts/security/authorization', 'e6e'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/concepts/security/transport',
                component: ComponentCreator('/docs/concepts/security/transport', '791'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/getting-started',
                component: ComponentCreator('/docs/getting-started', '565'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/guides/multi-agent-system/',
                component: ComponentCreator('/docs/guides/multi-agent-system/', 'f73'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/guides/multi-agent-system/agent-communication',
                component: ComponentCreator('/docs/guides/multi-agent-system/agent-communication', '6de'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/guides/multi-agent-system/distributed',
                component: ComponentCreator('/docs/guides/multi-agent-system/distributed', '044'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/guides/multi-agent-system/single-server',
                component: ComponentCreator('/docs/guides/multi-agent-system/single-server', 'cd8'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/guides/supervisor-pattern/',
                component: ComponentCreator('/docs/guides/supervisor-pattern/', 'b02'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/guides/supervisor-pattern/arc-ledger-integration',
                component: ComponentCreator('/docs/guides/supervisor-pattern/arc-ledger-integration', '98a'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/guides/supervisor-pattern/basic-implementation',
                component: ComponentCreator('/docs/guides/supervisor-pattern/basic-implementation', '2ea'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/guides/supervisor-pattern/dynamic-prompts',
                component: ComponentCreator('/docs/guides/supervisor-pattern/dynamic-prompts', '7e9'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/sdk/',
                component: ComponentCreator('/docs/sdk/', '3a8'),
                exact: true
              },
              {
                path: '/docs/sdk/python/',
                component: ComponentCreator('/docs/sdk/python/', '51a'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/sdk/python/client/',
                component: ComponentCreator('/docs/sdk/python/client/', 'd46'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/sdk/python/client/chat-methods',
                component: ComponentCreator('/docs/sdk/python/client/chat-methods', '818'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/sdk/python/client/task-methods',
                component: ComponentCreator('/docs/sdk/python/client/task-methods', '5af'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/sdk/python/client/thread-manager',
                component: ComponentCreator('/docs/sdk/python/client/thread-manager', 'a4f'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/sdk/python/getting-started',
                component: ComponentCreator('/docs/sdk/python/getting-started', '930'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/spec/errors',
                component: ComponentCreator('/docs/spec/errors', 'bcc'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/spec/methods',
                component: ComponentCreator('/docs/spec/methods', 'b55'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/spec/overview',
                component: ComponentCreator('/docs/spec/overview', '3bf'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/spec/types',
                component: ComponentCreator('/docs/spec/types', '628'),
                exact: true,
                sidebar: "docs"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
