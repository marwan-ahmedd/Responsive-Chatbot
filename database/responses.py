from database.connector import *
import long_responses as long
import re
import time

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True
    
    # Loop through each word in the user message
    for word in user_message:
        # If the word is in the recognised words list, increase the probability
        if word in recognised_words:
            message_certainty += 1
    
    # Calculate the probability as a percentage
    percentage = float(message_certainty) / float(len(recognised_words))
    
    # Check if all required words are present in the user message
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break
    
    # If all required words are present in the user message, or single_response is True, return the probability
    if has_required_words or single_response:
        return int(percentage * 100)
    # If not all required words are present in the user message and single_response is False, return 0
    return 0

    
def get_response(user_input):
    # Connect to the database and create a cursor
    c = conn.cursor()
    # Retrieve all responses from the database
    c.execute('SELECT * FROM responses')
    responses = c.fetchall()
    # Initialize variables to keep track of the best response and its probability
    highest_prob = 0
    best_response = ''
    
    # Split the user input into a list of words, ignoring common punctuation
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    
    # Iterate over each response in the database
    for r in responses:
        # Calculate the probability of the response being a good match for the user input
        prob = message_probability(split_message, r[1].split(','), r[2], r[3].split(','))
        # If the probability is higher than the current highest probability, update the best response
        if prob > highest_prob:
            highest_prob = prob
            best_response = r[0]

    # If the highest probability is greater than 1 (meaning it's a good match), return the best response
    # Otherwise, return a generic unknown response
    return best_response if highest_prob > 1 else long.unknown()


def add_response(response, words, single_response=False, required_words=[]):
    # Create a cursor to interact with the database
    c = conn.cursor()
    
    # Execute an SQL query to insert the response and its details into the 'responses' table
    # The response, words, single_response, and required_words values are passed in as parameters
    # The words and required_words lists are joined into comma-separated strings before being inserted into the database
    c.execute('''
        INSERT INTO responses (response, words, single_response, required_words)
        VALUES (%s, %s, %s, %s)
    ''', (response, ','.join(words), single_response, ','.join(required_words)))
    
    # Commit the changes to the database
    conn.commit()

    
# Responses ----------------------------------------------------------------------------------
# add_response("Hello!", ['hello', 'hey', 'hello', 'yo', 'hi'], single_response=True)

# add_response("great, thanks for asking!", ['how', 'are', 'you', 'doing'], required_words=['how'])

# add_response("i'm glad to hear that!", ['good', 'great', 'fantastic', 'terrific'], required_words=['how', 'you'])

# add_response(long.R_SORRY, ['not', 'so', 'great', 'terrible', 'awful'], required_words=['how', 'you'])

# add_response("it's sunny today!", ['what', 'weather'], required_words=['how', 'weather', 'what'])

# add_response("looks like it's going to rain", ['what', 'weather'], required_words=['how', 'weather', 'what'])

# add_response("it's a bit chilly out", ['what', 'weather'], required_words=['how', 'is'])

# # Responses for asking about the time
# t = time.localtime()
# current_time = time.strftime("%H:%M:%S", t)
# add_response(f"It's currently {current_time}.", ['what', 'time', 'is', 'it'], required_words=['what'])

# # Responses for greeting
# add_response("Hello! How can I assist you?", ['hi', 'hello', 'hey', 'yo'], required_words=['hello', 'hi'])
# add_response("Good [morning/afternoon/evening]! How can I assist you?", ['good', 'morning', 'afternoon', 'evening'])

# # Responses for thanking
# add_response("You're welcome!", ['thank', 'thanks'], required_words=['thank'])
# add_response("No problem, happy to help!", ['thank', 'thanks', 'help'], required_words=['thank'])

# # Responses for asking about the bot
# add_response("I'm a chatbot designed to assist you with your inquiries!", ['who', 'are', 'you'], required_words=['who'])
# add_response("I was created by [your name or company name] to assist with inquiries.", ['who', 'created', 'you'], required_words=['who'])

# # Responses for asking for help
# add_response("What do you need help with?", ['help', 'assistance'], required_words=['help'])
# add_response("Sure, how can I assist you?", ['help', 'need'], required_words=['help'])

# # Responses for goodbye
# add_response("Goodbye! Have a great day!", ['bye', 'goodbye'], required_words=['bye'])
# add_response("Take care, goodbye!", ['bye', 'goodbye'], required_words=['bye'])
