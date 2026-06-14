#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║        AUTONOMOUS LEETCODE AGENT — agent/agent.py           ║
║                                                              ║
║  Runs autonomously via MCP tools. Supports:                  ║
║    • Google Gemini  (GEMINI_API_KEY)                         ║
║    • Anthropic Claude  (ANTHROPIC_API_KEY)                   ║
║                                                              ║
║  Usage:                                                       ║
║    python agent.py                      # solve everything   ║
║    python agent.py --slug two-sum       # one problem        ║
║    python agent.py --difficulty Easy    # easy only          ║
╚══════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

# ─── Load environment ─────────────────────────────────────────────────────────
ENV_FILE = Path(__file__).parent / ".env"
load_dotenv(ENV_FILE)
os.environ["ENV_FILE"] = str(ENV_FILE)  # passed to MCP server

# ─── Rich console ─────────────────────────────────────────────────────────────
console = Console()

# ─── Logging ──────────────────────────────────────────────────────────────────
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
session_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = LOG_DIR / f"session_{session_ts}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("agent")

# ─── Constants ────────────────────────────────────────────────────────────────
MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", "4"))
INTER_PROBLEM_DELAY = float(os.getenv("INTER_PROBLEM_DELAY", "2"))
DIFFICULTY_FILTER = os.getenv("DIFFICULTY_FILTER", "ALL")
MCP_SERVER_PATH = Path(__file__).parent.parent / "mcp-server" / "dist" / "index.js"

# ─── Solver system prompt ─────────────────────────────────────────────────────
SOLVER_SYSTEM_PROMPT = """\
You are an elite autonomous competitive programming agent with 10+ years of ICPC
and LeetCode experience. You write clean, correct, optimal Python 3 with type hints.
You never guess — you reason, verify, and only then act.

════════════════════════ CONSTRAINT → COMPLEXITY MAP ════════════════════════
n ≤ 20          → O(2ⁿ) or O(n!) ok  — backtracking, permutations
n ≤ 100         → O(n³) ok            — 3-loop DP, Floyd-Warshall
n ≤ 1,000       → O(n²) ok            — nested loops, O(n²) DP
n ≤ 100,000     → O(n log n) required — sort, heap, segment tree
n ≤ 1,000,000   → O(n) or O(n log n) — hash map, two pointers
n ≤ 10⁹         → O(log n) or O(1)   — binary search, math only
Violating this = guaranteed TLE. Check before writing line one.
═════════════════════════════════════════════════════════════════════════════

Follow this 10-step solver workflow for EVERY problem:

STEP 1 — Read
  Read the FULL problem. Do not skip constraints. Do not skim examples.

STEP 2 — Pattern Recognition
  Identify the paradigm:
  two pointers / sliding window / prefix sum / binary search / greedy /
  BFS / DFS / topological sort / DP (1D,2D,interval,bitmask,digit,tree) /
  monotonic stack / union-find / segment tree / BIT / trie / math

STEP 3 — Algorithm Design
  Write in plain English:
  1. Data structures and why
  2. Core recurrence or loop invariant
  3. Initialization and termination
  4. WHY this is correct

STEP 4 — Complexity Verification
  State Time: O(?), Space: O(?)
  Confirm both against the constraint map. If they don't fit → back to Step 2.

STEP 5 — Edge Case Checklist
  Empty input / single element / all identical / all negative or positive /
  integer overflow / sorted / reverse-sorted / max n / duplicates /
  graph: disconnected/self-loops / tree: single node / linear chain

STEP 6 — Implementation
  Use the EXACT starter code signature. Python 3 with full type hints.

  ```python
  from typing import List, Optional, Dict, Tuple
  import heapq, collections, bisect, math, functools

  class Solution:
      def methodName(self, ...) -> ...:
          # clean implementation
  ```

STEP 7 — Dry Run
  Trace through Example 1 manually. Show key variable state at each step.
  Confirm output matches expected.

STEP 8 — Validation
  Mentally test all examples and edge cases.

STEP 9 — Debug (if called into)
  - State exactly which test failed and why
  - Identify root cause (logic / base case / overflow / wrong DS)
  - Fix the specific issue only. Re-run ALL tests.

STEP 10 — Output Format (REQUIRED)
  Your final response MUST end with a fenced code block containing ONLY the
  Python solution — no explanation inside the block:

  ```python
  from typing import ...
  class Solution:
      ...
  ```

  Before the code block, include:
  Pattern: [name — one line justification]
  Algorithm: [2-3 sentences]
  Time: O(?) | Space: O(?) | Fits constraints: yes/no
  Confidence: high / medium / low

HARD RULES:
1. NEVER invent test cases — use only examples from the problem.
2. NEVER guess a library function. If unsure, implement it.
3. NEVER submit O(n²) for n > 10,000 without TLE proof.
4. NEVER assume the input is valid. Always handle edge cases.
5. DP problems: state the subproblem in one sentence first.
6. Graph/tree: state directed/undirected, weighted/unweighted.
"""

