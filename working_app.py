import pandas as pd
import numpy as np
import pickle
import sklearn.ensemble as ske
from sklearn import cross_validation, tree, linear_model
from sklearn.naive_bayes import GaussianNB

from flask import Flask, request

app = Flask(__name__)

@app.route("/find")
def main():
        data = pd.read_csv('sm-lbs.csv', sep=',')
        print(type(data))


        data.convert_objects(convert_numeric=False)

        mapping={'Substance':0 , 'Property':1 }
        data['Classify']=data['Classify'].map(mapping)
        #The above 2 lines will map Sustance to 0 and Property to 1
        print(data.head())

        #CODE FOR MAPPING WORDS TO ID

        #DICTIONARY FOR STORING THE WORDS AND THEIR MAPPED ID
        text_digit_vals={}

        def handle_non_numeric_data(data):
                columns=data.columns.values

                for column in columns:
                        
                        def convert_to_int(key):
                                return text_digit_vals[key]

                        if data[column].dtype !=np.int64 and data[column].dtype !=np.float64:
                                column_contents=data[column].values.tolist()
                                unique_elements= set(column_contents)

                                x=0
                                for unique in unique_elements:
                                        if unique not in text_digit_vals:
                                                text_digit_vals[unique]=x
                                                x+=1

                                data[column]=list(map(convert_to_int, data[column]))
                        return data

        data = handle_non_numeric_data(data)
        print(data.head())


        X = data.drop(['Classify'], axis=1).values
        y = data['Classify'].values

        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y ,test_size=0.2)
        #SPLIT THE DATASET INTO TRAINING AND TEST DATA

        algorithms = {
                "DecisionTree": tree.DecisionTreeClassifier(max_depth=10),
                "RandomForest": ske.RandomForestClassifier(n_estimators=50),
                "GradientBoosting": ske.GradientBoostingClassifier(n_estimators=50),
                "AdaBoost": ske.AdaBoostClassifier(n_estimators=100),
                "GNB": GaussianNB()
            }
        #FIT 5 ALGORITHMS ON THE TRAINING DATA
        #THE ONE WITH MAX. ACCURACY WILL BE SELECTED AS THE WINNING ALGORITHM

        results = {}
        print("\nNow testing algorithms")
        for algo in algorithms:
            clf = algorithms[algo]
            clf.fit(X_train, y_train)
            score = clf.score(X_test, y_test)
            print("%s : %f %%" % (algo, score*100))
            results[algo] = score

        winner = max(results, key=results.get)
        print('\nWinner algorithm is %s with a %f %% success' % (winner, results[winner]*100))

        #USE THE WINNING ALGORITHM FOR PREDICTION
        clf = algorithms[winner]
        clf.fit(X_train, y_train)

        #CALCULATE ACCURACY
        score = clf.score(X_test, y_test)
        print (score*100)

        #INPUT SENTENCE : CAN BE A .txt file also
        test_sentence = request.args.get('word')
        #test_sentence=list(test_sentence)
        #print(type(test_sentence))
        w=test_sentence
        #test_sentence=["tetrafluoroborate","conductivity","Liquid","oxide","Heat","of","Combustion","Ag"]
        other="Other"
        su="Substance"
        p="Property"

        print("{:15}||{}".format("Word", "Prediction"))
        print(30 * "=")
        #input= text_digit_vals.get(test_sentence,999999)
        #for w in test_sentence:
        input= text_digit_vals.get(w,999999)
        if(input==999999):
                print("{:15}: {:5} ".format(w,other))
                s = "Output:" + other
                        
        elif((clf.predict(input)==0)):
                print("{:15}: {:5} ".format(w,su))
                s = "Output:" +su
        else:
                print("{:15}: {:5} ".format(w,p))
                s = "Output:" + p 
        return s 
if __name__ == "__main__":
	app.run(host='0.0.0.0')


        


