import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
import sys

class MediniChatbot:
    def __init__(self, data_path=None):
        # Default or custom data path
        self.data_path = data_path or r"e:\proooo\techvriti\dataset\train.csv"
        
        # Load full dataset with robust error handling
        try:
            # Read CSV with explicit encoding and error handling
            self.df = pd.read_csv(
                self.data_path, 
                encoding='utf-8', 
                encoding_errors='replace',
                on_bad_lines='skip'
            )
            
            # Validate columns (case-insensitive)
            columns = [col.lower() for col in self.df.columns]
            if 'query' not in columns or 'answer' not in columns:
                raise ValueError("CSV must have 'Query' and 'Answer' columns")
            
            # Normalize column names
            self.df.columns = [col.lower() for col in self.df.columns]
            
            # Drop rows with missing data
            self.df.dropna(subset=['query', 'answer'], inplace=True)
            
            # Preprocess questions and answers
            self.df['query'] = self.df['query'].str.lower().str.strip()
            self.df['answer'] = self.df['answer'].str.strip()
            
            # Create lists for vectorization
            self.questions = self.df['query'].tolist()
            self.answers = self.df['answer'].tolist()
            
            print(f"Loaded {len(self.questions)} question-answer pairs from {self.data_path}")
        
        except Exception as e:
            print(f"Error loading dataset: {e}")
            self.questions = []
            self.answers = []
        
        # Initialize TF-IDF Vectorizer with advanced settings
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            token_pattern=r'(?u)\b\w+\b',
            max_features=5000,  # Reduced for performance
            ngram_range=(1, 2)  # Capture phrase-level semantics
        )
        
        # Fit vectorizer if questions exist
        if len(self.questions) > 0:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)
        else:
            self.tfidf_matrix = None
    
    def preprocess_text(self, text):
        """Advanced text preprocessing"""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def get_response(self, user_query, threshold=0.3):
        """
        Intelligent response generation with advanced matching
        """
        # Check if TF-IDF matrix is None or empty
        if self.tfidf_matrix is None or self.tfidf_matrix.shape[0] == 0:
            return "I apologize, but my knowledge base is currently empty."
        
        # Preprocess query
        processed_query = self.preprocess_text(user_query)
        
        # Vectorize query
        query_vector = self.vectorizer.transform([processed_query])
        
        # Compute cosine similarities
        cosine_similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Find top matches
        top_indices = cosine_similarities.argsort()[::-1][:3]
        
        # Select best match above threshold
        for idx in top_indices:
            if cosine_similarities[idx] > threshold:
                return self.answers[idx]
        
        # Fallback response
        return "I'm not certain about that. Could you rephrase or ask something else?"

# Interactive mode
if __name__ == "__main__":
    chatbot = MediniChatbot()
    print("Medini Chatbot: Hello! How Can i Assist you?")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Medini Chatbot: Goodbye!")
                break
            
            response = chatbot.get_response(user_input)
            print("Bot:", response)
        
        except KeyboardInterrupt:
            print("\nMedini Chatbot: Exiting...")
            break