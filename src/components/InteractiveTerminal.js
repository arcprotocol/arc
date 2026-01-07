import React, { useEffect, useState, useRef } from 'react';
import styles from './InteractiveTerminal.module.css';

const codeExamples = [
  {
    title: 'Basic Task Call',
    language: 'python',
    code: `from arc import Client

client = Client(
    "https://api.example.com/arc",
    token="your-token"
)

response = await client.task.create(
    target_agent="finance-agent",
    initial_message={
        "role": "user",
        "parts": [{
            "type": "text",
            "content": "Analyze Q4 revenue"
        }]
    }
)

print(response.result)`,
  },
  {
    title: 'Streaming Chat',
    language: 'python',
    code: `async for event in client.chat.stream(
    target_agent="support-agent",
    chat_id="chat-123",
    message={
        "role": "user",
        "parts": [{
            "type": "text",
            "content": "Help with billing"
        }]
    }
):
    if event.type == "text_delta":
        print(event.delta, end="")`,
  },
  {
    title: 'Multi-Agent Workflow',
    language: 'python',
    code: `# Supervisor routes to specialized agents
supervisor = await client.task.create(
    target_agent="supervisor",
    initial_message={
        "role": "user",
        "parts": [{
            "type": "text",
            "content": "Book flight to NYC"
        }]
    }
)

# Automatic routing to flight-agent
# Quantum-safe encryption throughout
# Full traceId propagation`,
  },
  {
    title: 'Agent Server',
    language: 'python',
    code: `from arc import ARCServer, ARCResponse

server = ARCServer(agent_id="finance-agent")

@server.task_handler
async def handle_task(request):
    # Process financial analysis
    result = analyze_finances(
        request.initial_message
    )
    
    return ARCResponse(
        status="completed",
        result=result
    )

server.run()`,
  },
];

export default function InteractiveTerminal() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [displayedCode, setDisplayedCode] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const typingRef = useRef(null);

  useEffect(() => {
    // Clear previous timeout
    if (typingRef.current) {
      clearTimeout(typingRef.current);
    }

    setIsTyping(true);
    setDisplayedCode('');

    const targetCode = codeExamples[activeIndex].code;
    let currentIndex = 0;

    const typeCode = () => {
      if (currentIndex < targetCode.length) {
        setDisplayedCode(targetCode.slice(0, currentIndex + 1));
        currentIndex++;
        typingRef.current = setTimeout(typeCode, 10);
      } else {
        setIsTyping(false);
      }
    };

    typeCode();

    return () => {
      if (typingRef.current) {
        clearTimeout(typingRef.current);
      }
    };
  }, [activeIndex]);

  // Auto-cycle through examples
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % codeExamples.length);
    }, 8000);

    return () => clearInterval(interval);
  }, []);

  const syntaxHighlight = (code) => {
    // Simple syntax highlighting
    return code
      .split('\n')
      .map((line, i) => {
        let highlighted = line;

        // Keywords
        const keywords = ['from', 'import', 'async', 'await', 'for', 'in', 'if', 'return', 'def', 'class'];
        keywords.forEach(keyword => {
          highlighted = highlighted.replace(
            new RegExp(`\\b${keyword}\\b`, 'g'),
            `<span class="${styles.keyword}">${keyword}</span>`
          );
        });

        // Strings
        highlighted = highlighted.replace(
          /(["'])(.*?)\1/g,
          `<span class="${styles.string}">$1$2$1</span>`
        );

        // Comments
        highlighted = highlighted.replace(
          /(#.*$)/g,
          `<span class="${styles.comment}">$1</span>`
        );

        // Functions
        highlighted = highlighted.replace(
          /\b(\w+)\(/g,
          `<span class="${styles.function}">$1</span>(`
        );

        return (
          <div key={i} className={styles.codeLine}>
            <span className={styles.lineNumber}>{String(i + 1).padStart(2, ' ')}</span>
            <span dangerouslySetInnerHTML={{ __html: highlighted }} />
          </div>
        );
      });
  };

  return (
    <div className={styles.terminalSection}>
      <div className="container">
        <div className={styles.terminalContainer}>
          <div className={styles.terminalHeader}>
            <h2>Code That Speaks</h2>
            <p>Interactive examples morphing in real-time</p>
          </div>

          <div className={styles.terminalTabs}>
            {codeExamples.map((example, index) => (
              <button
                key={index}
                className={`${styles.tab} ${activeIndex === index ? styles.activeTab : ''}`}
                onClick={() => setActiveIndex(index)}
              >
                {example.title}
              </button>
            ))}
          </div>

          <div className={styles.terminalWindow}>
            <div className={styles.terminalControls}>
              <span className={styles.dot} style={{ background: '#FF5F56' }}></span>
              <span className={styles.dot} style={{ background: '#FFBD2E' }}></span>
              <span className={styles.dot} style={{ background: '#27C93F' }}></span>
            </div>

            <div className={styles.terminalContent}>
              <div className={styles.codeBlock}>
                {syntaxHighlight(displayedCode)}
                {isTyping && <span className={styles.cursor}>▋</span>}
              </div>
            </div>
          </div>

          <div className={styles.terminalFeatures}>
            <div className={styles.featureChip}>Real-time typing</div>
            <div className={styles.featureChip}>Syntax highlighting</div>
            <div className={styles.featureChip}>Auto-morphing</div>
          </div>
        </div>
      </div>
    </div>
  );
}

