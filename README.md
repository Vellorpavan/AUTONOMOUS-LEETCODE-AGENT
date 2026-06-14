<div align="center">

<!-- ANIMATED BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=LeetCode%20Autonomous%20Agent&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=38&desc=AI-powered%20%7C%20Fully%20Autonomous%20%7C%20Solves%20Every%20Problem&descAlignY=58&descAlign=50" width="100%"/>

<!-- BADGES ROW 1 -->
<p>
  <img src="https://img.shields.io/badge/Built%20With-Claude%20Opus%204-blueviolet?style=for-the-badge&logo=anthropic&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google-Vertex%20AI-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white"/>
  <img src="https://img.shields.io/badge/Protocol-MCP-00B4D8?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTVMMTIgMnpNMiAxN2wxMCA1IDEwLTUiLz48L3N2Zz4=&logoColor=white"/>
  <img src="https://img.shields.io/badge/Language-Python%203.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Runtime-Node.js%2018+-339933?style=for-the-badge&logo=node.js&logoColor=white"/>
</p>

<!-- BADGES ROW 2 -->
<p>
  <img src="https://img.shields.io/badge/LeetCode-Problems%20Solved%20Auto-FFA116?style=for-the-badge&logo=leetcode&logoColor=black"/>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Production%20Ready-22c55e?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge"/>
</p>

<!-- ANIMATED TYPING -->
<br/>

```
██╗     ███████╗███████╗████████╗ ██████╗ ██████╗ ██████╗ ███████╗
██║     ██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
██║     █████╗  █████╗     ██║   ██║     ██║   ██║██║  ██║█████╗  
██║     ██╔══╝  ██╔══╝     ██║   ██║     ██║   ██║██║  ██║██╔══╝  
███████╗███████╗███████╗   ██║   ╚██████╗╚██████╔╝██████╔╝███████╗
╚══════╝╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═════╝╚══════╝
     A U T O N O M O U S   A G E N T   ×   M C P   ×   A I
```

<br/>

> **🤖 One command. Every LeetCode problem. Zero human input.**
>
> Built on Google Cloud · Powered by Claude Opus 4 · Custom MCP Protocol

<br/>

<!-- DEMO VIDEO PLACEHOLDER -->
<a href="https://www.youtube.com/watch?v=hFbV2DI4xHM">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2000&pause=500&color=00D9FF&center=true&vCenter=true&multiline=true&width=600&height=80&lines=▶+Watch+Demo+Video;Agent+solving+3000%2B+problems+autonomously" alt="Demo Video"/>
</a>

<br/><br/>

