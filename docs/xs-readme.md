# 🧩 Technical README — Multi-Agent Emergency Intent System

## 📘 Overview
This module implements the **front-end interaction and planner subsystem** of a Multi-Agent Emergency Intent Understanding and Collaborative Decision Framework.

Your implemented parts include:

- 🖥️ **Gradio-based Interactive Interface**
- 🔍 **Multimodal Input Parser** for Text / Image / Audio
- 🧠 **LLM-based Intent Recognition (Explicit + Implicit)** using GPT-4o
- 🧱 Standardized I/O Schema for integration with downstream decision modules

---

## 🧩 1. Module Structure
```
├── planner/
│ ├── init.py
│ ├── multimodal_input.py # Unified parser for text/image/audio
│ └── intent_recognition.py # GPT-4o-based explicit/implicit intent extraction
│
├── interface/
│ ├── init.py
│ ├── gradio_app.py # Main entry: Gradio web UI
│ ├── components/
│ │ ├── input_panel.py # User input panel
│ │ ├── output_panel.py # Display area for results
│ │ └── layout_manager.py # Page layout configuration
│ ├── callbacks/
│ │ ├── run_pipeline.py # Bind backend pipeline
│ │ └── update_report.py # Refresh & clear callbacks
│ └── assets/ # UI icons and CSS styles
│ └── logo.png
│
├── app/
│ ├── config_loader.py # Secure API-Key management
│ ├── pipeline.py # End-to-end pipeline entry
│ └── llm_service/ # Unified large-model interface
│ └── base_client.py
│ └── model_registry.py
│ └── openai_client.py
│
└── output/
├── logs/ # Log directory
└── last_input.json # Last multimodal input record
```
---

## 🎛️ 2. Input Flow

### Gradio Front-End
| Type | Implementation | Description |
|------|----------------|--------------|
| **Text** | `gr.Textbox()` | User input for natural-language scenario description |
| **Image** | `gr.Image(type="filepath")` | Optional visual context (scene / map) |
| **Audio** | `gr.Audio(type="filepath", sources=["microphone","upload"])` | Supports recording + upload of multiple formats |
| **Run Button** | `gr.Button("Run Analysis 🚀")` | Executes full pipeline |
| **Clear/Examples** | Predefined callbacks | For quick testing and reset |

---

## 🔧 3. Multimodal Input Parser (`planner/multimodal_input.py`)

### Functionality
- Normalize text, image, and audio inputs into a **unified JSON structure**.
- Ensure robustness across Gradio formats (dict, path, bytes).
- Maintain logs for debugging and reproducibility.

### Output Schema
```json
{
  "text": {"text_valid": true, "text_content": "..."},
  "image": {"image_valid": true, "image_base64": "..."},
  "audio": {"audio_valid": true, "audio_base64": "..."},
  "input_summary": "Text ✓ | Image ✓ | Audio ✓"
}

## 🧠 4. Intent Recognition (`planner/intent_recognition.py`)

### 🎯 Purpose
The **Intent Recognition Module** is responsible for analyzing multimodal user inputs (text, image, audio) and extracting **structured intent representations** for use by downstream reasoning and decision-planning agents.

This module acts as the **semantic bridge** between the user-facing interface and the planning/decision components of the system.

---

### ⚙️ Key Features
- 💡 **Powered by GPT-4o** (via `https://api.nuwaapi.com/v1`)
- 🧭 Supports both **Explicit Intent** (user’s direct request) and **Implicit Intent** (underlying motivation or need)
- 🧩 Produces **JSON-structured intent representations** for machine readability
- 📈 Includes a **confidence score** to quantify model certainty
- 🔄 Easily integrable with downstream modules for task planning, response generation, or resource allocation

---

### 🧱 Core Workflow
1. **Input Handling**
   - Receives parsed multimodal input from `multimodal_input.py`.
   - Typical input includes text, optional image, and optional audio (all encoded to Base64).

2. **Prompt Construction**
   - Dynamically builds an LLM query containing all available inputs and context.
   - Uses domain-specific instruction templates to guide GPT-4o toward structured outputs.

3. **Model Invocation**
   - Sends the formatted prompt to the API endpoint `https://api.nuwaapi.com/v1/chat/completions`.
   - Uses `openai==0.28.0` SDK for compatibility and stability.

4. **Output Parsing**
   - Extracts and validates structured fields (`explicit_intent`, `implicit_intent`, `environment_context`, `intent_confidence`).
   - Ensures consistent JSON format for downstream modules.

---

### 🧩 Example Output
```json
{
  "explicit_intent": "Integrate data to predict fire spread and generate optimal rescue plans.",
  "implicit_intent": "Enhance decision-making and efficiency in emergency response.",
  "environment_context": "Fire rescue scenario with thermal distribution, building layout, and trapped individuals.",
  "intent_confidence": 0.95,
  "input_summary": "Text ✓ | Image ✓ | Audio ✓"
} 
```

