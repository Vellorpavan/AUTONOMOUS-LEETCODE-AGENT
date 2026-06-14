import axios, { AxiosInstance, AxiosError } from "axios";

const LEETCODE_BASE = "https://leetcode.com";
const GRAPHQL_URL = `${LEETCODE_BASE}/graphql`;

export interface LeetCodeCredentials {
  session: string;
  csrfToken: string;
}

export class LeetCodeClient {
  private http: AxiosInstance;
  private csrfToken: string;

  constructor(creds: LeetCodeCredentials) {
    this.csrfToken = creds.csrfToken;
    this.http = axios.create({
      baseURL: LEETCODE_BASE,
      timeout: 30000,
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        Cookie: `LEETCODE_SESSION=${creds.session}; csrftoken=${creds.csrfToken}`,
        "x-csrftoken": creds.csrfToken,
        Referer: LEETCODE_BASE,
        Origin: LEETCODE_BASE,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
  }

  async graphql<T = unknown>(
    query: string,
    variables: Record<string, unknown> = {}
  ): Promise<T> {
    const resp = await this.http.post<{ data: T; errors?: unknown[] }>(
      GRAPHQL_URL,
      { query, variables }
    );
    if (resp.data.errors) {
      throw new Error(`GraphQL errors: ${JSON.stringify(resp.data.errors)}`);
    }
    return resp.data.data;
  }

  async get<T = unknown>(path: string): Promise<T> {
    const resp = await this.http.get<T>(path);
    return resp.data;
  }

  async post<T = unknown>(
    path: string,
    body: Record<string, unknown>
  ): Promise<T> {
    const resp = await this.http.post<T>(path, body);
    return resp.data;
  }

  getHttp() {
    return this.http;
  }
}

// Singleton factory — credentials come from env vars
export function createClientFromEnv(): LeetCodeClient {
  const session = process.env.LEETCODE_SESSION;
  const csrfToken = process.env.CSRF_TOKEN || process.env.LEETCODE_CSRF_TOKEN;

  if (!session || !csrfToken) {
    throw new Error(
      "Missing LEETCODE_SESSION or CSRF_TOKEN environment variables. " +
        "Get these from your browser cookies at leetcode.com."
    );
  }

  return new LeetCodeClient({ session, csrfToken });
}
