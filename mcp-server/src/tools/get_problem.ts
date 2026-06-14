import { LeetCodeClient } from "../leetcode-client.js";
import { convert } from "html-to-text";

export interface ProblemDetail {
  id: number;
  slug: string;
  title: string;
  difficulty: string;
  content: string; // plain text description
  constraints: string;
  examples: string;
  starterCode: string; // Python 3 starter code
  topicTags: string[];
  hints: string[];
}

interface QuestionData {
  question: {
    questionId: string;
    questionFrontendId: string;
    title: string;
    titleSlug: string;
    difficulty: string;
    content: string;
    hints: string[];
    topicTags: Array<{ name: string }>;
    codeSnippets: Array<{ lang: string; langSlug: string; code: string }>;
  };
}

const QUERY = `
  query questionData($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
      questionId
      questionFrontendId
      title
      titleSlug
      difficulty
      content
      hints
      topicTags {
        name
      }
      codeSnippets {
        lang
        langSlug
        code
      }
    }
  }
`;

function extractSection(text: string, header: string): string {
  const lines = text.split("\n");
  const startIdx = lines.findIndex((l) =>
    l.toLowerCase().includes(header.toLowerCase())
  );
  if (startIdx === -1) return "";

  const result: string[] = [];
  for (let i = startIdx + 1; i < lines.length; i++) {
    const l = lines[i];
    // Stop at next major section
    if (/^(example|constraint|note|follow.up|input|output)/i.test(l.trim()) && i > startIdx + 1) break;
    result.push(l);
  }
  return result.join("\n").trim();
}

export async function getProblem(
  client: LeetCodeClient,
  slug: string
): Promise<ProblemDetail> {
  const data = await client.graphql<QuestionData>(QUERY, { titleSlug: slug });
  const q = data.question;

  // Convert HTML content to readable plain text
  const plainText = convert(q.content || "", {
    wordwrap: 120,
    selectors: [
      { selector: "img", format: "skip" },
      { selector: "a", options: { ignoreHref: true } },
    ],
  });

  // Find Python 3 starter code
  const pySnippet =
    q.codeSnippets.find((s) => s.langSlug === "python3") ??
    q.codeSnippets.find((s) => s.langSlug === "python");

  const starterCode = pySnippet?.code ?? "class Solution:\n    pass\n";

  // Extract subsections from plain text
  const constraints = extractSection(plainText, "constraints");
  const examples = plainText
    .split("\n")
    .filter((l) => /example\s*\d*/i.test(l))
    .slice(0, 10)
    .join("\n");

  return {
    id: parseInt(q.questionFrontendId, 10),
    slug: q.titleSlug,
    title: q.title,
    difficulty: q.difficulty,
    content: plainText,
    constraints,
    examples,
    starterCode,
    topicTags: q.topicTags.map((t) => t.name),
    hints: q.hints,
  };
}
