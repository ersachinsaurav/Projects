# Contributing to LinkedIn Post Generator

First off, thank you for considering contributing! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** describing the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs what actually happened
- **Screenshots** if applicable
- **Environment details** (OS, Python version, Node version)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Clear title** describing the enhancement
- **Detailed description** of the proposed functionality
- **Why this would be useful** to most users
- **Possible implementation** approach (optional)

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Follow the code style** of the project
3. **Add tests** if applicable
4. **Update documentation** if needed
5. **Ensure all tests pass**
6. **Submit a PR** with a clear description

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- At least one AI provider configured:
  - **Ollama** (free, local) - Recommended for getting started
  - **AWS Bedrock** (paid, cloud) - For production quality
  - **SDXL WebUI** (free, local) - For image generation

### Quick Start

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/linkedin_post_generator.git
cd linkedin_post_generator

# Backend setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..

# Configure environment
cp env.example .env
# Edit .env with your settings

# Run development servers
./launch.sh
```

### Code Style

**Python (Backend)**
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions focused and small

**TypeScript (Frontend)**
- Use TypeScript strictly (no `any` unless necessary)
- Follow React best practices
- Use functional components with hooks
- Keep components focused

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add carousel generation support
fix: resolve image overlay positioning
docs: update README with new providers
refactor: simplify session management
```

### Testing

```bash
# Backend (from project root)
pytest

# Frontend (from frontend directory)
npm test
```

## Project Structure

```
├── backend/
│   ├── api/          # FastAPI routes and schemas
│   ├── providers/    # AI provider implementations
│   ├── services/     # Business logic
│   ├── prompts/      # LLM prompt templates
│   └── utils/        # Shared utilities
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   ├── lib/         # Utilities and constants
│   │   └── types/       # TypeScript types
└── logs/             # Generated logs (gitignored)
```

## Adding New Features

### Adding a New AI Provider

1. Create provider class in `backend/providers/`
2. Extend `BaseTextProvider` or `BaseImageProvider`
3. Register in `backend/api/provider_factory.py`
4. Add to `backend/utils/constants.py`
5. Update frontend model selection if needed

### Adding a New Image Type

1. Add type to `backend/utils/constants.py`
2. Create prompt template in `backend/prompts/image_gen/usecases/`
3. Add to frontend `IMAGE_TYPE_CONFIG` in `frontend/src/lib/constants.ts`
4. Update image generation logic if needed

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

