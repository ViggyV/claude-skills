# Claude Code Skills Library

A comprehensive collection of skills for Claude Code, combining official Anthropic skills, community-contributed skills, and custom skills for enhanced development workflows.

## Overview

This skill library contains **200+ skills** from multiple sources:

| Source | Skills Count | Description |
|--------|--------------|-------------|
| Custom Skills | 62 | Custom-built skills across 8 categories |
| Anthropic Official | 13 | Official skills from Anthropic |
| obra/superpowers | 20 | Battle-tested development workflow skills |
| Scientific Skills | 116 | Scientific computing and bioinformatics |
| Community | 8+ | Individual community contributions |

**Total: 200+ skills** organized into **22 skill stacks**

## Directory Structure

```
.claude/skills/
├── ai-ml-development/          # 8 custom AI/ML skills
├── backend-api/                # 8 custom backend skills
├── business-communication/     # 11 custom business skills
├── code-quality/               # 9 custom code quality skills
├── data-engineering/           # 6 custom data engineering skills
├── devops-infrastructure/      # 6 custom DevOps skills
├── frameworks/                 # 9 custom framework skills
├── version-control/            # 5 custom version control skills
├── anthropics-official/        # Official Anthropic skills
├── obra-superpowers/           # obra/superpowers collection
├── community/                  # Community skill repositories
│   ├── scientific-skills/      # 116 scientific computing skills
│   ├── playwright-skill/       # Browser automation
│   ├── d3js-visualization/     # D3.js visualizations
│   ├── ios-simulator-skill/    # iOS app testing
│   ├── ffuf-web-fuzzing/       # Security testing
│   ├── web-asset-generator/    # Web asset generation
│   ├── superpowers-skills/     # Additional superpowers
│   └── superpowers-lab/        # Experimental skills
└── awesome-claude-skills/      # Community skill index
```

## Skill Sources

### Official Anthropic Skills

Located in `anthropics-official/`:

| Skill | Description |
|-------|-------------|
| `algorithmic-art` | Generative art with p5.js |
| `brand-guidelines` | Anthropic brand colors and typography |
| `canvas-design` | Visual art in PNG/PDF formats |
| `document-skills/docx` | Word document manipulation |
| `document-skills/pdf` | PDF creation and extraction |
| `document-skills/pptx` | PowerPoint presentations |
| `document-skills/xlsx` | Excel spreadsheets |
| `frontend-design` | Frontend design assistance |
| `internal-comms` | Internal communications writing |
| `mcp-builder` | MCP server development |
| `skill-creator` | Interactive skill creation |
| `slack-gif-creator` | Animated GIFs for Slack |
| `theme-factory` | Theme creation |
| `web-artifacts-builder` | HTML artifacts with React |
| `webapp-testing` | Playwright web testing |

### obra/superpowers Skills

Located in `obra-superpowers/skills/`:

| Skill | Description |
|-------|-------------|
| `brainstorming` | Structured brainstorming sessions |
| `condition-based-waiting` | Wait for specific conditions |
| `defense-in-depth` | Security defense patterns |
| `dispatching-parallel-agents` | Run agents in parallel |
| `executing-plans` | Execute structured plans |
| `finishing-a-development-branch` | Complete feature branches |
| `receiving-code-review` | Handle code review feedback |
| `requesting-code-review` | Request and prepare reviews |
| `root-cause-tracing` | Debug root cause analysis |
| `sharing-skills` | Share and document skills |
| `subagent-driven-development` | Develop with subagents |
| `systematic-debugging` | Systematic debugging process |
| `test-driven-development` | TDD workflows |
| `testing-anti-patterns` | Avoid testing mistakes |
| `testing-skills-with-subagents` | Test skills using agents |
| `using-git-worktrees` | Git worktree workflows |
| `using-superpowers` | Core superpowers guide |
| `verification-before-completion` | Verify before completing |
| `writing-plans` | Write structured plans |
| `writing-skills` | Create new skills |

### Scientific Skills (116 skills)

Located in `community/scientific-skills/scientific-skills/`:

**Bioinformatics & Genomics:**
- `alphafold-database`, `biopython`, `ensembl-database`, `gene-database`
- `clinvar-database`, `cosmic-database`, `gwas-database`, `esm`

**Chemistry & Drug Discovery:**
- `chembl-database`, `drugbank-database`, `datamol`, `deepchem`, `diffdock`

**Data Science:**
- `numpy`, `scipy`, `pandas`, `dask`, `anndata`
- `exploratory-data-analysis`, `hypothesis-generation`

**Astronomy:**
- `astropy`

**Clinical & Medical:**
- `clinicaltrials-database`, `clinpgx-database`, `fda-database`, `hmdb-database`

### Community Individual Skills

| Skill | Location | Description |
|-------|----------|-------------|
| `playwright-skill` | `community/playwright-skill/` | Browser automation |
| `d3js-visualization` | `community/d3js-visualization/` | D3.js charts |
| `ios-simulator-skill` | `community/ios-simulator-skill/` | iOS testing |
| `ffuf-web-fuzzing` | `community/ffuf-web-fuzzing/` | Security fuzzing |
| `web-asset-generator` | `community/web-asset-generator/` | Web assets |

