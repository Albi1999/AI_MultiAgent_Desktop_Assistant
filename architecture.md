                ┌────────────────────────────┐
                │        Streamlit UI        │
                │  (Claude + Tool Use Loop)  │
                └────────────┬───────────────┘
                             │
                tool_use: adk_agent_tool
                             ▼
                 ┌────────────────────────┐
                 │     agent_adk.py       │ ← Claude chiama ADK Agent
                 │  (Agent A - entrypoint)│
                 └────┬───────────┬───────┘
                      │           │
                      ▼           ▼
         /relay/ → relay_agent.py │             (Proposta 1/2)
        (Agent B - delega secondaria)
                                   ▼
                          MCP Server (FastAPI)
                      ┌────────────────────────┐
                      │ tool: /rag-query       │
                      │ tool: /summarize       │  ← Real MCP (Proposta 3)
                      └────────────────────────┘
