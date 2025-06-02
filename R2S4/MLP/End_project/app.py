import sys
import re
import string
import random
import json
import pickle
import spacy
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer as WNL
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from tensorflow import keras
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.utils import pad_sequences
from PyQt6.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit,
	QTabWidget, QMessageBox, QTableWidget, QTableWidgetItem, QSizePolicy
)
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import QTimer

def remove_stopwords(text):
    stop_words = stopwords.words('english')
    words = text.split()
    filtered_sentence = ''
    for word in words:
        if word not in stop_words:
            filtered_sentence = filtered_sentence + word + ' '
    return filtered_sentence

def remove_punctuation(text):
    table = str.maketrans('','',string.punctuation)
    words = text.split()
    filtered_sentence = ''
    for word in words:
        word = word.translate(table)
        filtered_sentence = filtered_sentence + word + ' '
    return filtered_sentence

def normalize_text(text):
    text = text.lower()
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('\\W', ' ', text)
    text = re.sub('\n', '', text)
    text = re.sub(' +', ' ', text)
    text = re.sub('^ ', '', text)
    text = re.sub(' $', '', text)
    return text

def stemming(text):
    ps = PorterStemmer()
    words = text.split()
    filtered_sentence = ''
    for word in words:
        word = ps.stem(word)
        filtered_sentence = filtered_sentence + word + ' '
    return filtered_sentence

def clean_text(text):
    text = text.lower()
    text = text.replace(',',' , ')
    text = text.replace('.',' . ')
    text = text.replace('/',' / ')
    text = text.replace('@',' @ ')
    text = text.replace('#',' # ')
    text = text.replace('?',' ? ')
    text = normalize_text(text)
    text = remove_punctuation(text)
    text = remove_stopwords(text)
    text = stemming(text)
    return text

