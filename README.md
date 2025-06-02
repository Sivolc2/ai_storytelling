# My Adventure Tale - A Choose Your Own Adventure Game

An interactive storytelling game for young children (ages 4-8) where they can create their own adventures!
This application uses a Large Language Model (LLM) on the backend to generate unique story segments, image prompts, and choices based on the child's decisions.

## 🌟 Features

- **Dynamic Story Generation:** Every playthrough can be unique.
- **Child-Friendly Interface:** Simple, intuitive, and engaging for young users.
- **Image Prompts:** For each story scene, a descriptive prompt is provided to spark imagination (actual image generation can be a future enhancement).
- **Branching Choices:** Children guide the story with their decisions.

## 🤖 How to Use This Repository with AI

This repository is designed for effective human-AI collaboration. Follow this process:

### Contributing with AI Assistance
1. **Add documentation first**: Create or update guides in `docs/guides/` to document new features or processes
2. **Prompt the AI model with**:
   - `docs/feature_flow.md` - Shows the process for contributing (update as workflows evolve)
   - Registry context files in `registry/` (backend_context.md, frontend_context.md)
3. **Use README files** in each folder as guidance for your contributions
4. **Develop iteratively**: Test features after implementing and check for output

### Best Practices
- **Encode business logic in pipelines**: Expand pipeline documentation to capture domain knowledge
- **Update documentation as you code**: Have your AI assistant update docs as pipelines are implemented
- **Follow testing patterns**: Use the established testing harness for both frontend and backend

## 🎮 Game Overview

This repository is structured as a monorepo with a clean separation between pure functions (functional core) and side effects (adapters/IO). This architecture makes it particularly friendly for AI-assisted development and reasoning.

## 🏗️ Project Structure

```
.
├── repo_src
│   ├── backend            # Python backend with functional core
│   │   ├── llm_services/  # LLM integration for story generation
│   │   ├── routers/       # API endpoint definitions (e.g., for story)
│   │   ├── data/          # Pydantic schemas for API requests/responses
│   │   ├── tests/         # unit and integration tests
│   │   ├── utils/         # generic helpers
│   │   ├── main.py        # entrypoint
│   │   └── README_backend.md
│   ├── frontend           # React/TypeScript frontend
│   │   ├── src/
│   │   │   ├── App.tsx      # Main application component for the game
│   │   │   ├── main.tsx     # Entry point for React app
│   │   │   ├── components/  # Reusable UI components (ThemeInput, StoryDisplay, ChoiceButtons)
│   │   │   ├── styles/      # CSS styles
│   │   │   ├── types/       # TypeScript type definitions
│   │   └── README_frontend.md
│   ├── scripts            # developer tooling and utilities
│   └── shared             # shared types and utilities
│       └── README_shared.md
├── docs
│   ├── adr/             # architecture decision records
│   ├── diagrams/        # system and component diagrams
│   ├── pipelines/       # auto-generated pipeline documentation
│   ├── prd/             # product requirements documents (if any for this game)
│   └── README_*.md      # documentation guides
├── registry/            # auto-generated documentation and indexes
└── .github/workflows    # CI/CD configuration
```

## 🚀 Getting Started

```bash
# One-command project setup
pnpm setup-project       # Install dependencies, create venv, install Python packages, and set up env files

# Or manual step-by-step setup:
pnpm install              # Frontend dependencies
python -m venv .venv      # Create Python virtual environment
source .venv/bin/activate # Activate Python virtual environment
pip install -r repo_src/backend/requirements.txt # Backend dependencies (includes FastAPI, google-generativeai)
pnpm setup-env            # Set up environment variables (creates .env files, including GOOGLE_API_KEY placeholder)

# Run development servers
pnpm dev                  # Start both frontend and backend servers (using Turborepo)
pnpm dev:clean            # Reset ports and start dev servers
pnpm dev:frontend         # Run only frontend
pnpm dev:backend          # Run only backend

# Individual commands
pnpm reset                # Kill processes using ports 8000, 5173, and 5174
pnpm --filter frontend dev      # Start Vite dev server
uvicorn repo_src.backend.main:app --reload  # Start backend server

# Development workflow
pnpm lint                # Run linters
pnpm typecheck           # Run type checking
pnpm test                # Run tests for both frontend and backend
pnpm e2e                 # Run end-to-end tests with Playwright
pnpm ci                  # Run lint, typecheck, and tests (CI pipeline)
pnpm refresh-docs        # Update documentation and diagrams
```

## 🧪 Testing

This project uses a comprehensive testing harness:

- **Frontend**: Vitest + React Testing Library (to be expanded for game components)
- **Backend**: pytest (to be expanded for story generation service and API)
- **E2E**: Playwright

See [README.testing.md](README.testing.md) for detailed information about the testing setup.

## 📝 Development Flow

See [docs/feature_flow.md](docs/feature_flow.md) for the step-by-step process for adding new features.
For this game, the primary flow involves: defining story logic, implementing LLM prompts, building UI components, and connecting them via APIs.

## 📚 Documentation

Each directory contains a README file with specific guidance for that component.

### Registry

The [registry](registry/) directory contains auto-generated documentation and indexes that provide AI-friendly context:

- **backend_context.md**: Concise index of backend functionality
- **frontend_context.md**: Concise index of frontend components and hooks
- **pipeline_context.md**: Summary of any backend orchestration pipelines
- **context.json**: Machine-readable metadata for AI tools

To update the registry:

```bash
pnpm ctx:sync
```

### Diagrams

The [docs/diagrams](docs/diagrams/) directory contains automatically generated diagrams that visualize:

- **Function Overview**: All functions from the `functions/` directory grouped by module
- **Pipeline Diagrams**: (If applicable) Individual pipeline functions and their relationships

To generate or update diagrams:

```bash
pnpm diagrams:generate
```

## 🔄 CI/CD

The project uses GitHub Actions for continuous integration and deployment.

## 📄 License (from original template)
MIT License (Please check the LICENSE file. The original template had ISC in README but MIT in LICENSE file.)
