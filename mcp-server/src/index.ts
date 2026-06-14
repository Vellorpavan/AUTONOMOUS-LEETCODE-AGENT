#!/usr/bin/env node
/**
 * LeetCode MCP Server
 * Exposes 6 tools to the autonomous agent via the MCP stdio transport.
 *
 * Tools:
 *   check_auth      — verify LeetCode session
 *   get_progress    — solved/total counts by difficulty
 *   list_problems   — paginated problem list with filters
 *   get_problem     — full description + Python starter code
 *   submit_code     — submit a solution
 *   get_result      — poll for verdict + diagnostics
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";

// Load .env from the agent directory (passed via env or fallback)
const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: process.env.ENV_FILE ?? path.join(__dirname, "../../agent/.env") });

import { createClientFromEnv } from "./leetcode-client.js";
import { checkAuth } from "./tools/check_auth.js";
import { getProgress } from "./tools/get_progress.js";
import { listProblems } from "./tools/list_problems.js";
import { getProblem } from "./tools/get_problem.js";
import { submitCode } from "./tools/submit_code.js";
import { getResult } from "./tools/get_result.js";

// ─── Tool Schemas ─────────────────────────────────────────────────────────────

const CheckAuthInput = z.object({});

const GetProgressInput = z.object({
  username: z.string().describe("LeetCode username to fetch stats for"),
});

const ListProblemsInput = z.object({
  unsolvedOnly: z
    .boolean()
    .optional()
    .default(false)
    .describe("If true, only return unsolved problems"),
  difficulty: z
    .enum(["Easy", "Medium", "Hard"])
    .optional()
    .describe("Filter by difficulty"),
  fetchAll: z
    .boolean()
    .optional()
    .default(false)
    .describe("Fetch all problems in one shot (up to 3000)"),
  limit: z.number().optional().default(50).describe("Page size"),
  skip: z.number().optional().default(0).describe("Offset for pagination"),
});

const GetProblemInput = z.object({
  slug: z.string().describe("Problem title slug, e.g. 'two-sum'"),
});

const SubmitCodeInput = z.object({
  slug: z.string().describe("Problem title slug"),
  lang: z
    .string()
    .default("python3")
    .describe("Language slug, e.g. 'python3', 'cpp'"),
  code: z.string().describe("Full solution code to submit"),
  questionId: z
    .number()
    .describe("Numeric questionId (not frontendId) from get_problem"),
});

const GetResultInput = z.object({
  submissionId: z.number().describe("Submission ID returned by submit_code"),
  maxWaitMs: z
    .number()
    .optional()
    .default(30000)
    .describe("Max milliseconds to wait for result"),
});

// ─── Server Setup ─────────────────────────────────────────────────────────────

const server = new Server(
  { name: "leetcode-mcp-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// ─── Tool Registration ────────────────────────────────────────────────────────

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "check_auth",
      description:
        "Verify that the LeetCode session cookies are valid. Call this once at startup.",
      inputSchema: {
        type: "object",
        properties: {},
        required: [],
      },
    },
    {
      name: "get_progress",
      description:
        "Return solved/total problem counts broken down by difficulty (Easy, Medium, Hard).",
      inputSchema: {
        type: "object",
        properties: {
          username: {
            type: "string",
            description: "LeetCode username",
          },
        },
        required: ["username"],
      },
    },
    {
      name: "list_problems",
      description:
        "List LeetCode problems. Supports filtering by difficulty and unsolved status.",
      inputSchema: {
        type: "object",
        properties: {
          unsolvedOnly: { type: "boolean", default: false },
          difficulty: { type: "string", enum: ["Easy", "Medium", "Hard"] },
          fetchAll: { type: "boolean", default: false },
          limit: { type: "number", default: 50 },
          skip: { type: "number", default: 0 },
        },
        required: [],
      },
    },
    {
      name: "get_problem",
      description:
        "Fetch the full problem: description (plain text), constraints, examples, and Python 3 starter code.",
      inputSchema: {
        type: "object",
        properties: {
          slug: {
            type: "string",
            description: "Problem slug, e.g. 'two-sum'",
          },
        },
        required: ["slug"],
      },
    },
    {
      name: "submit_code",
      description: "Submit a solution to LeetCode. Returns the submission ID.",
      inputSchema: {
        type: "object",
        properties: {
          slug: { type: "string" },
          lang: { type: "string", default: "python3" },
          code: { type: "string" },
          questionId: {
            type: "number",
            description: "Internal questionId (numeric) from get_problem",
          },
        },
        required: ["slug", "code", "questionId"],
      },
    },
    {
      name: "get_result",
      description:
        "Poll for the verdict of a submission. Returns verdict, runtime, memory, and failure diagnostics.",
      inputSchema: {
        type: "object",
        properties: {
          submissionId: { type: "number" },
          maxWaitMs: { type: "number", default: 30000 },
        },
        required: ["submissionId"],
      },
    },
  ],
}));

// ─── Tool Dispatcher ──────────────────────────────────────────────────────────

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    const client = createClientFromEnv();

    switch (name) {
      case "check_auth": {
        CheckAuthInput.parse(args);
        const result = await checkAuth(client);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      }

      case "get_progress": {
        const { username } = GetProgressInput.parse(args);
        const result = await getProgress(client, username);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      }

      case "list_problems": {
        const opts = ListProblemsInput.parse(args);
        const result = await listProblems(client, opts);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      }

      case "get_problem": {
        const { slug } = GetProblemInput.parse(args);
        const result = await getProblem(client, slug);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      }

      case "submit_code": {
        const { slug, lang, code, questionId } = SubmitCodeInput.parse(args);
        const result = await submitCode(client, slug, lang, code, questionId);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      }

      case "get_result": {
        const { submissionId, maxWaitMs } = GetResultInput.parse(args);
        const result = await getResult(client, submissionId, maxWaitMs);
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    return {
      content: [{ type: "text", text: `ERROR: ${msg}` }],
      isError: true,
    };
  }
});

// ─── Start ────────────────────────────────────────────────────────────────────

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("LeetCode MCP Server running on stdio");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
