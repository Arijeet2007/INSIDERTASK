# 🎓 SRM INSIDER LLM - Student Query Assistant

A local LLM-powered chatbot trained to answer student queries about SRM University, based on content from SRM INSIDER Instagram and other sources.

## 📋 Prerequisites

### Option 1: Ollama (Recommended - Easier)
1. **Install Ollama**: Download from https://ollama.ai
2. **Pull a model**: Run `ollama pull mistral` in terminal
3. **Verify**: Run `ollama run mistral` to test

### Option 2: HuggingFace Transformers (Advanced)
- Python 3.8+
- GPU recommended (8GB+ VRAM for 7B models)
- At least 16GB RAM for CPU inference

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python src/main.py
```

### Step 3: Chat!
Ask questions like:
- "What is the placement scenario at SRM?"
- "How is hostel food?"
- "When is Tech Fest?"
- "What is the attendance requirement?"
- "Tell me about scholarships"

## 📁 Project Structure
```
srm_insider_llm/
├── src/
│   ├── main.py           # Entry point
│   ├── data_collector.py # Data collection
│   ├── vector_store.py   # Vector database
│   ├── llm_engine.py     # LLM inference
│   └── config.py         # Configuration
├── data/                 # Collected data (auto-created)
├── vector_db/            # Vector database (auto-created)
├── models/               # Downloaded models (auto-created)
├── requirements.txt
└── README.md
```

## 🔄 Adding Your Own Data

### Method 1: Instagram Data Collection
Create a script to collect posts from @srm.insider:

```python
from data_collector import SRMInsiderDataCollector

collector = SRMInsiderDataCollector()

posts = [
    {
        "source": "instagram",
        "content": "Your post content here...",
        "category": "campus_events",
    },
    # Add more posts...
]

collector._save_data(posts, "instagram_posts.json")
```

### Method 2: Manual JSON Files
Add JSON files to the `data/` folder with this format:
```json
[
  {
    "source": "instagram",
    "content": "Post content...",
    "category": "placements"
  }
]
```

### Method 3: Rebuild Vector Database
```bash
python src/main.py
# When prompted, choose to rebuild knowledge base
```

## ⚙️ Configuration

Edit `src/config.py` to customize:
- Model name and path
- Vector database settings
- Knowledge categories
- Response parameters

## 🎯 Example Queries

| Category | Example Questions |
|----------|------------------|
| Placements | "What companies visit SRM?", "Average package?" |
| Academics | "Attendance rules?", "Exam schedule?" |
| Hostel | "Hostel food quality?", "Room allocation?" |
| Events | "When is Tech Fest?", "Club activities?" |
| Admissions | "Cutoff for CSE?", "Scholarship info?" |
| Campus | "Library timings?", "Transport facilities?" |

## 🛠️ Troubleshooting

### Ollama not working?
```bash
# Check if Ollama is running
ollama list

# Restart Ollama service
# Windows: Check system tray
# Linux: sudo systemctl restart ollama
```

### Out of memory?
- Use smaller model: `ollama pull phi` (2.7B)
- Reduce batch size in config
- Use CPU mode (slower but works)

### No relevant answers?
- Add more data to the knowledge base
- Check vector_db is populated
- Verify data format in JSON files

## 📝 Notes

- Instagram content must be collected manually or via official API
- This is a local system - no data leaves your computer
- Responses are based on provided knowledge base
- Always verify critical information from official sources

## 🤝 Contributing

Add more SRM-related content to improve the bot's knowledge!

## 📄 License

Educational use only. Respect SRM University's policies.
```

Now let me create a simple setup script:

```bash setup.sh
#!/bin/bash
# SRM INSIDER LLM - Setup Script

echo "🎓 SRM INSIDER LLM - Setup"
echo "=========================="

# Check Python
echo -e "\n📌 Checking Python..."
python --version || python3 --version

# Create virtual environment
echo -e "\n📌 Creating virtual environment..."
python -m venv venv || python3 -m venv venv

# Activate virtual environment
echo -e "\n📌 Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo -e "\n📌 Installing dependencies..."
pip install -r requirements.txt

# Create directories
echo -e "\n📌 Creating directories..."
mkdir -p data vector_db models

# Check Ollama
echo -e "\n📌 Checking Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found!"
    ollama pull mistral
else
    echo "⚠️  Ollama not found. Install from https://ollama.ai"
    echo "   Or use HuggingFace option when running"
fi

echo -e "\n✅ Setup complete!"
echo -e "\n🚀 Run with: python src/main.py"
```

```powershell setup.ps1
# SRM INSIDER LLM - Setup Script (Windows PowerShell)

Write-Host "🎓 SRM INSIDER LLM - Setup" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan

# Check Python
Write-Host "`n📌 Checking Python..." -ForegroundColor Yellow
python --version

# Create virtual environment
Write-Host "`n📌 Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "`n📌 Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "`n📌 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create directories
Write-Host "`n📌 Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path data
New-Item -ItemType Directory -Force -Path vector_db
New-Item -ItemType Directory -Force -Path models

# Check Ollama
Write-Host "`n📌 Checking Ollama..." -ForegroundColor Yellow
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Write-Host "✅ Ollama found!" -ForegroundColor Green
    ollama pull mistral
} else {
    Write-Host "⚠️  Ollama not found. Install from https://ollama.ai" -ForegroundColor Yellow
    Write-Host "   Or use HuggingFace option when running" -ForegroundColor Yellow
}

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`n🚀 Run with: python src/main.py" -ForegroundColor Cyan
```

## 🎯 How to Run - Quick Guide

### **Option 1: Using Ollama (Easiest)**

```bash
# 1. Install Ollama from https://ollama.ai

# 2. Pull a model
ollama pull mistral

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run the application
python src/main.py

# 5. Choose option 1 (Ollama) when prompted
```

### **Option 2: Using HuggingFace (Advanced)**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python src/main.py

# 3. Choose option 2 (HuggingFace)
# 4. Enter model path or use default
```

### **Sample Conversation**
