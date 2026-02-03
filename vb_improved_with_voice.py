import sys
import random
import requests
import pyttsx3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QMessageBox
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QFont, QBrush
from PyQt5.QtCore import Qt
import secrets

class VocabularyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vocabulary Builder")
        self.setGeometry(100, 100, 800, 500)
        self.create_ui()


        # Predefined set of easy words
        self.easy_words_set = {
            "apple", "banana", "ball", "bird", "book", "boy", "car", "cat", "chair", "chicken",
            "clock", "dog", "door", "egg", "elephant", "family", "fish", "flower", "friend", "girl",
            "goat", "grass", "hand", "house", "kitten", "leaf", "lemon", "library", "monkey", "moon",
            "mouse", "orange", "paper", "pencil", "rabbit", "school", "sheep", "shoe", "snow", "sun",
            "table", "tree", "turtle", "water", "window", "word", "zoo"
            # Verbs
    "act", "add", "ask", "bake", "walk", "run", "jump", "play", "eat", "drink",
    "read", "write", "sing", "dance", "draw", "laugh", "help", "see", "hear", "talk",
    "swim", "clean", "watch", "open", "close", "teach", "learn", "build", "catch", "throw",
    "kick", "climb", "push", "pull", "stop", "start", "buy", "sell", "move", "fix",
    "paint", "travel", "play",

    # Adjectives
    "big", "small", "happy", "sad", "fast", "slow", "hot", "cold", "bright", "dark",
    "clean", "dirty", "good", "bad", "old", "young", "tall", "short", "fat", "thin",
    "soft", "hard", "sweet", "sour", "loud", "quiet", "pretty", "ugly", "easy", "difficult",
    "nice", "mean", "funny", "serious", "friendly",

    # Adverbs
    "quickly", "slowly", "happily", "sadly", "loudly", "quietly", "carefully", "easily", 
    "often", "sometimes", "always", "never", "here", "there", "everywhere", "nowhere", 
    "away", "back", "forward", "inside", "outside", "together", "apart", "straight", "round",

    # Pronouns
    "I", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",

    # Prepositions
    "on", "in", "under", "over", "next", "between", "beside", "around", "through", 
    "behind", "in front of", "above", "below", "at", "with", "about", "for", "to",

    # Conjunctions
    "and", "but", "or", "so", "because", "if", "when", "although", "while", "unless",

    # Colors
    "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black", "white",

    # Days and Months
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", 
    "January", "February", "March", "April", "May", "June", "July", "August", 
    "September", "October", "November", "December",

    # Numbers
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", 
    "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", 
    "eighty", "ninety", "hundred",

    # Family
    "mother", "father", "sister", "brother", "aunt", "uncle", "cousin", "grandmother", 
    "grandfather", "parent",

    # School
    "teacher", "student", "class", "desk", "book", "paper", "pencil", "eraser", 
    "notebook", "homework",

    # Food
    "bread", "butter", "cheese", "chicken", "cookie", "cereal", "salad", "soup", 
    "rice", "pasta", "pizza",

    # Animals
    "horse", "cow", "pig", "duck", "bear", "lion", "tiger", "rabbit", "deer", "fox",

    # Miscellaneous
    "watermelon", "peach", "grape", "strawberry", "kiwi", "coconut", "pancake", 
    "sandwich", "popcorn", "chips", "carrot", "onion", "tomato", "peanut", 
    "chocolate", "vanilla", "marshmallow", "candy", "cake", "cookie", "jam", 
    "pudding", "soda", "tea", "coffee", "juice", "milk", "yogurt", "cheesecake", 
    "brownie", "donut", "pie", "cereal", "snack", "dinner", "breakfast", "lunch", 
    "feast", "picnic", "party", "birthday", "celebration", "holiday", "vacation",
        }
        # Set the random daily word
        self.set_daily_word()

        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()

    def create_ui(self):
        # Set a gradient background
        gradient = QLinearGradient(0, 0, 0, 500)
        gradient.setColorAt(0, QColor(255, 204, 204))  # Light pink
        gradient.setColorAt(1, QColor(204, 204, 255))  # Light blue

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        main_layout = QHBoxLayout()

        # Sidebar layout for Easy Level daily word
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(20)

        # Easy level label
        easy_level_label = QLabel("Easy Level Word of the Day")
        easy_level_label.setFont(QFont("Arial", 20, QFont.Bold))
        easy_level_label.setStyleSheet("color: #4B0082;")
        easy_level_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(easy_level_label)

        # Daily word label
        self.daily_word_label = QLabel("", self)
        self.daily_word_label.setFont(QFont("Arial", 24))
        self.daily_word_label.setAlignment(Qt.AlignCenter)
        self.daily_word_label.setStyleSheet("color: #4B0082; margin-top: 10px; padding: 15px;")
        sidebar_layout.addWidget(self.daily_word_label)

        # Button to get a new random word
        self.new_word_button = QPushButton("New Word", self)
        self.new_word_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.new_word_button.setStyleSheet(
            "background-color: #FF69B4; color: white; padding: 15px; border-radius: 10px; font-size: 20px; border: none;"
        )
        self.new_word_button.setFixedHeight(50)
        self.new_word_button.clicked.connect(self.set_daily_word)
        sidebar_layout.addWidget(self.new_word_button)

        # Button for voice pronunciation of the daily word
        self.daily_word_voice_button = QPushButton("Pronounce Word", self)
        self.daily_word_voice_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.daily_word_voice_button.setStyleSheet(
            "background-color: #FF69B4; color: white; padding: 15px; border-radius: 10px; font-size: 20px; border: none;"
        )
        self.daily_word_voice_button.setFixedHeight(50)
        self.daily_word_voice_button.clicked.connect(self.pronounce_daily_word)
        sidebar_layout.addWidget(self.daily_word_voice_button)

        # Add a vertical line separator
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #4B0082;")
        main_layout.addLayout(sidebar_layout)
        main_layout.addWidget(line)

        # Main app layout for input and meaning display
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)

        # Title label
        title_label = QLabel("Vocabulary Builder", self)
        title_font = QFont("Arial", 28, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #4B0082;")
        content_layout.addWidget(title_label)

        # Input label and line edit
        self.label = QLabel("Enter a word:", self)
        self.label.setFont(QFont("Arial", 20))
        self.label.setStyleSheet("color: #4B0082;")
        content_layout.addWidget(self.label)

        self.word_input = QLineEdit(self)
        self.word_input.setFont(QFont("Arial", 20))
        self.word_input.setStyleSheet("padding: 10px; border-radius: 10px; border: 1px solid #4B0082;")
        content_layout.addWidget(self.word_input)

        self.result_label = QLabel("", self)
        self.result_label.setFont(QFont("Arial", 20))
        self.result_label.setStyleSheet("color: #4B0082; padding: 20px; background-color: #F8F0FF; border-radius: 10px;")
        self.result_label.setWordWrap(True)
        self.result_label.setMaximumWidth(600)  # Set a maximum width
        content_layout.addWidget(self.result_label)

        # Button to fetch meaning
        self.fetch_meaning_button = QPushButton("Get Meaning", self)
        self.fetch_meaning_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.fetch_meaning_button.setStyleSheet(
            "background-color: #FF69B4; color: white; padding: 15px; border-radius: 10px; font-size: 20px; border: none;"
        )
        self.fetch_meaning_button.setFixedHeight(50)
        self.fetch_meaning_button.clicked.connect(self.fetch_meaning)
        content_layout.addWidget(self.fetch_meaning_button)

        # Button for voice pronunciation of the entered word and its meaning
        self.word_voice_button = QPushButton("Pronounce Word and Meaning", self)
        self.word_voice_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.word_voice_button.setStyleSheet(
            "background-color: #FF69B4; color: white; padding: 15px; border-radius: 10px; font-size: 20px; border: none;"
        )
        self.word_voice_button.setFixedHeight(50)
        self.word_voice_button.clicked.connect(self.pronounce_word_and_meaning)
        content_layout.addWidget(self.word_voice_button)

        main_layout.addLayout(content_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def set_daily_word(self):
        daily_word = secrets.choice(list(self.easy_words_set))
        self.daily_word_label.setText(daily_word)

    def fetch_meaning(self):
        word = self.word_input.text()
        if word:
            meaning = self.fetch_meaning_from_api(word)
            if meaning:
                self.display_meaning(meaning)
            else:
                meaning = self.fetch_meaning_from_api(word)
                if meaning:
                    self.display_meaning(meaning)
                else:
                    self.result_label.setText("Meaning not found.")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a word.")

    def fetch_meaning_from_api(self, word):
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            return data[0]['meanings'][0]['definitions'][0]['definition']
        else:
            return None


    def display_meaning(self, meaning):
        if len(meaning) > 100:
            self.result_label.setFont(QFont("Arial", 16))
        else:
            self.result_label.setFont(QFont("Arial", 20))
        self.result_label.setText(meaning)

    def pronounce_daily_word(self):
        daily_word = self.daily_word_label.text()
        if daily_word:
            self.tts_engine.say(daily_word)
            self.tts_engine.runAndWait()

    def pronounce_word_and_meaning(self):
        word = self.word_input.text()
        meaning = self.result_label.text()
        if word and meaning:
            self.tts_engine.say(f"The word is {word}.")
            self.tts_engine.say(f"The meaning is {meaning}.")
            self.tts_engine.runAndWait()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a word and fetch its meaning first.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VocabularyApp()
    window.show()
    sys.exit(app.exec_())