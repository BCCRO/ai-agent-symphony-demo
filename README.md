# 🎶 AI-Agent-Symphony-Demo

[![LangChain](https://img.shields.io/badge/langchain-v0.0.0-blue)](https://github.com/langchain-ai/langchain)  [![LangChain Blog](https://img.shields.io/badge/Blog-LangChain-lightgrey)](https://blog.langchain.dev)  [![AI Agents Architecture – Part 6](https://img.shields.io/badge/Medium-AI%20Agents%20Architecture%20Part%206-orange)](https://medium.com/@vipra_singh/ai-agents-architectures-part-6-538812b1e17d) [![PyCon Colombia 2025](https://img.shields.io/badge/PyCon%20Colombia-2025-F137A6)](https://2025.pycon.co/#/talks/8)

> **Sinfonía de Mentes Artificiales**: Orchestrating Cognitive Agents with LangChain & Python to Build Intelligent Ecosystems  
> *PyCon Colombia 2025*

---

## 📖 Overview

Welcome to the AI-Agent-Symphony-Demo repository—your companion for the PyCon Colombia 2025 talk **“Sinfonía de Mentes Artificiales”**. Here you’ll find interactive Jupyter notebooks, reusable tool modules, architecture diagrams, and everything you need to see LangChain in action:

- 🎯 **Demo 1**: Simple Math Agent (`add_numbers` + `subtract_numbers`)  
- 🎯 **Demo 2**: Multi-tool ReactAgent (Math + Wikipedia search + support tools)  
- 🎨 **Architecture diagrams**: Monolithic LLM vs. Agent Ecosystem  

![Agent Support Diagram](https://github.com/BCCRO/ai-agent-symphony-demo/blob/main/images/agent_suport_diagram.png)

---

## 📂 Repository Structure

```text
ai-agent-symphony-demo/
│
├── 📄 README.md
├── 🔧 requirements.txt
├── .gitignore
│
├── 🗒️ notebooks/
│ ├── 01-agent-math-demo.ipynb
│ └── 02-agent-support-tools-demo.ipynb
│
├── 📦 src/
│ ├── tools/
│ │ ├── math_tools.py
│ │ ├── search_tools.py
│ │ ├── jira_tools.py
│ │ └── google_tools.py
│ └── utils/
│ └── chat_utils.py
│
├── 🖼️ images/
│ ├── llm_monolithic.png
│ ├── ecosystem_diagram.png
│ └── orchestration_intro.png
│
├── 📑 examples/
│ └── demo_prompts.txt
│
└── 📚 docs/
└── architecture.md
```
---

## 🚀 Quick Start

1. **Clone the repo**  
   ```bash
   git clone https://github.com/BCCRO/ai-agent-symphony-demo.git
   cd ai-agent-symphony-demo
   ```
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3. **Set up your API key**
    ```bash
    export OPENAI_API_KEY="your_openai_api_key"
    export GOOGLE_CREDENTIALS_PATH="/path/to/your/google-credentials.json"
    export JIRA_URL="https://your-domain.atlassian.net"
    export JIRA_USER="your_jira_email@example.com"
    export JIRA_TOKEN="your_jira_api_token"
    ```
4. **Launch Notebooks**
    ```bash
    jupyter lab notebooks/
    ```
--- 

## 🎓 Demo Notebooks
* 01-agent-math-demo.ipynb
🔸 Define two @tool functions: add_numbers & subtract_numbers
🔸 Create a ReactAgent example
🔸 Run interactive prompts

* 02-agent-support-tools-demo.ipynb
🔸 Extend toolkit with wiki_search, jira_tools, gmail_tools
🔸 Build multi-tool ReactAgent orchestration
🔸 Showcase real-world workflow: ticketing + notifications
---

## 🏗️ Architecture Diagrams
* Monolithic LLM
* Agent Ecosystem
* Directed orchestration: LLM call → tools → feedback loop → updated memory.
* Orchestration Intro
---

## 🌟 Why LangChain + PyCon Colombia 2025?
* Modularity: spin up new agents in minutes with `@tool`.
* Orchestration: built-in ReactAgent & AgentExecutor simplify flows.
* Scalability: from demo notebooks to production containers.
* Interactivity: perfect for live demos at PyCon Colombia—show your audience how to compose AI “symphonies.”

---
## 📝 License
This project is licensed under the MIT License. See the LICENSE file for details.

Enjoy the symphony! 🎵🧠

@bccruzo
