"""
SRM INSIDER LLM - Main Entry Point
Run this file to start the chatbot
"""

import os
import sys
from data_collector import SRMInsiderDataCollector
from vector_store import SRMVectorStore
from llm_engine import SRMLLMEngine, OllamaLLMEngine

def setup_knowledge_base():
    """Initialize and populate the knowledge base"""
    print("=" * 50)
    print("Setting up SRM INSIDER Knowledge Base")
    print("=" * 50)
    
    # Initialize components
    collector = SRMInsiderDataCollector()
    vector_store = SRMVectorStore()
    
    # Load existing data or create sample data
    all_data = collector.load_all_data()
    
    if not all_data:
        print("No existing data found. Creating sample knowledge base...")
        create_sample_data(collector)
        all_data = collector.load_all_data()
    
    # Add documents to vector store
    vector_store.add_documents(all_data)
    
    print(f"\nKnowledge base ready with {vector_store.get_collection_stats()['count']} documents")
    return vector_store

def create_sample_data(collector: SRMInsiderDataCollector):
    """Create sample SRM INSIDER data for demonstration"""
    
    # Sample Instagram-style posts
    instagram_posts = [
        {
            "source": "instagram",
            "content": "SRM Tech Fest 2024 registrations are open! Join us for 3 days of innovation, workshops, and competitions. Register at srmtechfest.com #SRMTechFest #Innovation",
            "category": "campus_events",
        },
        {
            "source": "instagram",
            "content": "Placement season update: 95% of our students placed with average package of 8.5 LPA! Top recruiters include Microsoft, Amazon, Google. #Placements #SRM",
            "category": "placements",
        },
        {
            "source": "instagram",
            "content": "Hostel mess menu updated! New vegan options available. Check the SRM app for weekly menu. #HostelLife #Food",
            "category": "hostel_life",
        },
        {
            "source": "instagram",
            "content": "Library extended hours during exam season! Open 24/7 from next week. Bring your ID card. #Exams #Library",
            "category": "academics",
        },
        {
            "source": "instagram",
            "content": "Coding Club workshop on AI/ML this Saturday 2PM in Block 5, Room 301. Limited seats, register fast! #CodingClub #AI",
            "category": "clubs_and_societies",
        },
        {
            "source": "instagram",
            "content": "Scholarship applications open for meritorious students. Deadline: 31st March. Check eligibility on portal. #Scholarships #Admissions",
            "category": "fees_and_scholarships",
        },
        {
            "source": "instagram",
            "content": "New shuttle bus route added from hostel to main campus. Timings: 7AM, 9AM, 5PM, 7PM. #Transport #Campus",
            "category": "transport",
        },
        {
            "source": "instagram",
            "content": "Pro tip: Use the SRM app for attendance tracking, marks viewing, and fee payment. Download now! #SRMApp #Tips",
            "category": "tips_and_tricks",
        },
    ]
    
    # Sample FAQ
    faq_data = [
        {
            "source": "faq",
            "question": "What is the cutoff for CSE at SRM?",
            "answer": "The cutoff for CSE varies each year based on JEE/Main ranks and category. Generally, rank under 50,000 for general category. Check official admission portal for current year cutoffs.",
            "category": "admissions",
        },
        {
            "source": "faq",
            "question": "How is the hostel food at SRM?",
            "answer": "Hostel mess provides vegetarian and non-vegetarian options. Menu changes weekly. Most students find it decent, with additional canteen options available on campus.",
            "category": "hostel_life",
        },
        {
            "source": "faq",
            "question": "What companies visit SRM for placements?",
            "answer": "Top recruiters include Microsoft, Amazon, Google, TCS, Infosys, Wipro, Cognizant, Zoho, and many startups. Average package: 6-8 LPA, highest: 40+ LPA.",
            "category": "placements",
        },
        {
            "source": "faq",
            "question": "Is attendance mandatory at SRM?",
            "answer": "Yes, 75% attendance is mandatory to appear for exams. Some relaxation available for medical reasons with proper documentation.",
            "category": "academics",
        },
        {
            "source": "faq",
            "question": "What are the major fests at SRM?",
            "answer": "Major fests include: Tech Fest (technical), Vision (cultural), Uthsava (sports), and various department symposiums throughout the year.",
            "category": "campus_events",
        },
    ]
    
    # Save sample data
    collector._save_data(instagram_posts, "instagram_posts.json")
    collector._save_data(faq_data, "faq_data.json")
    
    print(f"Created {len(instagram_posts)} sample posts and {len(faq_data)} FAQ entries")

def chat_loop(vector_store, llm_engine, use_ollama=False):
    """Main chat loop"""
    print("\n" + "=" * 50)
    print("🎓 SRM INSIDER Bot - Ready to Help!")
    print("=" * 50)
    print("Ask me anything about SRM University!")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        try:
            user_query = input("📝 You: ").strip()
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for using SRM INSIDER Bot! Good luck with your studies!")
                break
            
            if not user_query:
                continue
            
            # Search for relevant context
            print("\n🔍 Searching knowledge base...")
            results = vector_store.search(user_query, n_results=3)
            
            if results:
                context_docs = [doc for doc, meta, dist in results]
                print(f"📚 Found {len(context_docs)} relevant sources\n")
                
                # Generate response
                if use_ollama:
                    response = llm_engine.generate_response(user_query, "\n".join(context_docs))
                else:
                    response = llm_engine.generate_with_rag(user_query, context_docs)
                
                print(f"🤖 SRM INSIDER: {response}\n")
            else:
                print("🤖 SRM INSIDER: I couldn't find specific information about that. Try asking about placements, hostels, fests, academics, or campus life!\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

def main():
    """Main function"""
    print("\n🚀 Starting SRM INSIDER LLM System\n")
    
    # Choose LLM engine
    print("Select LLM Engine:")
    print("1. Ollama (Recommended - Easy setup)")
    print("2. HuggingFace Transformers (Advanced)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    use_ollama = choice == "1"
    
    # Setup knowledge base
    vector_store = setup_knowledge_base()
    
    # Initialize LLM engine
    print("\nInitializing LLM Engine...")
    if use_ollama:
        llm_engine = OllamaLLMEngine(model_name="mistral")
        print("Using Ollama with Mistral model")
    else:
        llm_engine = SRMLLMEngine()
        model_path = input("Enter model path (or press enter for default mistral-7b): ").strip()
        llm_engine.load_model(model_path if model_path else None)
    
    # Start chat
    chat_loop(vector_store, llm_engine, use_ollama)

if __name__ == "__main__":
    main()