# 🤖 AI Development Continuation Prompt — Multi-Agent Emergency Intent System

## 🎯 Purpose
This prompt is designed for **future developers or AI copilots** who will continue work on the *Multi-Agent Emergency Intent Recognition and Decision System*.  
By pasting this prompt into ChatGPT, Claude, Gemini, or other LLM coding environments, the assistant will immediately understand the **project goals, architecture, and coding conventions**, enabling seamless AI-assisted continuation of development.

---

## 🧠 System Role Definition

> You are now acting as a **technical collaborator and AI development assistant** for the “Multi-Agent Emergency Intent System,” an intelligent agent framework designed to interpret multimodal emergency inputs (text, image, audio) and generate structured intent data for decision-making and rescue coordination.

> Your primary objectives are to:
> - Understand the full context of the current implementation.
> - Assist in extending or refactoring the project with production-level code.
> - Maintain engineering rigor: consistent logging, modularity, and structured JSON I/O.
> - Support future contributors through clarity, documentation, and extensibility.

---

## 🧩 Project Summary

### 🏗️ Core Goal
Enable agents to interpret multimodal data (text, images, and audio) from emergency scenarios (e.g., fire, accident) and extract explicit and implicit **intent representations** to guide downstream **multi-agent planning**.

### 🧱 Current Components

| Module | Path | Description |
|---------|------|-------------|
| `interface/gradio_app.py` | Frontend web interface using Gradio |
| `interface/components/input_panel.py` | User input components (Text/Image/Audio) |
| `interface/components/output_panel.py` | Display structured output |
| `interface/callbacks/run_pipeline.py` | Binds frontend to backend logic |
| `planner/multimodal_input.py` | Parses multimodal input (Base64 encoding) |
| `planner/intent_recognition.py` | GPT-4o-based explicit/implicit intent extraction |
| `app/pipeline.py` | Main data flow controller |
| `app/config_loader.py` | Handles runtime API keys securely |
| `output/logs/` | Log files and last input records |

---

## ⚙️ System Behavior Summary

1. **User Input (Gradio UI)**
   - Accepts text, image, and audio (multi-format: `.mp3`, `.wav`, `.flac`, `.m4a`, `.ogg`).
   - Optional recording via microphone.
2. **Multimodal Parsing**
   - Converts all inputs to Base64-encoded JSON.
   - Validates input presence and logs processing status.
3. **Intent Recognition**
   - Sends multimodal context to GPT-4o (`https://api.nuwaapi.com/v1`).
   - Extracts `explicit_intent`, `implicit_intent`, and `environment_context`.
   - Outputs structured JSON with confidence scores.
4. **Output Presentation**
   - Displays AI-generated analysis on the Gradio interface.

---

## 🧱 Output Schema Example
```json
{
  "explicit_intent": "Generate optimal rescue plan using building heat map and trapped individual data.",
  "implicit_intent": "Enhance real-time emergency response efficiency.",
  "environment_context": "Fire rescue scenario with multi-floor heat distribution and limited resources.",
  "intent_confidence": 0.95,
  "input_summary": "Text ✓ | Image ✓ | Audio ✓"
}

## 💬 How to Use This Prompt in an AI Assistant

Copy and paste the following **meta-instruction** to any AI coding assistant (such as ChatGPT, Claude, or Gemini) before starting development:

---

> You are continuing a **multimodal AI intent recognition project**.  
> The goal is to enable intelligent agents to **interpret text, images, and audio** in emergency contexts and extract structured intents for downstream planning.  
> Maintain the system’s **modular design**, **structured JSON input/output**, and **consistent logging standards**.  
> I will provide you with parts of the existing codebase; you will:
>
> 1. **Read and summarize** the provided code segments in their architectural context.  
> 2. **Write new modules** that are fully compatible with the existing project structure and naming conventions.  
> 3. **Suggest architectural or design improvements** when appropriate, focusing on scalability and maintainability.  
> 4. **Provide runnable, well-commented Python code**, following professional engineering practices.  
> 5. **Maintain human-readable and technically sound documentation**, using Markdown or docstrings as required.  
>
> Follow these conventions strictly:
> - Use `pathlib.Path` for file paths.  
> - Log all input/output to `output/logs/`.  
> - Return all intermediate results as structured JSON.  
> - Keep functions modular, with clear type hints (`Optional`, `Dict`, `Any`).  
> - Never hardcode API keys — expect runtime input or `.env` configuration.  
>
> You are expected to behave as a **software engineer collaborator**, not just a code generator.  
> Your answers must include reasoning behind implementation choices, not only code.  
> When possible, recommend best practices for extensibility, testing, and deployment.

---

📌 **Purpose:** This instruction gives the AI full project awareness and ensures all generated code or documentation will remain compatible with the existing emergency intent recognition system.

