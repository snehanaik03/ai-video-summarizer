# 🎓 SynapseAI: AI Study Companion

> **Transform passive educational video watching into structured mastery, actionable insights, and self-assessment.**  
> *Built by Sneha Uday Naik and Sai Kumar Telang*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_18-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_CSS-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini_Flash-8E75B2.svg?logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)

---

## 📖 About the Application

Modern students and professionals consume hours of lecture videos, technical talks, and educational tutorials, yet retain only a fraction of what they hear. Passive watching rarely leads to deep comprehension.

**SynapseAI** bridges this gap. It serves as an intelligent study partner that ingests any educational video link or local media file, transcribes spoken dialogue, and employs advanced Large Language Models (LLMs) to automatically synthesize the material into:
1. **High-Retention Structured Summaries**: Complete with executive overviews, analytical breakdowns, concept matrices, core themes, and chronological progression timelines.
2. **Interactive MCQ Quizzes**: Tailored multiple-choice questions with difficulty grading and instant answer explanations to test recall immediately after studying.

Designed as an **open-access, zero-friction tool**, SynapseAI eliminates mandatory sign-ups and paywalls, delivering a sleek, distraction-free dark-mode workspace.

---

## ✨ Key Features

- **Robust Video & URL Parsing**:
  - Seamlessly handles standard YouTube URLs, shortened `youtu.be` links, mobile `m.youtube.com`, YouTube Shorts, YouTube Live streams, and playlists.
  - Multi-client fallback engine (Android/iOS emulation) prevents bot-detection and connection rejection errors.
- **Automated Caption & Audio Transcription Pipeline**:
  - Leverages official captions when available for near-instant responses.
  - Automatically falls back to high-fidelity audio extraction and speech-to-text transcription via `faster-whisper` when captions are absent.
- **Tiered & Structured Summarization**:
  - Choose between **Basic** (concise high-yield review) and **Premium** (comprehensive multi-section breakdown).
  - Employs standardized Markdown formatting: Concept Definition Tables, Analytical Subsections, Core Themes, and Timeline Matrices.
- **Automated MCQ Quiz Generation**:
  - Automatically synthesizes multiple-choice questions directly from the video's core arguments.
  - Interactive quiz UI featuring animated card transitions, immediate score evaluation, and concept explanations.
- **No-Login Open Access**:
  - Free from onboarding friction or login walls; start summarizing videos immediately from the landing page.
- **Modern Dark-Mode Aesthetic & Animations**:
  - High-converting landing page with animated hero sections, step-by-step guides, smooth CSS card slide-ups, and button glow effects.

---

## 🏗️ Architecture & How It Works

The data flow is architected as an asynchronous, resilient four-stage pipeline:

```
┌─────────────────┐       ┌──────────────────────┐       ┌────────────────────────┐       ┌─────────────────┐
│   User Input    │ ----> │ Audio / Transcript   │ ----> │    LLM Processing      │ ----> │  UI Rendering   │
│ (YouTube / File)│       │      Extraction      │       │ (Gemini @ Temp = 0.1)  │       │ (React + GFM)   │
└─────────────────┘       └──────────────────────┘       └────────────────────────┘       └─────────────────┘
```

1. **User Input Stage**:
   The user provides a YouTube link or uploads a media file on the React frontend. The request is dispatched via TanStack Query and Axios to FastAPI.
2. **Extraction Stage**:
   - The backend checks for video captions via `youtube-transcript-api` and `yt-dlp` mobile client signatures.
   - If captions are unavailable, the backend downloads the audio track and transcribes it locally using `faster-whisper`.
3. **LLM Synthesis Stage**:
   - The verified transcript is passed to Google Gemini (`gemini-2.0-flash` / `gemini-1.5-flash`).
   - The model temperature is explicitly locked at **`0.1`** to enforce deterministic, strictly factual summaries and eliminate hallucinations.
   - A secondary structured JSON prompt generates 4-option multiple-choice questions grounded solely in the summary facts.
   - *Resilience Guarantee*: An integrated concept-extraction engine serves as an automatic fallback if API keys are absent or rate limits are reached.
