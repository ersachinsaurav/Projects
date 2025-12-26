# LinkedIn Post Generator 🚀

AI-powered LinkedIn post and image generator using AWS Bedrock (Claude + Nova Canvas).

## ✨ Features

- **AI Text Generation**: Create engaging LinkedIn posts using Claude (Opus, Sonnet, Haiku)
- **Smart Image Recommendations**: AI suggests the best image type for your post
- **AI Image Generation**: Generate matching visuals using Amazon Nova Canvas
- **Instant Post Cards**: Code-generated typography cards (no AI, instant)
- **LinkedIn-Style Preview**: See exactly how your post will look in the feed
- **Unicode Formatting**: Bold, italic, strikethrough support for LinkedIn
- **PDF Export**: Merge multiple images into carousel-ready PDFs

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite + TypeScript)             │
│  ┌───────────────┐  ┌─────────────────┐  ┌──────────────────────┐   │
│  │  Input Form   │  │ LinkedIn Preview│  │  Image Gallery       │   │
│  │  - Idea       │  │ - Editable text │  │  - AI or Post Cards  │   │
│  │  - Tone       │  │ - Formatting    │  │  - PDF download      │   │
│  │  - Audience   │  │ - Copy/export   │  │  - Regenerate        │   │
│  └───────────────┘  └─────────────────┘  └──────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ HTTP/REST
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       BACKEND (FastAPI + Python)                    │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ Modular Routes                                                 │ │
│  │ routes_text.py │ routes_image.py │ routes_health.py │ routes...│ │
│  └────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ Providers (Abstract Base + Implementations)                    │ │
│  │ BedrockTextProvider │ NovaCanvasProvider │ TitanImageProvider  │ │
│  └────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ Services                                                       │ │
│  │ SessionManager │ ImageProcessor │ PostCardBuilder │ Loggers    │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        AWS BEDROCK                                  │
│  Claude (Text) ──── Nova Canvas (Images) ──── Titan (Fallback)      │
└─────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- AWS credentials configured (`~/.aws/credentials` or environment variables)
- AWS Bedrock access to Claude and Nova Canvas models

### Installation

```bash
# Clone and navigate
cd linkedin_post_generator

# One-command launch (creates venv, installs deps, starts both servers)
chmod +x launch.sh
./launch.sh
```

This starts:
- **Backend**: http://localhost:8000 (Python + FastAPI)
- **Frontend**: http://localhost:5173 (React + Vite)
- **API Documentation**: http://localhost:8000/docs (Swagger docs)

### Manual Setup

**Backend:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check + provider status |
| `/api/v1/models` | GET | List available models |
| `/api/v1/generate-text` | POST | Generate LinkedIn post text |
| `/api/v1/generate-image-prompts` | POST | Generate AI image prompts |
| `/api/v1/generate-images` | POST | Generate images from prompts |
| `/api/v1/generate-post-card` | POST | Generate instant post card |
| `/api/v1/session/{session_id}` | GET | Get session state |
| `/api/v1/usage/daily` | GET | Get daily usage statistics |

### Example: Generate Text

```bash
curl -X POST http://localhost:8000/api/v1/generate-text \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "Why most developers waste time on wrong optimizations",
    "post_length": "medium",
    "tone": "opinionated",
    "audience": ["engineers", "founders"],
    "cta_style": "question"
  }'
```

### Example: Generate Images

```bash
curl -X POST http://localhost:8000/api/v1/generate-images \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "provider": "nova"
  }'
```

## 🤖 Available Models

### Text Generation (Claude via Bedrock)

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| `claude-opus-4.5` | Slow | ⭐⭐⭐⭐⭐ | Best quality posts |
| `claude-sonnet-4.5` | Medium | ⭐⭐⭐⭐ | Balanced performance |
| `claude-haiku-4.5` | Fast | ⭐⭐⭐ | Quick iterations |

### Image Generation

| Model | Type | Best For |
|-------|------|----------|
| Nova Canvas | AI | High-quality visuals |
| Titan v2 | AI | Fallback option |
| Post Card | Code | Instant typography cards |

## 📁 Project Structure

```
linkedin_post_generator/
├── backend/
│   ├── api/
│   │   ├── routes.py                   # Combined router
│   │   ├── routes_text.py              # Text generation
│   │   ├── routes_image.py             # Image generation
│   │   ├── routes_health.py            # Health & utility
│   │   ├── routes_session.py           # Session management
│   │   ├── provider_factory.py
│   │   └── schemas.py                  # Pydantic models
│   ├── providers/
│   │   ├── base.py                     # Abstract base classes
│   │   ├── bedrock_text.py             # Claude provider
│   │   ├── nova_image.py               # Nova Canvas provider
│   │   └── titan_image.py              # Titan provider
│   ├── services/
│   │   ├── session_manager.py          # Async session storage
│   │   ├── image_processor.py          # Image post-processing
│   │   ├── post_card_builder.py        # Typography card generator
│   │   ├── prompt_logger.py            # Debug logging
│   │   └── usage_logger.py             # Usage tracking
│   ├── prompts/
│   │   ├── linkedin_text.py            # Text generation prompts
│   │   └── image_prompts.py            # Image prompt templates
│   ├── utils/
│   │   └── constants.py                # Enums & constants
│   ├── config.py
│   └── main.py
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── InputForm.tsx
│       │   ├── LinkedInPreview.tsx
│       │   ├── RecommendationSection.tsx
│       │   ├── TextPreview.tsx
│       │   └── ImagePreview.tsx
│       ├── hooks/
│       │   ├── useGenerateText.ts
│       │   ├── useGenerateImages.ts
│       │   └── useGeneratePostCard.ts
│       ├── lib/
│       │   ├── api.ts                  # API client
│       │   ├── constants.ts            # App constants
│       │   ├── unicode.ts              # Unicode formatting
│       │   └── utils.ts                # Utilities
│       ├── types/
│       │   └── index.ts
│       ├── App.tsx
│       └── main.tsx
├── logs/                               # Runtime logs (gitignored)
├── requirements.txt
├── launch.sh
└── README.md
```

## 🎨 Image Types

The AI recommends the best image type based on your post content:

| Type | Description | When to Use |
|------|-------------|-------------|
| **Post Card** | Typography-based card (instant, no AI) | Text-focused posts, quotes |
| **Hero Image** | Single impactful visual | Emotional, story-driven posts |
| **Infographic** | Data visualization | Stats, processes, lists |
| **Carousel** | Multi-image sequence | Step-by-step content |
| **Meme** | Relatable humor | Engagement-focused posts |

## 💰 Cost Controls

- **Token caps**: Max 4000 output tokens per generation
- **Image limits**: Max 7 images per request
- **Post cards**: Zero AI cost (pure code generation)
- **Usage logging**: All operations tracked for monitoring

## 🔧 Configuration

Environment variables (`.env`):

```env
# AWS Configuration (uses default credentials if not set)
AWS_REGION=us-east-1

# App Settings
DEBUG=false
LOG_LEVEL=INFO
```

## 📝 Development

```bash
# Backend with auto-reload
uvicorn backend.main:app --reload

# Frontend with HMR
cd frontend && npm run dev

# Type check frontend
cd frontend && npx tsc --noEmit
```

## 📄 License

MIT License

---

Built with ❤️ by **Sachin Saurav**
🔗 https://sachinsaurav.dev
🐙 GitHub: [@ersachinsaurav](https://www.sachinsaurav.dev/)

Powered by AWS Bedrock (Claude & Nova), React, Python, and FastAPI.
