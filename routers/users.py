from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from .auth import get_current_active_user, User

# Create router
router = APIRouter()

# Models
class UserProfile(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[dict] = None

class UserProfileUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[dict] = None

# Mock database - in a real app, this would be a database
fake_profiles_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "full_name": "John Doe",
        "bio": "I am a student interested in computer science and mathematics.",
        "avatar_url": "https://example.com/avatars/johndoe.jpg",
        "preferences": {
            "theme": "dark",
            "notifications": True,
            "study_reminder": True
        }
    }
}

# Routes
@router.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get the current user's profile.
    """
    if current_user.username not in fake_profiles_db:
        # Create a default profile if it doesn't exist
        fake_profiles_db[current_user.username] = {
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "bio": None,
            "avatar_url": None,
            "preferences": {
                "theme": "light",
                "notifications": True,
                "study_reminder": False
            }
        }
    
    return fake_profiles_db[current_user.username]

@router.put("/profile", response_model=UserProfile)
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update the current user's profile.
    """
    # Get existing profile or create default
    if current_user.username not in fake_profiles_db:
        fake_profiles_db[current_user.username] = {
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "bio": None,
            "avatar_url": None,
            "preferences": {
                "theme": "light",
                "notifications": True,
                "study_reminder": False
            }
        }
    
    # Update profile with new values
    current_profile = fake_profiles_db[current_user.username]
    
    if profile_update.email is not None:
        current_profile["email"] = profile_update.email
    
    if profile_update.full_name is not None:
        current_profile["full_name"] = profile_update.full_name
    
    if profile_update.bio is not None:
        current_profile["bio"] = profile_update.bio
    
    if profile_update.avatar_url is not None:
        current_profile["avatar_url"] = profile_update.avatar_url
    
    if profile_update.preferences is not None:
        # Merge preferences instead of replacing
        if "preferences" not in current_profile:
            current_profile["preferences"] = {}
        
        current_profile["preferences"].update(profile_update.preferences)
    
    # Save updated profile
    fake_profiles_db[current_user.username] = current_profile
    
    return current_profile

@router.get("/preferences")
async def get_user_preferences(current_user: User = Depends(get_current_active_user)):
    """
    Get the current user's preferences.
    """
    if current_user.username not in fake_profiles_db:
        return {
            "theme": "light",
            "notifications": True,
            "study_reminder": False
        }
    
    return fake_profiles_db[current_user.username].get("preferences", {})

@router.put("/preferences")
async def update_user_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_active_user)
):
    """
    Update the current user's preferences.
    """
    # Get existing profile or create default
    if current_user.username not in fake_profiles_db:
        fake_profiles_db[current_user.username] = {
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "bio": None,
            "avatar_url": None,
            "preferences": {}
        }
    
    # Update preferences
    if "preferences" not in fake_profiles_db[current_user.username]:
        fake_profiles_db[current_user.username]["preferences"] = {}
    
    fake_profiles_db[current_user.username]["preferences"].update(preferences)
    
    return fake_profiles_db[current_user.username]["preferences"] 