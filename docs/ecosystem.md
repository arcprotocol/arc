---
id: ecosystem
title: Ecosystem Architecture
sidebar_position: 2
hide_table_of_contents: false
---

# Ecosystem Architecture

The ARC ecosystem consists of three independent yet integrated systems: Protocol for communication, Ledger for registry, and Compass for intelligence. Each operates autonomously while enabling three distinct integration models.

## System Components

<div className="arc-features-grid">
  <div className="arc-feature-card">
    <h4>ARC Protocol</h4>
    <p>Stateless RPC communication layer. Handles message routing, workflow tracing, and quantum-safe transport between agents. Operates independently with hardcoded endpoints or integrates with discovery services.</p>
  </div>
  
  <div className="arc-feature-card">
    <h4>ARC Ledger</h4>
    <p>Centralized agent registry. Maintains database of agent capabilities, endpoints, and metadata. Field-based query API returns all matching agents.</p>
  </div>
  
  <div className="arc-feature-card">
    <h4>ARC Compass</h4>
    <p>Intelligent ranking engine. Applies semantic analysis, capability matching, and ML-based scoring to agent queries. Returns ranked agent selections from Ledger data.</p>
  </div>
</div>

---

## Ledger vs Compass

<div style={{
  display: 'grid',
  gridTemplateColumns: '1fr 2px 1fr',
  gap: 0,
  margin: '3rem 0',
  border: '1px solid rgba(17, 83, 97, 0.15)',
  borderRadius: '12px',
  overflow: 'hidden',
}}>
  <div style={{background: '#ffffff'}}>
    <div style={{
      background: 'linear-gradient(135deg, rgba(17, 83, 97, 0.08) 0%, rgba(17, 83, 97, 0.12) 100%)',
      padding: '1.5rem',
      borderBottom: '2px solid rgba(17, 83, 97, 0.2)',
    }}>
      <h3 style={{margin: 0, color: '#115361', fontSize: '1.25rem', fontWeight: '700', textAlign: 'center'}}>ARC Ledger</h3>
    </div>
    <div style={{padding: '2rem'}}>
      <div style={{marginBottom: '1.75rem'}}>
        <div style={{
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#115361',
          marginBottom: '0.5rem',
        }}>Function</div>
        <div style={{color: '#383F5B', fontSize: '1rem'}}>Passive registry and search</div>
      </div>
      
      <div style={{marginBottom: '1.75rem'}}>
        <div style={{
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#115361',
          marginBottom: '0.5rem',
        }}>Input</div>
        <div style={{color: '#383F5B', fontSize: '1rem'}}>Field-based database query</div>
      </div>
      
      <div style={{marginBottom: '1.75rem'}}>
        <div style={{
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#115361',
          marginBottom: '0.5rem',
        }}>Output</div>
        <div style={{color: '#383F5B', fontSize: '1rem'}}>All matching records (unranked)</div>
      </div>
      
      <div style={{marginBottom: '1.75rem'}}>
        <div style={{
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#115361',
          marginBottom: '0.5rem',
        }}>Logic</div>
        <div style={{color: '#383F5B', fontSize: '1rem'}}>Exact field matching</div>
      </div>
      
      <div style={{
        background: 'rgba(17, 83, 97, 0.04)',
        padding: '1rem',
        borderRadius: '8px',
        borderLeft: '3px solid #115361',
      }}>
        <div style={{
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#115361',
          marginBottom: '0.5rem',
        }}>Example</div>
        <div style={{fontFamily: 'monospace', fontSize: '0.875rem', color: '#5A6273', lineHeight: '1.6'}}>
          Query: tag="hotel", capability="booking"<br/>
          Returns: 50 agents
        </div>
      </div>
    </div>
  </div>

  <div style={{
    background: 'linear-gradient(180deg, rgba(17, 83, 97, 0.2) 0%, rgba(17, 83, 97, 0.1) 100%)',
  }}></div>

  <div style={{background: '#ffffff'}}>
    <div style={{
      background: 'linear-gradient(135deg, rgba(13, 68, 80, 0.12) 0%, rgba(13, 68, 80, 0.16) 100%)',
      padding: '1.5rem',
      borderBottom: '2px solid rgba(13, 68, 80, 0.25)',
    }}>
      <h3 style={{margin: 0, color: '#0d4450', fontSize: '1.25rem', fontWeight: '700', textAlign: 'center'}}>ARC Compass</h3>
    </div>
    <div style={{padding: '2rem'}}>
      <div style={{marginBottom: '1.75rem'}}>
        <div style={{
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#0d4450',
          marginBottom: '0.5rem',
        }}>Function</div>
        <div style={{color: '#383F5B', fontSize: '1rem'}}>Active intelligence and ranking</div>
      </div>
      
      <div style={{marginBottom: '1.75rem'}}>
        <div style={{
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#0d4450',
          marginBottom: '0.5rem',
        }}>Input</div>
        <div style={{color: '#383F5B', fontSize: '1rem'}}>Natural language query</div>
      </div>
      
      <div style={{marginBottom: '1.75rem'}}>
        <div style={{
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#0d4450',
          marginBottom: '0.5rem',
        }}>Output</div>
        <div style={{color: '#383F5B', fontSize: '1rem'}}>Top-N ranked agents</div>
      </div>
      
      <div style={{marginBottom: '1.75rem'}}>
        <div style={{
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#0d4450',
          marginBottom: '0.5rem',
        }}>Logic</div>
        <div style={{color: '#383F5B', fontSize: '1rem'}}>Semantic analysis + ML scoring</div>
      </div>
      
      <div style={{
        background: 'rgba(13, 68, 80, 0.06)',
        padding: '1rem',
        borderRadius: '8px',
        borderLeft: '3px solid #0d4450',
      }}>
        <div style={{
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          color: '#0d4450',
          marginBottom: '0.5rem',
        }}>Example</div>
        <div style={{fontFamily: 'monospace', fontSize: '0.875rem', color: '#5A6273', lineHeight: '1.6'}}>
          Query: "luxury hotel Paris Michelin"<br/>
          Returns: Top 3 specialized agents
        </div>
      </div>
    </div>
  </div>
