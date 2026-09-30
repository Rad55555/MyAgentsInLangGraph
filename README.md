# LangGraph Agent Tutorial

This project builds a small command-line LLM agent one LangGraph concept at a time: state, nodes, conditional routing, tools, persistence, and human approval.

## 1. Set up Python

Use Python 3.11 or newer. From this project directory, make and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

A virtual environment keeps this project's packages separate from the rest of your computer.

## 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` names the libraries. `langgraph` builds and runs the graph, `langchain-openai` connects an OpenAI chat model and its tools, `langgraph-checkpoint-sqlite` stores graph checkpoints in SQLite, and `python-dotenv` reads settings from a local `.env` file.

## 3. Configure the model

```bash
cp .env.example .env
```

Open `.env` and replace the sample `OPENAI_API_KEY` value with your key. The key is a secret; do not commit `.env` or paste the key into source code. `.gitignore` already excludes `.env`. The model defaults to `gpt-4o-mini`; set `OPENAI_MODEL` to another tool-capable model available to your account if needed. Model API usage may incur charges.

## 4. Run the agent

```bash
python agent.py
```

Try `What time is it?` to exercise a tool call, then ask it to send a message to someone to see the approval pause. The message tool is deliberately a demo: even if approved, it only prints a preview and sends nothing. Type `/quit` to exit.

## How the graph works

Read `agent.py` from top to bottom:

1. **State:** `AgentState` describes the values carried between graph steps. `add_messages` appends new user, assistant, and tool messages to the existing conversation rather than replacing the history.
2. **Tools:** `@tool` turns ordinary Python functions into tools the model can request. The demo offers a local-time lookup and a message preview.
3. **Nodes:** `assistant` asks the model what to do. `tools` runs a requested tool. `human_approval` pauses before the message-preview tool. `deny_tool` records a denial as a tool result so the model can explain what happened.
4. **Conditional routing:** `route_after_assistant` chooses whether to finish, run a tool, or pause for approval. After approval, `route_after_approval` sends the graph to the tool or to the denial node.
5. **Human approval:** LangGraph's `interrupt` saves the paused run and exposes the proposed action to the CLI. The CLI resumes that same run with `Command(resume=...)` after the person answers.
6. **Persistence:** `SqliteSaver` checkpoints graph state in `checkpoints.sqlite`. The configured `thread_id` identifies this conversation, so its history can be continued after restarting the program.

The model call requires an internet connection and a working API key. No key is required just to install the Python packages.

## File guide

- `agent.py`: the complete runnable graph and interactive CLI.
- `requirements.txt`: third-party Python packages used by the project.
- `.env.example`: safe-to-share template for local configuration; copy it to `.env` and add your secret there.
- `.gitignore`: excludes the virtual environment, secrets, Python cache files, and local SQLite databases from Git.
- `README.md`: setup instructions and the learning guide.





our final file is react_agent.py, and it demonstrates:

A tool-backed model call
ReAct-style reasoning and action
Tool execution from Python
Observation returned to the model
Final answer generation
Interactive CLI input
How to use it
Run:


Then try prompts like:

“What is 123 plus 456?”
“What time is it?”
“What is 7 times 8?”
“Add 10 and 25”
Type /quit to exit.

Why this matters
This is the first chapter pattern from the course:

Model decides whether it needs a tool
Your Python function executes it
Tool result is passed back as an observation
Model answers using the tool output
If you want, I can take the next chapter step with you and turn this into a proper LangGraph graph with:

state
nodes
routing
tool calling
persistence
human approval