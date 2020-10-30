from flask import Flask, request, render_template
import pickle
from textblob import TextBlob

app = Flask(__name__)
classifier = pickle.load(open('Classify_emotion.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sentiment_analyzer',methods=['POST']) 
def sentiment_analyzer():
    tweet = request.form['tweet']
    words = tweet.split()
    input_tweet = dict([word,True] for word in words)

    analysis = TextBlob(tweet) 
    if analysis.sentiment.polarity > 0: 
        percentage = analysis.sentiment.polarity*100
        if analysis.sentiment.polarity > 0.5:
            sentiment= 'Very Positive'
        else:
            sentiment= 'Positive'
        emotion = classifier.classify(input_tweet)
        return render_template('result.html', tweet=tweet, percentage='The tweet is {}% postive'.format(percentage), category='{}'.format(sentiment), emotion='Emotion: {}'.format(emotion))
    elif analysis.sentiment.polarity == 0: 
        sentiment= 'Neutral'
        return render_template('result.html', tweet=tweet, category='{}'.format(sentiment))
    else: 
        percentage = abs(analysis.sentiment.polarity)*100
        if abs(analysis.sentiment.polarity) > 0.5:
            sentiment= 'Very Negative'
        else:
            sentiment= 'Negative'
        emotion = classifier.classify(input_tweet)
        return render_template('result.html', tweet=tweet, percentage='The tweet is {}% negative'.format(percentage), category='{}'.format(sentiment), emotion='Emotion: {}'.format(emotion))
    
if __name__ == "__main__":
    app.run(debug=True)