</div>

---

## Integration Levels

Three deployment configurations enable different operational requirements:

<div style={{
  display: 'grid',
  gridTemplateColumns: 'repeat(3, 1fr)',
  gap: '1.5rem',
  margin: '2rem 0 3rem',
}}>
  <div style={{
    background: 'rgba(255, 255, 255, 0.6)',
    border: '1px solid rgba(17, 83, 97, 0.1)',
    borderRadius: '12px',
    padding: '1.5rem',
    textAlign: 'center',
  }}>
    <h4 style={{margin: '0 0 0.75rem 0', color: '#383F5B', fontSize: '1.125rem'}}>Level 1</h4>
    <p style={{margin: '0 0 0.5rem 0', color: '#115361', fontWeight: '600'}}>Protocol Only</p>
    <p style={{margin: 0, color: '#5A6273', fontSize: '0.875rem'}}>Manual configuration, static endpoints</p>
  </div>
  
  <div style={{
    background: 'rgba(255, 255, 255, 0.6)',
    border: '1px solid rgba(17, 83, 97, 0.1)',
    borderRadius: '12px',
    padding: '1.5rem',
    textAlign: 'center',
  }}>
    <h4 style={{margin: '0 0 0.75rem 0', color: '#383F5B', fontSize: '1.125rem'}}>Level 2</h4>
    <p style={{margin: '0 0 0.5rem 0', color: '#115361', fontWeight: '600'}}>Protocol + Ledger</p>
    <p style={{margin: 0, color: '#5A6273', fontSize: '0.875rem'}}>Dynamic discovery, manual selection</p>
  </div>
  
  <div style={{
    background: 'rgba(255, 255, 255, 0.6)',
    border: '1px solid rgba(17, 83, 97, 0.1)',
    borderRadius: '12px',
    padding: '1.5rem',
    textAlign: 'center',
  }}>
    <h4 style={{margin: '0 0 0.75rem 0', color: '#383F5B', fontSize: '1.125rem'}}>Level 3</h4>
    <p style={{margin: '0 0 0.5rem 0', color: '#115361', fontWeight: '600'}}>Full Ecosystem</p>
    <p style={{margin: 0, color: '#5A6273', fontSize: '0.875rem'}}>Intelligent ranking, autonomous routing</p>
  </div>
