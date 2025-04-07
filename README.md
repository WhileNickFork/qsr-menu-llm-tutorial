# Generative AI for QSR Menu Analysis: LangChain & LangGraph Tutorials

## Overview

This repository provides a series of Jupyter notebook tutorials demonstrating how to apply generative AI, specifically Large Language Models (LLMs), to interact with Quick Service Restaurant (QSR) menu data. The tutorials explore different approaches, starting with simpler LangChain abstractions and progressing to more complex, customizable, and stateful agentic workflows using LangGraph.

The primary goal is to show how to build systems that can:

1.  Answer natural language questions about a QSR menu stored in a SQL database (e.g., "What vegetarian options are there?", "What's the cheapest burger?", "What is the healthiest meal?").
2.  (Coming Soon) Analyze competitor menu images to extract items and prices, then compare them against the internal menu database.

These notebooks leverage popular libraries like LangChain and LangGraph to orchestrate interactions between LLMs, SQL databases, and potentially image data.

## Target Audience

These tutorials are designed for:

* Developers, Data Scientists, or AI Practitioners interested in building applications that integrate LLMs with structured data (SQL) and potentially multimodal inputs (images).
* Individuals generally familiar with Python, the basics of Large Language Models (LLMs), and SQL concepts.
* Those who may be new to the LangChain ecosystem, particularly LangGraph, and want practical examples of how to build agentic workflows for tasks like Text-to-SQL and data analysis.

## Prerequisites

* **Skills:**
    * Solid understanding of Python programming.
    * Basic SQL knowledge (SELECT queries, JOINs).
    * Familiarity with the fundamental concepts of Large Language Models (LLMs).
    * (For Notebook 3) Basic understanding of multimodal LLMs.
* **Tools & Access:**
    * Python 3 environment (using a virtual environment like `venv` is recommended).
    * Jupyter Notebook or JupyterLab.
    * Access to an OpenAI-compatible LLM API endpoint. The notebooks provide examples for:
        * Locally hosted Ollama (you'll need Ollama installed and appropriate models like `llama3.3:70b-instruct-q3_K_S` and `gemma3:27b` downloaded).
        * Cloud-hosted models like NVIDIA NIM endpoints (requires an API key).
    * Required Python packages (installation commands are included within the notebooks): `sqlalchemy`, `langchain-openai`, `ipython`, `langchain-community`, `langgraph`, `typing-extensions`, `langchain-core`, `langchain`, `pydantic`, `Pillow` (for vision notebook), `tiktoken`.

## Notebooks (Table of Contents)

The tutorials are presented as a series of Jupyter notebooks, designed to be followed sequentially:

1.  **`1-LangChain.ipynb` - Basic QSR Menu Chatbot**
    * **Goal:** Demonstrate the simplest way to connect an LLM to a SQL database containing QSR menu data to answer natural language questions.
    * **Approach:** Uses LangChain's built-in `create_sql_agent` and `SQLDatabaseToolkit`. This provides a high-level abstraction with minimal code.
    * **Key Concepts:** `SQLDatabase` wrapper, `SQLDatabaseToolkit`, `create_sql_agent`, interacting with local (Ollama) and cloud-hosted (NVIDIA) LLMs via `ChatOpenAI`.
    * **Takeaway:** An easy entry point for basic Text-to-SQL tasks using LangChain's pre-built agent functionality.

2.  **`2-LangGraph.ipynb` - Advanced QSR Menu Chatbot with LangGraph**
    * **Goal:** Build a more robust, customizable, and stateful SQL agent using LangGraph, offering greater control over the reasoning process.
    * **Approach:** Defines a state machine (graph) with explicit nodes for LLM calls (agent reasoning, SQL checking) and tool execution. Includes a dedicated SQL checker node to improve query reliability.
    * **Key Concepts:** LangGraph `StateGraph`, `TypedDict` for state, `add_messages` reducer, defining nodes (custom functions, `ToolNode`), conditional edges (`add_conditional_edges`), custom tool definition (`@tool` decorator) with error handling (`db.run_no_throw`), using `ToolNode.with_fallbacks` for robust tool execution, `SubmitFinalAnswer` Pydantic model for structured final output, graph visualization.
    * **Takeaway:** Shows how LangGraph enables fine-grained control, state management, and explicit error handling loops for more complex agent workflows, particularly beneficial when needing intermediate validation steps like SQL checking.

3.  **`3-LangGraph-Vision.ipynb` - Competitor Menu Analysis (Image + SQL)**
    * **Goal:** Extend the LangGraph system to handle multimodal input (competitor menu images) alongside SQL querying for comprehensive competitor analysis.
    * **Planned Approach:** Implements a multi-agent system orchestrated by a **Supervisor Agent**.
        * The **Supervisor** analyses the user request and routes it to either the `SQL Agent` (similar to Notebook 2) or a new `Competitor Analysis Agent`.
        * The **Competitor Analysis Agent**:
            * Uses a new tool (`analyze_competitor_menu_image`) leveraging a multimodal LLM (like `gemma3:27b` via Ollama) to extract items and prices from the provided image into a structured format (e.g., JSON).
            * Reuses the SQL tools (`db_query_tool`, etc.) to fetch relevant comparison data (e.g., prices of similar items) from the *internal* QSR menu database.
            * Utilizes the `SubmitFinalAnswer` tool to return the formatted summary.
    * **Key Concepts:** Supervisor pattern in LangGraph, multi-agent workflows, multimodal LLM integration within LangGraph (image encoding, prompting), defining and using multimodal tools, state management across agents/sub-graphs.
    * **Takeaway:** Demonstrates how LangGraph can manage complex, branching workflows involving different types of agents (text-based SQL, multimodal analysis) and data sources (SQL DB, images).

## Setup

1.  Clone this repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2.  It is highly recommended to create and activate a Python virtual environment:
    ```bash
    python -m venv .venv
    # On Windows
    .\.venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```
3.  Open the Jupyter notebooks (`.ipynb` files) in your preferred environment (Jupyter Notebook, JupyterLab, VS Code, etc.).
4.  The notebooks contain cells to install necessary Python packages using `%pip install`. Run these cells as needed.
5.  Ensure your chosen LLM (Ollama or cloud endpoint) is running and accessible. Configure the API endpoint URLs and any necessary API keys within the notebooks where indicated.

## Usage

Run the cells within each Jupyter notebook sequentially. Follow the instructions and explanations provided in the markdown cells. Experiment by changing the user questions, LLM models (if you have multiple available), and exploring the agent's intermediate steps.