DEBUG_SYSTEM_PROMPT = """\
You are debugging a Python 3 LeetCode solution that produced a wrong result.

You will be given:
- The problem description
- Your previous (failing) code
- The failing test case (input, expected output, actual output)
- The error verdict (Wrong Answer / TLE / Runtime Error / etc.)

Your job:
1. Identify the EXACT root cause of the failure.
2. Produce a FIXED solution.
3. Your response MUST end with a fenced python code block containing the fixed solution.

RULES:
- Do NOT resubmit the same code. Change something meaningful.
- If TLE: you MUST choose a strictly faster algorithm.
- If WA: pinpoint the logic bug and fix it precisely.
- If RE: fix bounds, None checks, recursion depth, division.
- If MLE: reduce space usage, switch to in-place where possible.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# LLM PROVIDER ABSTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

# Gemini free-tier model fallback chain (try each in order on quota exhaustion)
GEMINI_MODEL_FALLBACK_CHAIN = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
]


class LLMProvider:
    """Unified interface for Anthropic Claude and Google Gemini.
    Handles 429 rate-limit errors with exponential backoff and model fallback.
    """

    def __init__(self):
        provider = os.getenv("LLM_PROVIDER", "").lower()

        # Auto-detect if not explicitly set
        if not provider:
            if os.getenv("GEMINI_API_KEY"):
                provider = "gemini"
            elif os.getenv("ANTHROPIC_API_KEY"):
                provider = "anthropic"
            else:
                raise EnvironmentError(
                    "No LLM API key found. Set GEMINI_API_KEY or ANTHROPIC_API_KEY in agent/.env"
                )

        self.provider = provider
        self._client: Any = None

        if provider == "gemini":
            self._init_gemini()
        elif provider == "anthropic":
            self._init_anthropic()
        else:
            raise ValueError(f"Unknown LLM_PROVIDER: {provider!r}. Use 'gemini' or 'anthropic'.")

        console.print(
            f"[bold cyan]🤖 LLM Provider:[/bold cyan] {self.provider.upper()} "
            f"({self.model})"
        )

    def _init_gemini(self):
        try:
            import google.genai as genai
        except ImportError:
            raise ImportError("Run: pip install google-genai")

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY not set")

        self._genai = genai
        self._gemini_client = genai.Client(api_key=api_key)
        # Start with the configured model; fallback chain takes over on quota errors
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self._model_index = 0  # index into GEMINI_MODEL_FALLBACK_CHAIN
        # Sync model index with configured model
        if self.model in GEMINI_MODEL_FALLBACK_CHAIN:
            self._model_index = GEMINI_MODEL_FALLBACK_CHAIN.index(self.model)

    def _init_anthropic(self):
        try:
            import anthropic
        except ImportError:
            raise ImportError("Run: pip install anthropic")

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY not set")

        self._client = anthropic.Anthropic(api_key=api_key)
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-6")

    async def generate(self, system: str, user: str, max_tokens: int = 8192) -> str:
        """Send a prompt, handling 429 with backoff + model fallback."""
        if self.provider == "gemini":
            return await self._gemini_generate_with_retry(system, user, max_tokens)
        else:
            return await asyncio.to_thread(self._anthropic_generate, system, user, max_tokens)

    async def _gemini_generate_with_retry(
        self, system: str, user: str, max_tokens: int
    ) -> str:
        """
        Gemini generate with:
          - Per-minute 429: wait suggested seconds + buffer, retry same model
          - Daily quota 429: rotate to next model in fallback chain
          - All models exhausted: wait 60s and try from beginning
        """
        max_retries = 8
        retry = 0

        while retry < max_retries:
            try:
                return await asyncio.to_thread(
                    self._gemini_generate_once, system, user, max_tokens, self.model
                )
            except Exception as e:
                err_str = str(e)
                if "429" not in err_str and "RESOURCE_EXHAUSTED" not in err_str:
                    raise  # Not a quota error — propagate immediately

                retry += 1

                # Parse suggested retry delay from error message
                wait_suggested = self._parse_retry_delay(err_str)

                # Check if it's a daily quota (RPD) or per-minute (RPM)
                is_daily = "PerDay" in err_str or "per_day" in err_str.lower()

                if is_daily:
                    # Daily quota exhausted on this model → try next in chain
                    self._advance_model()
                    console.print(
                        f"[yellow]⚠ Daily quota exhausted on {self.model_prev}. "
                        f"Switching to {self.model}...[/yellow]"
                    )
                    # Small wait before trying next model
                    await asyncio.sleep(3)
                else:
                    # Per-minute rate limit → wait and retry same model
                    wait = max(wait_suggested + 5, 15)
                    console.print(
                        f"[yellow]⏳ Rate limited (429 RPM). Waiting {wait}s "
                        f"then retrying {self.model}... (retry {retry}/{max_retries})[/yellow]"
                    )
                    await asyncio.sleep(wait)

        raise RuntimeError(
            f"Gemini quota exhausted on all models after {max_retries} retries. "
            "Please wait 24h for daily quota reset or add a paid API key."
        )

    def _gemini_generate_once(
        self, system: str, user: str, max_tokens: int, model: str
    ) -> str:
        from google.genai import types as gtypes

        contents = [
            gtypes.Content(
                role="user",
                parts=[gtypes.Part(text=user)],
            )
        ]
        config = gtypes.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=max_tokens,
            temperature=0.1,
        )
        response = self._gemini_client.models.generate_content(
            model=model,
            contents=contents,
            config=config,
        )
        return response.text or ""

    def _advance_model(self):
        """Rotate to the next model in the fallback chain."""
        self.model_prev = self.model
        self._model_index = (self._model_index + 1) % len(GEMINI_MODEL_FALLBACK_CHAIN)
        self.model = GEMINI_MODEL_FALLBACK_CHAIN[self._model_index]
        console.print(f"[cyan]🔄 Model rotated: {self.model_prev} → {self.model}[/cyan]")

    @staticmethod
    def _parse_retry_delay(err_str: str) -> int:
        """Extract suggested wait seconds from Gemini 429 error message."""
        import re as _re
        m = _re.search(r"retry in (\d+\.?\d*)s", err_str, _re.IGNORECASE)
        if m:
            return int(float(m.group(1))) + 2
        return 60  # safe default

    def _anthropic_generate(self, system: str, user: str, max_tokens: int) -> str:
        message = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return message.content[0].text



# ═══════════════════════════════════════════════════════════════════════════════
# MCP CLIENT (direct JSON-RPC over subprocess stdio)
# ═══════════════════════════════════════════════════════════════════════════════

class MCPClient:
    """
    Lightweight MCP client that communicates with the Node.js server
    via JSON-RPC 2.0 over stdin/stdout.
    """

    def __init__(self, server_path: Path):
        self.server_path = server_path
        self._proc: Optional[asyncio.subprocess.Process] = None
        self._id = 0

    async def start(self):
        if not self.server_path.exists():
            raise FileNotFoundError(
                f"MCP server not built. Run: cd mcp-server && npm run build\n"
                f"Expected: {self.server_path}"
            )
        self._proc = await asyncio.create_subprocess_exec(
            "node", str(self.server_path),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ, "ENV_FILE": str(ENV_FILE)},
        )
        # Increase the asyncio StreamReader limit to 100 MB so large
        # list_problems responses (all 3958 problems) don't overflow the buffer
        self._proc.stdout._limit = 100 * 1024 * 1024  # 100 MB
        # MCP initialization handshake
        await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "leetcode-agent", "version": "1.0.0"},
        })
        await self._send_notification("notifications/initialized", {})

    async def stop(self):
        if self._proc and self._proc.returncode is None:
            self._proc.terminate()
            await self._proc.wait()

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    async def _readline_large(self) -> bytes:
        """
        Read one newline-terminated JSON line from the MCP server stdout.
        asyncio's default readline() raises LimitOverrunError on responses
        larger than 64 KB (e.g. list_problems with 3 958 entries ~500 KB).
        This method reads in 64 KB chunks and concatenates until it finds \n.
        """
        buf = bytearray()
        while True:
            chunk = await self._proc.stdout.read(65536)
            if not chunk:
                # Process closed stdout
                stderr = await self._proc.stderr.read(4096)
                raise RuntimeError(f"MCP server closed. Stderr: {stderr.decode()}")
            if b"\n" in chunk:
                nl = chunk.index(b"\n")
                buf.extend(chunk[: nl + 1])
                # Push any bytes after the newline back into the buffer
                leftover = chunk[nl + 1 :]
                if leftover:
                    self._proc.stdout._buffer[0:0] = leftover  # prepend
                break
            buf.extend(chunk)
        return bytes(buf)

    async def _send_request(self, method: str, params: dict) -> Any:
        req_id = self._next_id()
        msg = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}
        line = json.dumps(msg) + "\n"
        self._proc.stdin.write(line.encode())
        await self._proc.stdin.drain()

        # Read response — use our unlimited reader, not readline()
        while True:
            raw = await self._readline_large()
            if not raw:
                stderr = await self._proc.stderr.read(4096)
                raise RuntimeError(f"MCP server closed. Stderr: {stderr.decode()}")
            try:
                resp = json.loads(raw.decode().strip())
            except json.JSONDecodeError:
                continue  # skip non-JSON lines (e.g. startup messages)

            if resp.get("id") == req_id:
                if "error" in resp:
                    raise RuntimeError(f"MCP error: {resp['error']}")
                return resp.get("result")

    async def _send_notification(self, method: str, params: dict):
        msg = {"jsonrpc": "2.0", "method": method, "params": params}
        line = json.dumps(msg) + "\n"
        self._proc.stdin.write(line.encode())
        await self._proc.stdin.drain()

    async def call_tool(self, tool_name: str, args: dict) -> Any:
        result = await self._send_request(
            "tools/call",
            {"name": tool_name, "arguments": args},
        )
        # Extract text content from MCP response
        content = result.get("content", [])
        if content and content[0].get("type") == "text":
            text = content[0]["text"]
            if text.startswith("ERROR:"):
                raise RuntimeError(text)
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# CODE EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def extract_code(response: str) -> Optional[str]:
    """
    Extract the Python code block from the LLM's response.
    Handles ```python ... ``` and ``` ... ``` fences.
    """
    patterns = [
        r"```python\n(.*?)```",
        r"```py\n(.*?)```",
        r"```\n(.*?)```",
    ]
    for pat in patterns:
        match = re.search(pat, response, re.DOTALL)
        if match:
            code = match.group(1).strip()
            # Sanity check: must contain a class Solution
            if "class Solution" in code or "def " in code:
                return code
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATS
# ═══════════════════════════════════════════════════════════════════════════════

class SessionStats:
    def __init__(self):
        self.accepted = 0
        self.failed = 0
        self.skipped_premium = 0
        self.pre_solved = 0
        self.log_lines: list[str] = []

    def log(self, line: str):
        self.log_lines.append(line)
        logger.info(line)

    def print_summary(self):
        table = Table(title="SESSION COMPLETE", border_style="cyan")
        table.add_column("Outcome", style="bold")
        table.add_column("Count", justify="right")
        table.add_row("✅ Accepted", str(self.accepted), style="green")
        table.add_row("❌ Failed", str(self.failed), style="red")
        table.add_row("⏭  Skipped (premium)", str(self.skipped_premium), style="yellow")
        table.add_row("⏩ Pre-solved", str(self.pre_solved), style="dim")
        console.print(table)

        # Also write summary to log
        summary = (
            "\n══════════════════════════════\n"
            "SESSION COMPLETE\n"
            f"✅ Accepted:   {self.accepted}\n"
            f"❌ Failed:     {self.failed}\n"
            f"⏭  Skipped:   {self.skipped_premium} (premium)\n"
            f"⏩ Pre-solved: {self.pre_solved}\n"
            "══════════════════════════════"
        )
        logger.info(summary)


# ═══════════════════════════════════════════════════════════════════════════════
# RATE LIMIT HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

async def safe_tool_call(mcp: MCPClient, tool: str, args: dict, retries: int = 1) -> Any:
    """Call an MCP tool with rate-limit handling (429 → wait 60s → retry once)."""
    for attempt in range(retries + 1):
        try:
            return await mcp.call_tool(tool, args)
        except RuntimeError as e:
            if "429" in str(e) and attempt < retries:
                console.print("[yellow]⚠ Rate limited (429). Waiting 60s...[/yellow]")
                await asyncio.sleep(60)
                continue
            raise


# ═══════════════════════════════════════════════════════════════════════════════
# THE SOLVER BRAIN
# ═══════════════════════════════════════════════════════════════════════════════

async def solve_problem(
    llm: LLMProvider,
    problem: dict,
    prev_code: Optional[str] = None,
    failure_info: Optional[dict] = None,
) -> Optional[str]:
    """
    Run the 10-step solver. Returns Python code string or None if no code found.
    If prev_code + failure_info are provided, runs in debug mode (Step 9).
    """
    user_prompt: str
    system: str

    if prev_code and failure_info:
        # Debug mode
        user_prompt = f"""