</div>

---

### Level 1: Protocol Only

**Architecture:** Standalone communication layer with manual endpoint configuration.

**Components:**
- ARC Protocol

**Flow:**
```
Client → Protocol → Agent (hardcoded endpoint)
```

**Configuration:**
```python
client = ARCClient(
    endpoint="https://booking-agent.com/arc",
    token="token"
)
```

**Characteristics:**
- Static agent endpoints
- No discovery mechanism
- Direct point-to-point communication
- Manual configuration management

**Use Case:** Small-scale systems, known agent topology, controlled environment.

---

### Level 2: Protocol + Ledger

**Architecture:** Communication layer with dynamic agent discovery.

**Components:**
- ARC Protocol
- ARC Ledger

**Flow:**
```
Client → Ledger (field-based query: capabilities, tags, filters)
       → Ledger returns all matching agents (unranked)
       → Manual selection
       → Protocol routes to selected agent
```

**Implementation:**
```python
# Query Ledger by field filters
ledger = LedgerClient(api_key="key")
agents = ledger.query(
    tag="hotel",
    capabilities=["hotel-booking", "luxury-travel"]
)

# Manual selection from unranked results
selected = agents[0]

# Protocol communication
client = ARCClient(endpoint=selected.endpoint, token="token")
response = await client.task_create(...)
```

**Characteristics:**
- Dynamic endpoint resolution
- Field-based capability search
- Manual agent selection from unranked results
- Decoupled agent deployment

**Use Case:** Medium-scale systems, field-based agent search, human-in-loop selection.

---

### Level 3: Protocol + Ledger + Compass

**Architecture:** Full autonomous system with intelligent agent selection.

**Components:**
- ARC Protocol
- ARC Ledger  
- ARC Compass

**Flow:**
```
Client → Compass (natural language query)
       ↓
     Compass queries Ledger (field-based capability search)
       ↓
     Ledger returns all matching agents (unranked)
       ↓
     Compass ranks agents (semantic + ML + performance)
       ↓
     Protocol routes to top-ranked agent
       ↓
     Agent executes → Response
```

**Implementation:**
```python
# Single semantic query to Compass
compass = CompassClient(api_key="key")
result = compass.select_agent(
    query="Book luxury hotel in Paris with Michelin restaurant"
)

# Compass returns top-ranked agent after querying Ledger internally
client = ARCClient(
    endpoint=result.top_agent.endpoint,
    token="token"
)
response = await client.task_create(...)
```

**Characteristics:**
- Natural language query input
- Intelligent multi-factor ranking
- Autonomous optimal agent selection
- Performance-based optimization over time

**Use Case:** Large-scale systems, natural language queries, autonomous intelligent routing.

---

## Data Flow Example

**User Query:** "Book luxury hotel in Paris with Michelin restaurant"

**Step 1: Compass Receives Natural Language Query**
- Parse semantic intent: luxury accommodation, Paris location, Michelin dining
- Map to field filters for Ledger query

**Step 2: Compass Queries Ledger**
- Compass sends field-based query: `tag="hotel", capabilities=["luxury-travel", "restaurant-booking"], location="Paris"`
- Ledger returns: 47 matching agents (unranked)

**Step 3: Compass Applies Ranking Algorithm**
- Semantic relevance: Score agent descriptions against original natural language query
- Performance history: Weight by historical response times and success rates
- Capability depth: Evaluate specialization strength in luxury hospitality
- Availability: Filter by real-time agent status

**Step 4: Compass Returns Ranked Results**
```
1. Agent: paris-luxury-concierge (Score: 0.94)
2. Agent: michelin-travel-specialist (Score: 0.89)
3. Agent: europe-hospitality-pro (Score: 0.82)
```

**Step 5: Protocol Routes to Top Agent**
- Client receives top-ranked agent from Compass
- Protocol establishes connection to `paris-luxury-concierge`
- Execute booking request with workflow tracing
- Return response to client

---

## Links

- [Getting Started](./getting-started.md)
- [Protocol Specification](./spec/overview.md)
- [ARC Ledger](https://github.com/arcprotocol/arcledger)
- [ARC Compass](https://github.com/arcprotocol/arccompass)
