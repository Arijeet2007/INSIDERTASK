"""
Configuration settings for SRM INSIDER LLM System
"""

# Model Configuration
MODEL_CONFIG = {
    "model_name": "mistral-7b-instruct-v0.2",  # or "llama-2-7b-chat", "phi-2", etc.
    "model_path": "./models/mistral-7b-instruct",
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
}

# Vector Database Configuration
VECTOR_DB_CONFIG = {
    "db_path": "./vector_db/srm_insider_db",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "chunk_size": 500,
    "chunk_overlap": 50,
}

# SRM INSIDER Knowledge Categories
KNOWLEDGE_CATEGORIES = [
    "campus_events",
    "festivals",
    "placements",
    "academics",
    "hostel_life",
    "clubs_and_societies",
    "examinations",
    "infrastructure",
    "food_and_canteen",
    "transport",
    "admissions",
    "fees_and_scholarships",
    "student_experiences",
    "tips_and_tricks",
    "recent_updates",
]

# Instagram Content Sources (to be collected manually or via API)
CONTENT_SOURCES = [
    "instagram_posts",
    "instagram_stories",
    "instagram_reels",
    "instagram_comments",
    "official_website",
    "student_feedback",
]