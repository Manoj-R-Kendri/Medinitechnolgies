import os
import logging
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

class CADChatbot:
    """
    Chatbot class for handling intelligent responses using cosine similarity.
    
    Attributes:
        vectorizer (TfidfVectorizer): Text vectorization tool.
        responses (list): Collection of predefined responses.
        data (pd.DataFrame): Dataset containing training data.
    """

    def __init__(self, csv_path='dataset.csv'):
        """
        Initialize the CADChatbot with training data.

        Args:
            csv_path (str, optional): Path to the CSV file. Defaults to 'dataset.csv'.
        
        Raises:
            FileNotFoundError: If the dataset file is not found.
            ValueError: If the dataset is empty or improperly formatted.
        """
        try:
            self.data = pd.read_csv(csv_path)
            
            if self.data.empty:
                raise ValueError("Dataset is empty")
            
            if 'question' not in self.data.columns or 'answer' not in self.data.columns:
                raise ValueError("Dataset must contain 'question' and 'answer' columns")
            
            self.vectorizer = TfidfVectorizer()
            self.tfidf_matrix = self.vectorizer.fit_transform(self.data['question'])
            logging.info('Chatbot initialized successfully')
        
        except FileNotFoundError:
            logging.error('Dataset file not found: %s', csv_path)
            raise
        except ValueError as ve:
            logging.error('Dataset validation error: %s', str(ve))
            raise

    def get_response(self, user_input):
        """
        Generate an intelligent response based on user input.

        Args:
            user_input (str): The input text from the user.

        Returns:
            str: The most relevant response from the dataset.
        
        Raises:
            ValueError: If user input is invalid or processing fails.
        """
        try:
            if not user_input or not isinstance(user_input, str):
                raise ValueError("Invalid user input")
            
            user_tfidf = self.vectorizer.transform([user_input])
            cosine_scores = cosine_similarity(user_tfidf, self.tfidf_matrix)[0]
            best_match_index = cosine_scores.argmax()
            
            logging.info('Response generated for input: %s', user_input)
            return self.data.loc[best_match_index, 'answer']
        
        except ValueError as ve:
            logging.error('Value error in response generation: %s', str(ve))
            return "I'm sorry, I couldn't understand your question."
        except IndexError:
            logging.error('No matching response found for input')
            return "I don't have a suitable response for that query."

    def train_model(self, new_questions, new_answers):
        """
        Update the chatbot's knowledge base with new training data.

        Args:
            new_questions (list): List of new questions.
            new_answers (list): Corresponding list of answers.
        
        Raises:
            ValueError: If input lists are invalid or mismatched.
        """
        try:
            if len(new_questions) != len(new_answers):
                raise ValueError("Questions and answers lists must be of equal length")
            
            new_data = pd.DataFrame({
                'question': new_questions,
                'answer': new_answers
            })
            self.data = pd.concat([self.data, new_data], ignore_index=True)
            self.tfidf_matrix = self.vectorizer.fit_transform(self.data['question'])
            logging.info('Model trained with %d new samples', len(new_questions))
        
        except ValueError as ve:
            logging.error('Error training model: %s', str(ve))
            raise

# Flask Application Setup
app = Flask(__name__)
chatbot = CADChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat requests and return bot responses.

    Returns:
        JSON response with the chatbot's answer.
    
    Raises:
        ValueError: If request is invalid.
    """
    try:
        data = request.get_json()
        
        if not data:
            raise ValueError("No JSON data received")
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        bot_response = chatbot.get_response(user_message)
        logging.info('Chat request processed successfully')
        
        return jsonify({'response': bot_response})
    
    except ValueError as ve:
        logging.error('Value error in chat endpoint: %s', str(ve))
        return jsonify({'error': 'Invalid request'}), 400

def main():
    """
    Main function to run the Flask application.
    """
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()