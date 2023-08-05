import pandas as pd
from pprint import pprint
import csv


class Naive_Bayes_Classifier:
    def __init__(self):
        pass

    def fit(self, data):
        features = data.drop(['Stolen'], axis=1)
        self.ds_features = {}

        # get P(Yes) and P(No)
        total_yes = len(data['Stolen'].loc[data['Stolen'] == 'Yes'])
        total_no = len(data['Stolen'].loc[data['Stolen'] == 'No'])
        self.p_yes = total_yes / len(data['Stolen'])
        self.p_no = total_no / len(data['Stolen'])

        # create the data structure and populate it
        for c in features.columns:
            self.ds_features[c] = {}
            for item in list(set(features[c])):
                self.ds_features[c][item] = {}

                x = data[(data[c]==item)]
                y = len(x['Stolen'].loc[x['Stolen']=='Yes'])
                
                self.ds_features[c][item]['YES'] = y / total_yes

                n = len(x['Stolen'].loc[x['Stolen']=='No'])

                self.ds_features[c][item]['NO'] = n / total_no
    
    def predict(self, l):
        ans = {'Yes': 1, 'No': 1}
        pprint(self.ds_features)
        ans['Yes'] *= self.ds_features['Color'][l[0]]['YES'] * \
                        self.ds_features['Type'][l[1]]['YES'] * \
                        self.ds_features['Origin'][l[2]]['YES'] * self.p_yes

        ans['No'] *= self.ds_features['Color'][l[0]]['NO'] * \
                        self.ds_features['Type'][l[1]]['NO'] * \
                        self.ds_features['Origin'][l[2]]['NO'] * self.p_no

        return max(ans, key=lambda x: ans[x])


def main():
    naive_bayes = Naive_Bayes_Classifier()
    data = pd.read_csv("data.csv")
    naive_bayes.fit(data)
    pred = naive_bayes.predict(['Red', 'SUV', 'Domestic'])
    print('Stolen: {}'.format(pred))


if __name__ == '__main__':
    main()


'''
{'Color': {'Red': {'NO': 0.4, 'YES': 0.6}, 'Yellow': {'NO': 0.6, 'YES': 0.4}},
 'origin': {'Domestic': {'NO': 0.6, 'YES': 0.4},
            'Imported': {'NO': 0.4, 'YES': 0.6}},
 'type': {'SUV': {'NO': 0.6, 'YES': 0.2}, 'Sports': {'NO': 0.4, 'YES': 0.8}}}
Stolen: No
'''


