import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

    #List of Required nltk libraries
    #nltk.download('stopwords')
    #nltk.download('punkt')
    #nltk.download('wordnet')
    #nltk.download('averaged_perceptron_tagger')
    #nltk.download('maxent_ne_chunker')
    #nltk.download('words')

#Checking for gramatical errors present on a website
def incorrectWordCount(input):
    try:
        incorrectWordCount = 0
        totalWordCount = 0
        stopWords = set()
        for language in stopwords.fileids():
            stopWords.update(set(stopwords.words(language)))
        tokens = [token for token in input if token.isalpha()]
        for token in tokens:
            tokenStrip = token.rstrip()
            if not wordnet.synsets(tokenStrip):
                if not tokenStrip in stopWords:
                    incorrectWordCount += 1
        totalWordCount = len(input)
        percentageWrong = ((incorrectWordCount/totalWordCount) * 100)
        percentageAccuracy = 100 - percentageWrong
        if percentageAccuracy >= 85:
            return 25
        else:
            return 0
    except:
        return 0

#Using Named Entity Recognition to extract all organizations that are stated on the website
def NER(domain, input):
    organizations = []
    forChunk = domain + input
    chunkFinding = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(forChunk)))
    for nerAlert in chunkFinding:
        if hasattr(nerAlert, 'label') and nerAlert.label() == "ORGANIZATION":
            organizations.append(" ".join([token[0] for token in nerAlert.leaves()]))
    return organizations

#Using cosine simularity to see the simularity of two websites
def similarityCheck(site1, site2):
    stopWords = set(stopwords.words('english'))
    word1Token = nltk.word_tokenize(site1.lower())
    word2Token = nltk.word_tokenize(site2.lower())
    words1 = [token for token in word1Token if token.isalnum() and token not in stopWords]
    text1 = ' '.join(words1)
    words2 = [token for token in word2Token if token.isalnum() and token not in stopWords]
    text2 = ' '.join(words2)
    vectorizer = CountVectorizer().fit([text1, text2])
    vector1 = vectorizer.transform([text1])
    vector2 = vectorizer.transform([text2])
    similarity = cosine_similarity(vector1, vector2)
    similarityPercent = round(float(similarity[0][0])*100)
    return similarityPercent