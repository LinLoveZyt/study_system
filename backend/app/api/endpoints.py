# app/api/endpoints.py
from fastapi import APIRouter, HTTPException, Body
from ..services import profile_manager, task_manager
from typing import Dict, Any, List

router = APIRouter()

@router.get("/profile/check", summary="Check if User Profile Exists")
def check_user_profile():
    """Checks if the default user profile JSON file exists."""
    return {"profile_exists": profile_manager.check_profile_exists()}

@router.get("/profile", summary="Get User Profile")
def get_user_profile():
    """Retrieves the user's profile if it exists."""
    profile = profile_manager.get_profile()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found.")
    return profile

@router.post("/profile/create", summary="Create User Profile")
def create_user_profile(assessment_data: Dict[str, Any] = Body(...)):
    """
    Receives assessment data from the frontend, generates a user profile via LLM,
    and saves it.
    """
    profile = profile_manager.create_profile(assessment_data)
    if not profile:
        raise HTTPException(status_code=500, detail="Failed to create user profile. LLM might have failed to generate valid JSON.")
    return profile

@router.get("/tasks", summary="Get All Learning Tasks", response_model=List[Dict[str, Any]])
def get_all_learning_tasks():
    """Retrieves metadata for all created learning tasks."""
    return task_manager.get_all_tasks()

@router.post("/tasks/create", summary="Create a New Learning Task")
def create_new_learning_task(task_request: Dict[str, Any] = Body(...)):
    """
    Creates a new learning task. This involves:
    1. Getting the user profile.
    2. Calling the LLM to generate learning material JSON.
    3. Calling the service to generate a PDF from the JSON.
    4. Saving all artifacts and returning task metadata.
    """
    try:
        task_metadata = task_manager.create_learning_task(task_request)
        if not task_metadata:
            raise HTTPException(status_code=500, detail="Failed to create learning task.")
        return task_metadata
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Catch-all for other potential errors during task creation
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

