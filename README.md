# Claude Code Skills Library

A comprehensive collection of **200+ skills** for Claude Code, combining official Anthropic skills, community contributions, and custom skills for enhanced AI-assisted development workflows.

[![Skills](https://img.shields.io/badge/Skills-200+-brightgreen.svg)](#skill-catalog)
[![Categories](https://img.shields.io/badge/Categories-15+-blue.svg)](#skill-categories)
[![Stacks](https://img.shields.io/badge/Skill%20Stacks-22-orange.svg)](#skill-stacks)

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Skill Sources](#skill-sources)
- [Skill Catalog](#skill-catalog)
  - [Custom Skills (62)](#custom-skills-62-skills)
  - [Anthropic Official (16)](#anthropic-official-skills-16-skills)
  - [obra/superpowers (20)](#obrasuperpowers-skills-20-skills)
  - [Scientific Skills (120+)](#scientific-skills-120-skills)
  - [Community Skills](#community-skills)
- [Skill Stacks](#skill-stacks)
- [How to Use Skills](#how-to-use-skills)
- [Installation](#installation)
- [Resources & Links](#resources--links)
- [Contributing](#contributing)

---

## Overview

This skill library aggregates the best Claude Code skills from multiple sources:

| Source | Count | Description | Link |
|--------|-------|-------------|------|
| **Custom Skills** | 62 | Custom-built skills across 8 categories | Local |
| **Anthropic Official** | 16 | Official skills from Anthropic | [GitHub](https://github.com/anthropics/skills) |
| **obra/superpowers** | 20 | Battle-tested development workflows | [GitHub](https://github.com/obra/superpowers) |
| **Scientific Skills** | 120+ | Scientific computing & bioinformatics | [GitHub](https://github.com/K-Dense-AI/claude-scientific-skills) |
| **Community** | 15+ | Individual community contributions | Various |
| **SkillsMP** | 15,000+ | Marketplace with thousands of skills | [skillsmp.com](https://skillsmp.com) |

---

## Quick Start

### Using This Library

```bash
# Clone the repository
git clone https://github.com/your-username/claude-skills.git

# Copy skills to your Claude Code directory
cp -r claude-skills/.claude/skills ~/.claude/skills
```

### Install from Official Sources

```bash
# Anthropic Official Skills
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills

# obra/superpowers
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace

# Scientific Skills
/plugin marketplace add K-Dense-AI/claude-scientific-skills
```

---

## Skill Sources

### SkillsMP Marketplace
**[skillsmp.com](https://skillsmp.com)** - The largest skill marketplace with 15,000+ skills

Featured skills include:
- `frontend-design` (Anthropic) - Production-grade frontend interfaces
- `creating-financial-models` (Anthropic) - DCF analysis and financial modeling
- `typescript-review` (Metabase) - TypeScript code review
- `payload` (Payload CMS) - Payload CMS development
- `run-nx-generator` (Nx) - Nx monorepo generators

### Official Repositories

| Repository | Description | Install Command |
|------------|-------------|-----------------|
| [anthropics/skills](https://github.com/anthropics/skills) | Official Anthropic skills | `/plugin marketplace add anthropics/skills` |
| [obra/superpowers](https://github.com/obra/superpowers) | Development workflow skills | `/plugin marketplace add obra/superpowers-marketplace` |
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | 120+ scientific skills | `/plugin marketplace add K-Dense-AI/claude-scientific-skills` |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Curated skill list | Reference only |

---

## Skill Catalog

### Custom Skills (62 Skills)

#### AI/ML Development (8 skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| [`rag-builder`](/.claude/skills/ai-ml-development/rag-builder/SKILL.md) | Build RAG pipelines with vector databases | "Build a RAG system for my documentation" |
| [`llm-optimizer`](/.claude/skills/ai-ml-development/llm-optimizer/SKILL.md) | Optimize LLM costs and performance | "Optimize my LLM API costs" |
| [`prompt-engineer`](/.claude/skills/ai-ml-development/prompt-engineer/SKILL.md) | Design effective prompts | "Help me engineer a better prompt" |
| [`model-trainer`](/.claude/skills/ai-ml-development/model-trainer/SKILL.md) | Train and fine-tune models | "Train a classification model" |
| [`chatbot-creator`](/.claude/skills/ai-ml-development/chatbot-creator/SKILL.md) | Build conversational AI | "Create a customer support chatbot" |
| [`mlops-pipeline`](/.claude/skills/ai-ml-development/mlops-pipeline/SKILL.md) | MLOps automation | "Set up ML pipeline with CI/CD" |
| [`vector-db-manager`](/.claude/skills/ai-ml-development/vector-db-manager/SKILL.md) | Manage vector databases | "Configure Pinecone for my app" |
| [`agent-designer`](/.claude/skills/ai-ml-development/agent-designer/SKILL.md) | Design AI agents | "Design a multi-agent system" |

#### Backend & API (8 skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| [`api-designer`](/.claude/skills/backend-api/api-designer/SKILL.md) | Design REST/GraphQL APIs | "Design a REST API for users" |
| [`api-documenter`](/.claude/skills/backend-api/api-documenter/SKILL.md) | Generate API documentation | "Document my API endpoints" |
| [`endpoint-tester`](/.claude/skills/backend-api/endpoint-tester/SKILL.md) | Test API endpoints | "Test my authentication endpoint" |
| [`database-schema`](/.claude/skills/backend-api/database-schema/SKILL.md) | Design database schemas | "Design schema for e-commerce" |
| [`sql-optimizer`](/.claude/skills/backend-api/sql-optimizer/SKILL.md) | Optimize SQL queries | "Optimize this slow query" |
| [`microservices-architect`](/.claude/skills/backend-api/microservices-architect/SKILL.md) | Design microservices | "Architect microservices for payments" |
| [`webhook-creator`](/.claude/skills/backend-api/webhook-creator/SKILL.md) | Create webhook handlers | "Create Stripe webhook handler" |
| [`oauth-implementer`](/.claude/skills/backend-api/oauth-implementer/SKILL.md) | Implement OAuth/auth | "Add OAuth2 to my app" |

#### Business & Communication (13 skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| [`pitch-coach`](/.claude/skills/business-communication/pitch-coach/SKILL.md) | Investor/sales pitches | "Help me pitch to investors" |
| [`meeting-recap`](/.claude/skills/business-communication/meeting-recap/SKILL.md) | Meeting summaries | "Summarize this meeting transcript" |
| [`email-polisher`](/.claude/skills/business-communication/email-polisher/SKILL.md) | Professional emails | "Polish this email draft" |
| [`story-mapper`](/.claude/skills/business-communication/story-mapper/SKILL.md) | User story mapping | "Create user stories for checkout" |
| [`linkedin-post-formatter`](/.claude/skills/business-communication/linkedin-post-formatter/SKILL.md) | LinkedIn post formatting | "Format this for LinkedIn" |
| [`linkedin-post`](/.claude/skills/business-communication/linkedin-post/SKILL.md) | LinkedIn content strategy | "Write a LinkedIn post about AI" |
| [`newsletter`](/.claude/skills/business-communication/newsletter/SKILL.md) | Email newsletters | "Create a product newsletter" |
| [`medium-post`](/.claude/skills/business-communication/medium-post/SKILL.md) | Medium articles | "Write a Medium article" |
| [`video-script`](/.claude/skills/business-communication/video-script/SKILL.md) | Video scripts | "Write a YouTube script" |
| [`decision-journal`](/.claude/skills/business-communication/decision-journal/SKILL.md) | Decision documentation | "Document this decision" |
| [`goal-translator`](/.claude/skills/business-communication/goal-translator/SKILL.md) | Goal to action plans | "Break down Q1 goals into tasks" |
| [`alex-hormozi-pitch`](/.claude/skills/business-communication/alex-hormozi-pitch/SKILL.md) | $100M Offers methodology | "Create an irresistible offer" |
| [`content-trend-researcher`](/.claude/skills/business-communication/content-trend-researcher/SKILL.md) | Content trends | "Research trending topics" |

#### Code Quality (9 skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| [`code-reviewer`](/.claude/skills/code-quality/code-reviewer/SKILL.md) | Code review | "Review this pull request" |
| [`code-refactor`](/.claude/skills/code-quality/code-refactor/SKILL.md) | Refactoring | "Refactor this function" |
| [`code-documenter`](/.claude/skills/code-quality/code-documenter/SKILL.md) | Documentation | "Add JSDoc comments" |
| [`bug-hunter`](/.claude/skills/code-quality/bug-hunter/SKILL.md) | Bug finding | "Find bugs in this code" |
| [`security-auditor`](/.claude/skills/code-quality/security-auditor/SKILL.md) | Security review | "Audit for vulnerabilities" |
| [`test-generator`](/.claude/skills/code-quality/test-generator/SKILL.md) | Test writing | "Generate unit tests" |
| [`test-automation`](/.claude/skills/code-quality/test-automation/SKILL.md) | CI test setup | "Set up automated testing" |
| [`debug-assistant`](/.claude/skills/code-quality/debug-assistant/SKILL.md) | Debugging | "Help debug this error" |
| [`performance-profiler`](/.claude/skills/code-quality/performance-profiler/SKILL.md) | Performance | "Profile this function" |

#### Data Engineering (6 skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| [`data-pipeline`](/.claude/skills/data-engineering/data-pipeline/SKILL.md) | ETL/ELT pipelines | "Build a data pipeline" |
| [`data-validator`](/.claude/skills/data-engineering/data-validator/SKILL.md) | Data validation | "Validate CSV data quality" |
| [`schema-migrator`](/.claude/skills/data-engineering/schema-migrator/SKILL.md) | Schema migrations | "Migrate database schema" |
| [`etl-optimizer`](/.claude/skills/data-engineering/etl-optimizer/SKILL.md) | ETL optimization | "Optimize ETL performance" |
| [`analytics-builder`](/.claude/skills/data-engineering/analytics-builder/SKILL.md) | Analytics | "Build analytics dashboard" |
| [`pandas-expert`](/.claude/skills/data-engineering/pandas-expert/SKILL.md) | Pandas operations | "Help with pandas dataframe" |

#### DevOps & Infrastructure (7 skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| [`docker-composer`](/.claude/skills/devops-infrastructure/docker-composer/SKILL.md) | Docker configs | "Create docker-compose.yml" |
| [`ci-cd-builder`](/.claude/skills/devops-infrastructure/ci-cd-builder/SKILL.md) | CI/CD pipelines | "Set up GitHub Actions" |
| [`cloud-architect`](/.claude/skills/devops-infrastructure/cloud-architect/SKILL.md) | Cloud infrastructure | "Design AWS architecture" |
| [`terraform-generator`](/.claude/skills/devops-infrastructure/terraform-generator/SKILL.md) | Terraform IaC | "Generate Terraform for EC2" |
| [`kubernetes-helper`](/.claude/skills/devops-infrastructure/kubernetes-helper/SKILL.md) | K8s configs | "Create K8s deployment" |
| [`monitoring-setup`](/.claude/skills/devops-infrastructure/monitoring-setup/SKILL.md) | Monitoring/alerting | "Set up Prometheus monitoring" |
| [`mcp-management`](/.claude/skills/devops-infrastructure/mcp-management/SKILL.md) | MCP server management | "Manage MCP servers" |

#### Frameworks (9 skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| [`python-architect`](/.claude/skills/frameworks/python-architect/SKILL.md) | Python projects | "Structure Python project" |
| [`fastapi-builder`](/.claude/skills/frameworks/fastapi-builder/SKILL.md) | FastAPI apps | "Build FastAPI app" |
| [`django-helper`](/.claude/skills/frameworks/django-helper/SKILL.md) | Django | "Create Django model" |
| [`flask-optimizer`](/.claude/skills/frameworks/flask-optimizer/SKILL.md) | Flask | "Optimize Flask app" |
| [`pytest-generator`](/.claude/skills/frameworks/pytest-generator/SKILL.md) | Pytest | "Generate pytest tests" |
| [`react-component`](/.claude/skills/frameworks/react-component/SKILL.md) | React | "Create React component" |
| [`ui-builder`](/.claude/skills/frameworks/ui-builder/SKILL.md) | UI components | "Build UI component" |
| [`typescript-helper`](/.claude/skills/frameworks/typescript-helper/SKILL.md) | TypeScript | "Fix TypeScript types" |
| [`frontend-optimizer`](/.claude/skills/frameworks/frontend-optimizer/SKILL.md) | Frontend perf | "Optimize bundle size" |

#### Version Control (5 skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| [`git-automation`](/.claude/skills/version-control/git-automation/SKILL.md) | Git hooks | "Create pre-commit hook" |
| [`pr-reviewer`](/.claude/skills/version-control/pr-reviewer/SKILL.md) | PR review | "Review this PR" |
| [`merge-resolver`](/.claude/skills/version-control/merge-resolver/SKILL.md) | Merge conflicts | "Resolve merge conflict" |
| [`commit-helper`](/.claude/skills/version-control/commit-helper/SKILL.md) | Commit messages | "Write commit message" |
| [`branch-strategist`](/.claude/skills/version-control/branch-strategist/SKILL.md) | Branching | "Design branching strategy" |

---

### Anthropic Official Skills (16 Skills)

Source: [github.com/anthropics/skills](https://github.com/anthropics/skills)

#### Document Skills
| Skill | Description | Usage | Link |
|-------|-------------|-------|------|
| `docx` | Create/edit Word documents | "Create a Word document" | [View](https://github.com/anthropics/skills/tree/main/document-skills/docx) |
| `pdf` | PDF manipulation toolkit | "Extract text from PDF" | [View](https://github.com/anthropics/skills/tree/main/document-skills/pdf) |
| `pptx` | PowerPoint presentations | "Create presentation slides" | [View](https://github.com/anthropics/skills/tree/main/document-skills/pptx) |
| `xlsx` | Excel spreadsheets | "Create Excel report" | [View](https://github.com/anthropics/skills/tree/main/document-skills/xlsx) |

#### Creative & Design
| Skill | Description | Usage | Link |
|-------|-------------|-------|------|
| `algorithmic-art` | Generative art with p5.js | "Create generative art" | [View](https://github.com/anthropics/skills/tree/main/algorithmic-art) |
| `canvas-design` | Visual art in PNG/PDF | "Design a poster" | [View](https://github.com/anthropics/skills/tree/main/canvas-design) |
| `slack-gif-creator` | Animated GIFs for Slack | "Create Slack GIF" | [View](https://github.com/anthropics/skills/tree/main/slack-gif-creator) |
| `theme-factory` | Professional themes | "Create dark theme" | [View](https://github.com/anthropics/skills/tree/main/theme-factory) |

#### Development
| Skill | Description | Usage | Link |
|-------|-------------|-------|------|
| `mcp-builder` | MCP server development | "Build MCP server" | [View](https://github.com/anthropics/skills/tree/main/mcp-builder) |
| `skill-creator` | Create Claude skills | "Create a new skill" | [View](https://github.com/anthropics/skills/tree/main/skill-creator) |
| `webapp-testing` | Playwright web testing | "Test my web app" | [View](https://github.com/anthropics/skills/tree/main/webapp-testing) |
| `frontend-design` | Production frontend UI | "Design frontend interface" | [View](https://github.com/anthropics/skills/tree/main/frontend-design) |

#### Enterprise
| Skill | Description | Usage | Link |
|-------|-------------|-------|------|
| `brand-guidelines` | Anthropic brand colors | "Apply brand guidelines" | [View](https://github.com/anthropics/skills/tree/main/brand-guidelines) |
| `internal-comms` | Internal communications | "Write status report" | [View](https://github.com/anthropics/skills/tree/main/internal-comms) |

**Install:**
```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

---

### obra/superpowers Skills (20 Skills)

Source: [github.com/obra/superpowers](https://github.com/obra/superpowers)

#### Testing Skills
| Skill | Description | Usage |
|-------|-------------|-------|
| `test-driven-development` | RED-GREEN-REFACTOR cycle | "Use TDD for this feature" |
| `condition-based-waiting` | Async test patterns | "Test async operations" |
| `testing-anti-patterns` | Common pitfalls to avoid | "Review test quality" |

#### Debugging Skills
| Skill | Description | Usage |
|-------|-------------|-------|
| `systematic-debugging` | 4-phase root cause process | "Debug this systematically" |
| `root-cause-tracing` | Find the real problem | "Find root cause" |
| `verification-before-completion` | Verify before finishing | "Verify this fix works" |
| `defense-in-depth` | Multiple validation layers | "Add defense layers" |

#### Collaboration Skills
| Skill | Description | Usage |
|-------|-------------|-------|
| `brainstorming` | Socratic design refinement | `/superpowers:brainstorm` |
| `writing-plans` | Detailed implementation plans | `/superpowers:write-plan` |
| `executing-plans` | Batch execution | `/superpowers:execute-plan` |
| `dispatching-parallel-agents` | Concurrent subagents | "Run agents in parallel" |
| `requesting-code-review` | Pre-review checklist | "Request code review" |
| `receiving-code-review` | Handle feedback | "Address review feedback" |

#### Development Skills
| Skill | Description | Usage |
|-------|-------------|-------|
| `using-git-worktrees` | Parallel development | "Use git worktrees" |
| `finishing-a-development-branch` | Merge/PR workflow | "Finish this branch" |
| `subagent-driven-development` | Fast iteration | "Use subagents" |

#### Meta Skills
| Skill | Description | Usage |
|-------|-------------|-------|
| `writing-skills` | Create new skills | "Create a skill" |
| `sharing-skills` | Contribute skills | "Share this skill" |
| `testing-skills-with-subagents` | Validate skills | "Test my skill" |
| `using-superpowers` | Introduction guide | "How to use superpowers" |

**Install:**
```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

**Slash Commands:**
- `/superpowers:brainstorm` - Interactive design refinement
- `/superpowers:write-plan` - Create implementation plan
- `/superpowers:execute-plan` - Execute plan in batches

---

### Scientific Skills (120+ Skills)

Source: [github.com/K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)

#### Bioinformatics & Genomics (15+ skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| `biopython` | Sequence analysis | "Analyze DNA sequence" |
| `scanpy` | Single-cell RNA-seq | "Analyze 10X data" |
| `alphafold-database` | Protein structures | "Get AlphaFold structure" |
| `ensembl-database` | Gene annotations | "Query Ensembl" |
| `pysam` | BAM/VCF processing | "Parse VCF file" |
| `arboreto` | Gene regulatory networks | "Infer GRN" |

#### Chemistry & Drug Discovery (10+ skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| `chembl-database` | Bioactivity data | "Query ChEMBL for inhibitors" |
| `rdkit` | Molecular manipulation | "Calculate molecular properties" |
| `deepchem` | Deep learning chemistry | "Predict ADMET" |
| `diffdock` | Molecular docking | "Dock compounds" |
| `datamol` | Molecule processing | "Generate analogs" |

#### Clinical & Medical (8+ skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| `clinicaltrials-database` | Clinical trials | "Search clinical trials" |
| `clinvar-database` | Variant interpretation | "Query ClinVar" |
| `fda-database` | Drug safety | "Check FDA data" |
| `cosmic-database` | Cancer mutations | "Search COSMIC" |

#### Data Science & ML (15+ skills)
| Skill | Description | Usage |
|-------|-------------|-------|
| `numpy` | Numerical computing | "NumPy operations" |
| `scipy` | Scientific computing | "Statistical tests" |
| `pandas` | Data manipulation | "Pandas dataframe" |
| `dask` | Parallel computing | "Scale pandas" |
| `pytorch-lightning` | Deep learning | "Train model" |
| `scikit-learn` | Machine learning | "Build classifier" |

#### Scientific Databases (26+ skills)
| Database | Description | Usage |
|----------|-------------|-------|
| `pubmed` | Literature search | "Search PubMed" |
| `uniprot` | Protein database | "Query UniProt" |
| `pdb` | Protein structures | "Get PDB structure" |
| `pubchem` | Chemical compounds | "Search PubChem" |
| `kegg` | Pathway database | "Query KEGG pathway" |
| `string` | Protein interactions | "Get STRING network" |

**Install:**
```bash
/plugin marketplace add K-Dense-AI/claude-scientific-skills
# Then select "scientific-skills" from the marketplace
```

**MCP Server:**
```
https://mcp.k-dense.ai/claude-scientific-skills/mcp
```

---

### Community Skills

#### Playwright Skill
Browser automation with Playwright
- Source: Community contribution
- Usage: "Automate browser testing"

#### D3.js Visualization
Create D3.js charts and visualizations
- Source: Community contribution
- Usage: "Create D3 visualization"

#### iOS Simulator Skill
iOS app testing in simulator
- Source: Community contribution
- Usage: "Test iOS app"

#### ffuf Web Fuzzing
Security testing with ffuf (authorized use only)
- Source: Community contribution
- Usage: "Fuzz web endpoints"

#### Web Asset Generator
Generate web assets (icons, favicons)
- Source: Community contribution
- Usage: "Generate favicon set"

---

## Skill Stacks

Pre-configured skill combinations for common workflows:

| Stack | Skills Included | Use Case |
|-------|-----------------|----------|
| `full-stack-ai` | rag-builder, chatbot-creator, api-designer, react-component | AI-powered full-stack apps |
| `production-ml` | model-trainer, mlops-pipeline, data-pipeline, monitoring-setup | Production ML systems |
| `rapid-poc` | fastapi-builder, docker-composer, ui-builder | Quick prototypes |
| `backend-development` | api-designer, database-schema, sql-optimizer, test-generator | Backend services |
| `frontend-development` | react-component, typescript-helper, frontend-optimizer, ui-builder | Frontend apps |
| `devops-complete` | docker-composer, ci-cd-builder, terraform-generator, kubernetes-helper | DevOps infrastructure |
| `data-pipeline` | data-pipeline, pandas-expert, data-validator, etl-optimizer | Data engineering |
| `code-quality` | code-reviewer, test-generator, security-auditor, performance-profiler | Code quality |
| `superpowers-development` | systematic-debugging, test-driven-development, verification-before-completion | Advanced dev workflows |
| `scientific-research` | biopython, scanpy, rdkit, pandas | Scientific computing |
| `bioinformatics` | biopython, ensembl-database, clinvar-database, alphafold-database | Genomics analysis |
| `document-processing` | docx, pdf, pptx, xlsx | Document manipulation |
| `creative-design` | canvas-design, algorithmic-art, theme-factory | Visual design |
| `mcp-development` | mcp-builder, skill-creator, api-designer | MCP servers |
| `business-pitch` | pitch-coach, alex-hormozi-pitch, goal-translator | Business communication |
| `content-creation` | linkedin-post, newsletter, medium-post, video-script | Content writing |

---

## How to Use Skills

### Automatic Activation
Skills activate automatically based on context:
```
"Build a RAG system for my documentation"
# Activates: rag-builder skill
```

### Direct Invocation
Reference skills explicitly:
```
"Use the api-designer skill to design a REST API for user management"
```

### Slash Commands (superpowers)
```bash
/superpowers:brainstorm    # Start brainstorming session
/superpowers:write-plan    # Create implementation plan
/superpowers:execute-plan  # Execute plan step-by-step
```

### Skill Format
Each skill follows this structure:
```markdown
---
name: skill-name
description: What this skill does and when to use it
---

# Skill Name

## When to Activate
- Context 1
- Context 2

## Process
1. Step 1
2. Step 2

## Output Format
What the skill produces
```

---

## Installation

### Option 1: Clone This Repository
```bash
git clone https://github.com/your-username/claude-skills.git
cp -r claude-skills/.claude/skills ~/.claude/skills
```

### Option 2: Install from Marketplaces

**Anthropic Skills:**
```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

**Superpowers:**
```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

**Scientific Skills:**
```bash
/plugin marketplace add K-Dense-AI/claude-scientific-skills
```

### Option 3: Browse SkillsMP
Visit [skillsmp.com](https://skillsmp.com) to browse 15,000+ skills

---

## Resources & Links

### Official Documentation
- [What are Skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Agent Skills Engineering Blog](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

### Skill Repositories
| Repository | Description | Stars |
|------------|-------------|-------|
| [anthropics/skills](https://github.com/anthropics/skills) | Official Anthropic skills | - |
| [obra/superpowers](https://github.com/obra/superpowers) | Development workflows | - |
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | Scientific computing | - |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Curated skill list | - |

### Marketplaces
- [SkillsMP](https://skillsmp.com) - 15,000+ skills marketplace
- [Notion Skills](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0) - Notion integration

### Community
- [K-Dense Slack](https://join.slack.com/t/k-densecommunity/shared_invite/zt-3iajtyls1-EwmkwIZk0g_o74311Tkf5g) - Scientific skills community
- [obra/superpowers Issues](https://github.com/obra/superpowers/issues) - Superpowers support

---

## Contributing

### Add a New Skill

1. Create directory under appropriate category:
```bash
mkdir -p .claude/skills/category/my-skill
```

2. Create `SKILL.md`:
```markdown
---
name: my-skill
description: Clear description of what this skill does
---

# My Skill

## When to Activate
- Relevant context 1
- Relevant context 2

## Process
1. Step 1
2. Step 2

## Output Format
Expected deliverables
```

3. Submit a PR

### Skill Guidelines
- Clear, actionable descriptions
- Specific activation triggers
- Practical code examples
- Best practices and anti-patterns

---

## Directory Structure

```
.claude/skills/
├── ai-ml-development/          # 8 AI/ML skills
├── backend-api/                # 8 backend skills
├── business-communication/     # 13 business skills
├── code-quality/               # 9 code quality skills
├── data-engineering/           # 6 data skills
├── devops-infrastructure/      # 7 DevOps skills
├── frameworks/                 # 9 framework skills
├── version-control/            # 5 git skills
├── anthropics-official/        # 16 official skills
├── obra-superpowers/           # 20 workflow skills
├── community/
│   ├── scientific-skills/      # 120+ scientific skills
│   ├── playwright-skill/       # Browser automation
│   ├── d3js-visualization/     # D3.js charts
│   ├── ios-simulator-skill/    # iOS testing
│   ├── ffuf-web-fuzzing/       # Security testing
│   ├── superpowers-skills/     # Additional superpowers
│   └── superpowers-lab/        # Experimental skills
└── awesome-claude-skills/      # Community index
```

---

## License

- Custom skills: MIT License
- Anthropic skills: Apache 2.0 (example skills), Source-available (document skills)
- obra/superpowers: MIT License
- Scientific skills: MIT License

---

**Made with Claude Code**
