import { LeetCodeClient } from "../leetcode-client.js";

interface GlobalData {
  userStatus: {
    username: string;
    isSignedIn: boolean;
    isPremium: boolean;
  };
}

const QUERY = `
  query globalData {
    userStatus {
      username
      isSignedIn
      isPremium
    }
  }
`;

export async function checkAuth(client: LeetCodeClient): Promise<{
  authenticated: boolean;
  username: string | null;
  isPremium: boolean;
  error?: string;
}> {
  try {
    const data = await client.graphql<GlobalData>(QUERY);
    const { isSignedIn, username, isPremium } = data.userStatus;
    return {
      authenticated: isSignedIn,
      username: isSignedIn ? username : null,
      isPremium,
      error: isSignedIn ? undefined : "Not signed in — check your cookies.",
    };
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    return { authenticated: false, username: null, isPremium: false, error: msg };
  }
}
