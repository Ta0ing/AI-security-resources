---
name: ai-security-resources
description: Use when the user asks to search, filter, recommend, summarize, or navigate the AI安全资源军火库 / AI security resource arsenal, including AI Agent security, LLM/model security, Prompt injection and jailbreak, AI red teaming, MCP, RAG, AI security communities, courses, papers, or tools.
---

# AI 安全资源军火库

## Overview

Use this skill to query the curated AI 安全资源军火库 converted from `导航页面.html`. The bundled index contains 325 resources across six AI security modules with importance grades, resource types, categories, descriptions, stars/forks, and URLs.

## Core workflow

1. Use `scripts/search_resources.py` first; do not manually scan the JSON unless the script cannot answer the query.
2. Filter narrowly when the user names a module, topic, importance grade, resource type, or category.
3. Return concise recommendations with: resource name, module/category, grade, stars/forks when relevant, why it matches, and URL.
4. Preserve technical terminology: use `Agent`, `LLM`, `Prompt`, `MCP`, `RAG`, `Guardrail`, `Tool Poisoning`, `Skill Poisoning`, and `Bug Bounty`. Do not translate `Agent` as “代理” or `LLM` as “法学硕士”.

## Resources

- `references/resource-index.json` — full machine-readable index extracted from the navigation page.
- `references/resource-summary.md` — module counts, grading rules, and terminology notes.
- `scripts/search_resources.py` — deterministic search/filter/list helper.

## Search examples

```bash
python scripts/search_resources.py --query "MCP Agent" --module M1 --limit 8
python scripts/search_resources.py --query "Prompt 注入" --module M3 --sort stars --limit 10
python scripts/search_resources.py --importance S --json --limit 20
python scripts/search_resources.py --list-categories --module M1
```

## Module guide

| Module | Focus |
|---|---|
| M1 | AI Agent 安全：Agent 框架、运行时、MCP、多 Agent 协同安全 |
| M2 | 大模型安全：后门、模型窃取、训练数据、模型供应链 |
| M3 | Prompt 安全与越狱攻防：Prompt 注入、防御、越狱、对抗 Prompt |
| M4 | AI 驱动安全测试：AI 渗透测试、智能红队、自动化漏洞挖掘 |
| M5 | LLM 应用与部署安全：RAG、API、安全合规治理与风险管控 |
| M6 | AI 安全生态：博客、社区、课程、会议、论文与知识传播 |

## Ranking guidance

Prefer `S` and `A` resources for “核心/最好/推荐” requests. Include `B` resources when the user wants breadth or niche tools. Use `C/D` resources only when they directly match a narrow request or when the user asks for exhaustive coverage.