[![Demo Video](https://img.shields.io/badge/▶%20Watch%20Full%20Demo-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=hFbV2DI4xHM)

</div>

---

<!-- ANIMATED SEPARATOR -->
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%"/>

## 📌 Table of Contents

<details open>
<summary>Click to expand / collapse</summary>

- [🧠 What Is This?](#-what-is-this)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [📁 Project Structure](#-project-structure)
- [⚡ Quickstart](#-quickstart)
- [🔧 Prerequisites](#-prerequisites)
- [🍪 Getting Your LeetCode Cookies](#-getting-your-leetcode-cookies)
- [🔑 Getting Your Anthropic API Key](#-getting-your-anthropic-api-key)
- [⚙️ Configuration](#️-configuration)
- [🚀 Running the Agent](#-running-the-agent)
- [🛠️ MCP Server — Tool Reference](#️-mcp-server--tool-reference)
- [🤖 Agent System Prompt](#-agent-system-prompt)
- [📊 Session Logs](#-session-logs)
- [☁️ Google Cloud Deployment](#️-google-cloud-deployment)
- [🐛 Troubleshooting](#-troubleshooting)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)

</details>

---

## 🧠 What Is This?

<table>
<tr>
<td width="60%">

**LeetCode Autonomous Agent** is a fully automated AI system that logs into your LeetCode account and solves **every single problem** — on its own, without any human input after you press start.

It combines three things:

1. **A custom MCP Server** (Model Context Protocol) built from scratch — wraps LeetCode's private GraphQL API as clean, callable tools
2. **Claude Opus 4** as the AI brain — reads problems, reasons about algorithms, writes optimal Python 3 code
3. **An autonomous agent loop** — manages the problem queue, submits solutions, reads verdicts, fixes failures, and moves on — forever

You start it once. It runs until your LeetCode profile is solved.

</td>
<td width="40%">

```
You
 │
 └─▶ ./run.sh solve-all
         │
         ▼
    Agent starts
         │
    ┌────▼────┐
    │  Queue  │ ← 3000+ problems
    └────┬────┘
         │
    ┌────▼────────┐
    │  Read prob  │
    │  Write code │
    │  Submit     │
    │  Check      │
    │  Fix/retry  │
    └────┬────────┘
         │
    ┌────▼────┐
    │  Next   │──▶ loop forever
    └─────────┘
```

</td>
</tr>
</table>

---

## ✨ Features

<div align="center">

| Feature | Description |
|---|---|
| 🤖 **Fully Autonomous** | Zero human input after start. The agent manages the entire loop |
| 🧠 **Elite Solver Prompt** | 10-step competitive programming workflow built into the system prompt |
| 📋 **Smart Queue** | Fetches all problems, sorts Easy → Medium → Hard, skips already-solved |
| 🔄 **Verdict-aware Retry** | Different fix strategy for WA, TLE, MLE, RE, CE — not the same blind retry |
| 🛡️ **Rate Limit Guard** | Auto-waits on 429, retries once, skips and continues if persistent |
| 📊 **Session Logging** | Every problem outcome logged to JSON with timestamps |
| ☁️ **Google Cloud Ready** | Designed to run on Google Cloud Vertex AI / Compute Engine |
| 🔌 **Custom MCP Server** | Built from scratch in TypeScript — 6 tools covering all LeetCode actions |
| ⚡ **Constraint-aware** | Maps n-constraints to complexity ceilings before writing any code |
| 🎯 **Max 4 Retries** | Never loops forever — documents failures and moves on |

</div>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        YOUR MACHINE / GOOGLE CLOUD                      │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                     PYTHON AGENT  (agent.py)                     │   │
│  │                                                                  │   │
│  │   ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐   │   │
│  │   │  Queue Mgr  │───▶│  Claude      │───▶│  Result Handler  │   │   │
│  │   │  Skip logic │    │  Opus 4      │    │  WA/TLE/RE/MLE   │   │   │
│  │   │  Retry loop │    │  (AI brain)  │    │  Retry / Move on │   │   │
│  │   └─────────────┘    └──────┬───────┘    └──────────────────┘   │   │
│  │                             │ MCP Protocol (stdio)               │   │
│  └─────────────────────────────┼────────────────────────────────────┘   │
│                                │                                         │
│  ┌─────────────────────────────▼────────────────────────────────────┐   │
│  │              LEETCODE MCP SERVER  (Node.js / TypeScript)         │   │
│  │                                                                  │   │
│  │  ┌────────────┐  ┌──────────────┐  ┌───────────┐  ┌─────────┐  │   │
│  │  │check_auth  │  │list_problems │  │get_problem│  │ submit  │  │   │
│  │  └────────────┘  └──────────────┘  └───────────┘  └─────────┘  │   │
│  │  ┌────────────┐  ┌──────────────┐                               │   │
│  │  │get_result  │  │get_progress  │                               │   │
│  │  └────────────┘  └──────────────┘                               │   │
│  └─────────────────────────────┬────────────────────────────────────┘   │
│                                │ HTTPS / GraphQL                         │
└────────────────────────────────┼────────────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   leetcode.com API       │
                    │   GraphQL + REST         │
                    │   Your account session   │
                    └─────────────────────────┘
```

---

## 📁 Project Structure

```
leetcode-agent/
│
├── 📂 mcp-server/                  ← Custom MCP Server (TypeScript)
│   ├── 📂 src/
│   │   ├── 📄 index.ts             ← Server entry + tool registry
│   │   ├── 📄 leetcode-client.ts   ← All HTTP/GraphQL calls to LeetCode
│   │   └── 📂 tools/
│   │       ├── 📄 check_auth.ts    ← Verify session cookies
│   │       ├── 📄 get_problem.ts   ← Fetch full problem details
│   │       ├── 📄 get_progress.ts  ← Account solve statistics
│   │       ├── 📄 get_result.ts    ← Poll submission verdict
│   │       ├── 📄 list_problems.ts ← List/filter all problems
│   │       └── 📄 submit_code.ts   ← Submit solution
│   ├── 📄 package.json
│   └── 📄 tsconfig.json
│
├── 📂 agent/                       ← Autonomous Agent (Python)
│   ├── 📄 agent.py                 ← Main loop + Claude API calls
│   ├── 📄 requirements.txt
│   ├── 📄 .env.example             ← Config template
│   ├── 📄 .env                     ← Your credentials (never commit!)
│   └── 📂 logs/                    ← JSON session logs
│       └── 📄 session_YYYYMMDD.json
│
├── 📄 run.sh                       ← One-click setup & run script
├── 📄 claude_desktop_config.json   ← Claude Desktop MCP config
├── 📄 .gitignore
└── 📄 README.md                    ← You are here
```

---

## ⚡ Quickstart

> Full setup in under 5 minutes.

```bash
# 1. Clone the repo
git clone https://github.com/Vellorpavan/AUTONOMOUS-LEETCODE-AGENT.git
cd AUTONOMOUS-LEETCODE-AGENT

# 2. Run setup (installs everything, builds MCP server)
./run.sh setup

# 3. Add your credentials
cp agent/.env.example agent/.env
nano agent/.env          # paste your keys (see sections below)

# 4. Launch the agent
./run.sh solve-all
```

That's it. The agent takes over from here.

---

## 🔧 Prerequisites

| Tool | Version | Check | Install |
|---|---|---|---|
| **Node.js** | 18+ | `node --version` | [nodejs.org](https://nodejs.org) |
| **npm** | any | `npm --version` | included with Node.js |
| **Python** | 3.10+ | `python3 --version` | [python.org](https://python.org) |
| **Git** | any | `git --version` | [git-scm.com](https://git-scm.com) |

---

## 🍪 Getting Your LeetCode Cookies

The agent authenticates using your browser session. Here's exactly how to get the cookies:

<details>
<summary><b>🖥️ Chrome / Edge (Recommended) — Click to expand</b></summary>

**Step 1** — Log into [leetcode.com](https://leetcode.com)

**Step 2** — Press `F12` to open DevTools

**Step 3** — Click the **Application** tab

**Step 4** — In the left sidebar: **Storage** → **Cookies** → `https://leetcode.com`

**Step 5** — Find these two rows in the cookie table:

| Cookie Name | What it looks like | Length |
|---|---|---|
| `LEETCODE_SESSION` | `eyJ0eXAiOiJKV1QiLCJ...` | ~200+ chars |
| `csrftoken` | `abc123xyz789def...` | ~32 chars |

**Step 6** — Click each one → the full value shows at the bottom of the panel → right-click → **Copy**

> ⚠️ **Cookies expire every 2–4 weeks.** If the agent says "not authenticated", repeat this step.

</details>

<details>
<summary><b>🦊 Firefox — Click to expand</b></summary>

**Step 1** — Log into [leetcode.com](https://leetcode.com)

**Step 2** — Press `F12` → click the **Storage** tab (not Application)

**Step 3** — Expand **Cookies** → click `https://leetcode.com`

**Step 4** — Find `LEETCODE_SESSION` and `csrftoken` — same as above

</details>

---

## 🔑 Getting Your Anthropic API Key

1. Go to [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Click **Create Key** → give it a name like `leetcode-agent`
3. Copy the key — it starts with `sk-ant-api03-...`
4. Paste it into your `.env` file

> 💡 The agent uses **Claude Opus 4** for maximum problem-solving accuracy. Check [Anthropic's pricing page](https://www.anthropic.com/pricing) for current rates.

---

## ⚙️ Configuration

Edit `agent/.env`:

```env
# ── Anthropic ─────────────────────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# ── LeetCode Session (from your browser cookies) ──────────────
LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
LEETCODE_CSRF_TOKEN=your_csrftoken_value_here

# ── Agent Behaviour ───────────────────────────────────────────
DEFAULT_LANG=python3       # python3 | javascript | java | cpp
MAX_RETRIES=4              # max attempts per problem before moving on

# ── MCP Server Path ───────────────────────────────────────────
MCP_SERVER_PATH=../mcp-server/dist/index.js
```

### Language options

| Value | Language |
|---|---|
| `python3` | Python 3 (default, recommended) |
| `javascript` | JavaScript (ES6+) |
| `typescript` | TypeScript |
| `java` | Java |
| `cpp` | C++ |
| `golang` | Go |
| `rust` | Rust |

---

## 🚀 Running the Agent

```bash
# ── Solve everything ──────────────────────────────────────────
./run.sh solve-all

# ── Solve by difficulty ───────────────────────────────────────
./run.sh solve-easy           # All Easy problems first
./run.sh solve-medium         # All Medium problems
./run.sh solve-hard           # All Hard problems

# ── Solve one specific problem ────────────────────────────────
./run.sh solve two-sum
./run.sh solve longest-substring-without-repeating-characters
./run.sh solve median-of-two-sorted-arrays

# ── Advanced flags ────────────────────────────────────────────
cd agent && source venv/bin/activate

python3 agent.py --limit 20               # Solve next 20 unsolved
python3 agent.py --lang javascript        # Use JavaScript
python3 agent.py --difficulty MEDIUM      # Medium only
python3 agent.py --slug trapping-rain-water --lang cpp  # One problem in C++
```

### What you see while it runs

```
╔══════════════════════════════════════════════╗
║     LeetCode Autonomous Agent  🤖            ║
║  Language: python3  |  Max retries: 4        ║
╚══════════════════════════════════════════════╝

Session start. 847 solved, 2174 remaining.

━━━━━━━━━━ Problem: two-sum ━━━━━━━━━━
✅ #001 | Two Sum | Easy | Accepted | attempt 1 | O(n) hashmap | 52ms

━━━━━━━━━━ Problem: add-two-numbers ━━━━━━━━━━
✅ #002 | Add Two Numbers | Medium | Accepted | attempt 1 | O(n) linked list

━━━━━━━━━━ Problem: longest-substring... ━━━━━━━━━━
✅ #003 | Longest Substring | Medium | Accepted | attempt 1 | O(n) sliding window

...

══════════════════════════════════════
SESSION COMPLETE
✅ Accepted:   312 problems
❌ Failed:      14 problems
⏭  Skipped:    87 problems (premium)
⏩ Pre-solved: 847 problems
══════════════════════════════════════
```

---

## 🛠️ MCP Server — Tool Reference

The MCP server exposes 6 tools to the AI agent:

<details>
<summary><b>📋 check_auth — Verify your LeetCode session</b></summary>

```typescript
check_auth()
// Returns: { isAuthenticated: true, username: "your_username" }
// Always called first. If false → agent stops immediately.
```

</details>

<details>
<summary><b>📊 get_progress — Your solve statistics</b></summary>

```typescript
get_progress()
// Returns:
// {
//   total: 3279,
//   solved: 847,
//   tried: 124,
//   untouched: 2308,
//   byDifficulty: {
//     EASY:   { total: 882,  solved: 612 },
//     MEDIUM: { total: 1849, solved: 213 },
//     HARD:   { total: 548,  solved: 22  }
//   },
//   progressPercent: "25.8%"
// }
```

</details>

<details>
<summary><b>📃 list_problems — Fetch the problem queue</b></summary>

```typescript
list_problems({
  unsolvedOnly: true,   // only unsolved
  fetchAll: true,       // all pages
  difficulty: "EASY",   // optional filter
})
// Returns array of { id, title, slug, difficulty, status, isPaidOnly }
```

</details>

<details>
<summary><b>🔍 get_problem — Full problem details</b></summary>

```typescript
get_problem({ slug: "two-sum" })
// Returns:
// {
//   id: "1",
//   title: "Two Sum",
//   difficulty: "Easy",
//   description: "Given an array of integers...",
//   exampleTestcases: "...",
//   starterCode: { python3: "class Solution:\n    def twoSum...", ... },
//   hints: [...],
//   tags: ["Array", "Hash Table"]
// }
```

</details>

<details>
<summary><b>📤 submit_code — Submit a solution</b></summary>

```typescript
submit_code({
  slug: "two-sum",
  lang: "python3",
  code: "class Solution:\n    def twoSum(self, nums, target):\n        ..."
})
// Returns: { submissionId: "1234567890", success: true }
```

</details>

<details>
<summary><b>✅ get_result — Poll the verdict</b></summary>

```typescript
get_result({ submission_id: "1234567890" })
// Returns:
// {
//   verdict: "Accepted",
//   isAccepted: true,
//   runtime: "52ms",
//   memory: "16.4MB",
//   runtimePercentile: "Beats 94.2% of submissions",
//   testsPassed: "63/63"
// }
// OR on failure:
// {
//   verdict: "Wrong Answer",
//   failingTestcase: "[2,7,11,15]\n9",
//   expectedOutput: "[0,1]",
//   actualOutput: "[1,0]"
// }
```

</details>

---

## 🤖 Agent System Prompt

The agent uses an elite 5-part system prompt:

```
PART 1 — IDENTITY
  Elite competitive programmer. 10+ years ICPC + LeetCode.
  Never guesses. Verifies everything.

PART 2 — AGENT LOOP
  Startup → auth check → load queue → sort Easy/Medium/Hard
  Per problem: skip check → solve → submit → check → branch on verdict
  Rate limit guard (wait 60s on 429) → session log → next problem

PART 3 — SOLVER BRAIN (per problem)
  Constraint → complexity map (n≤20: O(2ⁿ), n≤10⁶: O(n)...)
  10-step workflow: read → pattern → algorithm → complexity check
  → edge cases → implement → dry run → validate → debug → output

PART 4 — HARD RULES
  Never invent test cases. Never submit same code twice.
  Never loop more than 4 times. Never wait for human input.
  One failed problem never stops the session.

PART 5 — LOG FORMAT
  ✅ #001 | Two Sum | Easy | Accepted | attempt 1 | O(n) hashmap
  ❌ #042 | Trapping Rain Water | Hard | Failed | attempt 4 | TLE
```

---

## 📊 Session Logs

Every run saves a full JSON log to `agent/logs/`:

```json
{
  "session_id": "20240315_143022",
  "start_time": "2024-03-15T14:30:22",
  "duration_seconds": 14402,
  "total": 312,
  "accepted": 298,
  "failed": 9,
  "skipped": 5,
  "results": [
    {
      "timestamp": "2024-03-15T14:30:45",
      "id": "1",
      "title": "Two Sum",
      "slug": "two-sum",
      "difficulty": "Easy",
      "status": "accepted",
      "attempts": 1,
      "lang": "python3",
      "notes": "O(n) hashmap"
    },
    {
      "id": "42",
      "title": "Trapping Rain Water",
      "difficulty": "Hard",
      "status": "failed",
      "attempts": 4,
      "notes": "TLE on monotonic stack approach"
    }
  ]
}
```

---

## ☁️ Google Cloud Deployment

This project is built to run on **Google Cloud** for 24/7 autonomous operation.

<details>
<summary><b>Deploy to Google Cloud Compute Engine</b></summary>

```bash
# 1. Create a VM instance
gcloud compute instances create leetcode-agent \
  --machine-type=e2-standard-2 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --zone=us-central1-a

# 2. SSH into the instance
gcloud compute ssh leetcode-agent --zone=us-central1-a

# 3. Install dependencies on the VM
sudo apt update && sudo apt install -y nodejs npm python3 python3-pip python3-venv git

# 4. Clone your repo
git clone https://github.com/Vellorpavan/AUTONOMOUS-LEETCODE-AGENT.git
cd AUTONOMOUS-LEETCODE-AGENT

# 5. Setup
./run.sh setup

# 6. Add credentials
nano agent/.env

# 7. Run in background (stays alive after SSH disconnect)
nohup ./run.sh solve-all > agent/logs/stdout.log 2>&1 &

# 8. Watch it run
tail -f agent/logs/stdout.log
```

</details>

<details>
<summary><b>Deploy with Google Cloud Run (Containerized)</b></summary>

```dockerfile
# Dockerfile (add to project root)
FROM node:18-slim AS mcp-builder
WORKDIR /app/mcp-server
COPY mcp-server/package*.json ./
RUN npm install
COPY mcp-server/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y nodejs npm
COPY --from=mcp-builder /app/mcp-server/dist ./mcp-server/dist
COPY --from=mcp-builder /app/mcp-server/node_modules ./mcp-server/node_modules
COPY agent/requirements.txt ./agent/
RUN pip install -r agent/requirements.txt
COPY agent/ ./agent/
CMD ["python3", "agent/agent.py"]
```

```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT/leetcode-agent

# Deploy
gcloud run deploy leetcode-agent \
  --image gcr.io/YOUR_PROJECT/leetcode-agent \
  --platform managed \
  --set-env-vars ANTHROPIC_API_KEY=...,LEETCODE_SESSION=...,LEETCODE_CSRF_TOKEN=...
```

</details>

---

## 🐛 Troubleshooting

<details>
<summary><b>❌ "Not authenticated" error</b></summary>

Your cookies have expired (they last 2–4 weeks).

1. Log into leetcode.com in your browser
2. Get fresh cookies (see [Getting Your LeetCode Cookies](#-getting-your-leetcode-cookies))
3. Update `agent/.env` with the new values
4. Restart the agent

</details>

<details>
<summary><b>❌ "MCP server not found" / "Cannot find module"</b></summary>

The TypeScript hasn't been compiled yet.

```bash
cd mcp-server
npm install
npm run build
```

</details>

<details>
<summary><b>❌ Agent stops after one problem</b></summary>

Check `agent/logs/` for the latest session file. Look for the error. Common causes:

- API rate limit hit → add `time.sleep(2)` between problems
- Network timeout → check internet connection
- Wrong MCP path → check `MCP_SERVER_PATH` in `.env`

</details>

<details>
<summary><b>❌ "Premium problem" errors</b></summary>

The agent automatically skips premium-only problems. If you have LeetCode Premium, the cookies will already include premium access — no extra config needed.

</details>

<details>
<summary><b>❌ Python venv issues</b></summary>

```bash
cd agent
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

</details>

---

## 🗺️ Roadmap

- [x] Custom MCP server with 6 LeetCode tools
- [x] Autonomous agent loop (queue → solve → submit → check → retry → next)
- [x] Verdict-aware retry (WA / TLE / MLE / RE / CE each handled differently)
- [x] Rate limit guard (429 handling)
- [x] Session logging to JSON
- [x] Google Cloud deployment support
- [ ] Web dashboard to monitor progress in real time
- [ ] Discord / Telegram notifications on session complete
- [ ] Support for contest problems
- [ ] Multi-language parallel solving (try Python, fallback to C++)
- [ ] GitHub Actions scheduled runs
- [ ] Automatic cookie refresh via browser extension

---

## 🤝 Contributing

**Project Details:** This is a real, working project developed with significant engineering hours to autonomously solve problems on LeetCode. *(Note: This project is proprietary and does not have an open-source license.)*

Contributions are welcome! Here's how:

```bash
# Fork the repo, then:
git clone https://github.com/Vellorpavan/AUTONOMOUS-LEETCODE-AGENT.git
cd AUTONOMOUS-LEETCODE-AGENT

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes, then
git commit -m "feat: your feature description"
git push origin feature/your-feature-name

# Open a Pull Request on GitHub
```

---

<div align="center">

<!-- ANIMATED FOOTER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=twinkling" width="100%"/>

<br/>

**Built with 🤖 Claude Opus 4 · ☁️ Google Cloud · 🔌 MCP Protocol**

<br/>

<a href="https://github.com/Vellorpavan/AUTONOMOUS-LEETCODE-AGENT/stargazers">
  <img src="https://img.shields.io/github/stars/Vellorpavan/AUTONOMOUS-LEETCODE-AGENT?style=social" />
</a>
&nbsp;
<a href="https://github.com/Vellorpavan/AUTONOMOUS-LEETCODE-AGENT/network/members">
  <img src="https://img.shields.io/github/forks/Vellorpavan/AUTONOMOUS-LEETCODE-AGENT?style=social" />
</a>
&nbsp;
<a href="https://github.com/Vellorpavan/AUTONOMOUS-LEETCODE-AGENT/issues">
  <img src="https://img.shields.io/github/issues/Vellorpavan/AUTONOMOUS-LEETCODE-AGENT?style=social" />
</a>

<br/><br/>

*If this project helped you — drop a ⭐ on GitHub. It means everything.*

<br/>

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

</div>
