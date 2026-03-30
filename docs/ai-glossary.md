# Comprehensive AI Terminology Glossary (2025-2026)

> A living reference of 289 AI terms across 25 categories, compiled from extensive industry research as of April 2026.

---

## Table of Contents

1. [Core AI/ML Foundations](#1-core-aiml-foundations)
2. [Transformer Architecture & LLM Internals](#2-transformer-architecture--llm-internals)
3. [Model Types & Architectures](#3-model-types--architectures)
4. [Training Pipeline](#4-training-pipeline)
5. [Fine-Tuning & Adaptation](#5-fine-tuning--adaptation)
6. [Retrieval-Augmented Generation (RAG) & Knowledge](#6-retrieval-augmented-generation-rag--knowledge)
7. [Prompt Engineering](#7-prompt-engineering)
8. [Agentic AI & Tool Use](#8-agentic-ai--tool-use)
9. [AI Safety & Alignment](#9-ai-safety--alignment)
10. [AI Security & Adversarial Threats](#10-ai-security--adversarial-threats)
11. [AI Governance, Risk & Compliance](#11-ai-governance-risk--compliance)
12. [Generative AI & Multimodal](#12-generative-ai--multimodal)
13. [AI Infrastructure & Deployment](#13-ai-infrastructure--deployment)
14. [Inference Optimization](#14-inference-optimization)
15. [AI Coding & Development](#15-ai-coding--development)
16. [Performance Metrics & Evaluation](#16-performance-metrics--evaluation)
17. [Emerging & 2025-2026 Terminology](#17-emerging--2025-2026-terminology)
18. [AI in the Software Development Lifecycle (AI-DLC)](#18-ai-in-the-software-development-lifecycle-ai-dlc)
19. [AI Code Attribution & Compliance](#19-ai-code-attribution--compliance)
20. [AI-Assisted Team Practices](#20-ai-assisted-team-practices)
21. [Claude Code & Agent SDK](#21-claude-code--agent-sdk)
22. [Cursor, Copilot & AI Coding Tools](#22-cursor-copilot--ai-coding-tools)
23. [MCP Ecosystem (Deep Dive)](#23-mcp-ecosystem-deep-dive)
24. [Agentic Coding Patterns & Concepts](#24-agentic-coding-patterns--concepts)
25. [AI Coding Benchmarks](#25-ai-coding-benchmarks)

---

## 1. Core AI/ML Foundations

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 1 | **Artificial Intelligence (AI)** | The broad field of computer science focused on creating systems capable of performing tasks that typically require human intelligence, such as reasoning, learning, perception, and decision-making. | Core AI/ML |
| 2 | **Machine Learning (ML)** | A subset of AI where systems learn patterns from data and improve performance on tasks without being explicitly programmed, using statistical techniques to generalize from examples. | Core AI/ML |
| 3 | **Deep Learning** | A subset of machine learning that uses artificial neural networks with multiple layers (hence "deep") to learn hierarchical representations of data. Powers most modern AI breakthroughs. | Core AI/ML |
| 4 | **Neural Network** | A computational model inspired by the human brain, consisting of interconnected layers of nodes (neurons) that process and transform input data through weighted connections and activation functions. | Core AI/ML |
| 5 | **Supervised Learning** | A machine learning paradigm where models are trained on labeled data (input-output pairs), learning to map inputs to correct outputs. Used for classification and regression tasks. | Core AI/ML |
| 6 | **Unsupervised Learning** | A machine learning paradigm where models find patterns in unlabeled data without predefined outputs. Includes clustering, dimensionality reduction, and density estimation. | Core AI/ML |
| 7 | **Reinforcement Learning (RL)** | A learning paradigm where an agent learns optimal behavior by interacting with an environment, receiving rewards or penalties for actions, and maximizing cumulative reward over time. | Core AI/ML |
| 8 | **Transfer Learning** | A technique where a model trained on one task is repurposed as the starting point for a model on a different but related task, leveraging previously learned features to reduce training time and data requirements. | Core AI/ML |
| 9 | **Natural Language Processing (NLP)** | The branch of AI focused on enabling computers to understand, interpret, generate, and interact with human language in useful ways. | Core AI/ML |
| 10 | **Computer Vision** | The field of AI that enables machines to interpret and understand visual information from images and video, including object detection, image classification, and scene understanding. | Core AI/ML |

---

## 2. Transformer Architecture & LLM Internals

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 11 | **Transformer** | The dominant neural network architecture (introduced in the 2017 paper "Attention Is All You Need") that uses self-attention mechanisms to process sequential data in parallel. Powers virtually all modern LLMs and many vision models. | Architecture |
| 12 | **Self-Attention** | A mechanism within transformers that allows each token in a sequence to compute relevance scores against every other token, enabling the model to understand contextual relationships regardless of distance in the input. | Architecture |
| 13 | **Multi-Head Attention** | An extension of self-attention where the model runs multiple attention computations in parallel (each "head" learns different relationship patterns), then concatenates the results for richer representations. | Architecture |
| 14 | **Token** | The basic unit of text that an LLM processes. A token can represent a character, sub-word, word, or short phrase depending on the tokenizer. For example, "understanding" might be split into "under" + "standing". | Architecture |
| 15 | **Tokenization** | The process of converting raw text into a sequence of tokens that a model can process. Common tokenizers include Byte-Pair Encoding (BPE), WordPiece, and SentencePiece. | Architecture |
| 16 | **Context Window** | The maximum number of tokens an LLM can consider at once during inference. Determines how much text the model can "see" and reason about in a single interaction. Modern models range from 4K to 1M+ tokens. | Architecture |
| 17 | **Embedding** | A dense, fixed-dimensional vector representation of data (text, images, etc.) in a continuous space where semantically similar items are positioned closer together. Embeddings are fundamental to search, retrieval, and similarity tasks. | Architecture |
| 18 | **Positional Encoding** | A technique that injects information about the position of tokens in a sequence into the model, since transformers (unlike RNNs) process all tokens simultaneously and have no inherent sense of order. | Architecture |
| 19 | **KV Cache (Key-Value Cache)** | A memory optimization for autoregressive LLMs that stores previously computed key and value tensors from the attention mechanism, avoiding redundant computation when generating each new token. A critical target for inference optimization. | Architecture |
| 20 | **Softmax** | A mathematical function used in the attention mechanism (and output layer) that converts raw scores into a probability distribution, ensuring all attention weights sum to 1. | Architecture |

---

## 3. Model Types & Architectures

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 21 | **Large Language Model (LLM)** | A deep learning model trained on massive text corpora (billions to trillions of tokens) that can understand, generate, translate, and reason about human language. Examples: GPT-4, Claude, Llama, Gemini. | Model Types |
| 22 | **Foundation Model** | A large-scale, pre-trained AI model trained on broad data that can be adapted to a wide range of downstream tasks through fine-tuning or prompting. The term emphasizes that these models serve as a base ("foundation") for many applications. | Model Types |
| 23 | **Frontier Model** | A general-purpose AI model trained at extreme computational scale (typically >10^26 FLOPs) that pushes the state-of-the-art in capabilities. In 2026, the concept has fractured into regulatory frontier, efficiency frontier, and cost frontier. | Model Types |
| 24 | **Small Language Model (SLM)** | A language model with a smaller parameter count (typically <10B parameters) optimized for efficiency, edge deployment, and specific tasks. Trades some generality for speed and lower resource requirements. Examples: Phi-3, Gemma. | Model Types |
| 25 | **Vision Language Model (VLM)** | A model that jointly processes visual and textual information, enabling tasks like image captioning, visual question answering, and document understanding. Examples: GPT-4V, Claude Vision, LLaVA. | Model Types |
| 26 | **Mixture of Experts (MoE)** | An architecture where a model contains multiple specialized sub-networks ("experts") and a gating mechanism routes each input to only a subset of experts. This allows massive total parameter counts while keeping per-inference computation manageable. Used by DeepSeek-R1, Mixtral, and others. | Model Types |
| 27 | **Reasoning Model** | A model specifically trained (typically via reinforcement learning) to perform step-by-step logical reasoning before producing an answer. These models "think" through problems using chain-of-thought before responding. Examples: OpenAI o1/o3, DeepSeek-R1. | Model Types |
| 28 | **Generative Adversarial Network (GAN)** | An architecture with two networks -- a generator that creates synthetic data and a discriminator that distinguishes real from fake -- trained adversarially. Historically important for image generation; largely superseded by diffusion models for that task. | Model Types |
| 29 | **Variational Autoencoder (VAE)** | A generative model that learns a compressed latent representation of input data as a probability distribution, enabling smooth interpolation and generation of new samples. Often used as a component in larger systems like Stable Diffusion. | Model Types |
| 30 | **Diffusion Model** | A generative model that learns to create data by reversing a gradual noising process -- starting from pure noise and iteratively denoising to produce high-quality outputs (images, audio, video). Powers DALL-E, Stable Diffusion, Midjourney, and Sora. | Model Types |
| 31 | **Large Action Model (LAM)** | An emerging model type designed not just to generate text but to take actions in the real world or digital environments, such as controlling software, navigating websites, or operating tools autonomously. | Model Types |
| 32 | **Open-Weight Model** | A model whose trained parameters (weights) are publicly released for download and use, but may have restrictions on commercial use or modification. Distinct from fully "open-source" which also requires open training data and code. Examples: Llama, DeepSeek, Qwen. | Model Types |

---

## 4. Training Pipeline

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 33 | **Pre-training** | The initial, most compute-intensive phase of LLM training where the model learns general language understanding by predicting the next token across massive unlabeled text corpora (trillions of tokens). Creates the foundation of the model's knowledge. | Training |
| 34 | **Post-training** | All training stages that come after pre-training, including supervised fine-tuning, instruction tuning, RLHF, and other alignment techniques. Transforms a raw pre-trained model into a useful, safe assistant. | Training |
| 35 | **Supervised Fine-Tuning (SFT)** | The first post-training step where the model is trained on curated, high-quality input-output examples (typically human-written) to learn instruction-following behavior. Transforms a base model into an assistant. | Training |
| 36 | **Instruction Tuning** | A specialized form of fine-tuning that trains a model to follow natural language instructions and perform diverse tasks, using datasets of (instruction, response) pairs across many task types. | Training |
| 37 | **RLHF (Reinforcement Learning from Human Feedback)** | A training technique where the model is refined using human preference judgments. Humans rank model outputs, a reward model is trained on these preferences, and the LLM is optimized to maximize the reward via reinforcement learning (typically PPO). | Training |
| 38 | **RLAIF (Reinforcement Learning from AI Feedback)** | A variant of RLHF where AI-generated feedback replaces or supplements human feedback, enabling more scalable alignment. Used in Constitutional AI and other approaches. | Training |
| 39 | **Reward Model** | A model trained on human preference data that scores LLM outputs based on quality, helpfulness, and safety. Used as the reward signal in RLHF to guide the LLM toward preferred behaviors. | Training |
| 40 | **DPO (Direct Preference Optimization)** | A simpler alternative to RLHF that directly optimizes the language model on human preference pairs (preferred vs. rejected responses) without needing a separate reward model or RL training loop. Introduced in 2023, widely adopted by 2025. | Training |
| 41 | **GRPO (Group Relative Policy Optimization)** | An advanced preference optimization technique (popularized by DeepSeek) that extends DPO by evaluating groups of responses relative to each other rather than simple pairs, enabling more nuanced alignment. | Training |
| 42 | **PPO (Proximal Policy Optimization)** | A reinforcement learning algorithm commonly used in RLHF to update the language model policy. It constrains updates to be "proximal" (close) to the current policy to ensure stable training. | Training |
| 43 | **RLVR (Reinforcement Learning from Verifiable Rewards)** | A 2025 technique where LLMs are trained against automatically verifiable reward signals (e.g., math problem correctness) rather than human judgments. Models spontaneously develop reasoning strategies through this process. | Training |
| 44 | **Scaling Laws** | Empirical relationships showing that model performance improves predictably as training compute, model size, and dataset size increase. Originally discovered for training, now also validated for inference-time (test-time) compute. | Training |
| 45 | **Synthetic Data** | Data generated by AI models rather than collected from real-world sources. Increasingly used for training, but poses risks of model collapse when models are trained recursively on AI-generated content. By April 2025, over 74% of newly created webpages contained AI-generated text. | Training |
| 46 | **Data Curation** | The process of selecting, cleaning, filtering, and organizing training data to maximize model quality. Increasingly recognized as one of the most important factors in model performance, often more impactful than architecture changes. | Training |

---

## 5. Fine-Tuning & Adaptation

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 47 | **Fine-Tuning** | The process of further training a pre-trained model on a smaller, task-specific or domain-specific dataset to adapt it for particular use cases, improving performance on targeted tasks. | Fine-Tuning |
| 48 | **PEFT (Parameter-Efficient Fine-Tuning)** | A family of techniques that fine-tune only a small subset of model parameters (or add a small number of new parameters) rather than updating the entire model. Dramatically reduces compute and memory requirements. | Fine-Tuning |
| 49 | **LoRA (Low-Rank Adaptation)** | The most popular PEFT method. Inserts small, trainable low-rank matrices into transformer layers while keeping original weights frozen. Achieves near-full-fine-tuning performance at a fraction of the compute and memory cost. | Fine-Tuning |
| 50 | **QLoRA (Quantized LoRA)** | Combines LoRA with quantization -- the base model is loaded in 4-bit precision while LoRA adapters are trained in higher precision. Enables fine-tuning of very large models on consumer GPUs. | Fine-Tuning |
| 51 | **Adapter** | A lightweight module inserted into a pre-trained model's layers that can be trained for specific tasks while the base model remains frozen. An early form of PEFT that inspired LoRA and similar techniques. | Fine-Tuning |
| 52 | **Knowledge Distillation** | A model compression technique where a smaller "student" model is trained to mimic the behavior of a larger "teacher" model. The student can achieve 80-90% of the teacher's performance at a fraction of the compute cost. | Fine-Tuning |

---

## 6. Retrieval-Augmented Generation (RAG) & Knowledge

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 53 | **RAG (Retrieval-Augmented Generation)** | A technique that enhances LLM responses by retrieving relevant documents from an external knowledge base at query time and including them in the model's context. Reduces hallucinations and keeps responses grounded in up-to-date, domain-specific information without retraining. | RAG |
| 54 | **Vector Database** | A specialized database optimized for storing and querying high-dimensional vector embeddings. Uses approximate nearest neighbor (ANN) algorithms (HNSW, IVF, PQ) for fast similarity search. Examples: Pinecone, Weaviate, Qdrant, Chroma, pgvector. | RAG |
| 55 | **Semantic Search** | Search that matches based on meaning rather than exact keywords, using vector embeddings to find conceptually similar content. Typically powered by embedding models and vector databases. | RAG |
| 56 | **Chunking** | The process of splitting documents into smaller segments (chunks) for embedding and retrieval in RAG systems. Strategies include fixed-size, sentence-based, heading-aware, and semantic chunking (which detects thematic shifts). Semantic chunking improves recall up to 9% over fixed-size approaches. | RAG |
| 57 | **Reranking** | A second-stage retrieval step where a cross-encoder model scores query-document pairs together to reorder initial retrieval results by relevance. Improves precision by 10-30% compared to vector search alone. Models: Cohere Rerank, BGE Reranker. | RAG |
| 58 | **Hybrid Search** | A retrieval approach combining keyword-based search (BM25) with vector similarity search, then fusing results (often via Reciprocal Rank Fusion). Consistently outperforms either method alone. | RAG |
| 59 | **GraphRAG** | An advanced RAG approach that augments vector retrieval with knowledge graph relationships, building entity graphs during document ingestion and traversing relationships during retrieval to surface indirectly related content. Achieves up to 99% search precision for structured domains. | RAG |
| 60 | **Agentic RAG** | A RAG architecture where autonomous agents plan multi-step retrieval strategies, decompose complex queries into sub-queries, choose retrieval tools dynamically, reflect on intermediate answers, and adapt their approach for complex information needs. | RAG |
| 61 | **Grounding** | The practice of connecting LLM outputs to verifiable external data sources (documents, databases, APIs) to ensure factual accuracy and reduce hallucinations. RAG is the most common grounding technique. | RAG |

---

## 7. Prompt Engineering

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 62 | **Prompt** | The natural language input given to an LLM to elicit a desired output. The quality and structure of prompts significantly affects response quality. | Prompting |
| 63 | **System Prompt** | A special instruction set provided to an LLM at the beginning of a conversation that defines its role, behavior, constraints, and output format. Persists across the conversation and takes precedence over user messages. | Prompting |
| 64 | **Zero-Shot Prompting** | Asking a model to perform a task without providing any examples, relying entirely on the model's pre-trained knowledge and instruction-following ability. | Prompting |
| 65 | **Few-Shot Prompting** | Including a small number of input-output examples in the prompt to demonstrate the desired task format and behavior. Remains one of the highest-ROI prompting techniques. | Prompting |
| 66 | **Chain-of-Thought (CoT) Prompting** | A technique that instructs the model to "think step by step," breaking complex reasoning into intermediate steps before arriving at a final answer. Dramatically improves performance on math, logic, and multi-step reasoning tasks. | Prompting |
| 67 | **Self-Consistency Prompting** | An advanced technique that generates multiple chain-of-thought reasoning paths for the same problem and selects the most consistent answer, reducing errors from any single flawed reasoning chain. | Prompting |
| 68 | **Meta-Prompting** | Using a prompt to generate or optimize other prompts. The model acts as its own prompt engineer, iteratively refining instructions for better task performance. | Prompting |
| 69 | **Role Prompting** | Assigning the model a specific persona or role (e.g., "You are an expert financial analyst") to influence its response style, depth, and domain focus. | Prompting |
| 70 | **Context Engineering** | The engineering discipline of managing all non-prompt context supplied to an LLM -- including metadata, tool definitions, retrieved documents, conversation history, and system instructions -- to optimize model performance. Recognized as a genuine engineering skill distinct from casual prompting in 2025. | Prompting |
| 71 | **Prompt Injection** | A security attack where malicious instructions are embedded in user input (direct) or external data (indirect) to override the model's system prompt and intended behavior. A fundamental security challenge for LLM applications. | Prompting |
| 72 | **Prompt Leaking** | An attack variant where adversarial prompts trick the model into revealing its system prompt, internal instructions, or confidential context, potentially exposing proprietary logic or sensitive information. | Prompting |

---

## 8. Agentic AI & Tool Use

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 73 | **Agentic AI** | AI systems that can autonomously plan, reason, use tools, and take actions to accomplish complex goals with minimal human intervention. "Agentic" was the word of the year in 2025, though definitions vary across the industry. | Agentic AI |
| 74 | **AI Agent** | An autonomous system built on an LLM that can perceive its environment, make decisions, use tools, and take actions in a loop to accomplish goals. Differs from a chatbot in its ability to act, not just respond. | Agentic AI |
| 75 | **Tool Use / Tool Calling** | The capability of an LLM to invoke external tools, APIs, or functions by generating structured output (typically JSON) that instructs an external system to perform an action. The core mechanism that gives agents real-world capabilities. | Agentic AI |
| 76 | **Function Calling** | The specific API feature (pioneered by OpenAI) that allows LLMs to output structured function invocations with typed arguments. Often used interchangeably with "tool calling" though function calling is technically the API-level implementation. | Agentic AI |
| 77 | **MCP (Model Context Protocol)** | An open protocol created by Anthropic (donated to the Linux Foundation in December 2025) that standardizes how AI agents connect to external tools, data sources, and services. Often described as a "USB-C port for AI" -- build the tool interface once, any AI can use it. Crossed 97M monthly SDK downloads by February 2026. | Agentic AI |
| 78 | **A2A (Agent-to-Agent Protocol)** | An open protocol created by Google (donated to the Linux Foundation in June 2025) that standardizes how AI agents discover, communicate, and collaborate with each other regardless of their underlying framework. Described as "HTTP for AI agents." | Agentic AI |
| 79 | **AGENTS.md** | A workspace configuration file (alongside SOUL.md and USER.md) used in multi-agent systems to define agent instructions, capabilities, and behavior. Contributed to the Linux Foundation's Agentic AI Foundation alongside MCP. | Agentic AI |
| 80 | **Multi-Agent System** | An architecture where multiple specialized AI agents collaborate, with each agent handling different aspects of a task. Inquiries about multi-agent systems surged 1,445% from Q1 2024 to Q2 2025. Patterns include plan-and-execute, routing, and handoffs. | Agentic AI |
| 81 | **Agent Orchestration** | The coordination layer that manages how multiple agents interact, share context, delegate tasks, and handle handoffs. Frameworks like LangGraph, AutoGen, and CrewAI provide orchestration patterns. | Agentic AI |
| 82 | **Computer Use** | The ability of AI agents to interact with computer interfaces (clicking, typing, scrolling, reading screens) just as a human would, enabling automation of arbitrary software tasks without APIs. Pioneered by Anthropic's Claude Computer Use. | Agentic AI |
| 83 | **Browser Use** | A specialized form of computer use focused on web browser automation, where AI agents can navigate websites, fill forms, click buttons, and extract information. Tools like Browser Use optimize for this with 3-5x speed improvements over general computer use. | Agentic AI |
| 84 | **AI Sandbox** | An isolated execution environment (typically Docker containers) that safely contains AI agent actions -- including code execution, file operations, browser access, and tool use -- preventing unintended system modifications. Essential for safe agentic AI deployment. | Agentic AI |
| 85 | **Structured Output** | The ability of an LLM to generate responses that conform to a predefined schema (e.g., JSON Schema), guaranteeing both valid syntax and schema adherence. An evolution beyond simple "JSON mode" that is critical for reliable tool calling and data extraction. | Agentic AI |
| 86 | **AI Gateway** | A unified API proxy that sits between applications and multiple AI model providers, offering centralized routing, load balancing, budget controls, fallbacks, caching, and observability. Examples: Vercel AI Gateway, Cloudflare AI Gateway. | Agentic AI |
| 87 | **Model Routing** | The practice of dynamically selecting which AI model to use for a given request based on factors like complexity, cost, latency requirements, and task type. Enables cost optimization by routing simple queries to cheaper models. | Agentic AI |

---

## 9. AI Safety & Alignment

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 88 | **AI Alignment** | The practice of making AI systems behave in ways that are helpful, harmless, and honest -- ensuring the model's goals and behaviors match human values and intentions. The central challenge of AI safety. | Safety |
| 89 | **Constitutional AI (CAI)** | An alignment approach (developed by Anthropic) where models are trained to critique and revise their own outputs according to a written set of principles (a "constitution") encoded in natural language. Reduces reliance on human feedback for safety training. | Safety |
| 90 | **Red Teaming** | Systematic adversarial testing of AI systems by dedicated teams who attempt to elicit harmful, biased, or unintended outputs. Used to discover vulnerabilities before deployment. The 2026 International AI Safety Report notes that pre-deployment testing increasingly fails to reflect real-world behavior. | Safety |
| 91 | **Guardrails** | Safety mechanisms (input/output filters, content classifiers, rule-based checks) that constrain AI model behavior to prevent harmful, off-topic, or policy-violating outputs. Face trade-offs between safety and usability (overblocking). | Safety |
| 92 | **Alignment Tax** | The performance cost of safety alignment -- a model optimized for safety may become overly cautious (refusing harmless requests) while a model optimized for capability may compromise safety. Balancing this trade-off is a key research challenge. | Safety |
| 93 | **Hallucination** | When an LLM generates plausible-sounding but factually incorrect, fabricated, or unsupported information. One of the most significant reliability challenges for AI applications, particularly in high-stakes domains. | Safety |
| 94 | **AI Watermarking** | Techniques that embed invisible, detectable signals into AI-generated content (text, images, audio, video) to enable identification of synthetic content. Major tech companies are developing standards, though robustness remains challenging. | Safety |
| 95 | **Deepfake** | AI-generated synthetic media (images, video, audio) that convincingly depicts people saying or doing things they never did. By early 2025, deepfakes accounted for 40% of all biometric fraud incidents. | Safety |
| 96 | **Explainability / XAI (Explainable AI)** | The degree to which an AI system's internal decision-making process can be understood and interpreted by humans. Critical for trust, debugging, regulatory compliance, and identifying bias. | Safety |
| 97 | **Interpretability** | The research field focused on understanding what happens inside neural networks -- what features they detect, how they represent knowledge, and why they produce specific outputs. Related to but distinct from explainability. | Safety |

---

## 10. AI Security & Adversarial Threats

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 98 | **Jailbreaking** | Adversarial techniques that bypass an LLM's safety training and guardrails to produce restricted or harmful outputs. Methods range from social engineering ("pretend you are...") to sophisticated multi-step attacks. The line between aligned and adversarial behavior is thinner than most people think. | Security |
| 99 | **Data Poisoning** | An attack where corrupted, manipulated, or biased data is inserted into a model's training data, fine-tuning data, or retrieval sources to alter its behavior. In 2025-2026, attacks have expanded to target RAG indexes, tool outputs, and agent memory. | Security |
| 100 | **Memory Poisoning** | A 2025-2026 attack vector specific to AI agents with persistent memory. Malicious instructions are planted in an agent's long-term memory via indirect prompt injection, surviving across sessions and executing days or weeks later when triggered. | Security |
| 101 | **Indirect Prompt Injection** | An attack where malicious instructions are embedded in external data sources (documents, emails, websites) that the AI processes, causing it to execute unintended actions. More dangerous than direct prompt injection because the user may be unaware. | Security |
| 102 | **AI Detection** | Tools and techniques for identifying AI-generated content (text, images, audio). An ongoing arms race as generative models improve just as quickly as detection methods. | Security |
| 103 | **Benchmark Contamination** | When a model's training data inadvertently (or deliberately) includes data from evaluation benchmarks, inflating reported performance scores and giving misleading impressions of actual capability. | Security |

---

## 11. AI Governance, Risk & Compliance

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 104 | **EU AI Act** | The world's first comprehensive AI regulation, entered into force August 2024. Classifies AI systems by risk level (unacceptable, high, limited, minimal). Full application in August 2026, with penalties up to 35M EUR or 7% of global turnover. | Governance |
| 105 | **AI Governance** | The frameworks, policies, processes, and controls organizations put in place to manage AI systems responsibly -- covering risk, ethics, compliance, and accountability. Despite 90% of enterprises using AI, only 18% have fully implemented governance frameworks as of 2025. | Governance |
| 106 | **Responsible AI** | A set of principles and practices ensuring AI systems are developed and deployed ethically, including fairness, transparency, accountability, privacy, and safety. | Governance |
| 107 | **AI Bias** | Systematic errors in AI outputs that reflect and often amplify societal prejudices present in training data, leading to unfair treatment of certain groups. Requires regular bias testing throughout the AI lifecycle. | Governance |
| 108 | **Fairness** | The principle that AI systems should produce equitable outcomes across different demographic groups. Requires establishing context-appropriate fairness definitions and implementing regular testing. | Governance |
| 109 | **Transparency** | The principle that AI systems should be open about their capabilities, limitations, and decision-making processes. The EU AI Act introduces specific disclosure obligations to preserve trust. | Governance |
| 110 | **Accountability** | The principle that there should be clear responsibility for AI system outcomes, including mechanisms for redress when AI causes harm. | Governance |
| 111 | **AI Literacy** | The knowledge and skills needed to understand, use, and critically evaluate AI systems. The EU AI Act mandates AI literacy obligations for deployers of AI systems, applicable from February 2025. | Governance |
| 112 | **ISO/IEC 42001** | The international standard providing a certifiable framework for AI Management Systems, establishing requirements for responsible AI governance within organizations. | Governance |
| 113 | **NIST AI RMF (AI Risk Management Framework)** | The U.S. National Institute of Standards and Technology's framework for managing AI risks, organized around four functions: Govern, Map, Measure, and Manage. | Governance |

---

## 12. Generative AI & Multimodal

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 114 | **Generative AI (GenAI)** | AI systems that create new content -- text, images, audio, video, code, 3D models -- rather than just analyzing or classifying existing data. The category encompasses LLMs, diffusion models, and other generative architectures. | Generative AI |
| 115 | **Multimodal AI** | AI systems that can process, understand, and generate content across multiple data types (modalities) -- text, images, audio, video -- within a single unified model. 2025 saw multimodal supremacy become a major battleground. | Generative AI |
| 116 | **Text-to-Image** | The capability of generating images from natural language descriptions. Powered by diffusion models (DALL-E 3, Midjourney, Stable Diffusion) that learned to associate textual descriptions with visual features. | Generative AI |
| 117 | **Text-to-Video** | AI generation of video content from text prompts. A rapidly advancing frontier with models like Sora (OpenAI), Runway Gen-3, and Kling producing increasingly realistic results. | Generative AI |
| 118 | **Text-to-Speech (TTS)** | AI systems that convert written text into natural-sounding spoken audio, with modern models producing nearly indistinguishable-from-human speech with emotional range and multiple voice styles. | Generative AI |
| 119 | **Speech-to-Text (STT) / ASR** | Automatic speech recognition systems that transcribe spoken audio into text. Modern models like Whisper handle multiple languages, accents, and noisy environments with high accuracy. | Generative AI |
| 120 | **Image-to-Text** | AI systems that generate textual descriptions, captions, or structured data from images. Includes OCR, image captioning, visual question answering, and document understanding. | Generative AI |
| 121 | **Latent Space** | The compressed, abstract representation space that generative models (VAEs, diffusion models) learn internally. Manipulating points in latent space allows controlled generation, interpolation between concepts, and style transfer. | Generative AI |

---

## 13. AI Infrastructure & Deployment

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 122 | **Inference** | The process of using a trained model to generate predictions or outputs from new inputs. Distinct from training. Inference workloads are projected to account for two-thirds of all AI compute by 2026. | Infrastructure |
| 123 | **Training Compute** | The computational resources (measured in FLOPs) required to train a model. Frontier models now require 10^26+ FLOPs. Training costs remain high but are a one-time investment per model version. | Infrastructure |
| 124 | **GPU (Graphics Processing Unit)** | The primary hardware for AI training and inference. NVIDIA's A100 and H100 GPUs dominate the market. GPUs excel at parallel matrix operations fundamental to neural networks. | Infrastructure |
| 125 | **TPU (Tensor Processing Unit)** | Google's custom AI accelerator, designed specifically for tensor operations in neural networks. Optimized for large-batch workloads but less suited for low-latency single-request inference. | Infrastructure |
| 126 | **NPU (Neural Processing Unit)** | Purpose-built AI accelerators designed for edge devices (phones, laptops, IoT) with stringent power budgets. Increasingly found in consumer hardware for on-device AI. Uses architectures mimicking biological neural networks. | Infrastructure |
| 127 | **Edge AI** | Running AI models directly on edge devices (phones, sensors, embedded systems) rather than in the cloud, enabling lower latency, better privacy, and offline operation. Enabled by model compression and NPUs. | Infrastructure |
| 128 | **Model Serving** | The infrastructure and systems for deploying trained models to handle real-time inference requests at scale. Involves load balancing, batching, caching, scaling, and monitoring. Frameworks: vLLM, TensorRT-LLM, Triton. | Infrastructure |
| 129 | **Quantization** | Reducing the numerical precision of model weights and activations (e.g., from 32-bit floating point to 8-bit or 4-bit integers) to shrink model size and accelerate inference. Achieves ~75% size reduction with less than 1% accuracy loss. | Infrastructure |
| 130 | **Pruning** | Removing unnecessary weights, neurons, or entire layers from a neural network to reduce its size and computational requirements while maintaining acceptable performance. Can be combined with quantization and distillation. | Infrastructure |
| 131 | **Model Compression** | The umbrella term for techniques (quantization, pruning, distillation, weight sharing) that reduce model size and computational requirements for more efficient deployment. Can reduce infrastructure needs by up to 90%. | Infrastructure |
| 132 | **Federated Learning** | A distributed training approach where models are trained across multiple decentralized devices or servers holding local data, without exchanging raw data. Preserves data privacy by only sharing model updates, not the underlying data. | Infrastructure |
| 133 | **AIOps** | The practice of using AI, machine learning, and big data analytics to automate and improve IT operations -- including monitoring, incident detection, root cause analysis, and capacity planning. | Infrastructure |

---

## 14. Inference Optimization

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 134 | **Speculative Decoding** | An inference acceleration technique where a smaller, faster "draft" model generates multiple candidate tokens in parallel, which the larger "verifier" model then checks and accepts or rejects. Can speed up inference 2-3x with no quality loss. | Optimization |
| 135 | **Flash Attention** | A memory-efficient attention algorithm that reduces the memory footprint and improves the speed of attention computation by tiling the attention matrix and avoiding materializing the full attention matrix in GPU memory. | Optimization |
| 136 | **Sparse Attention** | Attention mechanisms that only attend to a subset of tokens rather than all tokens, breaking the quadratic computational cost of full attention. Approaches include sliding window, block-sparse, and content-dependent sparsity. | Optimization |
| 137 | **Paged Attention** | An attention management technique (introduced by vLLM) inspired by OS virtual memory paging, which dynamically allocates GPU memory for KV cache in non-contiguous blocks, dramatically improving memory utilization and throughput for serving. | Optimization |
| 138 | **Continuous Batching** | A serving optimization where new inference requests are added to running batches dynamically (rather than waiting for fixed batches to complete), maximizing GPU utilization and reducing wait times. | Optimization |
| 139 | **Test-Time Compute / Inference-Time Scaling** | The paradigm of improving model performance by spending more compute during inference (e.g., longer chain-of-thought reasoning, multiple samples, verification loops) rather than only during training. Shown to follow scaling laws analogous to training compute. | Optimization |
| 140 | **Constrained Decoding** | A technique that restricts which tokens the model can generate at each step based on a predefined schema or grammar, ensuring outputs conform to required formats (JSON, XML, code syntax) without post-processing. | Optimization |

---

## 15. AI Coding & Development

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 141 | **Vibe Coding** | A term coined by Andrej Karpathy in February 2025 describing a radically hands-off development approach where programmers guide AI through natural language conversation, focusing on high-level intent while trusting AI to handle implementation details. Collins Dictionary's word of the year 2025. | AI Coding |
| 142 | **AI Code Generation** | The use of LLMs to automatically write, complete, refactor, debug, and document source code from natural language descriptions or partial code context. 65% of developers use AI coding tools at least weekly (Stack Overflow 2025 Survey). | AI Coding |
| 143 | **AI Coding Assistant / Copilot** | IDE-integrated tools that provide real-time code suggestions, completions, explanations, and generation as developers write code. Examples: GitHub Copilot, Cursor, JetBrains AI, Tabnine, Amazon Q, Gemini Code Assist. | AI Coding |
| 144 | **Agentic Coding CLI** | Command-line AI coding tools that can autonomously plan and execute multi-step coding tasks across entire repositories -- editing files, running tests, debugging, and iterating. Represents the evolution beyond IDE chatbots. Examples: Claude Code, Aider, Goose. | AI Coding |
| 145 | **AI Coding Agent** | Autonomous AI systems that can take a high-level specification and independently plan, write, test, debug, and deploy code with minimal human guidance. Examples: Devin, Cursor Agent, Claude Code. | AI Coding |
| 146 | **Repository Intelligence** | AI that understands not just individual lines of code but the relationships, patterns, architecture, and history across an entire codebase, enabling more contextual and accurate code suggestions and refactoring. | AI Coding |

---

## 16. Performance Metrics & Evaluation

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 147 | **TTFT (Time to First Token)** | The latency from when an inference request is submitted until the first output token is generated. Includes queuing, prompt processing (prefill), and network latency. A sub-500ms TTFT is crucial for real-time conversational AI. | Metrics |
| 148 | **TPS (Tokens Per Second)** | The rate at which a model generates output tokens, measuring generation speed. Higher TPS means faster response completion. Also called inter-token throughput. | Metrics |
| 149 | **Throughput** | The total number of requests or tokens a serving system can process per unit of time. Distinct from latency -- systems optimize for one or the other depending on use case (batch processing vs. real-time). | Metrics |
| 150 | **Latency** | The time delay between sending a request and receiving the complete response. Critical for real-time applications. Inference costs have dropped from $20 to $0.07 per million tokens (Stanford AI Index 2025). | Metrics |
| 151 | **Perplexity** | A standard metric for evaluating language models, measuring how well the model predicts a sample of text. Lower perplexity indicates the model is less "surprised" by the text and better at modeling the language. | Metrics |
| 152 | **Benchmark** | A standardized test or dataset used to evaluate and compare AI model capabilities across specific tasks (e.g., MMLU for knowledge, HumanEval for coding, GSM8K for math). Subject to contamination risks and gaming. | Metrics |

---

## 17. Emerging & 2025-2026 Terminology

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 153 | **AI Slop** | Low-quality, mass-produced content generated by AI, often containing errors and not requested by the user. Used broadly as a suffix to describe anything lacking substance: "work slop," "friend slop." Popularized throughout 2025. | Emerging |
| 154 | **Model Collapse** | A degenerative process where AI models trained on AI-generated data progressively lose diversity and accuracy -- rare events vanish, outputs drift toward bland averages with weird outliers. A growing risk as synthetic content dominates the web. | Emerging |
| 155 | **Context Engineering** | The emerging software engineering discipline focused on systematically managing all context supplied to LLMs -- prompts, retrieved documents, tool definitions, metadata, conversation history -- to optimize model performance in production. Recognized as distinct from casual prompting in 2025. | Emerging |
| 156 | **World Model** | A simulated internal representation of an environment that enables AI agents to predict outcomes of actions and plan before acting. Showing potential in robotics, reinforcement learning, and generative video (e.g., Sora may use world model-like reasoning). | Emerging |
| 157 | **JEPA (Joint-Embedding Predictive Architecture)** | An architecture (proposed by Yann LeCun) that predicts abstract representations of inputs rather than pixel-level reconstructions, potentially enabling more robust and efficient learning. V-JEPA extends this to video understanding. | Emerging |
| 158 | **Objective-Validation Protocol** | An emerging development paradigm beyond vibe coding, where users define goals and validation criteria while collections of agents autonomously execute implementation, requesting human approval only at critical checkpoints. | Emerging |
| 159 | **AI Recommendation Poisoning** | A 2025-2026 attack vector identified by Microsoft where adversaries manipulate AI recommendation systems' underlying data to influence outputs for profit, brand manipulation, or disinformation. | Emerging |
| 160 | **Long Context Models** | Models designed to handle extremely long input sequences (100K to 1M+ tokens) in a single pass, enabling processing of entire codebases, books, or document collections without chunking. Examples: Claude (200K), Gemini (1M+), Jamba (256K). | Emerging |
| 161 | **Emergent Behavior** | Unpredictable capabilities that arise in large AI models that were not explicitly trained for, appearing only above certain scale thresholds. Examples include in-context learning, chain-of-thought reasoning, and multilingual abilities not present in smaller models. | Emerging |
| 162 | **Agentic AI Foundation (AAIF)** | A Linux Foundation project (formed December 2025) to steward open agentic AI standards and projects, including MCP, Goose, and AGENTS.md. Backed by major AI companies for cross-platform interoperability. | Emerging |
| 163 | **Quantum AI** | The nascent field combining quantum computing with AI/ML, exploring quantum speedups for optimization, sampling, and training. Still largely experimental but with growing research investment and early quantum-assisted optimization experiments. | Emerging |
| 164 | **Scientific AI / AI for Science** | The use of AI to accelerate scientific discovery -- generating hypotheses, designing experiments, analyzing results, and collaborating with human researchers across physics, chemistry, biology, and materials science. Expected to be a major 2026 trend. | Emerging |
| 165 | **Efficiency Frontier** | A 2026 concept describing models that achieve flagship-level reasoning with streamlined architectures, prioritizing performance-per-compute over raw scale. Represents the shift from "bigger is better" to "smarter is better." | Emerging |

---

## 18. AI in the Software Development Lifecycle (AI-DLC)

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 166 | **SDLC (Software Development Life Cycle)** | The structured process for planning, creating, testing, deploying, and maintaining software. Traditional phases include requirements, design, implementation, testing, deployment, and maintenance. AI is now being embedded at every stage. | AI-DLC |
| 167 | **AI-DLC (AI Development Life Cycle)** | An evolution of the traditional SDLC where AI tools are embedded at every stage of software delivery -- from requirements analysis and code generation to testing, code review, and deployment. Represents a shift from AI as a bolt-on tool to AI as an integral part of the workflow. | AI-DLC |
| 168 | **AI-Assisted Development** | A development approach where AI tools augment human developers throughout the coding process -- suggesting code, generating tests, reviewing merge requests, and explaining codebases -- while humans retain full decision-making authority and accountability. | AI-DLC |
| 169 | **AI Engineering Playbook** | A documented, living guide that codifies how an engineering team uses AI across their SDLC. Includes prompt templates per stage, verification checklists, guardrails, dos and don'ts, and real examples. Designed to be iterated on as the team learns. | AI-DLC |
| 170 | **Verification Checklist** | A structured list of checks that a developer must perform after accepting AI-generated output before committing it. Covers correctness, security, adherence to coding standards, test coverage, and domain-specific constraints. A human accountability mechanism. | AI-DLC |
| 171 | **Security Guardrails (AI Context)** | Non-negotiable rules defining what data, code, and context must never be sent to AI systems. In fintech, this typically includes PII, payment processing logic, secrets, API keys, and authentication tokens. Distinct from model-level guardrails. | AI-DLC |
| 172 | **AI Touchpoint** | A specific point in the development workflow where AI tools are systematically applied -- e.g., ticket kick-off (requirements generation), implementation (code assistance), pre-commit (spec generation), merge request (automated review). Mapping AI touchpoints to workflow stages is a key adoption practice. | AI-DLC |
| 173 | **AI-Assisted MR / PR** | A merge request (or pull request) where AI tools contributed to any part of the work -- code generation, test writing, review comments, or documentation. Typically tracked with a label (e.g., `ai-assisted`) for adoption metrics and compliance. | AI-DLC |
| 174 | **Spec Agent** | A domain-specific AI agent that takes a class, module, or function as input and generates a test specification (e.g., RSpec, Vitest) with meaningful contexts, edge cases, and assertions. The generated specs serve as a starting point that developers review and refine. | AI-DLC |
| 175 | **PR Review Agent** | An AI agent that analyses merge request diffs and produces structured review feedback covering code style, test coverage gaps, security concerns, and potential bugs. Can run as a CI step on every MR for automated first-pass review. | AI-DLC |
| 176 | **Requirements Agent** | An AI agent that takes a ticket description (e.g., from Jira) and generates structured acceptance criteria in Given/When/Then format, helping bridge the gap between product intent and engineering specification. | AI-DLC |
| 177 | **Codebase Explainer Agent** | An AI agent that answers natural-language questions about a codebase by reading source code and structured documentation (like `AI_CONTEXT.md`). Designed to break knowledge silos by enabling any developer to understand any part of the system without finding the domain expert. | AI-DLC |
| 178 | **Component Spec Agent** | The frontend equivalent of a Spec Agent -- takes a component name or design description and generates Storybook stories with meaningful variants and interaction tests (play functions). Enables story-first development. | AI-DLC |
| 179 | **Story-First Development** | A frontend development practice where Storybook stories (component specifications with variants and interaction tests) are generated before writing implementation code. AI agents generate the stories from design specs or Jira tickets, and the stories become the living spec. | AI-DLC |
| 180 | **Prompt Library** | A curated, shared collection of reusable prompts optimised for specific development tasks within a team's codebase and workflow. Evolves through team usage and is typically maintained per squad or domain. | AI-DLC |
| 181 | **Hard Problems Session** | A structured team meeting where developers bring AI prompts that didn't work, outputs they couldn't trust, or integration challenges they couldn't solve alone. The group problem-solves together, improving collective AI fluency and feeding learnings back into the playbook. | AI-DLC |

---

## 19. AI Code Attribution & Compliance

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 182 | **AI Code Attribution** | The practice of tracking which lines of code in a repository were written by AI vs. humans, including metadata about which model was used, who authored the prompt, and the conversation context. Essential for audit trails in regulated industries. | Attribution |
| 183 | **git-ai** | A tool that configures git hooks to mark AI contributions as AI-generated at the line level, preserving attribution across merges, rebases, cherry-picks, squashes, and resets. Works offline with no background daemons -- agents explicitly mark inserted hunks, avoiding heuristic detection. | Attribution |
| 184 | **Agent Trace** | An open specification released by Cursor (January 2026) that records AI and human contributions in a vendor-neutral JSON format within version-controlled codebases. Compatible with git-ai and designed to prevent vendor lock-in for AI code attribution. | Attribution |
| 185 | **AI Code Attribution Layers** | A four-layer model for tracking AI-generated code: (1) git-level attribution (line-by-line), (2) MR-level signal (labels and checklists), (3) CI pipeline gates (automated compliance checks), and (4) dashboard and compliance reporting (aggregated metrics for audit). | Attribution |
| 186 | **Human-Review Required Flag** | A CI/CD gate that flags merge requests where AI-generated code touches critical paths (e.g., payment processing, authentication, database migrations, PII handling) and requires explicit human sign-off before merge. | Attribution |
| 187 | **AI Compliance Dashboard** | A reporting interface that aggregates AI code attribution data across teams -- showing percentage of AI-generated lines per squad, AI-assisted MR rate over time, and which guardrail-protected files have had AI touches. The audit trail for regulators and compliance officers. | Attribution |
| 188 | **Co-Authored-By (AI)** | A git commit convention (e.g., `Co-Authored-By: Claude <noreply@anthropic.com>`) used to signal that an AI contributed to the commit. A lightweight, human-readable attribution mechanism that works with existing git tooling. | Attribution |

---

## 20. AI-Assisted Team Practices

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 189 | **AI Ambassador** | A designated team member (typically one per squad) who leads AI adoption within their group -- facilitating labs, unblocking setup issues, maintaining the squad prompt library, onboarding new joiners, and running regular AI retrospectives. A peer leader, not a manager. | Team Practices |
| 190 | **AI Ambassador Charter** | A formal agreement defining the responsibilities, cadence, and authority of AI ambassadors within an organisation. Typically includes monthly retros, prompt library maintenance, new-joiner onboarding, and a mechanism for proposing new agents or playbook updates. | Team Practices |
| 191 | **AI_CONTEXT.md** | A structured documentation file placed at the root of each engine, service, or module in a codebase. Describes purpose, public API, integration contracts, data models, events, dependencies, and known gotchas in a machine-readable format. Serves as the primary input to Codebase Explainer Agents and as a living contract between teams. | Team Practices |
| 192 | **COMPONENT_CONTEXT.md** | The frontend equivalent of `AI_CONTEXT.md` -- documents a component's props, variants, events, design tokens, accessibility notes, integration examples, and known limitations. Primary input to Component Explainer Agents. | Team Practices |
| 193 | **Cross-Squad Knowledge Sharing** | The practice of using AI agents (particularly Codebase Explainer Agents) and structured documentation (AI_CONTEXT.md) to enable developers from one team to understand and safely contribute to another team's domain without needing synchronous knowledge transfer from domain experts. | Team Practices |
| 194 | **AI Upskilling Program** | A structured, time-boxed training initiative (typically 1-2 weeks) to build AI fluency across an engineering organisation. Typically follows a train-the-trainer model: a pilot cohort builds the toolkit and playbook, then ambassadors scale it to the full team. | Team Practices |
| 195 | **Kanban + AI-DLC** | A delivery methodology combining continuous-flow Kanban (replacing batch-oriented Scrum sprints) with AI-embedded development practices. AI tools reduce cycle time and enable smaller, more frequent deliveries, making Kanban's continuous flow practical for complex systems. | Team Practices |
| 196 | **AI-DLC Metrics Baseline** | The initial measurement of key development metrics (cycle time, MR review time, test generation speed, AI-assisted MR rate, prompt reuse rate) before AI tool adoption, used as a benchmark to quantify productivity impact over time. | Team Practices |
| 197 | **AI-Assisted Pairing** | A development practice where an AI ambassador or experienced practitioner pairs with another developer, teaching them how to use AI tools effectively on real work. Combines traditional pair programming with AI tool coaching. | Team Practices |
| 198 | **Extreme Delivery** | A software delivery philosophy focused on minimising the time between idea and production. Combines continuous deployment, Kanban flow, automated testing, and AI-assisted development to achieve rapid, sustainable delivery cycles. | Team Practices |
| 199 | **Agent Inventory** | A catalogued list of AI agents available to a development team, with each agent's purpose, inputs, outputs, and usage guidelines documented. Versioned and maintained alongside the engineering playbook. | Team Practices |
| 200 | **Glazing** | AI-generated text that is excessively complimentary, sycophantic, or lacking critical substance. Originally internet slang, adopted in 2025 to describe AI outputs that agree with everything without adding value. Recognised alongside "slop" as a characteristic AI failure mode. | Team Practices |

---

## 21. Claude Code & Agent SDK

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 201 | **Claude Code** | Anthropic's terminal-based AI coding agent (launched February 2025). Reads your codebase, edits files, runs shell commands, and executes multi-step workflows directly from the command line. Available as CLI, desktop app, web app (claude.ai/code), and IDE extensions (VS Code, JetBrains). | Claude Code |
| 202 | **CLAUDE.md** | A markdown file placed at a project root (or in `~/.claude/`) that provides persistent instructions to Claude Code across sessions. Functions like a README for the AI -- defining coding standards, architecture notes, and behavioral rules. Supports project-level, user-level, and directory-level scoping. | Claude Code |
| 203 | **Skills (SKILL.md)** | Markdown-based guides that teach Claude Code how to handle specific tasks. Instead of pasting the same prompt repeatedly, you write a skill once and invoke it via a slash command (e.g., `/review-component`). Published as an open standard at agentskills.io (December 2025). | Claude Code |
| 204 | **Slash Commands** | User-triggered, repeatable prompt shortcuts in Claude Code. Custom commands (e.g., `/fix-lint`, `/write-test`) expand into full prompts. Serve as quick entry points to common workflows without retyping instructions. | Claude Code |
| 205 | **Hooks** | User-defined shell commands that execute automatically at specific lifecycle events in Claude Code -- similar to Git hooks, but for the AI agent. Events include `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `Notification`, `SessionStart`, `UserPromptSubmit`, and `PermissionRequest`. Example uses: auto-lint every file Claude writes, block dangerous commands, send Slack notifications when Claude finishes. | Claude Code |
| 206 | **Harness** | The execution runtime and coordination layer that wraps the Claude model in Claude Code. It manages the agent loop, tool dispatch, permission checks, context window, hooks, and session state. When you configure hooks or permissions, you are configuring the harness, not the model itself. | Claude Code |
| 207 | **Subagents** | Specialised, ephemeral Claude instances that Claude Code spawns to handle specific tasks in isolation. Each subagent gets a fresh context window, works on one task, and returns a summary to the parent agent. Types include Explore (codebase search), Plan (architecture), and general-purpose agents. | Claude Code |
| 208 | **Agent Teams** | Multiple independent Claude Code sessions that coordinate, message each other, and divide work in parallel (launched February 2026). Unlike subagents (isolated workers reporting to a parent), Agent Teams are a collaborative squad where agents communicate directly. | Claude Code |
| 209 | **Plan Mode** | A permission mode in Claude Code that restricts the agent to read-only operations. Claude can analyse code, explore the codebase, and create plans, but cannot make any modifications or execute tools. Activated via Shift+Tab cycling. | Claude Code |
| 210 | **Auto-Accept Mode** | A permission mode that eliminates confirmation prompts for file edits, enabling uninterrupted execution. The developer can still observe and intervene. Activated via Shift+Tab. | Claude Code |
| 211 | **Normal Mode** | The default Claude Code permission mode that prompts for every potentially dangerous operation (file writes, shell commands, etc.). | Claude Code |
| 212 | **Bypass Mode (YOLO Mode)** | The `--dangerously-skip-permissions` flag that skips all permission checks. Claude executes any tool without prompting. Intended only for fully isolated environments (containers, VMs, ephemeral CI runners). | Claude Code |
| 213 | **Headless Mode (--print / -p)** | Running Claude Code non-interactively by passing `-p` with a prompt. Output is collected at once rather than streamed interactively, making it suitable for CI pipelines, background jobs, and programmatic integration. | Claude Code |
| 214 | **Conversation Compaction (/compact)** | When context approaches capacity (~95% full), Claude Code summarises the conversation history and replaces it with a compressed summary, effectively extending the session indefinitely. Can be triggered manually with `/compact` or happens automatically. Unlike `/clear`, which wipes history, `/compact` preserves context as a summary. | Claude Code |
| 215 | **Extended Thinking** | A mode where Claude produces detailed internal reasoning (thinking blocks) before responding. Thinking blocks are automatically stripped from context on subsequent turns to preserve token capacity. Enables deeper analysis of complex problems. | Claude Code |
| 216 | **Worktree (Git Worktree Strategy)** | Using Git worktrees to isolate parallel Claude Code sessions. Each session operates on a distinct directory/branch, eliminating file conflicts when running multiple agents simultaneously on the same repo. | Claude Code |
| 217 | **Background Agents** | Claude Code instances that run asynchronously without requiring real-time interaction -- triggered from GitHub Issues, CI pipelines, or scheduled tasks. They clone a repo, work on a branch, and push changes when done. | Claude Code |
| 218 | **Claude Agent SDK** | A library (Python and TypeScript) that lets you embed Claude Code's agent loop, tools, and context management into your own applications. Formerly "Claude Code SDK", renamed late 2025. Provides built-in file operations, shell commands, web search, MCP integration, hooks, and subagent support. | Anthropic |
| 219 | **Claude Code GitHub Actions** | A GitHub Action built on the Claude Agent SDK that runs Claude Code within CI/CD workflows. Enables automated PR creation, code implementation, and review directly on GitHub's runners. | Anthropic |
| 220 | **Permission Rules** | Claude Code evaluates permission rules in priority order: deny, then ask, then allow. The first matching rule wins, and deny rules always take precedence. Configured in settings or via `/permissions`. | Claude Code |
| 221 | **Allowed Tools (--allowedTools)** | A CLI flag or configuration that pre-approves specific tools so Claude can use them without prompting for permission. Uses permission rule syntax with glob patterns. | Claude Code |
| 222 | **Plugins** | Self-contained directories of components (skills, agents, hooks, MCP servers, LSP servers) that extend Claude Code with custom functionality. Introduced October 2025. | Claude Code |
| 223 | **Context Window** | The maximum number of tokens Claude can consider at once. Claude Opus 4.6 and Sonnet 4.6 have a 1M-token context window (GA March 2026). A ~33,000-token buffer is reserved, leaving roughly 967K usable tokens. When nearing capacity, auto-compaction kicks in. | Claude Code |

---

## 22. Cursor, Copilot & AI Coding Tools

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 224 | **Cursor** | An AI-native IDE built on VS Code with deep Claude and GPT integration. Features include Cursor Tab (inline completion), Composer (multi-file editing), Agent Mode (autonomous coding), codebase indexing, and Background Agents. Acquired features and integrations make it a leading agentic coding tool. | Cursor |
| 225 | **Cursor Tab** | Cursor's predictive code completion engine. Goes beyond next-word suggestions -- it predicts cursor movement and multi-line edits based on recent changes, using a specialised model for speed. | Cursor |
| 226 | **Cursor Composer** | Cursor's coding model designed for building software inside the editor. Targets agentic workflows and large codebases, aiming to complete most turns in under 30 seconds. Introduced with Cursor 2.0 (October 2025). | Cursor |
| 227 | **Cursor Agent Mode** | The autonomous mode in Cursor where you give a high-level goal (e.g., "Build a user registration page") and Cursor determines which files to create/edit, runs commands, and iterates independently. Contrast with Chat Mode (conversational Q&A). | Cursor |
| 228 | **.cursorrules** | A file placed in a project's root directory that gives Cursor standing instructions -- coding styles, preferred libraries, architectural patterns. Keeps the AI's output consistent with team standards. Analogous to CLAUDE.md for Claude Code. | Cursor |
| 229 | **Codebase Indexing** | Computing embeddings (vector representations) for files in a project, enabling semantic search that understands meaning rather than matching exact text. Used by Cursor, Copilot, and others to find relevant context for AI responses. Requires periodic re-indexing. | Cross-tool |
| 230 | **BugBot / Autofix** | Cursor's automated PR reviewer. Scans pull requests, catches potential bugs, and leaves comments on GitHub. As of February 2026, graduated to "Autofix" -- when it finds a problem, it spins up a cloud agent, tests a fix, and proposes it directly on the PR. Over 35% of suggestions are merged. | Cursor |
| 231 | **GitHub Copilot** | GitHub/Microsoft's AI coding assistant, deeply embedded in VS Code and JetBrains IDEs. Provides inline completions, chat, and agent mode. The most widely adopted AI coding tool in enterprise settings. | GitHub |
| 232 | **copilot-instructions.md** | A file at `.github/copilot-instructions.md` that VS Code automatically detects and applies to all Copilot chat requests within that workspace. Provides project-specific instructions to Copilot. | GitHub Copilot |
| 233 | **Copilot Coding Agent** | GitHub Copilot's autonomous background agent that works independently to complete tasks assigned via GitHub Issues, PRs, or the Agents tab. Can be assigned work from github.com, GitHub Mobile, and VS Code. | GitHub Copilot |
| 234 | **GitHub Agent HQ** | GitHub's multi-agent hub (February 2026) where users can run Claude and OpenAI Codex agents alongside Copilot. Agents are assignable from issues, pull requests, and a dedicated Agents tab. | GitHub |
| 235 | **Windsurf** | An AI-native IDE developed by Codeium, built on a VS Code foundation. Features Cascade (agentic assistant) and Supercomplete (inline completion). Acquired by Cognition AI (makers of Devin) in December 2025. | Windsurf |
| 236 | **Cascade** | Windsurf's agentic AI assistant with tool calling, voice input, checkpoints, and real-time awareness. Tracks all user actions (edits, commands, history, clipboard, terminal) to infer intent and adapt in real time. | Windsurf |
| 237 | **Supercomplete** | Windsurf's advanced inline completion that predicts developer intent rather than just the next token. Inline and suggestion-based -- you stay in editor flow and accept or reject. | Windsurf |
| 238 | **Aider** | An open-source command-line AI pair programming tool that edits code in your local Git repository. Supports multiple LLM providers. Emphasises Git integration with automatic commits and the ability to review/undo changes. | Aider |
| 239 | **Repository Map** | A condensed map of the entire codebase that Aider builds before each request, showing file names, class definitions, function signatures, and import relationships. Helps the LLM understand project structure. | Aider |
| 240 | **Edit Format (Search/Replace)** | The method Aider uses to let LLMs modify source files. Outputs a SEARCH block with existing code and a REPLACE block with modifications. More token-efficient than sending whole files. Also used by Claude Code's Edit tool. | Cross-tool |
| 241 | **Devin** | An autonomous AI software engineer by Cognition that handles the full development lifecycle -- writing code, creating tests, debugging, and iterating until solutions work. Takes high-level requirements and delivers working software. | Cognition |
| 242 | **Cline** | A fully open-source, local-first VS Code extension that functions as an agentic coding assistant. Can create files, run terminal commands, manage multi-step tasks. Works within your existing VS Code setup. | Open source |
| 243 | **OpenAI Codex CLI** | OpenAI's terminal-based coding agent, competing with Claude Code. Available as a coding agent on GitHub alongside Claude. | OpenAI |
| 244 | **Prompt/Instruction Files** | Project-level configuration files that guide AI behaviour. Examples: `.cursorrules` (Cursor), `CLAUDE.md` (Claude Code), `.github/copilot-instructions.md` (Copilot), `AGENTS.md` (cross-tool). Encode coding standards, architecture decisions, and behavioural rules. | Cross-tool |
| 245 | **Checkpoints** | Snapshots of workspace state that an AI agent creates before making changes, allowing developers to roll back to a known-good state if the agent's modifications go wrong. Used by Windsurf Cascade and other agentic tools. | Cross-tool |

---

## 23. MCP Ecosystem (Deep Dive)

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 246 | **MCP Host** | The AI-enabled application that integrates and runs the MCP system. The host embeds MCP clients and acts as the user-facing interface. Examples: Claude Desktop, Claude Code, Cursor, VS Code, Raycast. | MCP |
| 247 | **MCP Client** | The communication layer within the host application. Receives structured tool definitions from servers and forwards tool calls from the model to the correct server implementations. Each host can run multiple client instances. | MCP |
| 248 | **MCP Server** | A lightweight program that exposes specific capabilities (tools, resources, prompts) via MCP primitives. Servers operate independently with focused responsibilities. Examples: a GitHub MCP server, a database MCP server, a browser automation MCP server. | MCP |
| 249 | **MCP Tools** | Executable functions that an MCP server exposes for the LLM to invoke. They represent arbitrary code execution (e.g., "create a GitHub PR", "run a database query") and must be treated with appropriate caution. The LLM decides when and how to call them. | MCP |
| 250 | **MCP Resources** | Structured data or content that MCP servers expose to clients -- textual documents, database entries, file contents, images, system logs, real-time data streams. Unlike tools, resources are data the model reads rather than actions it executes. | MCP |
| 251 | **MCP Prompts** | Reusable templates and workflows for LLM-server communication, defined by MCP servers. They provide pre-built interaction patterns that clients can present to users or invoke programmatically. | MCP |
| 252 | **MCP Sampling** | A capability that allows MCP servers to request the host's LLM to generate text on the server's behalf, enabling agentic multi-step interactions where servers can reason and make decisions. | MCP |
| 253 | **Streamable HTTP (MCP Transport)** | The transport mechanism introduced March 2025, replacing Server-Sent Events (SSE). Unifies bidirectional communication over a single HTTP endpoint (`/mcp`), supports chunked transfer encoding, progressive message delivery, and session resumability via `Mcp-Session-Id`. | MCP |
| 254 | **stdio Transport** | The original MCP transport for local communication where the host spawns the MCP server as a subprocess and communicates via standard input/output. Simple but limited to local processes. | MCP |
| 255 | **Tool Annotations** | Metadata on MCP tools (introduced March 2025) including `readOnly` and `destructive` flags. They programmatically trigger human-in-the-loop warnings before executing high-stakes actions like database deletions. | MCP |
| 256 | **MCP Registry** | A community-driven registry service for discovering and publishing MCP servers. Entered API freeze (v0.1) October 2025. Supports GitHub OAuth authentication and validates namespace ownership. | MCP |
| 257 | **Remote MCP Servers** | MCP servers hosted on remote infrastructure rather than running locally. Use Streamable HTTP transport and OAuth 2.1 for authentication. The June 2025 spec update separated the MCP server from the authorisation server. | MCP |
| 258 | **MCP OAuth / Authorisation** | The MCP authorisation specification standardises OAuth 2.1 flows for HTTP-based transports. Includes Dynamic Client Registration (RFC 7591), Resource Indicators to prevent token misuse, and enterprise-managed authorisation extensions. | MCP |

---

## 24. Agentic Coding Patterns & Concepts

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 259 | **Agent Loop** | The core execution cycle of an agentic coding tool: receive task, reason about next step, call a tool, observe the result, reason again, repeat until done. Each iteration can involve reading code, writing edits, running tests, or searching. | Agentic Patterns |
| 260 | **Inline Completion** | AI-generated code suggestions that appear directly in the editor as ghost text while typing. The developer accepts (Tab) or dismisses them. The original paradigm established by GitHub Copilot. | Agentic Patterns |
| 261 | **Chat Panel** | A side panel in the IDE where developers ask questions about code, request explanations, or give instructions in natural language. Conversational rather than predictive. | Agentic Patterns |
| 262 | **Agent Mode** | A mode where the AI operates autonomously: it plans steps, reads files, writes code, runs commands, checks results, and iterates -- all from a single high-level instruction. Contrast with Chat Mode (Q&A) and Inline Completion (passive suggestions). | Agentic Patterns |
| 263 | **Diff View** | A visual display showing the before/after of AI-proposed changes, letting developers review exactly what will be modified before accepting. Standard in Cursor, VS Code Copilot, and most AI coding tools. | Agentic Patterns |
| 264 | **Accept/Reject Workflow** | The fundamental interaction pattern in AI-assisted coding: the AI proposes a change (inline completion, diff, or multi-file edit), and the developer accepts or rejects it. Ensures human control over AI output. | Agentic Patterns |
| 265 | **Human-in-the-Loop (HITL)** | A pattern where certain agent actions require explicit human approval before execution. Rule of thumb: if a mistake is reversible, automate; if irreversible (money, compliance, reputation), gate with human review. Implemented via permission modes, tool annotations, and approval prompts. | Agentic Patterns |
| 266 | **Multi-Step Task Execution** | An agent's ability to break a high-level instruction into multiple sequential steps, executing each with appropriate tools, handling errors, and adapting the plan based on intermediate results. | Agentic Patterns |
| 267 | **File Read/Write/Edit Tools** | The built-in tool primitives that let an AI agent interact with the filesystem. Typically includes Read (view file contents), Write (create/overwrite files), Edit (apply targeted string replacements), and Glob/Grep (search for files/content). | Agentic Patterns |
| 268 | **Terminal Execution** | The ability of an AI coding agent to run arbitrary shell commands, observe their output, and use the results to inform next steps. Enables running tests, installing dependencies, checking git status, and interacting with any CLI tool. | Agentic Patterns |
| 269 | **Browser Automation (Computer Use)** | The ability of an AI agent to control a web browser -- navigate pages, fill forms, click buttons, read content -- for testing, scraping, or interacting with web-based tools. Implemented via MCP servers or native capabilities like Anthropic's Computer Use. | Agentic Patterns |
| 270 | **Supervisor Pattern / Reviewer-Developer Loop** | An agentic pattern where one LLM generates output and another evaluates and provides feedback in iterative loops. Example: a Developer agent writes code, a Reviewer agent checks it, and they iterate until quality standards are met. | Agentic Patterns |
| 271 | **Repository Context** | The full set of information an AI coding tool gathers about a codebase -- file structure, dependencies, imports, class hierarchies, function signatures -- to inform its responses. The quality of repository context directly determines AI output quality. | Agentic Patterns |
| 272 | **Semantic Code Search** | Search that uses vector embeddings to find code by meaning rather than exact text matching. When you search for "authentication handler", it finds relevant code even if those exact words do not appear. Powered by codebase indexing. | Agentic Patterns |
| 273 | **Agentic Engineering** | The successor concept to vibe coding (2026 terminology). The discipline of designing systems where AI agents plan, write, test, and ship code under structured human oversight. Emphasises orchestration, guardrails, and production quality rather than casual prompting. | Agentic Patterns |
| 274 | **AI Pair Programming** | Working with an AI assistant as a collaborative partner -- similar to human pair programming but with one developer and one AI. The AI suggests, generates, explains, and reviews while the human guides, decides, and validates. | Agentic Patterns |
| 275 | **AI Code Review** | Automated analysis of pull requests and code changes by AI. Tools like Cursor BugBot, Qodo, and Copilot review PRs for bugs, style violations, security issues, and logic errors. Some tools can also propose and test fixes automatically. | Agentic Patterns |
| 276 | **AI Refactoring** | AI-assisted restructuring of existing code without changing its behaviour. Includes renaming, extracting functions, converting between languages, modernising legacy code, and optimising performance. Typically operates across multiple files. | Agentic Patterns |
| 277 | **AI Test Generation** | The use of AI to automatically create unit tests, integration tests, or end-to-end tests from code, documentation, or natural language descriptions. A core capability of most AI coding assistants. | Agentic Patterns |
| 278 | **Token Budget / Token Limit** | The maximum number of tokens an AI model can process in a single conversation turn or session. Determines how much code, context, and history can fit. As of March 2026, Claude's 1M-token window is the largest generally available. | Agentic Patterns |
| 279 | **Remote Agents / Cloud Agents** | AI coding agents that run on remote cloud infrastructure rather than the developer's local machine. They clone repos, work on branches, and push changes asynchronously. Offered by Cursor (Background Agent), GitHub (Copilot Coding Agent), and others. | Agentic Patterns |
| 280 | **Multi-Agent Development** | The paradigm (formalised February 2026) where multiple AI agents from different providers (Copilot, Claude, Codex) run alongside each other. VS Code's multi-agent hub and GitHub's Agent HQ enable choosing the right agent for each task. | Agentic Patterns |
| 281 | **LSP (Language Server Protocol)** | A standardised protocol for code intelligence (autocomplete, go-to-definition, diagnostics). Claude Code plugins can include LSP servers to provide language-specific intelligence alongside AI capabilities. | Agentic Patterns |

---

## 25. AI Coding Benchmarks

| # | Term | Explanation | Category |
|---|------|-------------|----------|
| 282 | **SWE-bench** | The primary benchmark for evaluating LLMs on real-world software engineering. Given a GitHub codebase and an issue, the model must generate a patch that resolves the problem. Collected from real GitHub repositories. | Benchmarks |
| 283 | **SWE-bench Verified** | A human-validated subset of 500 high-quality SWE-bench test cases (released August 2024). Provides a more reliable evaluation signal by eliminating ambiguous or poorly specified problems. | Benchmarks |
| 284 | **SWE-agent** | An open-source framework (Princeton/Stanford) that wraps an LLM to automatically resolve GitHub issues. Achieves state-of-the-art results on SWE-bench. Provides agent scaffolding (tool interfaces, error handling) around the LLM. | Benchmarks |
| 285 | **Terminal-Bench** | Launched May 2025 (Stanford / Laude Institute). Evaluates whether AI agents can operate inside a real, sandboxed command-line environment, measuring planning, execution, and recovery across multi-step workflows. | Benchmarks |
| 286 | **Cline Bench** | Introduced November 2025. Evaluates agents inside realistic, repository-based development environments by converting real project snapshots and failure cases into reproducible evaluation scenarios. | Benchmarks |
| 287 | **DPAI Arena** | Launched October 2025 by JetBrains. Benchmarks coding agents across multiple languages, evaluating the full engineering lifecycle: patching, test generation, code review, and repository navigation. | Benchmarks |
| 288 | **HumanEval** | An OpenAI benchmark consisting of 164 hand-crafted Python programming problems used to evaluate code generation capabilities. Each problem includes a function signature, docstring, and unit tests. | Benchmarks |
| 289 | **MMLU (Massive Multitask Language Understanding)** | A benchmark testing LLMs across 57 academic subjects (STEM, humanities, social sciences). Used to measure general knowledge and reasoning, not coding-specific. | Benchmarks |

---

## Quick Reference: The 14 AI Terms of 2025 (MIT Technology Review)

The following terms were identified by MIT Technology Review as the defining AI terms of 2025:

1. **Agentic** -- The most pervasive AI buzzword of 2025
2. **Slop** -- Low-quality AI-generated content
3. **Vibe Coding** -- Natural language-driven programming
4. **Reasoning** -- Step-by-step thinking in models like o1 and DeepSeek-R1
5. **Scaling** -- The debate over whether bigger models yield better results
6. **Open-weight** -- Publicly available model weights
7. **Synthetic data** -- AI-generated training data
8. **Model collapse** -- Degradation from training on AI outputs
9. **Context engineering** -- Managing LLM context for production
10. **Guardrails** -- Safety constraints on AI behavior
11. **MCP** -- Model Context Protocol for tool integration
12. **Deepfake** -- AI-generated synthetic media
13. **Hallucination** -- AI fabrication of false information
14. **Superintelligence** -- Hypothetical AI surpassing all human capabilities

---

## Sources

- [LLM Terms Glossary: 50 Words You Should Know (2026 Edition) - Owlbuddy](https://owlbuddy.com/llm-terms-glossary-50-words-you-should-know-2026-edition/)
- [AI Models 2026: Complete Guide to Foundation Models & LLMs](https://www.techaimag.com/foundation-models/ai-models-2026-complete-guide)
- [MCP vs A2A: The Complete Guide to AI Agent Protocols in 2026](https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li)
- [AI Engineering Trends in 2025: Agents, MCP and Vibe Coding](https://thenewstack.io/ai-engineering-trends-in-2025-agents-mcp-and-vibe-coding/)
- [Linux Foundation Announces the Agentic AI Foundation (AAIF)](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [AI Risk & Compliance 2026: Enterprise Governance Overview](https://secureprivacy.ai/blog/ai-risk-compliance-2026)
- [AI Compliance in 2026: Definition, Standards, and Frameworks | Wiz](https://www.wiz.io/academy/ai-security/ai-compliance)
- [The Ultimate Guide to Prompt Engineering in 2026 | Lakera](https://www.lakera.ai/blog/prompt-engineering-guide)
- [The 2026 Guide to Prompt Engineering | IBM](https://www.ibm.com/think/prompt-engineering)
- [From Vibe Coding to Context Engineering: 2025 in Software Development | MIT Technology Review](https://www.technologyreview.com/2025/11/05/1127477/from-vibe-coding-to-context-engineering-2025-in-software-development/)
- [Model Serving Optimization: Quantization, Pruning, Distillation | Introl](https://introl.com/blog/model-serving-optimization-quantization-pruning-distillation-inference)
- [LLM Inference Optimization Techniques | Clarifai](https://www.clarifai.com/blog/llm-inference-optimization/)
- [AI Safety, Alignment, and Interpretability in 2026 | Zylos Research](https://zylos.ai/research/2026-02-09-ai-safety-alignment-interpretability)
- [AI Safety 2026: Constitutional AI and RLHF | Claude 5 Hub](https://www.claude5.com/news/ai-safety-2026-how-constitutional-ai-and-rlhf-shape-responsi)
- [AI Wrapped: The 14 AI Terms You Couldn't Avoid in 2025 | MIT Technology Review](https://www.technologyreview.com/2025/12/25/1130298/ai-wrapped-the-14-ai-terms-you-couldnt-avoid-in-2025/)
- [Slop, Vibe Coding and Glazing: AI Dominates 2025's Words of the Year](https://theconversation.com/slop-vibe-coding-and-glazing-ai-dominates-2025s-words-of-the-year-269688)
- [2025 LLM Year in Review | Karpathy](https://karpathy.bearblog.dev/year-in-review-2025/)
- [The Trends That Will Shape AI in 2026 | IBM](https://www.ibm.com/think/news/ai-tech-trends-predictions-2026)
- [7 Agentic AI Trends to Watch in 2026 | Machine Learning Mastery](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/)
- [Five Trends in AI and Data Science for 2026 | MIT Sloan Management Review](https://sloanreview.mit.edu/article/five-trends-in-ai-and-data-science-for-2026/)
- [What's Next in AI: 7 Trends to Watch in 2026 | Microsoft](https://news.microsoft.com/source/features/ai/whats-next-in-ai-7-trends-to-watch-in-2026/)
- [AI Coding Tools in 2025: Welcome to the Agentic CLI Era | The New Stack](https://thenewstack.io/ai-coding-tools-in-2025-welcome-to-the-agentic-cli-era/)
- [Best AI Coding Agents for 2026 | Faros AI](https://www.faros.ai/blog/best-ai-coding-agents-2026)
- [Vibe Coding Explained | Google Cloud](https://cloud.google.com/discover/what-is-vibe-coding)
- [Tool Calling Explained: The Core of AI Agents (2026 Guide) | Composio](https://composio.dev/content/ai-agent-tool-calling-guide)
- [RAG Infrastructure: Building Production RAG Systems | Introl](https://introl.com/blog/rag-infrastructure-production-retrieval-augmented-generation-guide)
- [The Ultimate RAG Blueprint 2025/2026 | LangWatch](https://langwatch.ai/blog/the-ultimate-rag-blueprint-everything-you-need-to-know-about-rag-in-2025-2026)
- [AI Hallucinations, Data Leaks & Deepfakes: Executive Guide 2026](https://www.drizgroup.com/driz_group_blog/ai-hallucinations-data-leaks-and-deepfakesthe-executives-guide-to-ai-risk-in-2026)
- [Manipulating AI Memory for Profit: AI Recommendation Poisoning | Microsoft](https://www.microsoft.com/en-us/security/blog/2026/02/10/ai-recommendation-poisoning/)
- [LLM Inference Benchmarking | NVIDIA](https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/)
- [Frontier Models Explained | DataCamp](https://www.datacamp.com/blog/frontier-models)
- [The State of Open Source AI Models in 2025 | Red Hat](https://developers.redhat.com/articles/2026/01/07/state-open-source-ai-models-2025)
- [GRPO: Group Relative Policy Optimization | Cameron Wolfe](https://cameronrwolfe.substack.com/p/grpo)
- [Generative AI Glossary | Zendesk](https://www.zendesk.com/blog/generative-ai-glossary/)
- [Top 5 AI Model Optimization Techniques | NVIDIA](https://developer.nvidia.com/blog/top-5-ai-model-optimization-techniques-for-faster-smarter-inference)
