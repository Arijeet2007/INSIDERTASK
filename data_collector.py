"""
Data Collection Module for SRM INSIDER Content
Collects and preprocesses content from various sources
"""

import json
import os
from datetime import datetime
from typing import List, Dict
import re

class SRMInsiderDataCollector:
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
    def collect_instagram_posts(self, posts_data: List[Dict]):
        """
        Collect Instagram posts data (manual collection or via API)
        
        Args:
            posts_data: List of post dictionaries with caption, hashtags, etc.
        """
        processed_posts = []
        for post in posts_data:
            processed = {
                "source": "instagram",
                "type": "post",
                "content": post.get("caption", ""),
                "hashtags": post.get("hashtags", []),
                "timestamp": post.get("timestamp", datetime.now().isoformat()),
                "likes": post.get("likes", 0),
                "comments_count": post.get("comments_count", 0),
            }
            processed_posts.append(processed)
        
        self._save_data(processed_posts, "instagram_posts.json")
        return processed_posts
    
    def collect_faq(self, faq_data: List[Dict]):
        """
        Collect FAQ data from students
        
        Args:
            faq_data: List of Q&A dictionaries
        """
        processed_faq = []
        for faq in faq_data:
            processed = {
                "source": "faq",
                "question": faq.get("question", ""),
                "answer": faq.get("answer", ""),
                "category": faq.get("category", "general"),
                "timestamp": datetime.now().isoformat(),
            }
            processed_faq.append(processed)
        
        self._save_data(processed_faq, "faq_data.json")
        return processed_faq
    
    def collect_student_reviews(self, reviews: List[Dict]):
        """
        Collect student reviews and experiences
        
        Args:
            reviews: List of review dictionaries
        """
        processed_reviews = []
        for review in reviews:
            processed = {
                "source": "student_review",
                "content": review.get("content", ""),
                "rating": review.get("rating", 0),
                "category": review.get("category", "general"),
                "year": review.get("year", ""),
                "branch": review.get("branch", ""),
                "timestamp": datetime.now().isoformat(),
            }
            processed_reviews.append(processed)
        
        self._save_data(processed_reviews, "student_reviews.json")
        return processed_reviews
    
    def collect_official_info(self, info_data: List[Dict]):
        """
        Collect official information from SRM website/documents
        
        Args:
            info_data: List of official information dictionaries
        """
        processed_info = []
        for info in info_data:
            processed = {
                "source": "official",
                "title": info.get("title", ""),
                "content": info.get("content", ""),
                "category": info.get("category", "general"),
                "url": info.get("url", ""),
                "timestamp": info.get("timestamp", datetime.now().isoformat()),
            }
            processed_info.append(processed)
        
        self._save_data(processed_info, "official_info.json")
        return processed_info
    
    def _save_data(self, data: List[Dict], filename: str):
        """Save data to JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(data)} records to {filepath}")
    
    def load_all_data(self) -> List[Dict]:
        """Load all collected data"""
        all_data = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_data.extend(data)
        return all_data
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text content"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text


# Example usage template
if __name__ == "__main__":
    collector = SRMInsiderDataCollector()
    
    # Example Instagram posts (you would collect these from the actual page)
    sample_posts = [
        {
            "caption": "SRM Tech Fest 2024 registrations are open! Join us for 3 days of innovation, workshops, and competitions. #SRMTechFest #Innovation",
            "hashtags": ["SRMTechFest", "Innovation", "SRM"],
            "timestamp": "2024-01-15T10:30:00",
            "likes": 1250,
            "comments_count": 87,
        },
        {
            "caption": "Placement season update: 95% of our students placed with average package of 8.5 LPA! Proud of our SRMians! #Placements #SRM",
            "hashtags": ["Placements", "SRM", "Career"],
            "timestamp": "2024-01-10T14:20:00",
            "likes": 2340,
            "comments_count": 156,
        },
    ]
    
    collector.collect_instagram_posts(sample_posts)