When building a
skill for an AI agent, Alistair Cockburn’s "dual-path" approach to a walking skeleton is particularly useful because it lets you isolate two very different types of failure: mechanical failure (the agent can’t talk to the tool) and logic failure (the agent doesn't know what to say).
Depending on which risk you need to kill first, you choose your "direction":

1. Outside-In: The "Hollow" Skill (Mechanical Risk)
This approach prioritizes the connectivity between the agent, the orchestrator, and the external world.

    The Implementation: You create the full technical path—from the LLM's prompt to a real API call—but you hard-code the business logic or the response.
    Why use it: Use this if the main risk is integration. For example, if you aren't sure if the agent can successfully authenticate with a legacy database or if the network latency for a specific tool will cause the LLM to time out.
    The "Walk": The agent triggers the tool, the tool returns a static "Hello World" from the real database, and the agent reports success. 

2. Inside-Out: The "Fake" Skill (Reasoning Risk)
This approach prioritizes the agent's "brain" and its ability to handle complex multi-step reasoning.

    The Implementation: You build the sophisticated prompt chains or logic flows but use hard-coded fakes (mocks) for the tools.
    Why use it: Use this if the main risk is stochastic/logic-based. For example, if you are building a complex tax-calculation skill, the risk isn't "can I call an API?"; the risk is "can the LLM actually follow these 20 logical steps without hallucinating?"
    The "Walk": You run the agent through a local test harness where every tool call returns a perfect, pre-defined JSON object. You are testing if the agent knows which tool to call and how to interpret the result.

Which one to choose for an Agent Skill?

    Choose Outside-In if your agent is a simple "router" for existing, temperamental infrastructure.
    Choose Inside-Out if your agent is performing high-stakes reasoning where the "correctness" of the output is more uncertain than the technical connection.