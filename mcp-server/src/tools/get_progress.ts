import { LeetCodeClient } from "../leetcode-client.js";

interface MatchedUser {
  submitStats: {
    acSubmissionNum: Array<{
      difficulty: string;
      count: number;
      submissions: number;
    }>;
  };
}

interface UserProgressData {
  matchedUser: MatchedUser | null;
  allQuestionsCount: Array<{ difficulty: string; count: number }>;
}

const QUERY = `
  query userProgress($username: String!) {
    allQuestionsCount {
      difficulty
      count
    }
    matchedUser(username: $username) {
      submitStats {
        acSubmissionNum {
          difficulty
          count
          submissions
        }
      }
    }
  }
`;

export async function getProgress(
  client: LeetCodeClient,
  username: string
): Promise<{
  total: number;
  solved: number;
  easy: { solved: number; total: number };
  medium: { solved: number; total: number };
  hard: { solved: number; total: number };
}> {
  const data = await client.graphql<UserProgressData>(QUERY, { username });

  const totals: Record<string, number> = {};
  for (const q of data.allQuestionsCount) {
    totals[q.difficulty] = q.count;
  }

  const acMap: Record<string, number> = {};
  if (data.matchedUser) {
    for (const s of data.matchedUser.submitStats.acSubmissionNum) {
      acMap[s.difficulty] = s.count;
    }
  }

  return {
    total: totals["All"] ?? 0,
    solved: acMap["All"] ?? 0,
    easy: { solved: acMap["Easy"] ?? 0, total: totals["Easy"] ?? 0 },
    medium: { solved: acMap["Medium"] ?? 0, total: totals["Medium"] ?? 0 },
    hard: { solved: acMap["Hard"] ?? 0, total: totals["Hard"] ?? 0 },
  };
}
