import { LeetCodeClient } from "../leetcode-client.js";

interface SubmitResponse {
  submission_id: number;
}

const LANG_SLUG_MAP: Record<string, string> = {
  python3: "python3",
  python: "python",
  cpp: "cpp",
  java: "java",
  javascript: "javascript",
  typescript: "typescript",
  go: "golang",
  rust: "rust",
  c: "c",
  csharp: "csharp",
};

export async function submitCode(
  client: LeetCodeClient,
  slug: string,
  lang: string,
  code: string,
  questionId: number
): Promise<{ submissionId: number }> {
  const langSlug = LANG_SLUG_MAP[lang.toLowerCase()] ?? lang;

  const body = {
    lang: langSlug,
    typed_code: code,
    question_id: questionId,
  };

  const data = await client.post<SubmitResponse>(
    `/problems/${slug}/submit/`,
    body
  );

  if (!data.submission_id) {
    throw new Error(
      `Submit failed — no submission_id in response: ${JSON.stringify(data)}`
    );
  }

  return { submissionId: data.submission_id };
}