### Custom Skills (62 skills)

#### Business & Communication (11 skills)
| Skill | Description |
|-------|-------------|
| `pitch-coach` | Investor and sales pitches |
| `meeting-recap` | Meeting summaries |
| `email-polisher` | Professional emails |
| `story-mapper` | User stories |
| `linkedin-post-formatter` | LinkedIn posts |
| `linkedin-post` | LinkedIn strategy |
| `newsletter` | Email newsletters |
| `medium-post` | Medium articles |
| `video-script` | Video scripts |
| `decision-journal` | Decision documentation |
| `goal-translator` | Goal to action plans |

#### AI/ML Development (8 skills)
| Skill | Description |
|-------|-------------|
| `rag-builder` | RAG pipelines |
| `llm-optimizer` | LLM cost optimization |
| `prompt-engineer` | Prompt engineering |
| `model-trainer` | Model training |
| `chatbot-creator` | Conversational AI |
| `mlops-pipeline` | ML operations |
| `vector-db-manager` | Vector databases |
| `agent-designer` | AI agent design |

#### Code Quality & Testing (9 skills)
| Skill | Description |
|-------|-------------|
| `code-reviewer` | Code review |
| `code-refactor` | Refactoring |
| `code-documenter` | Documentation |
| `bug-hunter` | Bug finding |
| `security-auditor` | Security review |
| `test-generator` | Test writing |
| `test-automation` | CI test setup |
| `debug-assistant` | Debugging |
| `performance-profiler` | Performance |

#### Backend & API (8 skills)
| Skill | Description |
|-------|-------------|
| `api-designer` | REST/GraphQL APIs |
| `api-documenter` | API docs |
| `endpoint-tester` | Endpoint testing |
| `database-schema` | Schema design |
| `sql-optimizer` | SQL optimization |
| `microservices-architect` | Microservices |
| `webhook-creator` | Webhooks |
| `oauth-implementer` | OAuth/auth |

#### DevOps & Infrastructure (6 skills)
| Skill | Description |
|-------|-------------|
| `docker-composer` | Docker configs |
| `ci-cd-builder` | CI/CD pipelines |
| `cloud-architect` | Cloud infrastructure |
| `terraform-generator` | Terraform IaC |
| `kubernetes-helper` | K8s configs |
| `monitoring-setup` | Monitoring/alerting |

#### Data Engineering (6 skills)
| Skill | Description |
|-------|-------------|
| `data-pipeline` | ETL/ELT pipelines |
| `data-validator` | Data validation |
| `schema-migrator` | Schema migrations |
| `etl-optimizer` | ETL optimization |
| `analytics-builder` | Analytics |
| `pandas-expert` | Pandas |

#### Version Control (5 skills)
| Skill | Description |
|-------|-------------|
| `git-automation` | Git hooks |
| `pr-reviewer` | PR review |
| `merge-resolver` | Merge conflicts |
| `commit-helper` | Commit messages |
| `branch-strategist` | Branching |

#### Frameworks (9 skills)
| Skill | Description |
|-------|-------------|
| `python-architect` | Python projects |
| `fastapi-builder` | FastAPI apps |
| `django-helper` | Django |
| `flask-optimizer` | Flask |
| `pytest-generator` | Pytest |
| `react-component` | React |
| `ui-builder` | UI components |
| `typescript-helper` | TypeScript |
| `frontend-optimizer` | Frontend perf |

## Skill Stacks (22 pre-configured)

See `skill-stacks.json` for available combinations:

| Stack | Description |
|-------|-------------|
| `full-stack-ai` | AI-powered applications |
| `production-ml` | Production ML pipelines |
| `rapid-poc` | Quick prototyping |
| `business-pitch` | Business communication |
| `backend-development` | Backend API development |
| `frontend-development` | Modern frontend |
| `devops-complete` | Full DevOps setup |
| `data-pipeline` | Data engineering |
| `code-quality` | Quality assurance |
| `content-creation` | Content writing |
| `microservices` | Microservices architecture |
| `chatbot-development` | AI chatbot development |
| `superpowers-development` | Advanced dev workflows |
| `code-review-workflow` | Code review process |
| `scientific-research` | Scientific computing |
| `bioinformatics` | Genomics analysis |
| `web-automation` | Browser automation |
| `document-processing` | Document manipulation |
| `creative-design` | Visual design |
| `mcp-development` | MCP server development |
| `security-testing` | Security testing |

## Usage

Skills activate automatically when you ask Claude Code for help in relevant areas. Each skill provides:

1. **Activation context** - When to use the skill
2. **Process steps** - Structured approach
3. **Code templates** - Ready-to-use examples
4. **Best practices** - Guidelines and tips
5. **Output format** - Expected deliverables

## Contributing

To add a new skill:
1. Create directory under appropriate category
2. Add `SKILL.md` following the format in existing skills
3. Update this README if applicable
4. Update `skill-stacks.json` if creating a new stack

## Resources

- [Official Anthropic Skills](https://github.com/anthropics/skills)
- [obra/superpowers](https://github.com/obra/superpowers)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
- [Scientific Skills](https://github.com/K-Dense-AI/claude-scientific-skills)