4. **UI Rendering Stage**:
   - The frontend renders summaries via `react-markdown` and `remark-gfm` with styled tables, badges, and tabs.
   - Interactive quiz cards animate into view with instant grading and explanations.

---

## 💻 Tech Stack

### Frontend (Client)
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS (Dark Mode, Custom Keyframe Animations, Glow Utilities)
- **Data Fetching & State:** TanStack Query (React Query v5)
- **Routing:** React Router v6
- **Markdown & Rendering:** `react-markdown`, `remark-gfm`
- **Icons:** Lucide React

### Backend (Server)
- **Framework:** FastAPI (Python 3.11+)
- **Asynchronous Server:** Uvicorn with WatchFiles
- **Data Validation:** Pydantic v2
- **Database ORM:** SQLAlchemy (Async) with `aiosqlite`
- **Audio Extraction:** `yt-dlp` (with Node.js runtime deciphering & mobile client emulation), `imageio-ffmpeg`
- **Transcription:** `faster-whisper`, `youtube-transcript-api`

### Database
- **Storage:** SQLite (development) / PostgreSQL-ready (production)

### AI & LLM Engine
- **Model:** Google Gemini (`gemini-2.0-flash`, `gemini-1.5-flash`) via `google-genai` SDK
- **Parameter Tuning:** `temperature = 0.1`, `response_mime_type = "application/json"`

---

## 📁 Project Directory Structure

```text
VideoSummarizer/
├── .gitignore                   # Master Git ignore (secrets, venv, node_modules)
├── README.md                    # Project documentation
│
├── frontend/                    # React + Vite Client Application
│   ├── public/                  # Static assets (favicons, public images)
│   ├── src/
│   │   ├── api/                 # Axios HTTP client & API route definitions
│   │   │   ├── client.ts        # Base Axios instance with proxy configurations
│   │   │   ├── notes.ts         # Saved notes endpoints
│   │   │   ├── quiz.ts          # Quiz generation & submission endpoints
│   │   │   └── summarize.ts     # Video/Text summarization endpoints
│   │   ├── components/          # Reusable UI components
│   │   │   ├── examples/        # Pre-loaded educational video cards
│   │   │   ├── input/           # URL input bars, file uploaders, tabs
│   │   │   ├── layout/          # Navbar, Sidebar, Branded Header & Footer
│   │   │   ├── notes/           # Saved notes list & card views
│   │   │   ├── output/          # Markdown summary viewer, Quiz container
│   │   │   └── quiz/            # Individual MCQ question cards, scoring modal
│   │   ├── hooks/               # Custom TanStack Query mutation & query hooks
│   │   ├── pages/               # Routed page views
│   │   │   ├── LandingPage.tsx  # High-converting Hero & How-It-Works page
│   │   │   ├── HomePage.tsx     # Interactive summarizer workspace
│   │   │   ├── ResultsPage.tsx  # Summary & Quiz display page
│   │   │   └── NotesPage.tsx    # Saved student notes archive
│   │   ├── types/               # TypeScript interfaces & API schemas
│   │   ├── App.tsx              # Application route tree
│   │   ├── main.tsx             # React DOM root & QueryClient provider
│   │   └── index.css            # Tailwind directives & CSS keyframe animations
│   ├── package.json             # Frontend dependencies & scripts
│   ├── tailwind.config.js       # Custom color palette, shadows, and animations
│   ├── tsconfig.json            # Strict TypeScript configuration
│   └── vite.config.ts           # Vite server & API proxy rules
│
└── backend/                     # FastAPI Python Server Application
    ├── app/
    │   ├── main.py              # Application factory, lifespan, CORS & router mount
    │   ├── config.py            # Pydantic environment settings
    │   ├── database.py          # Async SQLAlchemy engine & session factory
    │   ├── models/              # Database schema definitions
    │   │   ├── user.py          # User accounts
    │   │   ├── summary.py       # Transcripts, summaries & metadata
    │   │   └── quiz.py          # Quizzes, questions & scoring records
    │   ├── schemas/             # Pydantic request/response validation models
    │   │   ├── summary.py       # Summarize request/response schemas
    │   │   └── quiz.py          # Quiz and submission schemas
    │   ├── routers/             # API endpoint handlers
    │   │   ├── summarize.py     # POST /api/summarize/youtube, /api/summarize/text
    │   │   ├── quiz.py          # POST /api/quiz/generate, POST /api/quiz/submit
    │   │   ├── upload.py        # POST /api/upload (media & PDF processing)
    │   │   └── notes.py         # GET /api/notes, DELETE /api/notes/{id}
    │   ├── services/            # Core business logic
    │   │   ├── ai_service.py    # Gemini client, temperature control, fallback engine
    │   │   ├── youtube_service.py # URL parser, caption & audio extractors
    │   │   ├── transcription_service.py # Whisper local speech-to-text
    │   │   └── file_service.py  # Local media validation & audio conversion
    │   └── utils/
    │       ├── exceptions.py    # Custom HTTP exceptions
    │       └── prompts.py       # Factual system instructions & structured prompt templates
    ├── tests/
    │   └── test_api.py          # Pytest suite (URL regex, quiz scoring, notes)
    ├── requirements.txt         # Python package dependencies
    └── .env.example             # Template for local environment variables
```

