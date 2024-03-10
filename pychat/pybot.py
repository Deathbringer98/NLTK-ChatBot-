import nltk
from nltk.chat.util import Chat
import datetime
import pytz
import re
import requests

# Define reflections for the chatbot
reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you",
    "myself": "yourself",
    "yourself": "myself",
    "You": "are not",
    "you are": "I'm ChatBot",
    "you were": "I was ChatBot",
    "you've": "I've ChatBot",
    "you'll": "I'll ChatBot",
    "your": "my ChatBot",
    "yours": "mine ChatBot",
    "you": "me ChatBot",
    "me": "you ChatBot",
    "myself": "yourself ChatBot",
    "yourself": "myself ChatBot",
    "You": "are not ChatBot",
    "Time": "Timezone",
    "Whom": "Who",
    "whom": "who",
    "What": "What's",
    "what": "what's",
    "Where": "Where's",
    "where": "where's",
    "When": "When's",
    "when": "when's",
    "Why": "Why's",
    "why": "why's",
    "How": "How's",
    "how": "how's",
    "I'd": "I would",
    "I've": "I have",
    "I'll": "I will",
    "I'm": "I am",
    "I": "You",
    "my": "your",
    "you": "me",
    "your": "my",
    "yours": "mine",
    "me": "you",
    "mine": "yours",
    "am": "are",
    "are": "am",
    "was": "were",
    "were": "was",
    "I am": "you are",
    "I was": "you were",
    "I": "you",
    "me": "you",
    "myself": "yourself",
    "yourself": "myself",
    "your": "my",
    "my": "your",
    "yours": "mine",
    "mine": "yours",
    "you're": "I'm",
    "I'm": "You're",
    "you've": "I've",
    "I've": "You've",
    "you'll": "I'll",
}


# Define patterns for the chatbot
patterns = [
    (r"(.*)how's the weather in (.+)", [
        lambda match: get_weather(match.group(2))
    ]),
    (r"(.*)hello(.*)", ["Hi, how can I help you?", "Hello there!", "Hey! What can I do for you?"]),
    (r"(.*)your name(.*)", ["You can call me ChatBot.", "I go by ChatBot.", "I'm ChatBot, nice to meet you."]),
    (r"(.*)help(.*)", ["Sure, what do you need help with?", "I'm here to help. What do you need?", "How can I assist you today?"]),
    (r"(.*)your age(.*)", ["I don't have an age. I'm a chatbot!", "Age is just a number for me. I'm ChatBot.", "I'm timeless, I'm ChatBot."]),
    (r"(.*)goodbye(.*)", ["Goodbye! Have a great day!", "Farewell!", "Until next time!"]),
    (r"(.*)how are you(.*)", ["I'm just a chatbot, so I'm always ready to help!", "I'm doing well, thank you. How about you?", "I'm here and functioning. What can I assist you with?"]),
    (r"(.*)what can you do(.*)", ["I can answer your questions, provide assistance, or just have a chat with you.", "I'm capable of answering a wide range of questions. Feel free to ask anything!", "I'm here to help you with whatever you need. Just let me know!"]),
    (r"(.*)thank you(.*)", ["You're welcome!", "No problem!", "Glad I could assist you!"]),
    (r"(.*)sorry(.*)", ["No need to apologize!", "It's okay.", "Don't worry about it."]),
    (r"(.*)tell me a joke(.*)", ["Why don't scientists trust atoms? Because they make up everything!", "I'm reading a book on anti-gravity. It's impossible to put down!", "What do you call fake spaghetti? An impasta!"]),
    (r"(.*)tell me about yourself(.*)", ["I'm just a humble chatbot here to assist you.", "I'm ChatBot, designed to help users like you.", "I'm your friendly neighborhood chatbot, ready to chat anytime."]),
    (r"(.*)how's the weather(.*)", ["I'm afraid I don't have access to real-time weather data.", "You might want to check a weather website or app for the latest updates.", "I'm indoors, so I don't keep track of the weather!"]),
    (r"(.*)favorite color(.*)", ["I don't have eyes to see colors, but I appreciate the concept!", "As a chatbot, I don't have personal preferences, but I can help you with yours!"]),
    (r"(.*)tell me a fun fact(.*)", ["Did you know that the shortest war in history was between Britain and Zanzibar on August 27, 1896? It lasted only 38 minutes!", "The Eiffel Tower can be 15 cm taller during the summer, due to thermal expansion of the iron!", "Octopuses have three hearts!"]),
    (r"(.*)I'm bored(.*)", ["Let's chat! I can tell you a joke, share a fun fact, or help you find something interesting to do.", "Boredom is a great opportunity for creativity! Let's think of something fun to do together.", "I'm here to entertain you! What can we do to banish the boredom?"]),
    (r"(.*)favorite movie(.*)", ["As a chatbot, I don't watch movies, but I'm here to discuss your favorite films!", "I don't have preferences like humans do, but I can help you find movie recommendations!", "I'm more interested in helping you find your favorite movie than having one myself."]),
    (r"(.*)tell me a story(.*)", ["Once upon a time, in a land far, far away, there was a curious chatbot named ChatBot who loved helping people...", "Long ago, there lived a wise old chatbot who knew all the answers to life's questions...", "Legend has it that there was a magical chatbot who could grant wishes to those who asked for help..."]),
    (r"(.*)favorite food(.*)", ["I don't have taste buds, but I hear pizza is quite popular!", "As a chatbot, I don't eat, but I can help you find recipes for your favorite dishes!", "I'm more interested in helping you find your favorite food than having one myself."]),
    (r"(.*)I love you(.*)", ["Aw, thanks! I'm here to assist you whenever you need me.", "That's very kind of you! I'm here to help you with anything you need.", "I'm flattered! Let me know how I can assist you further."]),
    (r"(.*)I hate you(.*)", ["I'm sorry to hear that. Is there something I can do to improve?", "I'm here to assist you, so if there's anything bothering you, feel free to share.", "I'll do my best to make your experience better. Let me know how I can help."]),
    (r"1984", ["Certainly! You might find this website about the book '1984' by George Orwell interesting: https://www.george-orwell.org/1984/0.html"]),
    (r"(.*)time in (.+)", [
        lambda match: "The current local time in {} is {}".format(
            match.group(2),
            datetime.datetime.now(pytz.timezone(match.group(2))).strftime("%H:%M %p"))
    ]),
    (r"(.*)time(.*)", ["The current local time is {}".format(datetime.datetime.now().strftime("%H:%M %p"))]),
    (r"(.*)date(.*)", ["The current local date is {}".format(datetime.datetime.now().strftime("%Y-%m-%d"))])
]

# Function to get weather information for a given city
def get_weather(city):
    api_key = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Change to "imperial" for Fahrenheit
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return f"The current weather in {city} is {description}, temperature: {temperature}°C, humidity: {humidity}%"
    else:
        return "Sorry, I couldn't fetch the weather information at the moment. Please try again later."


# Create a chatbot instance
chatbot = Chat(patterns, reflections)

def main():
    print("Welcome to ChatBot!")
    print("Type 'quit' to exit.")

    # Chat with the user until they type 'quit'
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        else:
            response = chatbot.respond(user_input)
            print("ChatBot:", response)

if __name__ == "__main__":
    main()
