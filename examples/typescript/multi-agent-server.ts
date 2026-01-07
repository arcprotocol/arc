/**
 * Multi-Agent Server Example
 * 
 * Demonstrates hosting multiple agents on a single endpoint with agent-level routing.
 * This is a key feature of the ARC Protocol.
 */

import * as http from "http";

interface ARCRequest {
  arc: "1.0";
  id: string | number;
  method: string;
  requestAgent: string;
  targetAgent: string;
  params: Record<string, any>;
  traceId?: string;
}

interface ARCResponse {
  arc: "1.0";
  id: string | number;
  responseAgent: string;
  targetAgent: string;
  result: any | null;
  error: any | null;
  traceId?: string;
}

type AgentHandler = (params: any, context: any) => Promise<any>;

class MultiAgentServer {
  private serverId: string;
  private agents: Map<string, Map<string, AgentHandler>>;
  private port: number;

  constructor(serverId: string, port: number = 8000) {
    this.serverId = serverId;
    this.agents = new Map();
    this.port = port;
  }

  /**
   * Register an agent with specific method handlers
   */
  registerAgent(agentId: string, method: string, handler: AgentHandler): void {
    if (!this.agents.has(agentId)) {
      this.agents.set(agentId, new Map());
    }

    this.agents.get(agentId)!.set(method, handler);
    console.log(`Registered: ${agentId} -> ${method}`);
  }

  /**
   * Process incoming request
   */
  private async processRequest(request: ARCRequest): Promise<ARCResponse> {
    try {
      // Check if agent exists
      if (!this.agents.has(request.targetAgent)) {
        throw {
          code: -41001,
          message: `Agent not found: ${request.targetAgent}`,
          details: {
            requestedAgent: request.targetAgent,
            availableAgents: Array.from(this.agents.keys()),
          },
        };
      }

      // Check if method exists for this agent
      const agentHandlers = this.agents.get(request.targetAgent)!;
      if (!agentHandlers.has(request.method)) {
        throw {
          code: -32601,
          message: `Method ${request.method} not found for agent ${request.targetAgent}`,
          details: {
            supportedMethods: Array.from(agentHandlers.keys()),
          },
        };
      }

      // Execute handler
      const handler = agentHandlers.get(request.method)!;
      const result = await handler(request.params, {
        requestId: request.id,
        method: request.method,
        requestAgent: request.requestAgent,
        targetAgent: request.targetAgent,
        traceId: request.traceId,
      });

      return {
        arc: "1.0",
        id: request.id,
        responseAgent: request.targetAgent,
        targetAgent: request.requestAgent,
        result,
        error: null,
        ...(request.traceId && { traceId: request.traceId }),
      };
    } catch (error: any) {
      return {
        arc: "1.0",
        id: request.id,
        responseAgent: this.serverId,
        targetAgent: request.requestAgent,
        result: null,
        error: {
          code: error.code || -32603,
          message: error.message || "Internal error",
          details: error.details,
        },
        ...(request.traceId && { traceId: request.traceId }),
      };
    }
  }

  /**
   * Start the server
   */
  start(): void {
    const server = http.createServer(async (req, res) => {
      res.setHeader("Access-Control-Allow-Origin", "*");
      res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
      res.setHeader("Access-Control-Allow-Headers", "Content-Type");

      if (req.method === "OPTIONS") {
        res.writeHead(200);
        res.end();
        return;
      }

      if (req.method !== "POST" || req.url !== "/arc") {
        res.writeHead(404);
        res.end(JSON.stringify({ error: "Not found" }));
        return;
      }

      let body = "";
      req.on("data", (chunk) => (body += chunk));
      req.on("end", async () => {
        try {
          const request: ARCRequest = JSON.parse(body);
          const response = await this.processRequest(request);

          res.writeHead(200, { "Content-Type": "application/arc+json" });
          res.end(JSON.stringify(response, null, 2));
        } catch (error) {
          res.writeHead(400);
          res.end(JSON.stringify({ error: "Invalid request" }));
        }
      });
    });

    server.listen(this.port, () => {
      console.log(`\nMulti-Agent ARC Server running on http://localhost:${this.port}/arc`);
      console.log(`\nRegistered Agents:`);
      this.agents.forEach((methods, agentId) => {
        console.log(`   ${agentId}:`);
        methods.forEach((_, method) => {
          console.log(`     - ${method}`);
        });
      });
      console.log("\n");
    });
  }
}

