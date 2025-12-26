"""
Session & Usage Routes
=======================
Endpoints for session management and usage statistics.
"""

from fastapi import APIRouter, HTTPException, status

from ..services import session_manager, usage_logger


router = APIRouter(tags=["Session & Usage"])


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get current session state (for debugging/recovery)."""
    session = session_manager.get(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    return {
        "session_id": session.session_id,
        "has_text": session.post_text is not None,
        "has_hashtags": session.hashtags is not None,
        "has_image_prompts": session.image_prompts is not None,
        "has_images": session.generated_images is not None,
        "text_model": session.text_model_used,
        "image_model": session.image_model_used,
    }


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    deleted = session_manager.delete(session_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    return {"message": "Session deleted"}


@router.get("/usage")
async def get_usage():
    """Get usage statistics."""
    return usage_logger.get_usage()