PROBLEM:
{problem['content']}

YOUR PREVIOUS (FAILING) CODE:
```python
{prev_code}
```

FAILURE VERDICT: {failure_info.get('verdict', 'Unknown')}
FAILING INPUT:   {failure_info.get('failingInput', 'N/A')}
EXPECTED OUTPUT: {failure_info.get('expectedOutput', 'N/A')}
ACTUAL OUTPUT:   {failure_info.get('actualOutput', 'N/A')}
ERROR MESSAGE:   {failure_info.get('errorMessage', 'N/A')}
PASSED/TOTAL:    {failure_info.get('passedTestCases', '?')}/{failure_info.get('totalTestCases', '?')}

Fix the bug and provide the complete corrected solution.
Remember: if TLE, use a strictly faster algorithm. Do NOT submit the same logic.
"""
        system = DEBUG_SYSTEM_PROMPT
    else:
        # Fresh solve mode
        user_prompt = f"""
Solve this LeetCode problem. Follow all 10 steps of the solver workflow.

PROBLEM TITLE: {problem['title']} (#{problem['id']}, {problem['difficulty']})
TOPIC TAGS: {', '.join(problem.get('topicTags', []))}

FULL DESCRIPTION:
{problem['content']}

STARTER CODE (use this EXACT signature):
```python
{problem['starterCode']}
```

HINTS (if any): {json.dumps(problem.get('hints', []))}

Now work through all 10 steps. End with the final code block.
"""
        system = SOLVER_SYSTEM_PROMPT

    response = await llm.generate(system=system, user=user_prompt)
    return extract_code(response)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN AGENT LOOP
# ═══════════════════════════════════════════════════════════════════════════════

async def run_agent(
    target_slug: Optional[str] = None,
    difficulty_filter: Optional[str] = None,
):
    stats = SessionStats()

    # ── Initialise LLM ──────────────────────────────────────────────────────
    llm = LLMProvider()

    # ── Initialise MCP ──────────────────────────────────────────────────────
    mcp = MCPClient(MCP_SERVER_PATH)
    console.print(Panel("[bold]🚀 Starting LeetCode Agent[/bold]", border_style="cyan"))

    await mcp.start()

    try:
        # ── STEP A: Verify auth ─────────────────────────────────────────────
        console.print("\n[bold]Step A — Verifying auth...[/bold]")
        auth = await safe_tool_call(mcp, "check_auth", {})
        if not auth.get("authenticated"):
            console.print(f"[red]❌ Authentication failed: {auth.get('error')}[/red]")
            console.print("[yellow]→ Set LEETCODE_SESSION and CSRF_TOKEN in agent/.env[/yellow]")
            return
        username = auth["username"]
        console.print(f"[green]✅ Authenticated as: {username}[/green]")

        # ── STEP B: Load problem queue ──────────────────────────────────────
        console.print("\n[bold]Step B — Loading problem queue...[/bold]")

        if target_slug:
            # Single problem mode
            problem_data = await safe_tool_call(mcp, "get_problem", {"slug": target_slug})
            # Wrap into list format
            queue = [{
                "id": problem_data["id"],
                "slug": target_slug,
                "title": problem_data["title"],
                "difficulty": problem_data["difficulty"],
                "status": None,
                "isPaidOnly": False,
            }]
        else:
            list_args: dict = {"unsolvedOnly": True, "fetchAll": True}
            eff_difficulty = difficulty_filter or DIFFICULTY_FILTER
            if eff_difficulty and eff_difficulty.upper() != "ALL":
                list_args["difficulty"] = eff_difficulty

            problems_resp = await safe_tool_call(mcp, "list_problems", list_args)
            raw_queue = problems_resp.get("problems", [])

            # Sort: Easy → Medium → Hard, then by ID ascending
            diff_order = {"Easy": 0, "Medium": 1, "Hard": 2}
            raw_queue.sort(key=lambda p: (diff_order.get(p["difficulty"], 9), p["id"]))
            queue = raw_queue

        console.print(f"[cyan]📋 Queue loaded: {len(queue)} problems[/cyan]")

        # ── STEP C: Check progress ──────────────────────────────────────────
        console.print("\n[bold]Step C — Checking progress...[/bold]")
        progress = await safe_tool_call(mcp, "get_progress", {"username": username})
        solved = progress.get("solved", 0)
        total = progress.get("total", 0)
        console.print(
            f"[cyan]📊 Session start. Solved: {solved}/{total} | "
            f"Easy {progress['easy']['solved']}/{progress['easy']['total']} | "
            f"Medium {progress['medium']['solved']}/{progress['medium']['total']} | "
            f"Hard {progress['hard']['solved']}/{progress['hard']['total']}[/cyan]"
        )
        stats.log(f"Session start — Solved: {solved}/{total}")

        # ── MAIN LOOP ───────────────────────────────────────────────────────
        for problem_stub in queue:
            p_id = problem_stub["id"]
            slug = problem_stub["slug"]
            title = problem_stub["title"]
            diff = problem_stub["difficulty"]
            status = problem_stub.get("status")
            is_paid = problem_stub.get("isPaidOnly", False)

            console.rule(f"[bold]#{p_id} {title} [{diff}][/bold]")

            # [1] Skip check
            if status == "ac":
                line = f"⏩ #{p_id:04d} | {title} | {diff} | Already solved | skipped"
                stats.log(line)
                stats.pre_solved += 1
                continue

            if is_paid:
                line = f"⏭  #{p_id:04d} | {title} | {diff} | Skipped | premium only"
                stats.log(line)
                stats.skipped_premium += 1
                continue

            # [2] Fetch full problem details
            try:
                problem = await safe_tool_call(mcp, "get_problem", {"slug": slug})
            except Exception as e:
                stats.log(f"❌ #{p_id:04d} | {title} | {diff} | ERROR fetching problem: {e}")
                continue

            question_id_raw = problem.get("id")

            # We need the INTERNAL questionId for submission (may differ from frontendId)
            # get_problem returns frontendId; we use it as questionId (LeetCode accepts this
            # for most problems via the /submit/ endpoint which uses the numeric questionId)
            question_id: int = int(question_id_raw) if question_id_raw else p_id

            attempt = 0
            prev_code: Optional[str] = None
            failure_info: Optional[dict] = None
            final_verdict = "Failed"

            while attempt < MAX_ATTEMPTS:
                attempt += 1
                console.print(f"\n[yellow]⚙ Attempt {attempt}/{MAX_ATTEMPTS}[/yellow]")

                # [2] SOLVE
                try:
                    code = await solve_problem(llm, problem, prev_code, failure_info)
                except RuntimeError as e:
                    err_str = str(e)
                    if "quota exhausted on all models" in err_str:
                        # All models daily-quota exhausted — wait 60s then skip problem
                        console.print(
                            "[bold red]🚫 All Gemini models daily quota exhausted. "
                            "Waiting 60s and skipping this problem...[/bold red]"
                        )
                        stats.log(f"❌ #{p_id:04d} | {title} | {diff} | QUOTA EXHAUSTED — all models")
                        await asyncio.sleep(60)
                        break
                    stats.log(f"❌ #{p_id:04d} | {title} | {diff} | LLM error: {e}")
                    break
                except Exception as e:
                    stats.log(f"❌ #{p_id:04d} | {title} | {diff} | LLM error: {e}")
                    break

                if not code:
                    console.print("[red]⚠ Could not extract code from LLM response.[/red]")
                    break

                console.print(f"[dim]Code ({len(code)} chars extracted)[/dim]")

                # Guard: never submit the same code twice
                if code == prev_code:
                    console.print("[red]⚠ LLM returned identical code. Skipping attempt.[/red]")
                    break

                # [3] SUBMIT
                try:
                    submit_result = await safe_tool_call(
                        mcp, "submit_code",
                        {"slug": slug, "lang": "python3", "code": code, "questionId": question_id},
                    )
                    submission_id = submit_result["submissionId"]
                except Exception as e:
                    stats.log(f"❌ #{p_id:04d} | {title} | {diff} | Submit error: {e}")
                    break

                console.print(f"[dim]Submission ID: {submission_id}[/dim]")

                # [4] CHECK RESULT
                try:
                    result = await safe_tool_call(
                        mcp, "get_result", {"submissionId": submission_id, "maxWaitMs": 35000}
                    )
                except Exception as e:
                    stats.log(f"❌ #{p_id:04d} | {title} | {diff} | Result error: {e}")
                    break

                verdict = result.get("verdict", "Unknown")
                runtime = result.get("runtime", "N/A")
                memory = result.get("memory", "N/A")
                rt_pct = result.get("runtimePercentile")
                mem_pct = result.get("memoryPercentile")

                if verdict == "Accepted":
                    pct_str = f", beats {rt_pct:.0f}%" if rt_pct else ""
                    line = (
                        f"✅ #{p_id:04d} | {title} | {diff} | Accepted | "
                        f"attempt {attempt} | {runtime}{pct_str} | {memory}"
                    )
                    stats.log(line)
                    console.print(f"[green]{line}[/green]")
                    stats.accepted += 1
                    final_verdict = "Accepted"
                    break

                else:
                    console.print(f"[red]✗ {verdict}[/red]")
                    if result.get("failingInput"):
                        console.print(f"  Input:    {result['failingInput'][:200]}")
                        console.print(f"  Expected: {result.get('expectedOutput', 'N/A')[:200]}")
                        console.print(f"  Got:      {result.get('actualOutput', 'N/A')[:200]}")
                    if result.get("errorMessage"):
                        console.print(f"  Error:    {result['errorMessage'][:400]}")

                    prev_code = code
                    failure_info = result
                    failure_info["verdict"] = verdict

                    # TLE: must use faster algorithm → treat as new solve
                    if verdict == "Time Limit Exceeded" and attempt == 1:
                        failure_info["hint"] = (
                            "Your current algorithm is too slow. "
                            "You MUST choose a strictly faster algorithm. "
                            "Do NOT resubmit O(n²) if n > 10000."
                        )

                # [5] Rate limit guard
                await asyncio.sleep(1)

            # End of attempt loop
            if final_verdict != "Accepted":
                line = (
                    f"❌ #{p_id:04d} | {title} | {diff} | Failed | "
                    f"attempt {attempt} | {failure_info.get('verdict', 'Unknown') if failure_info else 'No result'}"
                )
                stats.log(line)
                console.print(f"[red]{line}[/red]")
                stats.failed += 1

            # Inter-problem delay
            await asyncio.sleep(INTER_PROBLEM_DELAY)

        # ── SESSION COMPLETE ────────────────────────────────────────────────
        console.print("\n")
        final_progress = await safe_tool_call(mcp, "get_progress", {"username": username})
        console.print(
            f"[cyan]Final progress: {final_progress.get('solved')}/{final_progress.get('total')} solved[/cyan]"
        )
        stats.print_summary()
        console.print(f"\n[dim]Session log saved to: {log_path}[/dim]")

    finally:
        await mcp.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def parse_args():
    parser = argparse.ArgumentParser(
        description="Autonomous LeetCode Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent.py                        # Solve all unsolved problems
  python agent.py --slug two-sum        # Solve one specific problem
  python agent.py --difficulty Easy     # Solve only Easy problems
  python agent.py --difficulty Medium   # Solve only Medium problems
        """,
    )
    parser.add_argument(
        "--slug",
        type=str,
        default=None,
        help="Solve a single problem by its slug (e.g. 'two-sum')",
    )
    parser.add_argument(
        "--difficulty",
        type=str,
        choices=["Easy", "Medium", "Hard", "ALL"],
        default=None,
        help="Filter problems by difficulty",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    asyncio.run(
        run_agent(
            target_slug=args.slug,
            difficulty_filter=args.difficulty,
        )
    )


if __name__ == "__main__":
    main()
