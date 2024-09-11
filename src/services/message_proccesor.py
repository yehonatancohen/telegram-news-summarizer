import re

def process_message(message):
    # Remove special characters and convert to lowercase
    cleaned_message = re.sub(r'[^a-zA-Z0-9\s]', '', message.lower())
    
    # Tokenize the message
    tokens = cleaned_message.split()
    
    # Remove stop words (common words that don't carry much meaning)
    stop_words = ['the', 'a', 'an', 'in', 'on', 'is', 'are', 'was', 'were']
    filtered_tokens = [token for token in tokens if token not in stop_words]
    
    # Join the filtered tokens back into a string
    processed_message = ' '.join(filtered_tokens)
    
    return processed_message