// Example: Travel & Booking Platform - Multi-Agent System
async function main() {
  const server = new MultiAgentServer("travel-booking-platform", 8000);

  // ===== FLIGHT FINDER AGENT =====
  server.registerAgent("flight-finder", "task.create", async (params, ctx) => {
    console.log(`[flight-finder] Searching flights...`);
    console.log(`  TraceId: ${ctx.traceId}`);
    
    // Simulate flight search
    const flights = [
      { airline: "Delta", price: 450, departure: "10:30 AM", arrival: "2:45 PM", duration: "4h 15m" },
      { airline: "United", price: 420, departure: "1:15 PM", arrival: "5:30 PM", duration: "4h 15m" },
      { airline: "Southwest", price: 380, departure: "6:00 AM", arrival: "10:15 AM", duration: "4h 15m" },
    ];
    
    return {
      type: "task",
      task: {
        taskId: `flight_${Date.now()}`,
        status: "COMPLETED",
        createdAt: new Date().toISOString(),
        completedAt: new Date().toISOString(),
        artifacts: [
          {
            artifactId: `artifact_${Date.now()}`,
            name: "Flight Search Results",
            parts: [{ type: "DataPart", content: JSON.stringify(flights), mimeType: "application/json" }],
            createdAt: new Date().toISOString(),
          },
        ],
      },
    };
  });

  server.registerAgent("flight-finder", "chat.start", async (params, ctx) => {
    console.log(`[flight-finder] Starting flight search conversation...`);
    return {
      type: "chat",
      chat: {
        chatId: `flight_chat_${Date.now()}`,
        status: "ACTIVE",
        message: {
          role: "agent",
          parts: [
            {
              type: "TextPart",
              content: "Flight Search Assistant: Where would you like to fly? I can help you find the best flights by price, time, or airline.",
            },
          ],
        },
      },
    };
  });

  // ===== HOTEL BOOKING AGENT =====
  server.registerAgent("hotel-booking", "task.create", async (params, ctx) => {
    console.log(`[hotel-booking] Searching hotels...`);
    console.log(`  TraceId: ${ctx.traceId}`);
    
    // Simulate hotel search
    const hotels = [
      { name: "Grand Plaza Hotel", rating: 4.5, price: 189, amenities: ["WiFi", "Pool", "Gym"] },
      { name: "City Center Inn", rating: 4.2, price: 149, amenities: ["WiFi", "Breakfast"] },
      { name: "Airport Suites", rating: 3.8, price: 99, amenities: ["WiFi", "Shuttle"] },
    ];
    
    return {
      type: "task",
      task: {
        taskId: `hotel_${Date.now()}`,
        status: "COMPLETED",
        createdAt: new Date().toISOString(),
        completedAt: new Date().toISOString(),
        artifacts: [
          {
            artifactId: `artifact_${Date.now()}`,
            name: "Hotel Options",
            parts: [{ type: "DataPart", content: JSON.stringify(hotels), mimeType: "application/json" }],
            createdAt: new Date().toISOString(),
          },
        ],
      },
    };
  });

  server.registerAgent("hotel-booking", "chat.start", async (params, ctx) => {
    console.log(`[hotel-booking] Starting hotel booking conversation...`);
    return {
      type: "chat",
      chat: {
        chatId: `hotel_chat_${Date.now()}`,
        status: "ACTIVE",
        message: {
          role: "agent",
          parts: [
            {
              type: "TextPart",
              content: "Hotel Booking Agent: I'll help you find the perfect accommodation. What city and dates are you looking for?",
            },
          ],
        },
      },
    };
  });

  // ===== ITINERARY PLANNER AGENT =====
  server.registerAgent("itinerary-planner", "task.create", async (params, ctx) => {
    console.log(`[itinerary-planner] Creating travel itinerary...`);
    console.log(`  TraceId: ${ctx.traceId}`);
    
    // Simulate itinerary creation
    const itinerary = {
      destination: "Paris, France",
      days: 5,
      schedule: [
        { day: 1, activities: ["Arrive", "Eiffel Tower", "Seine River Cruise"] },
        { day: 2, activities: ["Louvre Museum", "Notre-Dame", "Latin Quarter"] },
        { day: 3, activities: ["Versailles Palace", "Shopping", "Moulin Rouge"] },
        { day: 4, activities: ["Montmartre", "Sacré-Cœur", "Arc de Triomphe"] },
        { day: 5, activities: ["Last minute shopping", "Departure"] },
      ],
      estimatedBudget: 2500,
    };
    
    return {
      type: "task",
      task: {
        taskId: `itinerary_${Date.now()}`,
        status: "COMPLETED",
        createdAt: new Date().toISOString(),
        completedAt: new Date().toISOString(),
        artifacts: [
          {
            artifactId: `artifact_${Date.now()}`,
            name: "5-Day Paris Itinerary",
            parts: [{ type: "DataPart", content: JSON.stringify(itinerary), mimeType: "application/json" }],
            createdAt: new Date().toISOString(),
          },
        ],
      },
    };
  });

  server.registerAgent("itinerary-planner", "chat.start", async (params, ctx) => {
    console.log(`[itinerary-planner] Starting itinerary planning...`);
    return {
      type: "chat",
      chat: {
        chatId: `itinerary_chat_${Date.now()}`,
        status: "ACTIVE",
        message: {
          role: "agent",
          parts: [
            {
              type: "TextPart",
              content: "Travel Planner: I'll create a personalized itinerary for your trip! What's your destination and how many days?",
            },
          ],
        },
      },
    };
  });

  // ===== PRICE TRACKER AGENT =====
  server.registerAgent("price-tracker", "task.create", async (params, ctx) => {
    console.log(`[price-tracker] Setting up price alerts...`);
    console.log(`  TraceId: ${ctx.traceId}`);
    
    // Simulate price tracking setup
    const priceHistory = [
      { date: "2024-01-01", price: 520 },
      { date: "2024-01-08", price: 480 },
      { date: "2024-01-15", price: 450 },
      { date: "2024-01-22", price: 420 },
    ];
    
    return {
      type: "task",
      task: {
        taskId: `tracker_${Date.now()}`,
        status: "SUBMITTED",
        createdAt: new Date().toISOString(),
        metadata: {
          tracking: "JFK → LAX",
          currentPrice: 420,
          lowestPrice: 380,
          priceDropAlert: true,
          alertThreshold: 400,
        },
        artifacts: [
          {
            artifactId: `artifact_${Date.now()}`,
            name: "Price History",
            parts: [{ type: "DataPart", content: JSON.stringify(priceHistory), mimeType: "application/json" }],
            createdAt: new Date().toISOString(),
          },
        ],
      },
    };
  });

  server.registerAgent("price-tracker", "chat.start", async (params, ctx) => {
    console.log(`[price-tracker] Starting price alert setup...`);
    return {
      type: "chat",
      chat: {
        chatId: `tracker_chat_${Date.now()}`,
        status: "ACTIVE",
        message: {
          role: "agent",
          parts: [
            {
              type: "TextPart",
              content: "Price Tracker: I'll monitor prices and alert you when they drop! What route and price point are you interested in?",
            },
          ],
        },
      },
    };
  });

  server.registerAgent("price-tracker", "chat.message", async (params, ctx) => {
    console.log(`[price-tracker] Updating price alert in chat ${params.chatId}`);
    return {
      type: "chat",
      chat: {
        chatId: params.chatId,
        status: "ACTIVE",
        message: {
          role: "agent",
          parts: [
            {
              type: "TextPart",
              content: "Great! I've set up a price alert. You'll get notified when the price drops below $400. Current price: $420.",
            },
          ],
        },
      },
    };
  });

  server.start();
}

if (require.main === module) {
  main();
}

export { MultiAgentServer };

