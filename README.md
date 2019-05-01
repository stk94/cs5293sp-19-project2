# cs5293sp19-Project2

Name: SAI TEJA KANNEGANTI
Date: 04/30/2019


Description of the Project:

Whenever sensitive information is shared with the public, the data must go through a redaction process. That is, all sensitive names, places, and other sensitive information must be hidden. 
Documents such as police reports, court transcripts, and hospital records all contains sensitive information. Redacting this information is often expensive and time consuming.
As a part of this project (The Unredactor), The unredactor will take a redacted document and the redaction flag as input, in return it will give the most likely candidates to fill in the redacted location. 
The unredactor only needs to unredact names. To predict the name we solved the Entity Resolution problem.

As we can guess, discovering names is not easy. To discover the best names, we trained a model to help us predict missing words. 
For this project, we used the Large Movie Review Data Set. Dataset can be downloaded at(http://ai.stanford.edu/~amaas/data/sentiment/). This is a data set of movie reviews from IMDB. 
The initial goal of the data set is to discover the sentiment of each review. For this project, we used the reviews for their textual content.


Approach:

I have done this project in 5 steps. 

1. Redacting the data files (Reviews):
	
	We can take n number of text files (reviews) and extract names(name of persons) from these reviews. Later, after extracting names, names are redacted and the redacted files are stored in a directory. 
	Some of the steps involved in redacting data files are:
		
		1. Retrieve data
		2. Chunking and parsing data
		3. Retrieve Flags
		4. Redaction
		5. Output files
		
	1. Retrieve Data:
		a. Made a list of all text files that need to be redacted.
		b. Each file is accessed as per index in the list.
		c. Data is read by opening file in read mode.

	2. Chunking and parsing data:
		a. used nltk. word_tokenize to tokenize to words and PunktSentenceTokenizer to tokenize to sentences.
		b. Parsed text

	3. Retrieve Flags:
		a. data after tokenized by words to retrieve names.

	4. Redaction:
		a. A list contains all redaction words due to flags (names of person)

	5. Outputfiles:
		a. These files are stored in location(directory) given in the main.py, all output files have .redacted extension with same name as text file.
	   
 2. Retreive features for all names:
 
	Extracted features used for predicting redacted name. All these features are saved as a dictionary. Some of the features are:
		a. name_length: it is the length of the word redacted.
		b. movie_rating: Can be extracted from the name of the review file.
		c. No_of_names_in_review: Number of names in the review.
		d. sent_count = No. of sentences in given review.
		e. word_count = No. of words in given review.
		f. character_count = No. of characters in a given review.
		
3. Model a classifier:

	a. Used dict vectorizer to get the features from above dictionaries. This is input to the model(Classifier).
	b. Fit transform on the training features.
	c. Output to the model are the names that are rdacted.
	d. Fit a model by using Support Vector Classifier with probability. For each redacted word, this gives a probability for each name in the training data. 
	e. We take the redacted documents and extract features, by using these features predicted the top names suitable for the redacted word.
	f. By using the model and the probabilities, we predict the top 5 words for each Name. 
 
 4. Writing predicted words along with redacted block:

	Directory of these files can be changes. In these files redacted text is appended with the redaction blocks and the suitable words that would go with the redaction blocks.
 
Inspiration:

Project Link: https://oudalab.github.io/textanalytics/projects/project2 and https://oudalab.github.io/textanalytics/projects/project1

1. https://www.youtube.com/watch?list=PLQVvvaa0QuDfRO5bQFLcVgvIOIhNUZpZf&v=5heWVbihZrM
2. https://github.com/madisonmay/CommonRegex
3. https://stackoverflow.com/questions/3308102/how-to-extract-the-n-th-elements-from-a-list-of-tuples
4. https://www.oreilly.com/library/view/python-text-processing/9781849513609/ch01s07.html
5. https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
6. https://nlpforhackers.io/splitting-text-into-sentences/
7. https://www.tutorialspoint.com/python/python_command_line_arguments.htm
8. https://www.tutorialspoint.com/python/string_startswith.htm
9. https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
10. http://www.itsyourip.com/scripting/python/python-remove-last-n-characters-of-a-string/
11. https://stackoverflow.com/questions/5214578/python-print-string-to-text-file
12. https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
13. https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
14. https://docs.python.org/3/howto/regex.html
15. https://pypi.org/project/regex/
16. https://pythex.org
17. https://scikit-learn.org/stable/modules/feature_extraction.html
18. https://stackoverflow.com/questions/13070461/get-index-of-the-top-n-values-of-a-list-in-python
19. https://www.geeksforgeeks.org/python-format-function

People contacted:

1. Chanikya, chanukyalakamsani@ou.edu, He told to take top 'k' Names corresponding to each redacted word. 'k' can be any integer.  
2. Gowtham Teja Kanneganti, gowthamkanneganti@ou.edu, He mentioned me about framing features as dictionary and later using dict vectorizer. He helped me to write predicted names for a given name to a file.

Assumptions:
1. For displaying stats, I am always displaying stats to /stats/stats.txt. It will also display stats to stderr or stdout but not to a file if mentioned through command line.  
2. I assumed commonregex identifies all dates, street address, phone numbers.