---

## ⚙️ Installation & Setup

### Prerequisites
- **Git** installed on your system.
- **Node.js** (v18.0.0 or higher) and **npm**.
- **Python** (v3.10, v3.11, or v3.12).
- *(Optional)* **Google Gemini API Key** (A key is recommended for live AI generation, but the built-in concept extraction engine works offline as well).

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/synapse-ai.git
cd synapse-ai
```

---

### Step 2: Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables:
   ```bash
   # Windows
   copy .env.example .env

   # macOS / Linux
   cp .env.example .env
   ```
   *(Open `.env` in your text editor and add your API key if you have one).*

5. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   *The interactive Swagger API documentation will be available at `http://localhost:8000/docs`.*

---

### Step 3: Frontend Setup (React + Vite)

1. Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Launch the Vite development server:
   ```bash
   npm run dev
   ```
   *The application will open at `http://localhost:5173`.*

---

## 🔐 Environment Variables

Create a `.env` file in the `backend/` directory based on the `.env.example` template:

```ini
# ==============================================================================
# SynapseAI Backend Configuration
# ==============================================================================

# Google Gemini API Key (Get yours from https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key_here

# Secret key for token signing (Random string)
SECRET_KEY=generate_a_secure_random_secret_key_for_production

# Database Connection (Defaults to SQLite for local development)
DATABASE_URL=sqlite+aiosqlite:///./app.db

# Storage directory for temporary audio files
UPLOAD_DIR=./downloads
```

> **Note:** The application includes a resilient offline concept extraction engine. If `GEMINI_API_KEY` is not provided or runs out of quota, summaries and quizzes will still generate automatically!

---

## 🚀 Usage Guide

1. **Visit the Landing Page**: Open `http://localhost:5173` in your browser. Review the features and click **"Try it Now"**.
2. **Input Study Material**:
   - In the **AI Summarizer** workspace (`/app`), paste any YouTube lecture or educational video URL into the input field.
   - Alternatively, click any of the **Quick-Start Example Videos** (Harvard, Stanford, TED) to test instantly.
   - Choose your tier: **Basic** (quick overview) or **Premium** (comprehensive multi-section deep dive).
3. **Generate Summary**: Click **"Generate Summary"**.
4. **Read & Review**:
   - Navigate through the **Executive Overview**, **In-Depth Breakdown**, **Concept Matrix**, and **Timeline Progression**.
   - Use the **Copy** button to copy formatted Markdown to your clipboard or **Save to Notes** for future exam prep.
5. **Take the Interactive Quiz**:
   - Click the **"Quiz"** tab.
   - Answer the multiple-choice questions one by one.
   - Submit the quiz to view your overall percentage score, correct answers, and conceptual explanations.

---

## 👥 Authors & Acknowledgments

- **Sneha Uday Naik** — *Full-Stack Development & AI Integration*
- **Sai Kumar Telang** — *Full-Stack Development & Architecture*

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute for academic and personal projects.
