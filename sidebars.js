/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docs: [
    'index',
    'ecosystem',
    'getting-started',
    {
      type: 'category',
      label: 'Guides',
      collapsed: false,
      items: [
        {
          type: 'category',
          label: 'Multi-Agent System',
          items: [
            'guides/multi-agent-system/index',
            'guides/multi-agent-system/single-server',
            'guides/multi-agent-system/distributed',
            'guides/multi-agent-system/agent-communication',
          ],
        },
        {
          type: 'category',
          label: 'Supervisor Pattern',
          items: [
            'guides/supervisor-pattern/index',
            'guides/supervisor-pattern/basic-implementation',
            'guides/supervisor-pattern/arc-ledger-integration',
            'guides/supervisor-pattern/dynamic-prompts',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Concepts',
      collapsed: false,
      items: [
        {
          type: 'category',
          label: 'Protocol Design',
          items: [
            'concepts/protocol-design/index',
            'concepts/protocol-design/stateless-rpc',
            'concepts/protocol-design/single-endpoint',
            'concepts/protocol-design/error-codes',
          ],
        },
        {
          type: 'category',
          label: 'Architecture',
          items: [
            'concepts/architecture/index',
            'concepts/architecture/multi-agent',
            'concepts/architecture/supervisor-router',
            'concepts/architecture/workflow-composition',
          ],
        },
        {
          type: 'category',
          label: 'Security',
          items: [
            'concepts/security/index',
            'concepts/security/authentication',
            'concepts/security/transport',
            'concepts/security/authorization',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Python SDK',
      collapsed: false,
      items: [
        'sdk/python/index',
        'sdk/python/getting-started',
        {
          type: 'category',
          label: 'Client',
          items: [
            'sdk/python/client/index',
            'sdk/python/client/task-methods',
            'sdk/python/client/chat-methods',
            'sdk/python/client/thread-manager',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Specification',
      collapsed: false,
      items: [
        'spec/overview',
        'spec/methods',
        'spec/types',
        'spec/errors',
      ],
    },
  ],
};

export default sidebars;
