import sys, random, nltk
from nltk import bigrams

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__, template_folder='template')
app.static_folder = 'static' 
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Textarea_Input:', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route("/input")
def input():
    return render_template('input.html') 

@app.route("/output", methods=['GET'])
def output():
    
    #form = ReusableForm(request.form)
    #if request.method == 'GET':
    name = request.args.get('textQuery')
    #name=request.form['textQuery']
        #name=request.form.getlist('textQuery')
    #if form.validate():
        
    selected_features = None

    stopwords = ['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 
         'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 
         'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 
         'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 
         'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 
         'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 
         'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 
         'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 
         'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same','how', 'other', 'which', 'you', 'after', 'most',
         'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having','once']

    def add_lexical_features(fdist, feature_vector, text):
        feature_vector["len"] = len(text)
        text_nl = nltk.Text(text)
        for word, freq in fdist.items():
            fname = word 
            if selected_features == None or fname in selected_features:        
                #feature_vector[fname] = text_nl.count(word)
                feature_vector[fname] = 1

    def features(review_words):
        feature_vector = {}

        uni_dist = nltk.FreqDist(review_words)
        my_bigrams = list(bigrams(review_words))
        bi_dist = nltk.FreqDist(my_bigrams)
        
        add_lexical_features(uni_dist,feature_vector, review_words)
        
        return feature_vector

    with open("dataV11.txt", 'rb') as f:
        text = f.read()
    text = text.decode("utf-8")
    f.close()

    docs = text.split("\n")
    docs2 = docs[1: ]
    train = []
    #print(sent)

    for d in docs2:
        d = d.split()
        if len(d)!=0:
            cl = d[0]
            text_d = d[1: ]#we need to remove the stopwords
            text = []
            for w in text_d:
                if w not in stopwords:
                    text.append(w)
            item = (text, cl)
            train.append(item)

    random.seed(0)
    random.shuffle(train)
    #print(sentences)

    train_set = train[ :3271]
    valid_set = train[3272: ]

    featuresets_tr = [(features(words), label) for (words, label) in train_set ]
    featuresets_val = [(features(words), label) for (words, label) in valid_set ]

    featuresets = [(features(words), label) for (words, label) in train ]

    from nltk.classify.scikitlearn import SklearnClassifier
    from sklearn.naive_bayes import MultinomialNB,BernoulliNB
    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(featuresets_tr)
    MNB_classifier.train(featuresets)

    BNB_classifier = SklearnClassifier(BernoulliNB())
    BNB_classifier.train(featuresets_tr)
    BNB_classifier.train(featuresets)



#n = int(input())
    print(">>>>>>>")
    print(name)
    a = [a_temp for a_temp in name.strip().split(' ')]
    #for a_i in range(1): # to read a matrix
        #a_t = [a_temp for a_temp in input().strip().split(' ')]
        #a.append(a_t)
    print("<<<<<")
    print(a)

    inputData = ",".join(map(str, a))
    print("Input data:",inputData)  

    featuresets_test = [features(words) for words in a ]

    #features =  ",".join(map(str, featuresets_test))
    print("Features:",featuresets_test)    
    #a = []
    #a.append("doi1")
    #featuresets_test = []
    #featuresets_test.append("nanomaterial")
    predicted_labels = BNB_classifier.classify_many(featuresets_test)

    #print(a)
    #print(featuresets_test)
    for l in predicted_labels:
        print (str("Type of input data: "+l))

    #print(type(a))
    #print('Input:')
    #print(a)
    #print(type(predicted_labels))
    #print('Category:')
    #print(predicted_labels)
    #print(type(featuresets_test))
    #print('Features:')
    #print(featuresets_test)
    
    outputData = []
    import csv
    csvfile = open('result.csv', 'w')
    with csvfile:
        #for (col1, col2, col3) in zip(a, predicted_labels, featuresets_test):
            #outputData.append([col1, col2, col3])
        data1 = [["asif", "kary", "ravi"], ["xyz", "abc", "def"]]
        outputData = [[name, l, featuresets_test]]
        valueWriter = csv.writer(csvfile)
        
        valueWriter.writerows(outputData)
        #valueWriter.writerows([str(a),str(l),str(featuresets_test)])
        #csv = valueWriter.writerows(data)
    return render_template('results.html') 

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')


#