class nlpApp(QWidget):
	def __init__(self):
		super().__init__()
		self.windowTitle = "NLP Analysis App"
		main_layout = QHBoxLayout()

		self.tabs = QTabWidget()
		self.init_tab1()
		self.init_tab2()
		main_layout.addWidget(self.tabs)
		self.setLayout(main_layout)
		
		self.sentimentModel = None
		self.oneEncoder = None
		self.tokenizer = None
		self.nlp = None
		self.stemmer = None
		self.diLemma = WNL()

	def get_sentiment(self, text):
		if self.sentimentModel is None:
			try:
				self.sentimentModel = keras.models.load_model('sentiment.keras')
				self.oneEncoder = pickle.load(open("encoder.bin", "rb"))
				tokenizer_config = json.load(open('tok_conf.json', 'r'))
				self.tokenizer = tokenizer_from_json(tokenizer_config)
			except Exception as e:
				QMessageBox.critical(self, "Error", f"Failed to load sentiment model: {str(e)}")
				return str(e)
		
		input = clean_text(text)

		input = self.tokenizer.texts_to_sequences([input])

		input = pad_sequences(input, maxlen=50,
			                         padding="post",
			                         truncating="post")

		pred = self.sentimentModel.predict(input)
		pred = self.oneEncoder.inverse_transform(pred)
		return pred[0][0] if pred else "Error"
	
	def get_stelem(self, text):
		try:
			spacy.load("en_core_web_md")
		except OSError:
			spacy.cli.download("en_core_web_md")
	
		for resource in ['averaged_perceptron_tagger', 'wordnet', 'stopwords']:
			try:
				nltk.data.find(f'taggers/{resource}' if resource == 'averaged_perceptron_tagger' else f'corpora/{resource}')
			except LookupError:
				nltk.download(resource, quiet=True)

		if self.nlp is None:
			try:
				self.nlp = spacy.load("en_core_web_md")
				self.stemmer = PorterStemmer()
			except Exception as e:
				QMessageBox.critical(self, "Error", f"Failed to load NLP model: {str(e)}")
				return str(e)
			
		doc = self.nlp(text)
		results = []

		for token in doc:
			if token.is_alpha and not token.is_stop:
				lemma = token.lemma_.lower()
				stem = self.stemmer.stem(token.text.lower())
				results.append((token.text, lemma, stem))
		return results

	def init_tab1(self):
		widget = QWidget()
		layout = QVBoxLayout()
		layout.setSpacing(6)

		inputLabel = QLabel("Input Text:")
		self.inputText = QLineEdit()
		self.inputText.setPlaceholderText("Enter text for processing...")
		self.inputText.setClearButtonEnabled(True)
		layout.addWidget(inputLabel)
		layout.addWidget(self.inputText)

		buttonsRow = QHBoxLayout()
		buttonsRow.setSpacing(2)

		sentimentBtn = QPushButton("Analyze Sentiment")
		sentimentBtn.clicked.connect(self.sentimentBtn_clicked)
		buttonsRow.addWidget(sentimentBtn)

		stemlemBtn = QPushButton("Stem && Lemmatize")
		stemlemBtn.clicked.connect(self.stemlemBtn_clicked)
		buttonsRow.addWidget(stemlemBtn)

		layout.addLayout(buttonsRow)

		self.resultLabel = QLabel("Result: ")
		self.resultLabel.setWordWrap(True)
		layout.addWidget(self.resultLabel)

		self.resultTable = QTableWidget()
		self.resultTable.setColumnCount(3)
		self.resultTable.setHorizontalHeaderLabels(["Token", "Lemma", "Stem"])
		self.resultTable.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
		self.resultTable.horizontalHeader().setStretchLastSection(False)
		self.resultTable.hide()
		layout.addWidget(self.resultTable)

		layout.addStretch()
		widget.setLayout(layout)
		self.tabs.addTab(widget, "Tools")

	def sentimentBtn_clicked(self):
		self.resultTable.hide()
		text = self.inputText.text().strip()
		if not text:
			return
		
		response = self.get_sentiment(text)
		self.resultLabel.setText(f"Result: {response}")
		self.inputText.clear()

	def stemlemBtn_clicked(self):
		text = self.inputText.text().strip()
		response = self.get_stelem(text)
		self.resultTable.setRowCount(len(response))
		self.resultLabel.setText("Result:")
		for row, (token, lemma, stem) in enumerate(response):
			self.resultTable.setItem(row, 0, QTableWidgetItem(token))
			self.resultTable.setItem(row, 1, QTableWidgetItem(lemma))
			self.resultTable.setItem(row, 2, QTableWidgetItem(stem))
			
		self.resultTable.show()
		QTimer.singleShot(0, self.adjustTableToContents)
		self.inputText.clear()

	def adjustTableToContents(self):
		self.resultTable.resizeColumnsToContents()
		self.resultTable.resizeRowsToContents()

		header_width = self.resultTable.verticalHeader().width()
		frame_w = self.resultTable.frameWidth() * 2
		columns_width = 0
		for col in range(self.resultTable.columnCount()):
			columns_width += self.resultTable.columnWidth(col)
		total_width = header_width + columns_width + frame_w

		header_height = self.resultTable.horizontalHeader().height()
		frame_h = self.resultTable.frameWidth() * 2
		rows_height = 0
		for row in range(self.resultTable.rowCount()):
			rows_height += self.resultTable.rowHeight(row)
		total_height = header_height + rows_height + frame_h

		self.resultTable.setFixedSize(total_width, total_height)

	def init_tab2(self):
		widget = QWidget()
		layout = QVBoxLayout()
		layout.setSpacing(6)

		self.chatHistory = QTextEdit()
		self.chatHistory.setReadOnly(True)
		self.chatHistory.setStyleSheet("""
QTextEdit {
    background-color: #f0f0f0;
}
QScrollBar:vertical {
    background: #f0f0f0;
    width: 12px;
    margin: 0;
    border-radius: 6px;
}
QScrollBar::handle:vertical {
    background: #6c8cd5;
    min-height: 30px;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover {
    background: #3a5bbb;
}
QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
    height: 0px;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
""")
		layout.addWidget(self.chatHistory)

		input_layout = QHBoxLayout()
		self.chatInput = QLineEdit()
		self.chatInput.returnPressed.connect(self.send_prompt)
		self.chatInput.setPlaceholderText("Type your prompt here...")
		
		sendBtn = QPushButton("Send")
		sendBtn.clicked.connect(self.send_prompt)

		input_layout.addWidget(self.chatInput)
		input_layout.addWidget(sendBtn)

		layout.addLayout(input_layout)
		widget.setLayout(layout)
		self.tabs.addTab(widget, "Chat")

	def send_prompt(self):
		prompt = self.chatInput.text().strip()
		if not prompt:
			return
		
		self.appendChatHistory("You", prompt)

		response = self.get_response(prompt)
		self.appendChatHistory("Bot", response)

		self.chatInput.clear()

	def appendChatHistory(self, sender, message):
		color = "#007acc" if sender == "You" else "#444444"
		msgFormat = f'<b><span style="color:{color}">{sender}</span></b> {message}<br>'
		self.chatHistory.moveCursor(QTextCursor.MoveOperation.End)
		self.chatHistory.insertHtml(msgFormat)
		self.chatHistory.moveCursor(QTextCursor.MoveOperation.End)
		self.chatHistory.verticalScrollBar().setValue(self.chatHistory.verticalScrollBar().maximum())
	
	def get_response(self, prompt):
		if '"' not in prompt:
			desc = prompt.strip()
			text = ""
			return "You did not add text to process in quotations. Correct format is 'Action description \"Text\"'."

		if prompt.count('"') == 1:
			desc = prompt.replace('"', '').strip()
			text = ""
			return "You used only one quotation mark. Correct format is 'Action description \"Text\"'."
		
		pattern = re.compile(r'^(.*?)"([\s\S]*?)"(.*)$')

		match = pattern.match(prompt)

		desc = match.group(1).strip()
		text = match.group(2)

		if desc == "":
			return "You did not provide an action description. Correct format is 'Action description \"Text\"'."
		
		if text == "":
			return "Text in quotations is empty. Correct format is 'Action description \"Text\"'."
		
		response = self.ask(desc, text)
		return response
	
	def ask(self, desc, text):
		dialog = [
			("lemmatize", 1),
			("stem", 1),
			("process", 1),
			("sentiment", 0),
			("analyze", 0),
			("token", 1),
			("tokenize", 1),
			("lemma", 1),
			("stemming", 1),
			("stemmer", 1),
			("analyse", 0),
			("sent", 1),
			("attitude", 0),
			("emotion", 0),
			("feel", 0),
			("opinion", 0),
			("review", 0),
			("position", 0),
			("thought", 0),
			("view", 0),
			("perspective", 0),
			("stance", 0),
			("standpoint", 0),
			("decomposition", 1),
			("decay", 1),
			("breakdown", 1),
			("dissection", 1),
			("dissect", 1),
			("riddle", 0), 
			("describe", 0),
			("analyser", 0),
			("analyzer", 0),
			("analyzing", 0),
			("analysis", 0),
			("examine", 0),
			("examiner", 0),
			("examining", 0),
			("examination", 0),
			("mood", 0),
			("emotionally", 0),
			("positivity", 0),
			("negativity", 0),
			("positive", 0),
			("negative", 0),
			("tone", 0),
			("affective", 0),
			("sentimentally", 0),
			("reaction", 0),
			("vibe", 0),
			("judgment", 0),
			("critique", 0),
			("rating", 0),
			("feedback", 0),
			("appraisal", 0),
			("reception", 0),
			("evaluate", 0),
			("estimation", 0),
			("estimate", 0),
			("appreciation", 0),
			("response", 0),
			("emotive", 0),
			("normalize", 1),
			("normalise", 1),
			("simplify", 1),
			("base form", 1),
			("inflection", 1),
			("preprocess", 1),
			("clean", 1),
			("cleanse", 1),
			("format", 1),
			("deconstruct", 1),
			("processing", 1),
			("clean text", 1),
			("parser", 1),
			("parse", 1),
			("break into words", 1),
			("structure", 1),
			("text flow", 1),
			("syntactic", 1),
			("grammar", 1),
			("text form", 1),
			("phrase breakdown", 1),
		]
		
		def get_wordnet_pos(tag):
			if tag.startswith('J'):
				return wordnet.ADJ
			elif tag.startswith('V'):
				return wordnet.VERB
			elif tag.startswith('N'):
				return wordnet.NOUN
			elif tag.startswith('R'):
				return wordnet.ADV
			else:
				return None
			
		def split_and_clean(sentence):
			tokenized = word_tokenize(sentence.lower())
			tagged = pos_tag(tokenized)
			lemmatized = []

			for word, tag in tagged:
				if word.isalpha():
					pos = get_wordnet_pos(tag) or wordnet.NOUN
					lemmatized.append(self.diLemma.lemmatize(word, pos=pos))

			return lemmatized
		
		def find_matching(input_prompt):
			answer = None
			intersection_len_req = 0
			input_prompt = set(split_and_clean(input_prompt))
			for index, pair in enumerate(dialog):
				match = set(split_and_clean(pair[0]))
				intersection_len = len(set.intersection(input_prompt, match))
				if intersection_len > intersection_len_req:
					answer = index
					intersection_len_req = intersection_len
				if intersection_len == intersection_len_req and intersection_len != 0:
					if random.randint(0, 1) == 1:
						answer = index

			if answer is not None:
				answer = dialog[answer][1]
			return answer
		
		response_type = find_matching(desc)

		if response_type is None:
			return "I don\'t know how to answer that."
		
		if response_type == 0 or response_type == "0":
			try:
				response = self.get_sentiment(text)
				response = f"The sentiment of the text is: {response}"
			except Exception:
				response = None
				
		if response_type == 1 or response_type == "1":
			try:
				response = self.get_stelem(text)
				
				table_html = """
				The stemmed & lemmatized text is:<br>
				<table style="
					border-collapse: collapse; 
					margin-top: 6px; 
					font-family: Arial, sans-serif;
					background-color: #ffffff;
				">
				<thead>
				<tr style="
					background-color: #e0e0e0; 
					font-weight: bold;
					border-bottom: 2px solid #888;">
					<th style='padding: 6px; border: 1px solid #ccc;'>Token</th>
					<th style='padding: 6px; border: 1px solid #ccc;'>Lemma</th>
					<th style='padding: 6px; border: 1px solid #ccc;'>Stem</th>
				</tr>
				</thead>
				<tbody>
				"""
				for token, lemma, stem in response:
					table_html += f"""
				<tr>
					<td style='padding: 6px; border: 1px solid #ccc;'>{token}</td>
					<td style='padding: 6px; border: 1px solid #ccc;'>{lemma}</td>
					<td style='padding: 6px; border: 1px solid #ccc;'>{stem}</td>
				</tr>"""
				
				table_html += "</tbody></table><br>"
				
				response = table_html
			except Exception:
				response = None
		
		return response if response else "Something went wrong while processing your request."

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = nlpApp()
	window.resize(1000, 600)
	window.show()
	sys.exit(app.exec())