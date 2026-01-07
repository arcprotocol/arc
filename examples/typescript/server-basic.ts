/**
 * Basic ARC Protocol Server Example
 * 
 * Demonstrates:
 * - Creating an ARC server
 * - Registering method handlers
 * - Processing requests
 * - Sending responses
 * - Error handling
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
  error: ARCError | null;
  traceId?: string;
}

interface ARCError {
  code: number;
  message: string;
  details?: any;
}

type MethodHandler = (
  params: Record<string, any>,
  context: RequestContext
) => Promise<any>;

interface RequestContext {
  requestId: string | number;
  method: string;
  requestAgent: string;
  targetAgent: string;
  traceId?: string;
}

class ARCServer {
  private agentId: string;
  private handlers: Map<string, MethodHandler>;
  private port: number;

  constructor(agentId: string, port: number = 8000) {
    this.agentId = agentId;
    this.handlers = new Map();
    this.port = port;
  }

  /**
   * Register a method handler
   */
  registerHandler(method: string, handler: MethodHandler): void {
    this.handlers.set(method, handler);
    console.log(`Registered handler for method: ${method}`);
  }

  /**
   * Process an ARC request
   */
  private async processRequest(request: ARCRequest): Promise<ARCResponse> {
    const context: RequestContext = {
      requestId: request.id,
      method: request.method,
      requestAgent: request.requestAgent,
      targetAgent: request.targetAgent,
      traceId: request.traceId,
    };

    try {
      // Validate request
      if (!request.arc || request.arc !== "1.0") {
        throw {
          code: -45001,
          message: `Invalid ARC version: ${request.arc}`,
          details: { supportedVersion: "1.0" },
        };
      }

      // Check if handler exists
      const handler = this.handlers.get(request.method);
      if (!handler) {
        throw {
          code: -32601,
          message: `Method not found: ${request.method}`,
          details: {
            method: request.method,
            supportedMethods: Array.from(this.handlers.keys()),
          },
        };
      }

      // Execute handler
      const result = await handler(request.params, context);

      // Build response
      const response: ARCResponse = {
        arc: "1.0",
        id: request.id,
        responseAgent: this.agentId,
        targetAgent: request.requestAgent,
        result,
        error: null,
      };

      if (request.traceId) {
        response.traceId = request.traceId;
      }

      return response;
    } catch (error: any) {
      // Build error response
      const response: ARCResponse = {
        arc: "1.0",
        id: request.id,
        responseAgent: this.agentId,
        targetAgent: request.requestAgent,
        result: null,
        error: {
          code: error.code || -32603,
          message: error.message || "Internal error",
          details: error.details,
        },
      };

      if (request.traceId) {
        response.traceId = request.traceId;
      }

      return response;
    }
  }

  /**
   * Start the HTTP server
   */
  start(): void {
    const server = http.createServer(async (req, res) => {
      // Handle CORS
      res.setHeader("Access-Control-Allow-Origin", "*");
      res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
      res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

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

      // Read request body
      let body = "";
      req.on("data", (chunk) => {
        body += chunk.toString();
      });

      req.on("end", async () => {
        try {
          const request: ARCRequest = JSON.parse(body);
          const response = await this.processRequest(request);

          res.writeHead(200, { "Content-Type": "application/arc+json" });
          res.end(JSON.stringify(response, null, 2));
        } catch (error) {
          res.writeHead(400, { "Content-Type": "application/json" });
          res.end(
            JSON.stringify({
              error: "Invalid request",
              message: error instanceof Error ? error.message : "Unknown error",
            })
          );
        }
      });
    });

    server.listen(this.port, () => {
      console.log(`ARC Server listening on http://localhost:${this.port}/arc`);
      console.log(`Agent ID: ${this.agentId}`);
    });
  }
}

// Example usage
async function main() {
  const server = new ARCServer("example-agent", 8000);

  // Register task.create handler
  server.registerHandler("task.create", async (params, context) => {
    console.log(`\n[${context.method}] Request from ${context.requestAgent}`);
    console.log("Params:", JSON.stringify(params, null, 2));

    const taskId = `task_${Date.now()}`;

    return {
      type: "task",
      task: {
        taskId,
        status: "SUBMITTED",
        createdAt: new Date().toISOString(),
      },
    };
  });

  // Register task.info handler
  server.registerHandler("task.info", async (params, context) => {
    console.log(`\n[${context.method}] Request from ${context.requestAgent}`);
    console.log("Task ID:", params.taskId);

    return {
      type: "task",
      task: {
        taskId: params.taskId,
        status: "WORKING",
        createdAt: new Date().toISOString(),
        messages: [
          {
            role: "user",
            parts: [
              {
                type: "TextPart",
                content: "Analyze the quarterly financial report",
              },
            ],
          },
        ],
      },
    };
  });

  // Register chat.start handler
  server.registerHandler("chat.start", async (params, context) => {
    console.log(`\n[${context.method}] Request from ${context.requestAgent}`);
    console.log("Message:", params.initialMessage.parts[0].content);

    const chatId = `chat_${Date.now()}`;

    return {
      type: "chat",
      chat: {
        chatId,
        status: "ACTIVE",
        message: {
          role: "agent",
          parts: [
            {
              type: "TextPart",
              content: "Hello! How can I help you today?",
            },
          ],
        },
        createdAt: new Date().toISOString(),
      },
    };
  });

  // Start the server
  server.start();
}

// Run the server
if (require.main === module) {
  main();
}

export { ARCServer };

