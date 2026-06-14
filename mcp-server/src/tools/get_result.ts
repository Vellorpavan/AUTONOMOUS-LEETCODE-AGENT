import { LeetCodeClient } from "../leetcode-client.js";

export type Verdict =
  | "Accepted"
  | "Wrong Answer"
  | "Time Limit Exceeded"
  | "Runtime Error"
  | "Memory Limit Exceeded"
  | "Compile Error"
  | "Output Limit Exceeded"
  | "Unknown";

export interface SubmissionResult {
  verdict: Verdict;
  statusCode: number;
  runtime: string;
  memory: string;
  runtimePercentile: number | null;
  memoryPercentile: number | null;
  // Failure diagnostics
  failingInput?: string;
  expectedOutput?: string;
  actualOutput?: string;
  errorMessage?: string;
  totalTestCases?: number;
  passedTestCases?: number;
}

interface CheckResponse {
  state: string; // "PENDING" | "STARTED" | "SUCCESS"
  status_code: number;
  status_msg: string;
  lang: string;
  run_success: boolean;
  status_runtime: string;
  memory: number;
  status_memory: string;
  code_output: string;
  std_output: string;
  last_testcase?: string;
  expected_output?: string;
  runtime_percentile?: number;
  memory_percentile?: number;
  compile_error?: string;
  runtime_error?: string;
  total_correct?: number;
  total_testcases?: number;
  full_runtime_error?: string;
}

const STATUS_CODE_MAP: Record<number, Verdict> = {
  10: "Accepted",
  11: "Wrong Answer",
  12: "Memory Limit Exceeded",
  13: "Output Limit Exceeded",
  14: "Time Limit Exceeded",
  15: "Runtime Error",
  20: "Compile Error",
};

function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}

export async function getResult(
  client: LeetCodeClient,
  submissionId: number,
  maxWaitMs = 30000
): Promise<SubmissionResult> {
  const path = `/submissions/detail/${submissionId}/check/`;
  const deadline = Date.now() + maxWaitMs;
  let interval = 1000;

  while (Date.now() < deadline) {
    const data = await client.get<CheckResponse>(path);

    if (data.state === "PENDING" || data.state === "STARTED") {
      await sleep(interval);
      interval = Math.min(interval * 1.5, 5000); // exponential back-off
      continue;
    }

    // Result is ready
    const verdict: Verdict =
      STATUS_CODE_MAP[data.status_code] ?? "Unknown";

    return {
      verdict,
      statusCode: data.status_code,
      runtime: data.status_runtime ?? "N/A",
      memory: data.status_memory ?? "N/A",
      runtimePercentile: data.runtime_percentile ?? null,
      memoryPercentile: data.memory_percentile ?? null,
      failingInput: data.last_testcase,
      expectedOutput: data.expected_output,
      actualOutput: data.code_output,
      errorMessage:
        data.compile_error ?? data.full_runtime_error ?? data.runtime_error,
      totalTestCases: data.total_testcases,
      passedTestCases: data.total_correct,
    };
  }

  throw new Error(
    `Timed out waiting for submission ${submissionId} after ${maxWaitMs}ms`
  );
}
