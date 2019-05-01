import glob
import io
import os
import pdb
import sys
import numpy as np

import fnmatch
import re
from sklearn.linear_model import SGDClassifier
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk import ne_chunk

from commonregex import CommonRegex
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm

def Chunk_Data(data):
    tokenized = nltk.word_tokenize(data)
    tagged = nltk.pos_tag(tokenized)
    tree = nltk.ne_chunk(tagged, binary = False)
    return tree,tokenized

def Retrieve_Person(tree):
    Person = []
    for node in tree:
        if type(node) is nltk.Tree:
            if node.label() == 'PERSON':
                elements = node.leaves()
                length = len(elements)

                n = 0
                str = ""
                for x in range (0, length):
                    str = str + elements[x][n]
                    if x != length-1:
                        str = str + " "
                Person.append(str)
    return Person

def Fields_to_redact(Person):
    Replace = []
    for element in Person:
        Replace.append(element)
    return Replace

def Redact(Replace,data):
    for j in range(0,len(Replace)):
        if Replace[j] in data:
            length = len(Replace[j])
            data = re.sub(Replace[j], length*'\u2588', data, 1)
    return data

def Output_Files(data,Location):
    #f = open(Location,"w")
    with open(Location, "w", encoding="utf-8") as f:
        f.write(data)
        f.close()

Reviews_directory = 'Data'
Redacted_directory = 'Data/redacted/'
Predicted_directory = 'Data/predicted/'
files = os.listdir(Reviews_directory)
#print("Total number of reviews are", len(files))

def get_sc_wc_cc(text):
    """retrieve sentence count, word count and character count of the text."""
    cc = len(text)
    wc = len(text.split())
    sc = len(sent_tokenize(text))
    return sc,wc,cc

def retreive_train_features(text, Names, file_name):
    features = []
    No_of_names_in_review = len(Names)
    sent_count, word_count, character_count = get_sc_wc_cc(text)
    file_name = file_name[:-4]
    movie_rating = int(file_name.split('_')[1])
    for i in range(0, No_of_names_in_review):
        dict = {}
        # dict['name'] = Names[i]
        dict['name_length'] = len(Names[i])
        dict['movie_rating'] = movie_rating
        dict['No_of_names_in_review'] = No_of_names_in_review
        dict['sent_count'] = sent_count
        dict['word_count'] = word_count
        dict['character_count'] = character_count
        features.append(dict)

    # print(features)
    return features


No_of_Reviews = 200
All_train_features = []
Names_All_Reviews = []
for i in range(0, No_of_Reviews):
    path = Reviews_directory + '/' + files[i]
    f = open(path)

    text = f.read()
    tree, tokenized = Chunk_Data(text)
    Names = Retrieve_Person(tree)

    features = retreive_train_features(text, Names, files[i])
    All_train_features.extend(features)
    Names_All_Reviews.extend(Names)

    Replace = Fields_to_redact(Names)
    data = Redact(Replace, text)

    File_Name = files[i]
    File_Name = File_Name[:-4]
    # print(text)
    # print(data)
    Location = Redacted_directory + File_Name + '.redacted'
    Output_Files(data, Location)

print("number of observations are", len(Names_All_Reviews))

Names_All_Reviews_Unique = (set(Names_All_Reviews))
Names_All_Reviews_Unique = list(Names_All_Reviews_Unique)

files_redacted = os.listdir(Redacted_directory)
print("Total number of reviews considered for training are", len(files_redacted))

v = DictVectorizer()
X = v.fit_transform(All_train_features).toarray()
Names_All_Reviews = np.array(Names_All_Reviews)
model = svm.SVC(probability=True)
#model = SGDClassifier()
model.fit(X, Names_All_Reviews)

def retreive_test_features(text, Names_Redacted, file_name):
    features = []
    No_of_names_in_review = len(Names_Redacted)
    sent_count, word_count, character_count = get_sc_wc_cc(text)
    file_name = file_name[:-9]
    movie_rating = int(file_name.split('_')[1])
    for i in range(0, No_of_names_in_review):
        dict = {}
        # dict['name'] = Names[i]
        dict['name_length'] = len(Names_Redacted[i])
        dict['movie_rating'] = movie_rating
        dict['No_of_names_in_review'] = No_of_names_in_review
        dict['sent_count'] = sent_count
        dict['word_count'] = word_count
        dict['character_count'] = character_count
        features.append(dict)

    # print(features)
    return features

def retrieve_predicted_words(probabilities_all_classes, Names_Redacted):
    All_predicted_words_review = []
    for test_word in range(0, len(Names_Redacted)):
        test_word_probabilities = probabilities_all_classes[test_word]
        top_5_idx = np.argsort(test_word_probabilities)[-5:]
        #print(top_5_idx)
        predicted_words = []
        for i in range(0,5):
            index_range = top_5_idx[i]
            predicted_word = Names_All_Reviews_Unique[index_range]
            predicted_words.append(predicted_word)
        #print(predicted_words)
        All_predicted_words_review.append(predicted_words)
    #print(All_predicted_words_review)
    return (All_predicted_words_review)


No_of_Reviews = 10
# All_test_features = []
print("Total number of reviews considered for testing are", No_of_Reviews)
for i in range(0, No_of_Reviews):
    path = Redacted_directory + '/' + files_redacted[i]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        f.close()

    Names_Redacted = re.findall(r'(█+)', text)

    test_features = retreive_test_features(text, Names_Redacted, files_redacted[i])
    # All_test_features.extend(features)
    # print("test_features",test_features)

    if len(test_features) > 0:
        X_test = v.fit_transform(test_features).toarray()
        probabilities_all_classes = model.predict_proba(X_test)
        All_predicted_words_review = retrieve_predicted_words(probabilities_all_classes, Names_Redacted)

        path_predicted = Predicted_directory + '/' + files_redacted[i]
        with open(path_predicted, "w", encoding="utf-8") as f:
            for i in range(0, len(All_predicted_words_review)):
                text = text + "\n --- for {} top 5 predicted names are {} \n".format(Names_Redacted[i], [item for item in
                                                                                                         All_predicted_words_review[
                                                                                                             i]])

            f.write(text)
            f.close()