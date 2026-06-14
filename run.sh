#!/bin/bash
# ═══════════════════════════════════════════════════
# Autonomous LeetCode Agent — run.sh
# ═══════════════════════════════════════════════════
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
MCP_DIR="$ROOT_DIR/mcp-server"
AGENT_DIR="$ROOT_DIR/agent"

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
RED="\033[0;31m"
NC="\033[0m"

print_header() {
  echo -e "\n${CYAN}╔══════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║     AUTONOMOUS LEETCODE AGENT            ║${NC}"
  echo -e "${CYAN}╚══════════════════════════════════════════╝${NC}\n"
}

cmd_setup() {
  print_header
  echo -e "${YELLOW}[1/4] Installing MCP server dependencies...${NC}"
  cd "$MCP_DIR"
  npm install

  echo -e "\n${YELLOW}[2/4] Building MCP server (TypeScript → JS)...${NC}"
  npm run build

  echo -e "\n${YELLOW}[3/4] Setting up Python virtual environment...${NC}"
  cd "$AGENT_DIR"
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip -q
  pip install -r requirements.txt -q

  echo -e "\n${YELLOW}[4/4] Setting up .env file...${NC}"
  if [ ! -f "$AGENT_DIR/.env" ]; then
    cp "$AGENT_DIR/.env.example" "$AGENT_DIR/.env"
    echo -e "${GREEN}✅ Created agent/.env from template.${NC}"
    echo -e "${RED}⚠  Fill in your credentials in agent/.env before running!${NC}"
  else
    echo -e "${GREEN}✅ agent/.env already exists — skipping.${NC}"
  fi

  echo -e "\n${GREEN}✅ Setup complete!${NC}"
  echo -e "\nNext steps:"
  echo -e "  1. Edit ${CYAN}agent/.env${NC} with your credentials"
  echo -e "  2. Run ${CYAN}./run.sh solve-all${NC} to start solving"
}

cmd_solve_all() {
  print_header
  cd "$AGENT_DIR"
  source .venv/bin/activate 2>/dev/null || true
  echo -e "${GREEN}▶ Solving all unsolved problems (Easy → Medium → Hard)${NC}\n"
  python agent.py
}

cmd_solve_one() {
  local slug="$1"
  if [ -z "$slug" ]; then
    echo -e "${RED}Usage: ./run.sh solve <problem-slug>${NC}"
    echo -e "Example: ./run.sh solve two-sum"
    exit 1
  fi
  print_header
  cd "$AGENT_DIR"
  source .venv/bin/activate 2>/dev/null || true
  echo -e "${GREEN}▶ Solving problem: ${slug}${NC}\n"
  python agent.py --slug "$slug"
}

cmd_solve_easy() {
  print_header
  cd "$AGENT_DIR"
  source .venv/bin/activate 2>/dev/null || true
  echo -e "${GREEN}▶ Solving Easy problems only${NC}\n"
  python agent.py --difficulty Easy
}

cmd_solve_medium() {
  print_header
  cd "$AGENT_DIR"
  source .venv/bin/activate 2>/dev/null || true
  echo -e "${GREEN}▶ Solving Medium problems only${NC}\n"
  python agent.py --difficulty Medium
}

cmd_solve_hard() {
  print_header
  cd "$AGENT_DIR"
  source .venv/bin/activate 2>/dev/null || true
  echo -e "${GREEN}▶ Solving Hard problems only${NC}\n"
  python agent.py --difficulty Hard
}

cmd_logs() {
  ls -lt "$AGENT_DIR/logs/"*.log 2>/dev/null | head -20 || echo "No logs yet."
}

cmd_build() {
  echo -e "${YELLOW}Building MCP server...${NC}"
  cd "$MCP_DIR"
  npm run build
  echo -e "${GREEN}✅ Build complete.${NC}"
}

case "${1:-help}" in
  setup)        cmd_setup ;;
  solve-all)    cmd_solve_all ;;
  solve)        cmd_solve_one "$2" ;;
  solve-easy)   cmd_solve_easy ;;
  solve-medium) cmd_solve_medium ;;
  solve-hard)   cmd_solve_hard ;;
  build)        cmd_build ;;
  logs)         cmd_logs ;;
  help|--help|-h)
    print_header
    echo "Usage: ./run.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  setup          Install deps, build server, create .env"
    echo "  solve-all      Solve all unsolved problems (Easy→Medium→Hard)"
    echo "  solve <slug>   Solve one specific problem, e.g. 'two-sum'"
    echo "  solve-easy     Solve Easy problems only"
    echo "  solve-medium   Solve Medium problems only"
    echo "  solve-hard     Solve Hard problems only"
    echo "  build          Rebuild the MCP TypeScript server"
    echo "  logs           List recent session logs"
    ;;
  *)
    echo -e "${RED}Unknown command: $1${NC}"
    echo "Run ./run.sh help for usage."
    exit 1
    ;;
esac
