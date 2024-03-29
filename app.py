from flask import Flask, request, jsonify, make_response
import pandas as pd
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
credentials_df = pd.read_csv('credentials.csv')  # Load the credentials

@app.route('/status', methods=['GET'])
def status():
    return '1'

@app.route('/welcome', methods=['GET'])
def welcome():
    username = request.args.get('username', 'Guest')
    return f'Welcome, {username}!'

@app.route('/permissions', methods=['POST'])
def permissions():
    auth = request.authorization
    if not auth or not (credentials_df.loc[(credentials_df['username'] == auth.username) & (credentials_df['password'] == int(auth.password))].any()).any():
        return make_response('Unauthorized', 401)
    user_row = credentials_df.loc[(credentials_df['username'] == auth.username) & (credentials_df['password'] == int(auth.password))]
    response = make_response(jsonify({'v1': int(user_row['v1'].values[0]), 'v2': int(user_row['v2'].values[0])}))
    response.headers['X-User'] = auth.username
    return response

@app.route('/v1/sentiment', methods=['POST'])
def v1_sentiment():
    sentence = request.form.get('sentence')
    auth = request.authorization
    if not auth or not (credentials_df.loc[(credentials_df['username'] == auth.username) & (credentials_df['password'] == int(auth.password)) & (credentials_df['v1'] == 1)].any()).any():
        return make_response('Unauthorized or No Access to v1', 403)
    score = random.uniform(-1, 1)
    return jsonify({'score': score})

@app.route('/v2/sentiment', methods=['POST'])
def v2_sentiment():
    sentence = request.form.get('sentence')
    auth = request.authorization
    if not auth or not (credentials_df.loc[(credentials_df['username'] == auth.username) & (credentials_df['password'] == int(auth.password)) & (credentials_df['v2'] == 1)].any()).any():
        return make_response('Unauthorized or No Access to v2', 403)
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(sentence)
    return jsonify({'score': sentiment['compound']})

if __name__ == '__main__':
    app.run(debug=True)
