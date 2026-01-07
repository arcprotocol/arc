/**
 * Basic ARC Protocol Client Example
 * 
 * Demonstrates:
 * - Creating an ARC client
 * - Making task.create requests
 * - Making chat.start requests
 * - Basic error handling
 */

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

class ARCClient {
  private endpoint: string;
  private requestAgent: string;
  private token?: string;

  constructor(endpoint: string, requestAgent: string, token?: string) {
    this.endpoint = endpoint;
    this.requestAgent = requestAgent;
    this.token = token;
  }

  /**
   * Send a request to the ARC server
   */
  async sendRequest(
    method: string,
    targetAgent: string,
    params: Record<string, any>,
    traceId?: string
  ): Promise<ARCResponse> {
    const request: ARCRequest = {
      arc: "1.0",
      id: `req_${Date.now()}`,
      method,
      requestAgent: this.requestAgent,
      targetAgent,
      params,
      ...(traceId && { traceId }),
    };

    const headers: Record<string, string> = {
      "Content-Type": "application/arc+json",
      "Accept": "application/arc+json",
    };

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    const response = await fetch(this.endpoint, {
      method: "POST",
      headers,
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json() as ARCResponse;

    if (data.error) {
      throw new Error(`ARC Error ${data.error.code}: ${data.error.message}`);
    }

    return data;
  }

  /**
   * Create a new task
   */
  async createTask(
    targetAgent: string,
    message: string,
    priority: "LOW" | "NORMAL" | "HIGH" | "URGENT" = "NORMAL",
    traceId?: string
  ): Promise<ARCResponse> {
    return this.sendRequest(
      "task.create",
      targetAgent,
      {
        initialMessage: {
          role: "user",
          parts: [
            {
              type: "TextPart",
              content: message,
            },
          ],
        },
        priority,
      },
      traceId
    );
  }

  /**
   * Start a chat
   */
  async startChat(
    targetAgent: string,
    message: string,
    stream: boolean = false,
    traceId?: string
  ): Promise<ARCResponse> {
    return this.sendRequest(
      "chat.start",
      targetAgent,
      {
        initialMessage: {
          role: "user",
          parts: [
            {
              type: "TextPart",
              content: message,
            },
          ],
        },
        stream,
      },
      traceId
    );
  }

  /**
   * Get task information
   */
  async getTaskInfo(
    targetAgent: string,
    taskId: string,
    traceId?: string
  ): Promise<ARCResponse> {
    return this.sendRequest(
      "task.info",
      targetAgent,
      {
        taskId,
        includeMessages: true,
        includeArtifacts: true,
      },
      traceId
    );
  }

  /**
   * Send a message to an existing chat
   */
  async sendChatMessage(
    targetAgent: string,
    chatId: string,
    message: string,
    traceId?: string
  ): Promise<ARCResponse> {
    return this.sendRequest(
      "chat.message",
      targetAgent,
      {
        chatId,
        message: {
          role: "user",
          parts: [
            {
              type: "TextPart",
              content: message,
            },
          ],
        },
      },
      traceId
    );
  }
}

// Example usage
async function main() {
  const client = new ARCClient(
    "http://localhost:8000/arc",
    "travel-app-client",
    "your-oauth2-token-here"
  );

  try {
    console.log("Searching for flights...");
    const taskResponse = await client.createTask(
      "flight-finder",
      "Find flights from New York (JFK) to Los Angeles (LAX) for next Friday",
      "HIGH",
      "booking_flow_123"
    );

    console.log("Flight search task created:", taskResponse.result);
    const taskId = taskResponse.result.task.taskId;

    // Wait a bit then check status
    await new Promise((resolve) => setTimeout(resolve, 2000));

    console.log("\nChecking flight search status...");
    const taskInfo = await client.getTaskInfo(
      "flight-finder",
      taskId,
      "booking_flow_123"
    );

    console.log("Task status:", taskInfo.result.task.status);
    if (taskInfo.result.task.artifacts) {
      console.log("Found flights:", taskInfo.result.task.artifacts[0]);
    }

    // Start a price tracking chat
    console.log("\n\nStarting price tracker chat...");
    const chatResponse = await client.startChat(
      "price-tracker",
      "I want to track prices for JFK to LAX route",
      false,
      "booking_flow_456"
    );

    console.log("Price tracker chat started:", chatResponse.result);
    const chatId = chatResponse.result.chat.chatId;

    // Send follow-up message
    console.log("\nSetting price alert threshold...");
    const messageResponse = await client.sendChatMessage(
      "price-tracker",
      chatId,
      "Alert me when the price drops below $400",
      "booking_flow_456"
    );

    console.log("Alert configured:", messageResponse.result);
  } catch (error) {
    console.error("Error:", error);
  }
}

// Run the example
if (require.main === module) {
  main();
}

export { ARCClient };

