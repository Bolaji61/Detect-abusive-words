from flask import Flask, request, jsonify, render_template, redirect
import re
import nltk
# nltk.download()
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from profanityfilter import ProfanityFilter
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
stop_words = stopwords.words("english")

def GetCleanText(text):
  text = text.lower().split()

  stop_words = set(stopwords.words('english'))
  text = [w for w in text if not w in stop_words and len(w) >= 3]

  text = ' '.join(text)
  text = re.sub(r'https?://[A-Za-z0-9./]+' ,'url', text)
  text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]" ," ", text)
  text = re.sub(r"what's" ,"what is", text)
  text = re.sub(r"\'s" ," ", text)
  text = re.sub(r"\'ve" ," have", text)
  text = re.sub(r"\'t" ," not", text)
  text = re.sub(r"i'm" ,"i am", text)
  text = re.sub(r"\'re" ," are", text)
  text = re.sub(r"\'d" ," would", text)
  text = re.sub(r"\'ll" ," will", text)
  text = re.sub(r"," ," ", text)
  text = re.sub(r"\." ," ", text)
  text = re.sub(r"!" ," ", text)
  text = re.sub(r"\/" ," ", text)
  text = re.sub(r"\^" ," ^ ", text)
  text = re.sub(r"\+" ," + ", text)
  text = re.sub(r"\-" ," - ", text)
  text = re.sub(r"\=" ," = ", text)
  text = re.sub(r"'" ," ", text)
  text = re.sub(r"(\d+)(k)" ,r"\g<1>000", text)
  text = re.sub(r":" ," : ", text)
  text = re.sub(r" e g " ," eg ", text)
  text = re.sub(r" b g " ," bg ", text)
  text = re.sub(r" u s " ," us ", text)
  text = re.sub(r"\0s" ,"0", text)
  text = re.sub(r" 9 11 " ," 911 ", text)
  text = re.sub(r"e - maill" ," email ", text)
  text = re.sub(r" j k " ," jk ", text)
  text = re.sub(r"\s{2,}" ," ", text)
  text = re.sub(r"@[A-Za-z0-9]+" ," ", text)
  text = re.sub(r'(\w)\1{2,}' ,r'\1\1', text)
  text = re.sub(r"\w(\w)\1{2}" ," ", text)
  return text
  
text = str()
lemmatizer = WordNetLemmatizer()
word_list = nltk.word_tokenize(text)
lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])

pf = ProfanityFilter()
def censor(text):
    pf.set_censor("*")
    censored = pf.censor(text)
    return censored


# Initialize the app
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    """
    GET Request
    """
    #give message to user
    return redirect("https://documenter.getpostman.com/view/7885882/SW18waNq?version=latest")


@app.route('/', methods=['POST'])
def detect():
      """
      POST Request
      """
      # post = request.get_json(force=True)
      post = request.json["post"]
      text = GetCleanText(post)
      prediction = censor(text)
      return jsonify(result = prediction)

if  __name__ == "__main__":
    app.run(debug=True)




