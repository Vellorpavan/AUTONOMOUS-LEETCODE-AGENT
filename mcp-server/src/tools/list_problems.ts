import { LeetCodeClient } from "../leetcode-client.js";

export interface ProblemSummary {
  id: number;
  slug: string;
  title: string;
  difficulty: "Easy" | "Medium" | "Hard";
  status: string | null; // "ac" | "notac" | null
  isPaidOnly: boolean;
  topicTags: string[];
}

interface ProblemSetData {
  problemsetQuestionList: {
    total: number;
    questions: Array<{
      frontendQuestionId: string;
      titleSlug: string;
      title: string;
      difficulty: string;
      status: string | null;
      paidOnly: boolean;
      topicTags: Array<{ name: string }>;
    }>;
  };
}

const QUERY = `
  query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
    problemsetQuestionList: questionList(
      categorySlug: $categorySlug
      limit: $limit
      skip: $skip
      filters: $filters
    ) {
      total: totalNum
      questions: data {
        frontendQuestionId: questionFrontendId
        titleSlug
        title
        difficulty
        status
        paidOnly: isPaidOnly
        topicTags {
          name
        }
      }
    }
  }
`;

const PAGE_SIZE = 100; // LeetCode API caps responses at 100 per page

async function fetchPage(
  client: LeetCodeClient,
  filters: Record<string, unknown>,
  skip: number
): Promise<ProblemSetData["problemsetQuestionList"]> {
  const data = await client.graphql<ProblemSetData>(QUERY, {
    categorySlug: "",
    limit: PAGE_SIZE,
    skip,
    filters,
  });
  return data.problemsetQuestionList;
}

export async function listProblems(
  client: LeetCodeClient,
  opts: {
    unsolvedOnly?: boolean;
    difficulty?: "Easy" | "Medium" | "Hard";
    fetchAll?: boolean;
    limit?: number;
    skip?: number;
  } = {}
): Promise<{ total: number; problems: ProblemSummary[] }> {
  const filters: Record<string, unknown> = {};
  if (opts.difficulty) filters["difficulty"] = opts.difficulty.toUpperCase();

  let allQuestions: ProblemSetData["problemsetQuestionList"]["questions"] = [];
  let totalCount = 0;

  if (opts.fetchAll) {
    // Paginate through ALL problems — LeetCode caps at 100/page
    let skip = 0;
    let firstPage = true;

    while (true) {
      const page = await fetchPage(client, filters, skip);

      if (firstPage) {
        totalCount = page.total;
        firstPage = false;
      }

      allQuestions = allQuestions.concat(page.questions);

      if (allQuestions.length >= page.total || page.questions.length === 0) {
        break;
      }

      skip += PAGE_SIZE;

      // Small delay between pages to avoid rate limiting
      await new Promise((r) => setTimeout(r, 300));
    }
  } else {
    // Single page fetch
    const page = await fetchPage(client, filters, opts.skip ?? 0);
    totalCount = page.total;
    allQuestions = page.questions.slice(0, opts.limit ?? PAGE_SIZE);
  }

  // Filter unsolved if requested
  if (opts.unsolvedOnly) {
    allQuestions = allQuestions.filter((q) => q.status !== "ac");
  }

  const problems: ProblemSummary[] = allQuestions.map((q) => ({
    id: parseInt(q.frontendQuestionId, 10),
    slug: q.titleSlug,
    title: q.title,
    difficulty: q.difficulty as "Easy" | "Medium" | "Hard",
    status: q.status,
    isPaidOnly: q.paidOnly,
    topicTags: q.topicTags.map((t) => t.name),
  }));

  return { total: totalCount, problems };
}
