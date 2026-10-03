import pytest
from httpx import AsyncClient, ASGITransport
import json
from app.main import app, startup
from app.services.youtube_service import YouTubeService
from app.models.summary import Summary
from app.models.quiz import Quiz
from app.database import SessionLocal

@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session", autouse=True)
async def init_test_db():
    await startup()

def test_youtube_video_id_extraction():
    url1 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    url2 = "https://youtu.be/dQw4w9WgXcQ?si=abcdef"
    url3 = "https://www.youtube.com/embed/dQw4w9WgXcQ"
    url4 = "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
    url5 = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
    url6 = "https://www.youtube.com/live/dQw4w9WgXcQ"
    url7 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL123&t=45s"
    url8 = "  https://youtu.be/dQw4w9WgXcQ  "
    
    assert YouTubeService.extract_video_id(url1) == "dQw4w9WgXcQ"
    assert YouTubeService.extract_video_id(url2) == "dQw4w9WgXcQ"
    assert YouTubeService.extract_video_id(url3) == "dQw4w9WgXcQ"
    assert YouTubeService.extract_video_id(url4) == "dQw4w9WgXcQ"
    assert YouTubeService.extract_video_id(url5) == "dQw4w9WgXcQ"
    assert YouTubeService.extract_video_id(url6) == "dQw4w9WgXcQ"
    assert YouTubeService.extract_video_id(url7) == "dQw4w9WgXcQ"
    assert YouTubeService.extract_video_id(url8) == "dQw4w9WgXcQ"

@pytest.mark.asyncio
async def test_auth_workflow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Register user
        reg_payload = {
            "email": "student@example.com",
            "password": "Password123!",
            "full_name": "Test Student"
        }
        res = await ac.post("/api/auth/register", json=reg_payload)
        assert res.status_code in [200, 400] # 200 on first run, 400 if already exists

        # Login
        login_res = await ac.post("/api/auth/login", json={
            "email": "student@example.com",
            "password": "Password123!"
        })
        assert login_res.status_code == 200
        token_data = login_res.json()
        assert "access_token" in token_data
        token = token_data["access_token"]

        # Get profile with bearer token
        headers = {"Authorization": f"Bearer {token}"}
        me_res = await ac.get("/api/auth/me", headers=headers)
        assert me_res.status_code == 200
        assert me_res.json()["email"] == "student@example.com"
        assert me_res.json()["full_name"] == "Test Student"

@pytest.mark.asyncio
async def test_quiz_submit_and_scoring():
    # Insert a dummy summary and quiz directly in DB for testing
    async with SessionLocal() as session:
        sample_summary = Summary(
            title="Introduction to Neural Networks",
            source_type="youtube",
            source_url="https://youtube.com/watch?v=demo",
            transcript="Neural networks are inspired by biological neurons.",
            summary_text="Overview of neural network basics and activation functions.",
            processing_tier="basic"
        )
        session.add(sample_summary)
        await session.commit()
        await session.refresh(sample_summary)

        sample_quiz_questions = [
            {
                "question": "What inspires artificial neural networks?",
                "options": ["Computer transistors", "Biological neurons", "Quantum particles", "Steam engines"],
                "correct_answer": "Biological neurons",
                "correct_index": 1,
                "explanation": "ANNs are directly modeled after interconnected biological neural structures.",
                "difficulty": "Easy",
                "concept_tested": "Bio-inspiration"
            },
            {
                "question": "What is the primary role of an activation function?",
                "options": ["Linear scaling", "Introducing non-linearity", "Cooling the CPU", "Storing data"],
                "correct_answer": "Introducing non-linearity",
                "correct_index": 1,
                "explanation": "Activation functions introduce non-linear properties to allow deep networks to learn complex functions.",
                "difficulty": "Medium",
                "concept_tested": "Activation functions"
            }
        ]

        sample_quiz = Quiz(
            summary_id=sample_summary.id,
            questions_json=json.dumps(sample_quiz_questions)
        )
        session.add(sample_quiz)
        await session.commit()
        await session.refresh(sample_quiz)
        quiz_id = sample_quiz.id

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Fetch quiz
        get_res = await ac.get(f"/api/quiz/{quiz_id}")
        assert get_res.status_code == 200
        data = get_res.json()
        assert len(data["questions"]) == 2
        assert data["questions"][0]["question"] == "What inspires artificial neural networks?"

        # Submit answers: 1st correct (index 1), 2nd incorrect (index 0)
        submit_payload = {
            "answers": {
                0: 1,
                1: 0
            }
        }
        submit_res = await ac.post(f"/api/quiz/{quiz_id}/submit", json=submit_payload)
        assert submit_res.status_code == 200
        result = submit_res.json()
        assert result["score"] == 1.0
        assert result["total"] == 2
        assert result["percentage"] == 50.0
        assert result["results"][0]["is_correct"] is True
        assert result["results"][1]["is_correct"] is False

@pytest.mark.asyncio
async def test_notes_crud_workflow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Login to get token
        login_res = await ac.post("/api/auth/login", json={
            "email": "student@example.com",
            "password": "Password123!"
        })
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create note via text endpoint (with mock AI service)
        from unittest.mock import patch
        mock_summary = {
            "summary": "This is a concise summary of photosynthesis.",
            "detailed_summary": "Detailed breakdown of Light reactions and Calvin cycle."
        }
        mock_quiz = [
            {
                "question": "Where does the Calvin cycle take place?",
                "options": ["Thylakoid", "Stroma", "Mitochondria", "Cytoplasm"],
                "correct_answer": "Stroma",
                "correct_index": 1,
                "explanation": "The light-independent reactions of photosynthesis occur in the stroma of chloroplasts.",
                "difficulty": "Medium",
                "concept_tested": "Cellular location"
            }
        ]

        with patch("app.services.ai_service.ai_service.summarize_text", return_value=mock_summary), \
             patch("app.services.ai_service.ai_service.generate_quiz", return_value=mock_quiz):
            create_res = await ac.post(
                "/api/summarize/text",
                json={"urls": [], "text": "Photosynthesis turns light into chemical energy.", "tier": "basic"},
                headers=headers
            )
            assert create_res.status_code == 200
            note_data = create_res.json()
            note_id = note_data["id"]
            assert note_data["summary_text"] == "This is a concise summary of photosynthesis."

        # List notes
        notes_res = await ac.get("/api/notes", headers=headers)
        assert notes_res.status_code == 200
        notes_list = notes_res.json()
        assert any(item["id"] == note_id for item in notes_list["items"])

        # Retrieve specific note
        get_note_res = await ac.get(f"/api/notes/{note_id}", headers=headers)
        assert get_note_res.status_code == 200
        assert get_note_res.json()["id"] == note_id

        # Delete note
        del_res = await ac.delete(f"/api/notes/{note_id}", headers=headers)
        assert del_res.status_code == 200

        # Verify deleted
        get_deleted_res = await ac.get(f"/api/notes/{note_id}", headers=headers)
        assert get_deleted_res.status_code == 404

