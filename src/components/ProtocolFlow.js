import React, { useEffect, useRef, useState } from 'react';
import styles from './ProtocolFlow.module.css';

export default function ProtocolFlow() {
  const canvasRef = useRef(null);
  const [hoveredNode, setHoveredNode] = useState(null);
  const [nodeInfo, setNodeInfo] = useState({ x: 0, y: 0, label: '', type: '' });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const resizeCanvas = () => {
      canvas.width = canvas.offsetWidth * window.devicePixelRatio;
      canvas.height = canvas.offsetHeight * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Get canvas dimensions for responsive positioning
    const getCanvasWidth = () => canvas.offsetWidth;
    const getCanvasHeight = () => canvas.offsetHeight;

    // Define network topology - organic, complex layout
    // Using percentage-based positioning for responsiveness
    const getNodes = () => {
      const w = getCanvasWidth();
      const h = getCanvasHeight();
      
      return [
        // Clients (scattered entry points) - organic placement
        { id: 'client1', x: w * 0.12, y: h * 0.15, label: 'Partner Portal', type: 'client', color: '#115361', size: 28 },
        { id: 'client2', x: w * 0.50, y: h * 0.08, label: 'Travel App', type: 'client', color: '#115361', size: 28 },
        { id: 'client3', x: w * 0.08, y: h * 0.70, label: 'Public API', type: 'client', color: '#115361', size: 28 },
        
        // Supervisors (strategic central positions) - orchestrators
        { id: 'super1', x: w * 0.32, y: h * 0.35, label: 'Booking Supervisor', type: 'supervisor', color: '#383F5B', size: 38 },
        { id: 'super2', x: w * 0.28, y: h * 0.72, label: 'Customer Supervisor', type: 'supervisor', color: '#383F5B', size: 38 },
        
        // Agents (organically distributed) - workers
        { id: 'agent1', x: w * 0.55, y: h * 0.28, label: 'Flight Search', type: 'agent', color: '#A7BCC4', size: 30 },
        { id: 'agent2', x: w * 0.42, y: h * 0.52, label: 'Hotel Search', type: 'agent', color: '#A7BCC4', size: 30 },
        { id: 'agent3', x: w * 0.48, y: h * 0.75, label: 'Price Analytics', type: 'agent', color: '#A7BCC4', size: 30 },
        { id: 'agent4', x: w * 0.22, y: h * 0.88, label: 'Customer Support', type: 'agent', color: '#A7BCC4', size: 30 },
        { id: 'agent5', x: w * 0.68, y: h * 0.42, label: 'Payment', type: 'agent', color: '#A7BCC4', size: 30 },
        { id: 'agent6', x: w * 0.62, y: h * 0.65, label: 'Itinerary', type: 'agent', color: '#A7BCC4', size: 30 },
        { id: 'agent7', x: w * 0.75, y: h * 0.82, label: 'Notification', type: 'agent', color: '#A7BCC4', size: 30 },
        
        // MCPs (scattered on edges) - tools/resources
        { id: 'mcp1', x: w * 0.88, y: h * 0.25, label: 'Flight Database', type: 'mcp', color: '#115361', size: 32 },
        { id: 'mcp2', x: w * 0.92, y: h * 0.50, label: 'Payment Gateway', type: 'mcp', color: '#115361', size: 32 },
        { id: 'mcp3', x: w * 0.85, y: h * 0.72, label: 'Hotel Database', type: 'mcp', color: '#115361', size: 32 },
        { id: 'mcp4', x: w * 0.78, y: h * 0.15, label: 'Email Service', type: 'mcp', color: '#115361', size: 32 },
      ];
    };

    // Define sparse, strategic connections - organic network
    const connections = [
      // Clients to entry points (varied)
      { from: 'client1', to: 'super1', active: true }, // Partner Portal → Booking Supervisor
      { from: 'client2', to: 'agent1', active: true }, // Travel App → Flight Search (direct)
      { from: 'client3', to: 'super2', active: true }, // Public API → Customer Supervisor
      
      // Supervisor to supervisor (coordination)
      { from: 'super1', to: 'super2', active: false },
      
      // Booking Supervisor to agents
      { from: 'super1', to: 'agent1', active: true }, // → Flight Search
      { from: 'super1', to: 'agent2', active: true }, // → Hotel Search
      { from: 'super1', to: 'agent5', active: false }, // → Payment
      
      // Customer Supervisor to agents
      { from: 'super2', to: 'agent2', active: false }, // → Hotel Search (shared)
      { from: 'super2', to: 'agent3', active: true }, // → Price Analytics
      { from: 'super2', to: 'agent4', active: true }, // → Customer Support
      { from: 'super2', to: 'agent6', active: false }, // → Itinerary
      
      // Agent to agent (peer-to-peer, organic paths)
      { from: 'agent1', to: 'agent5', active: false }, // Flight → Payment
      { from: 'agent2', to: 'agent5', active: false }, // Hotel → Payment
      { from: 'agent5', to: 'agent6', active: false }, // Payment → Itinerary
      { from: 'agent2', to: 'agent3', active: false }, // Hotel → Price Analytics
      { from: 'agent3', to: 'agent6', active: false }, // Price Analytics → Itinerary
      { from: 'agent6', to: 'agent7', active: false }, // Itinerary → Notification
      
      // Agents to MCPs (varied connections)
      { from: 'agent1', to: 'mcp1', active: true }, // Flight Search → Flight Database
      { from: 'agent1', to: 'mcp4', active: false }, // Flight Search → Email Service
      { from: 'agent2', to: 'mcp3', active: true }, // Hotel Search → Hotel Database
      { from: 'agent3', to: 'mcp1', active: false }, // Price Analytics → Flight Database
      { from: 'agent3', to: 'mcp3', active: false }, // Price Analytics → Hotel Database
      { from: 'agent4', to: 'mcp4', active: false }, // Customer Support → Email Service
      { from: 'agent5', to: 'mcp2', active: true }, // Payment → Payment Gateway
      { from: 'agent6', to: 'mcp4', active: false }, // Itinerary → Email Service
      { from: 'agent7', to: 'mcp4', active: true }, // Notification → Email Service
      { from: 'agent7', to: 'mcp2', active: false }, // Notification → Payment Gateway
    ];

    let dataPackets = [];
    let animationId;
    let lastPacketTime = 0;
    let nodes = getNodes();

    const getNode = (id) => nodes.find(n => n.id === id);

    // Define realistic workflows - complete request/response cycles
    const workflows = [
      // Workflow 1: Partner Portal → Booking Supervisor → Flight Search → Flight DB → back
      ['client1', 'super1', 'agent1', 'mcp1', 'agent1', 'super1', 'client1'],
      
      // Workflow 2: Travel App → Flight Search (direct) → Flight DB → Email → back
      ['client2', 'agent1', 'mcp1', 'agent1', 'mcp4', 'agent1', 'client2'],
      
      // Workflow 3: Public API → Customer Supervisor → Hotel Search → Hotel DB → back
      ['client3', 'super2', 'agent2', 'mcp3', 'agent2', 'super2', 'client3'],
      
      // Workflow 4: Multi-agent: Booking flow with payment
      ['client1', 'super1', 'agent2', 'agent5', 'mcp2', 'agent5', 'agent6', 'agent7', 'mcp4', 'agent7', 'super1', 'client1'],
      
      // Workflow 5: Price analytics workflow
      ['client3', 'super2', 'agent3', 'mcp1', 'agent3', 'mcp3', 'agent3', 'super2', 'client3'],
    ];

    let currentWorkflowIndex = 0;
    let currentStepInWorkflow = 0;
    let activeWorkflow = null;

    const createPacket = (from, to, workflowId) => {
      return {
        from,
        to,
        progress: 0,
        speed: 0.012 + Math.random() * 0.003,
        id: Math.random(),
        workflowId,
      };
    };

    const drawConnection = (from, to, isActive, isHovered) => {
      ctx.beginPath();
      ctx.moveTo(from.x, from.y);
      ctx.lineTo(to.x, to.y);
      
      if (isHovered) {
        ctx.strokeStyle = 'rgba(17, 83, 97, 0.6)';
        ctx.lineWidth = 2.5;
        ctx.shadowBlur = 8;
        ctx.shadowColor = 'rgba(17, 83, 97, 0.4)';
      } else if (isActive) {
        ctx.strokeStyle = 'rgba(17, 83, 97, 0.25)';
        ctx.lineWidth = 1.5;
        ctx.shadowBlur = 0;
      } else {
        ctx.strokeStyle = 'rgba(167, 188, 196, 0.15)';
        ctx.lineWidth = 1;
        ctx.shadowBlur = 0;
      }
      
      ctx.stroke();
      ctx.shadowBlur = 0;
    };

    const drawNode = (node, isHovered) => {
      const scale = isHovered ? 1.2 : 1;
      const radius = node.size * scale;

      // Outer glow
      if (isHovered) {
        ctx.shadowBlur = 25;
        ctx.shadowColor = node.color;
      } else {
        ctx.shadowBlur = 12;
        ctx.shadowColor = node.color;
      }

      // Node background (glassmorphism effect)
      ctx.beginPath();
      ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
      ctx.fillStyle = isHovered ? node.color : 'rgba(255, 255, 255, 0.95)';
      ctx.fill();

      // Node border
      ctx.strokeStyle = node.color;
      ctx.lineWidth = isHovered ? 3 : 2;
      ctx.stroke();

      ctx.shadowBlur = 0;

      // Node type indicator (inner circle)
      if (node.type === 'supervisor') {
        ctx.beginPath();
        ctx.arc(node.x, node.y, radius * 0.4, 0, Math.PI * 2);
        ctx.fillStyle = isHovered ? '#FFFFFF' : node.color;
        ctx.fill();
      } else if (node.type === 'mcp') {
        // MCP gets a square indicator
        const size = radius * 0.5;
        ctx.fillStyle = isHovered ? '#FFFFFF' : node.color;
        ctx.fillRect(node.x - size/2, node.y - size/2, size, size);
      }

      // Always show label for all nodes
      ctx.fillStyle = isHovered ? '#115361' : '#5A6273';
      ctx.font = isHovered ? 'bold 13px Inter' : '600 11px Inter';
      ctx.textAlign = 'center';
      
      // Draw label below node
      const labelY = node.y + radius + 20;
      ctx.fillText(node.label, node.x, labelY);
      
      // Draw type label above node (smaller, subtle)
      ctx.font = '500 9px Inter';
      ctx.fillStyle = isHovered ? '#383F5B' : '#A7BCC4';
      ctx.textTransform = 'uppercase';
      const typeY = node.y - radius - 12;
      ctx.fillText(node.type.toUpperCase(), node.x, typeY);
    };

    const drawPacket = (packet) => {
      const fromNode = getNode(packet.from);
      const toNode = getNode(packet.to);

      if (!fromNode || !toNode) return;

      const x = fromNode.x + (toNode.x - fromNode.x) * packet.progress;
      const y = fromNode.y + (toNode.y - fromNode.y) * packet.progress;

      // Packet trail
      ctx.shadowBlur = 15;
      ctx.shadowColor = '#115361';

      // Main packet
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      
      const gradient = ctx.createRadialGradient(x, y, 0, x, y, 5);
      gradient.addColorStop(0, '#FFFFFF');
      gradient.addColorStop(0.5, '#115361');
      gradient.addColorStop(1, 'rgba(17, 83, 97, 0.3)');
      
      ctx.fillStyle = gradient;
      ctx.fill();

      ctx.shadowBlur = 0;

      // Outer glow ring
      ctx.beginPath();
      ctx.arc(x, y, 8, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(17, 83, 97, 0.15)';
      ctx.fill();
    };

    const animate = (timestamp) => {
      // Update nodes on each frame for responsiveness
      nodes = getNodes();
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Generate packets following complete workflows
      if (timestamp - lastPacketTime > 3000) {
        // Start a new workflow
        if (activeWorkflow === null || currentStepInWorkflow >= activeWorkflow.length - 1) {
          // Pick a random workflow
          currentWorkflowIndex = Math.floor(Math.random() * workflows.length);
          activeWorkflow = workflows[currentWorkflowIndex];
          currentStepInWorkflow = 0;
          
          // Start first packet of the workflow
          const from = activeWorkflow[currentStepInWorkflow];
          const to = activeWorkflow[currentStepInWorkflow + 1];
          dataPackets.push(createPacket(from, to, currentWorkflowIndex));
          currentStepInWorkflow++;
          lastPacketTime = timestamp;
        }
      }

      // Get hovered node connections
      const hoveredConnections = hoveredNode
        ? connections.filter(c => c.from === hoveredNode || c.to === hoveredNode)
        : [];

      // Highlight connections that are part of active workflows
      const activeConnections = new Set();
      dataPackets.forEach(packet => {
        activeConnections.add(`${packet.from}-${packet.to}`);
      });

      // Draw connections
      connections.forEach((conn) => {
        const fromNode = getNode(conn.from);
        const toNode = getNode(conn.to);
        const isHovered = hoveredConnections.includes(conn);
        const isActiveNow = activeConnections.has(`${conn.from}-${conn.to}`);
        if (fromNode && toNode) {
          drawConnection(fromNode, toNode, conn.active || isActiveNow, isHovered);
        }
      });

      // Draw nodes
      nodes.forEach(node => {
        drawNode(node, node.id === hoveredNode);
      });

      // Draw and update packets
      const completedPackets = [];
      dataPackets = dataPackets.filter((packet, index) => {
        packet.progress += packet.speed;
        if (packet.progress < 1) {
          drawPacket(packet);
          return true;
        } else {
          completedPackets.push(index);
          return false;
        }
      });

      // When a packet completes, start the next step in the workflow
      if (completedPackets.length > 0 && activeWorkflow && currentStepInWorkflow < activeWorkflow.length - 1) {
        const from = activeWorkflow[currentStepInWorkflow];
        const to = activeWorkflow[currentStepInWorkflow + 1];
        dataPackets.push(createPacket(from, to, currentWorkflowIndex));
        currentStepInWorkflow++;
      }

      animationId = requestAnimationFrame(animate);
    };

    animate(0);

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationId);
    };
  }, [hoveredNode]);

  const handleMouseMove = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const w = canvas.offsetWidth;
    const h = canvas.offsetHeight;

    const nodes = [
      { id: 'client1', x: w * 0.12, y: h * 0.15, label: 'Partner Portal', type: 'client', size: 28 },
      { id: 'client2', x: w * 0.50, y: h * 0.08, label: 'Travel App', type: 'client', size: 28 },
      { id: 'client3', x: w * 0.08, y: h * 0.70, label: 'Public API', type: 'client', size: 28 },
      { id: 'super1', x: w * 0.32, y: h * 0.35, label: 'Booking Supervisor', type: 'supervisor', size: 38 },
      { id: 'super2', x: w * 0.28, y: h * 0.72, label: 'Customer Supervisor', type: 'supervisor', size: 38 },
      { id: 'agent1', x: w * 0.55, y: h * 0.28, label: 'Flight Search', type: 'agent', size: 30 },
      { id: 'agent2', x: w * 0.42, y: h * 0.52, label: 'Hotel Search', type: 'agent', size: 30 },
      { id: 'agent3', x: w * 0.48, y: h * 0.75, label: 'Price Analytics', type: 'agent', size: 30 },
      { id: 'agent4', x: w * 0.22, y: h * 0.88, label: 'Customer Support', type: 'agent', size: 30 },
      { id: 'agent5', x: w * 0.68, y: h * 0.42, label: 'Payment', type: 'agent', size: 30 },
      { id: 'agent6', x: w * 0.62, y: h * 0.65, label: 'Itinerary', type: 'agent', size: 30 },
      { id: 'agent7', x: w * 0.75, y: h * 0.82, label: 'Notification', type: 'agent', size: 30 },
      { id: 'mcp1', x: w * 0.88, y: h * 0.25, label: 'Flight Database', type: 'mcp', size: 32 },
      { id: 'mcp2', x: w * 0.92, y: h * 0.50, label: 'Payment Gateway', type: 'mcp', size: 32 },
      { id: 'mcp3', x: w * 0.85, y: h * 0.72, label: 'Hotel Database', type: 'mcp', size: 32 },
      { id: 'mcp4', x: w * 0.78, y: h * 0.15, label: 'Email Service', type: 'mcp', size: 32 },
    ];

    let hoveredNode = null;
    for (const node of nodes) {
      const size = node.size || 30;
      const dx = x - node.x;
      const dy = y - node.y;
      if (Math.sqrt(dx * dx + dy * dy) < size) {
        hoveredNode = node;
        break;
      }
    }

    if (hoveredNode) {
      setHoveredNode(hoveredNode.id);
      setNodeInfo({
        x: e.clientX,
        y: e.clientY,
        label: hoveredNode.label,
        type: hoveredNode.type,
      });
    } else {
      setHoveredNode(null);
    }
  };

  const handleMouseLeave = () => {
    setHoveredNode(null);
  };

  return (
    <div className={styles.protocolFlow}>
      <div className={styles.flowContainer}>
        <canvas
          ref={canvasRef}
          className={styles.flowCanvas}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
        />
        {hoveredNode && (
          <div
            className={styles.tooltip}
            style={{
              left: `${nodeInfo.x + 15}px`,
              top: `${nodeInfo.y - 10}px`,
            }}
          >
            <div className={styles.tooltipType}>{nodeInfo.type.toUpperCase()}</div>
            <div className={styles.tooltipLabel}>{nodeInfo.label}</div>
          </div>
        )}
        <div className={styles.flowLegend}>
          <div className={styles.legendItem}>
            <span className={styles.legendDot} style={{background: '#115361', border: '2px solid #115361'}}></span>
            <span>Client / MCP</span>
          </div>
          <div className={styles.legendItem}>
            <span className={styles.legendDot} style={{background: '#383F5B', border: '2px solid #383F5B'}}></span>
            <span>Supervisor</span>
          </div>
          <div className={styles.legendItem}>
            <span className={styles.legendDot} style={{background: '#A7BCC4', border: '2px solid #A7BCC4'}}></span>
            <span>Agent</span>
          </div>
          <div className={styles.legendItem}>
            <span className={styles.legendDot} style={{background: 'rgba(17, 83, 97, 0.3)'}}></span>
            <span>Data Packet</span>
          </div>
        </div>
      </div>
    </div>
  );
}
