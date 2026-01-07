import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import ProtocolFlow from '@site/src/components/ProtocolFlow';
import InteractiveTerminal from '@site/src/components/InteractiveTerminal';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <section className={styles.heroSection}>
      <div className={styles.heroBanner}>
        <div className="container">
          <div className={styles.heroContent}>
            <Heading as="h1" className={styles.heroTitle}>
              Agent Remote
              <br />
              Communication
            </Heading>
            <p className={styles.heroSubtitle}>
              Stateless RPC protocol for multi-agent systems.
              <br />
              Quantum-safe. Single endpoint. End-to-end tracing.
            </p>
            <div className={styles.buttons}>
              <Link
                className="button button--primary button--lg"
                to="/docs/getting-started">
                Get Started
              </Link>
              <Link
                className="button button--secondary button--lg"
                to="/docs/spec/overview">
                View Specification
              </Link>
            </div>
            <div className={styles.quickInstall}>
              <code>pip install arc-sdk</code>
            </div>
          </div>
        </div>
      </div>

      {/* Network Visualization */}
      <div className={styles.networkSection}>
        <ProtocolFlow />
      </div>

      {/* Complete Ecosystem - Compact Strip */}
      <div className={styles.ecosystemStrip}>
        <div className="container">
          <div className={styles.ecosystemLabel}>Complete ecosystem</div>
          <div className={styles.ecosystemItems}>
            <div className={styles.ecosystemCard}>
              <h4>ARC Protocol</h4>
              <p>Core communication standard</p>
            </div>
            <div className={styles.ecosystemCard}>
              <h4>ARC Ledger</h4>
              <p>Agent discovery registry</p>
            </div>
            <div className={styles.ecosystemCard}>
              <h4>ARC Compass</h4>
              <p>Intelligent agent ranking system</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CodeExample() {
  return (
    <section className={styles.codeSection}>
      <div className="container">
        <div className={styles.codeGrid}>
          <div className={styles.codeContent}>
            <h2>Build in minutes</h2>
            <p>
              Deploy multi-agent systems with the Python SDK. Automatic conversation 
              continuity, agent routing, OAuth2 authentication, and quantum-safe TLS built-in.
            </p>
            <ul className={styles.featureList}>
              <li>✓ Conversation continuity (ThreadManager)</li>
              <li>✓ Multi-agent routing</li>
              <li>✓ OAuth2 authentication</li>
              <li>✓ SSE streaming support</li>
              <li>✓ Quantum-safe hybrid TLS</li>
              <li>✓ Production-ready storage backends</li>
            </ul>
            <Link to="/docs/guides/multi-agent-system" className="button button--primary">
              View Guides →
            </Link>
          </div>
          <div className={styles.codeBlock}>
            <pre>
              <code>{`from arc import Client

# Initialize client
client = Client(
    "https://api.example.com/arc",
    token="your-token"
)

# Call agent
response = await client.task.create(
    target_agent="finance-agent",
    initial_message={
        "role": "user",
        "parts": [{
            "type": "text",
            "content": "Analyze Q4 report"
        }]
    }
)

print(response.result)`}</code>
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
}

function UseCases() {
  return (
    <section className={styles.useCases}>
      <div className="container">
        <h2 className={styles.sectionTitle}>Built for modern AI systems</h2>
        <div className={styles.useCaseGrid}>
          <div className={styles.useCase}>
            <h3>Stateless RPC</h3>
            <p>
              Lightweight remote procedure call optimized for agent communication. 
              Route hundreds of specialized agents through a single endpoint with 
              built-in discovery and intelligent routing.
            </p>
          </div>
          <div className={styles.useCase}>
            <h3>Quantum-Safe Security</h3>
            <p>
              Hybrid TLS combining classical X25519 with post-quantum Kyber-768 
              (FIPS 203 ML-KEM). Future-proof encryption protecting against 
              quantum computing threats.
            </p>
          </div>
          <div className={styles.useCase}>
            <h3>Workflow Tracing</h3>
            <p>
              End-to-end observability across distributed agent interactions. 
              Automatic traceId propagation enables complete workflow visibility 
              and debugging capabilities.
            </p>
          </div>
          <div className={styles.useCase}>
            <h3>Multi-Agent Architectures</h3>
            <p>
              Deploy specialized agents for different domains. Finance, HR,
              support—all on one endpoint with intelligent routing.
            </p>
          </div>
          <div className={styles.useCase}>
            <h3>Enterprise Security</h3>
            <p>
              OAuth2 authentication, scope validation, and quantum-safe encryption.
              Production-ready security out of the box.
            </p>
          </div>
          <div className={styles.useCase}>
            <h3>Full Observability</h3>
            <p>
              Trace workflows across distributed agents. Integrate with LangFuse,
              OpenTelemetry, and monitoring tools.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

function Ecosystem() {
  return null; // Now part of HomepageHeader
}

function CTA() {
  return (
    <section className={styles.cta}>
      <div className="container">
        <h2>Ready to build?</h2>
        <p>Start deploying multi-agent systems in minutes</p>
        <div className={styles.ctaButtons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/getting-started">
            Get Started
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="https://github.com/arcprotocol/arcprotocol">
            View on GitHub
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Agent Remote Communication Protocol"
      description="Stateless RPC protocol for multi-agent systems with quantum-safe hybrid TLS and single-endpoint routing">
      <HomepageHeader />
      <main>
        {/* <InteractiveTerminal /> */}
        <CodeExample />
        <UseCases />
      </main>
    </Layout>
  );
}
