import pandas as pd
import numpy as np

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__, template_folder='template')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

@app.route("/find", methods=['GET', 'POST'])
def main():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
       name=request.form['name']
 #      name=request.form.getlist('name[]')
       print(name) 

    if form.validate():
            # Save the comment here.
       flash('Hello ' + name)

    
    data = pd.read_csv("nano.csv", encoding="latin1", engine = 'python')
    data = data.fillna(method="ffill")
    data.head(10)

    words = list(set(data["Name"].values))
    words.append("ENDPAD")
    n_words = len(words); n_words

    tags = list(set(data["Class"].values))
    n_tags = len(tags); n_tags

    class SentenceGetter(object):
        
        def __init__(self, data):
            self.n_sent = 1
            self.data = data
            self.empty = False
            agg_func = lambda s: [(w, t) for w, t in zip(s["Name"].values.tolist(),
                                                         s["Class"].values.tolist())]
            self.grouped = self.data.groupby("Name").apply(agg_func)
            self.sentences = [s for s in self.grouped]
        
        def get_next(self):
            try:
                s = self.grouped["Sentence: {}".format(self.n_sent)]
                self.n_sent += 1
                return s
            except:
                return None

    sent = getter.get_next()
    #print(sent)

    sentences = getter.sentences
    #print(sentences)

    max_len = 75
    word2idx = {w: i + 1 for i, w in enumerate(words)}
    tag2idx = {t: i for i, t in enumerate(tags)}

    #word2idx['graphene']
    #tag2idx['NONNANO']

    from keras.preprocessing.sequence import pad_sequences
    X = [[word2idx[w[0]] for w in s] for s in sentences]
    X = pad_sequences(maxlen=max_len, sequences=X, padding="post", value=0)

    y = [[tag2idx[w[1]] for w in s] for s in sentences]
    y = pad_sequences(maxlen=max_len, sequences=y, padding="post", value=tag2idx["NANO"])

    from keras.utils.np_utils import to_categorical
    y = [to_categorical(i, n_tags) for i in y]

    from sklearn.model_selection import train_test_split

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.1)

    from keras.models import Model
    from keras.layers import LSTM, Input, Embedding, Dense, TimeDistributed, Dropout, Bidirectional
    from keras_contrib.layers import CRF

    input = Input(shape=(max_len,))
    model = Embedding(input_dim=n_words + 1, output_dim=20,
                      input_length=max_len, mask_zero=True)(input)  # 20-dim embedding
    model = Bidirectional(LSTM(units=50, return_sequences=True,recurrent_dropout=0.2))(model)

    model = TimeDistributed(Dense(50, activation="relu"))(model)  # a dense layer as suggested by neuralNer
    crf = CRF(n_tags)  # CRF layer
    out = crf(model)  # output

    model = Model(input, out)

    model.compile(optimizer="rmsprop", loss=crf.loss_function, metrics=[crf.accuracy])

    model.summary()

    history = model.fit(X_tr, np.array(y_tr), batch_size=84, epochs=8,
                        validation_split=0.3, verbose=1)

    hist = pd.DataFrame(history.history)
    #print(hist)

    import matplotlib.pyplot as plt
    plt.style.use("ggplot")
    plt.figure(figsize=(12,12))
    plt.plot(hist["acc"])
    plt.plot(hist["val_acc"])
    plt.show()

    i = 0
    p = model.predict(np.array([X_te[i]]))
    p = np.argmax(p, axis=-1)
    true = np.argmax(y_te[i], -1)
    print("{:15}||{:5}||{}".format("Word", "True", "Pred"))
    print(30 * "=")
    for w, t, pred in zip(X_te[i], true, p[0]):
        if w != 0:
            print("{:15}: {:5} {}".format(words[w-1], tags[t], tags[pred]))


    from stanfordcorenlp import StanfordCoreNLP
    import logging
    import json

    class StanfordNLP:
        def __init__(self, host='http://localhost', port=9000):
            self.nlp = StanfordCoreNLP(host, port=port,
                                       timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
            self.props = {
                'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
                'pipelineLanguage': 'en',
                'outputFormat': 'json'
            }

        def word_tokenize(self, sentence):
            return self.nlp.word_tokenize(sentence)

        def tokens_to_dict(_tokens):
            tokens = defaultdict(dict)
            for token in _tokens:
                tokens[int(token['index'])] = {
                    'word': token['word'],
                    'lemma': token['lemma'],
                    'pos': token['pos'],
                    'ner': token['ner']
                }
            return tokens


    if __name__ == '__main__':
        sNLP = StanfordNLP()

    text = "Cantilever Island Atomic distance is 25 nm Force Microscopy Contact Roberts Microscopy"

    print(sNLP.word_tokenize(text))
    test = sNLP.word_tokenize(text)


    x_test_sent = pad_sequences(sequences=[[word2idx.get(w, 0) for w in test]],padding="post", value=0, maxlen=max_len)
    print(x_test_sent)

    p = model.predict(np.array([x_test_sent[0]]))
    p = np.argmax(p, axis=-1)
    print("{:15}||{}".format("Word", "Prediction"))
    print(30 * "=")
    for w, pred in zip(test, p[0]):
        print("{:15}: {:5}".format(w, tags[pred]))

        flash('You have given ' + name +' as input ')

    else:
        flash('Required: All the form fields are required. ')

    return render_template('hello.html', form=form)
if __name__ == "__main__":
	app.run(host='0.0.0.0')


