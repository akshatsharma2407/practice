from flask import Flask,render_template,request
import mlflow
from preprocessing_utility import normalize_text
import dagshub
import pickle

mlflow.set_tracking_uri('https://dagshub.com/akshatsharma2407/practice.mlflow')
dagshub.init(repo_owner='akshatsharma2407', repo_name='practice', mlflow=True)

app = Flask(__name__)

#load model from model registry
model_name = 'my_model'
model_version = 1

model_uri = f'models:/{model_name}/{model_version}'
model = mlflow.pyfunc.load_model(model_uri)

vectorizer = pickle.load(open('models/vectorizer.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    text = request.form['text']


    #clean
    text = normalize_text(text)

    #bow
    features = vectorizer.transform([text])

    #prediction
    result = model.predict(features)

    #show
    if str(result[0]) == 0:
        return 'sad'
    else:
        return 'happy'

app.run(debug=True)