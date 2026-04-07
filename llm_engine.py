"""
Local LLM Engine for SRM INSIDER
Handles model loading and inference
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from typing import List, Dict, Optional
import warnings

warnings.filterwarnings("ignore")

class SRMLLMEngine:
    def __init__(self, model_name: str = "mistral-7b-instruct-v0.2"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self, model_path: Optional[str] = None):
        """
        Load the LLM model
        
        Args:
            model_path: Path to local model (optional)
        """
        print(f"Loading model: {self.model_name} on {self.device}")
        
        if model_path:
            self.model_name = model_path
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )
        
        # Load model with appropriate settings based on available memory
        if self.device == "cuda":
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                device_map="auto",
                trust_remote_code=True,
            )
        
        # Create pipeline
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
        )
        
        print(f"Model loaded successfully on {self.device}")
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """
        Generate response from the model
        
        Args:
            prompt: User query
            context: Retrieved context from vector store
            
        Returns:
            Generated response
        """
        # Create formatted prompt with context
        system_prompt = """You are SRM INSIDER Bot, a helpful assistant for SRM University students.
You provide accurate, friendly, and helpful information about SRM University based on the context provided.
If you don't know something, be honest and suggest where students can find more information.
Always maintain a positive and supportive tone."""

        if context:
            full_prompt = f"""<s>[INST] {system_prompt}

Context Information:
{context}

User Question: {prompt}

Please provide a helpful answer based on the context above. If the context doesn't contain relevant information, use your general knowledge about SRM University but mention that the information might need verification. [/INST]"""
        else:
            full_prompt = f"""<s>[INST] {system_prompt}

User Question: {prompt}

Please provide a helpful answer. If you don't have specific information, mention that and suggest where students can find more information. [/INST]"""
        
        # Generate response
        try:
            outputs = self.pipeline(full_prompt)
            response = outputs[0]['generated_text']
            
            # Extract only the response part (after [/INST])
            if "[/INST]" in response:
                response = response.split("[/INST]")[-1].strip()
            
            return response
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def generate_with_rag(self, query: str, context_docs: List[str]) -> str:
        """
        Generate response using RAG (Retrieval-Augmented Generation)
        
        Args:
            query: User query
            context_docs: List of relevant documents from vector store
            
        Returns:
            Generated response
        """
        # Combine context documents
        context = "\n\n".join([f"Source {i+1}: {doc}" for i, doc in enumerate(context_docs)])
        
        return self.generate_response(query, context)
    
    def unload_model(self):
        """Unload model to free memory"""
        if self.model:
            del self.model
            del self.tokenizer
            del self.pipeline
            torch.cuda.empty_cache()
            print("Model unloaded")


# Alternative: Use Ollama for easier local deployment
class OllamaLLMEngine:
    """
    Simpler LLM engine using Ollama (recommended for most users)
    Install Ollama from: https://ollama.ai
    """
    
    def __init__(self, model_name: str = "mistral"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434"
        
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response using Ollama API"""
        import requests
        
        system_prompt = """You are SRM INSIDER Bot, a helpful assistant for SRM University students.
Provide accurate, friendly information about SRM University."""
        
        if context:
            full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion: {prompt}"
        else:
            full_prompt = f"{system_prompt}\n\nQuestion: {prompt}"
        
        try:
            response = requests.post(
                f"{self.base_url}/api/g