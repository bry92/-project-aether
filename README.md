# 🌌 Project Aether

**Project Aether** is a production-grade, autonomous startup engine that merges deep software engineering capabilities with broad business operational autonomy. Inspired by the likes of Emergent.sh and Polsia, Aether allows you to build, research, and operate a company through a high-fidelity, agentic dashboard.

## ✨ Features

- **Multi-Agent Swarm:** A hierarchy of specialized AI agents (CEO, Architect, Coder, Marketer) orchestrated via **LangGraph**.
- **Magical Live Pulse:** A "buttery smooth" real-time activity feed showing agent thoughts, tool execution, and system vitals.
- **The Forge:** An interactive workspace featuring a real-time file tree, agent terminal, and **Ghost Mode** plan previews for human-in-the-loop approvals.
- **Neural Memory:** Persistent vector memory powered by **ChromaDB**, allowing agents to retain long-term context across sessions.
- **High-Agency Toolbelt:** Native integrations for:
  - **Engineering:** GitHub API (Repo creation, commits, PRs).
  - **Research:** Playwright-powered autonomous browser control.
  - **Operations:** Stripe for product and payment orchestration.
- **Glass & Void UI:** A premium, dark-mode design system utilizing advanced glass-morphism, mesh gradients, and Framer Motion.

## 🚀 Tech Stack

- **Frontend:** Next.js 14+ (App Router), TypeScript, Vanilla CSS (Modular), Framer Motion.
- **Backend:** FastAPI (Python 3.11+), LangGraph, LangChain.
- **AI Models:** Powered by Hugging Face (Llama-3-8B-Instruct) or OpenAI (GPT-4o).
- **Database:** PostgreSQL (Structured Data) + ChromaDB (Vector Memory).

## 🛠️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/bry92/-project-aether.git
cd -project-aether
```

### 2. Setup the Backend
```bash
cd aether-core
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt # (Coming soon: I will generate this)
```
Create a `.env` file based on `.env.example` and add your keys.

### 3. Setup the Frontend
```bash
cd ../aether-web
npm install
npm run dev
```

## 🌌 The Vision

Aether is designed to bridge the gap between "coding assistants" and "autonomous co-founders." It doesn't just help you write code; it helps you strategize objectives, research competitors, and ship production-ready products while you maintain full oversight via the **Approval System**.

---

Built with 💙 by **bry92**
