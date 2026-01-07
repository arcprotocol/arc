---
id: index
title: ARC Protocol Documentation
sidebar_label: Home
sidebar_position: 1
slug: /
hide_table_of_contents: true
---

# ARC Protocol Documentation

<div class="arc-hero-description">
  <div class="arc-hero-accent"></div>
  <p class="arc-hero-text">
    <strong>Agent Remote Communication (ARC) Protocol</strong> — A stateless RPC protocol for multi-agent systems with quantum-safe hybrid TLS encryption and single-endpoint multi-agent routing.
  </p>
</div>

<div class="arc-families-container">
  <div class="arc-families-header">
    <p class="arc-families-subtitle">Complete infrastructure for agent communication, discovery, and routing</p>
  </div>
  
  <div class="arc-families-grid">
    <div class="arc-family-card arc-protocol">
      <div class="arc-family-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2L2 7L12 12L22 7L12 2Z"/>
          <path d="M2 17L12 22L22 17"/>
          <path d="M2 12L12 17L22 12"/>
        </svg>
      </div>
      <h3>ARC Protocol</h3>
      <p class="arc-family-role">Communication Layer</p>
      <p class="arc-family-description">
        Stateless RPC protocol that solves multi-agent deployment complexity with intelligent routing, quantum-safe encryption, and end-to-end workflow tracing.
      </p>
      <div class="arc-family-features">
        <span>Single Endpoint</span>
        <span>Quantum-Safe</span>
        <span>Workflow Tracing</span>
      </div>
    </div>
    
    <div class="arc-family-card arc-compass">
      <div class="arc-family-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 2L12 12L18 18"/>
          <circle cx="12" cy="12" r="2" fill="currentColor"/>
        </svg>
      </div>
      <h3>ARC Compass</h3>
      <p class="arc-family-role">Agent Search Engine</p>
      <p class="arc-family-description">
        Intelligent ranking system that finds optimal agents through advanced algorithms, semantic extraction, and capability matching based on input requirements.
      </p>
      <div class="arc-family-features">
        <span>Semantic Search</span>
        <span>Ranking Algorithm</span>
        <span>Dynamic Discovery</span>
      </div>
    </div>
    
    <div class="arc-family-card arc-ledger">
      <div class="arc-family-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <path d="M3 9L21 9"/>
          <path d="M9 21L9 9"/>
        </svg>
      </div>
      <h3>ARC Ledger</h3>
      <p class="arc-family-role">Discovery Registry</p>
      <p class="arc-family-description">
        Centralized registry maintaining comprehensive agent cards, capabilities, endpoints, and metadata enabling efficient discovery and understanding of agent ecosystems.
      </p>
      <div class="arc-family-features">
        <span>Agent Cards</span>
        <span>Capability Index</span>
        <span>Live Updates</span>
      </div>
    </div>
  </div>
  
  <div class="arc-families-flow">
    <div class="arc-flow-step">
      <span class="arc-flow-number">1</span>
      <span class="arc-flow-text">Initiate communication</span>
      <span class="arc-flow-target">Protocol</span>
    </div>
    <div class="arc-flow-arrow">→</div>
    <div class="arc-flow-step">
      <span class="arc-flow-number">2</span>
      <span class="arc-flow-text">Query agent capabilities</span>
      <span class="arc-flow-target">Compass → Ledger</span>
    </div>
    <div class="arc-flow-arrow">→</div>
    <div class="arc-flow-step">
      <span class="arc-flow-number">3</span>
      <span class="arc-flow-text">Intelligent agent ranking</span>
      <span class="arc-flow-target">Compass</span>
    </div>
    <div class="arc-flow-arrow">→</div>
    <div class="arc-flow-step">
      <span class="arc-flow-number">4</span>
      <span class="arc-flow-text">Secure communication</span>
      <span class="arc-flow-target">Protocol</span>
    </div>
  </div>
</div>

---

## Core Features

<div class="arc-features-grid">
  <div class="arc-feature-card">
    <h4>Single Endpoint</h4>
    <p>Deploy multiple agent types on one endpoint with intelligent routing</p>
  </div>
  
  <div class="arc-feature-card">
    <h4>Quantum-Safe</h4>
    <p>Hybrid TLS using X25519 + Kyber-768 (FIPS 203 ML-KEM)</p>
  </div>
  
  <div class="arc-feature-card">
    <h4>Workflow Tracing</h4>
    <p>End-to-end observability with automatic traceId propagation</p>
  </div>
  
  <div class="arc-feature-card">
    <h4>Stateless Design</h4>
    <p>Clean RPC-style method invocation with no session state</p>
  </div>
  
  <div class="arc-feature-card">
    <h4>Real-time Streaming</h4>
    <p>Server-Sent Events (SSE) for chat responses</p>
  </div>
  
  <div class="arc-feature-card">
    <h4>Multi-Agent Routing</h4>
    <p>Built-in routing via requestAgent and targetAgent fields</p>
  </div>
</div>

## Get Started

<div class="arc-learn-grid">
  <div class="arc-learn-section">
    <h3>Quick Start</h3>
    <ul>
      <li><a href="/docs/getting-started">Getting Started Guide</a></li>
      <li><a href="/docs/spec/overview">Protocol Specification</a></li>
    </ul>
  </div>
  
  <div class="arc-learn-section">
    <h3>SDK</h3>
    <ul>
      <li><a href="/docs/sdk/python">Python SDK</a></li>
      <li><a href="/docs/sdk/python/getting-started">Installation & Setup</a></li>
    </ul>
  </div>
  
  <div class="arc-learn-section">
    <h3>Examples</h3>
    <ul>
      <li><a href="https://github.com/arcprotocol/arcprotocol/tree/main/examples/python">Python Examples</a></li>
      <li><a href="https://github.com/arcprotocol/arcprotocol/tree/main/examples/typescript">TypeScript Examples</a></li>
    </ul>
  </div>
</div>

## Learn More

<div class="arc-learn-grid">
  <div class="arc-learn-section">
    <h3>Guides</h3>
    <ul>
      <li><a href="/docs/guides/multi-agent-system">Multi-Agent System</a></li>
      <li><a href="/docs/guides/supervisor-pattern">Supervisor Pattern</a></li>
    </ul>
  </div>
  
  <div class="arc-learn-section">
    <h3>Concepts</h3>
    <ul>
      <li><a href="/docs/concepts/protocol-design">Protocol Design</a></li>
      <li><a href="/docs/concepts/architecture">Architecture</a></li>
      <li><a href="/docs/concepts/security">Security</a></li>
    </ul>
  </div>
  
  <div class="arc-learn-section">
    <h3>Resources</h3>
    <ul>
      <li><a href="https://github.com/arcprotocol/arcprotocol">GitHub</a></li>
      <li><a href="https://github.com/arcprotocol/arcprotocol/issues">Issues</a></li>
      <li><a href="https://github.com/arcprotocol/arcprotocol/blob/main/LICENSE">License</a></li>
    </ul>
  </div>
</div>
