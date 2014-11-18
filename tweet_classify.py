import nltk
import csv
import pickle

SENTIMENT_MAP = {'0': 'negative', '2': 'neutral', '4': 'positive'}

def hasRepeats(document):
    """Returns True if more than 3 consecutive letters are the same in document."""
    previous = ''
    two_previous = ''
    for letter in document:
        if letter == previous == two_previous:
            return True
        two_previous = previous
        previous = letter
    return False

# features for the classifier
# all features should return a boolean
all_features = {
    'hasGood': lambda document: any(word in ['good', 'awesome', 'wonderful'] for word in document.split()),
    'hasBad': lambda document: any(word in ['bad', 'terrible', 'horrible'] for word in document.split()),
    'hasHappy': lambda document: 'happy' in document or 'happi' in document,
    'hasSad': lambda document: 'sad' in document,
    'hasLove': lambda document: 'love' in document or 'loving' in document,
    'hasHate': lambda document: 'hate' in document,
    'hasSmiley': lambda document: any(word in [':)', ':-)', ':D', '(:', '=)', '(='] for word in document.split()),
    'hasWinky': lambda document: any(word in [';)', ';D'] for word in document.split()),
    'hasFrowny': lambda document: any(word in [':(', ':-(', '):', 'D:', ':.('] for word in document.split()),
    'hasBest': lambda document: 'best' in document,
    'hasWorst': lambda document: 'worst' in document,
    'hasDont': lambda document: any(word in ['dont','don\'t','do not','does not','doesn\'t'] for word in document.split()),
    'hasExclamation': lambda document: '!' in document,
    'hasRepeats': lambda document: hasRepeats(document),
    'hasHeart': lambda document: any(word in ['<3', '&lt;3'] for word in document.split()),
    'hasCant': lambda document: any(word in ['cant','can\'t','can not'] for word in document.split()),
    'hasExpense': lambda document: any(word in ['expensive', 'expense'] for word in document.split()),
    'hasFavorite': lambda document: 'favorite' in document,
    'hasFantastic': lambda document: 'fantastic' in document,
    'hasFuck': lambda document: 'fuck' in document or 'f*ck' in document,
    'hasFriend': lambda document: any(word in ['bff', 'friend'] for word in document.split()),
    'hasAche': lambda document: any(word in ['ache', 'aching'] for word in document.split()),
    'hasLol': lambda document: any(word in ['lol', 'lmao'] for word in document.split()),
    'hasHaha': lambda document: 'haha' in document,
    'hasGreat': lambda document: 'great' in document,
    'hasNo': lambda document: 'no' in document.split(),
    'hasYes': lambda document: 'yes' in document.split(),
    'hasCold': lambda document: 'hot' in document.split(),
    'hasHot': lambda document: 'cold' in document.split(),
    'hasFree': lambda document: 'free' in document,
    'hasImprove': lambda document: 'improve' in document,
    'hasFail': lambda document: 'fail' in document,
    'hasSweet': lambda document: 'sweet' in document,
    'hasSuck': lambda document: 'suck' in document,
    'hasCool': lambda document: 'cool' in document,
    'hasPay': lambda document: 'pay' in document,
    'hasFast': lambda document: 'fast' in document,
    'hasCheap': lambda document: 'cheap' in document,
    'hasPlay': lambda document: 'play' in document,
    'hasIdiot': lambda document: 'idiot' in document,
    'hasUgh': lambda document: 'ugh' in document,
    'hasWtf': lambda document: 'wtf' in document,
    'hasNew': lambda document: 'new' in document.split(),
    'hasSmell': lambda document: 'smell' in document,
    'hasAss': lambda document: 'ass' in document.split(),
    'hasCurse': lambda document: 'curse' in document,
    'hasFunny': lambda document: any(word in ['funny', 'hilarious', 'silly'] for word in document.split()),
    'hasLoss': lambda document: any(word in ['lost', 'loss', 'lose'] for word in document.split()),
    'hasWin': lambda document: any(word in['win', 'won'] for word in document.split()),
    'hasOpportunity': lambda document: 'opportunity' in document,
    'hasAwesome': lambda document: 'awesome' in document,
    'hasConfident': lambda document: 'confident' in document,
    'hasFun': lambda document: 'fun' in document,
    'hasSuper': lambda document: 'super' in document,
    'hasSmile': lambda document: 'smile' in document,
    'hasWow': lambda document: 'wow' in document,
    'hasScary': lambda document: 'scary' in document.split(),
    'hasHurt': lambda document: 'hurt' in document,
    'hasThanks': lambda document: any(word in ['thanks', 'thank you'] for word in document.split()),
    'hasLike': lambda document: 'like' in document.split(),
    'hasDislike': lambda document: 'dislike' in document.split(),
    'hasSave': lambda document: 'save' in document,
    'hasRocks': lambda document: any(word in ['rocks', 'rocked'] for word in document.split()),
    'hasExcited': lambda document: any(word in ['excited', 'exciting'] for word in document.split()),
    'hasRidiculous': lambda document: 'ridiculous' in document,
    'hasCool': lambda document: 'cool' in document,
    'hasHate': lambda document: 'hate' in document or 'hating' in document,
    'hasDisgusting': lambda document: 'disgusting' in document or 'disgust' in document or 'ew' in document or 'gross' in document,
    'hasHorrible': lambda document: 'horrible' in document or 'terrible' in document,
    'hasStupid': lambda document: 'stupid' in document or 'dumb' in document,
    'hasIgnorant': lambda document: 'ignorant' in document,
    'hasShallow': lambda document: 'shallow' in document or 'superficial' in document,
    'hasFail': lambda document: 'fail' in document or 'failed' in document or 'failure' in document,
    'hasFlunk': lambda document: 'flunk' in document,
    'hasUgly': lambda document: 'ugly' in document or 'hideous' in document,
    'hasUnfair': lambda document: 'unfair' in document,
    'hasDirty': lambda document: 'dirty' in document,
    'hasDreadful': lambda document: 'dreadful' in document,
    'hasDepressing': lambda document: 'depressing' in document,
    'hasUnwise': lambda document: 'unwise' in document,
    'hasUpset': lambda document: 'upset' in document,
    'hasRude': lambda document: 'rude' in document or 'mean' in document,
    'hasCruel': lambda document: 'cruel' in document,
    'hasClumsy': lambda document: 'clumsy' in document,
    'hasRocks': lambda document: any(word in ['rocks', 'rocked'] for word in document.split()),
    'hasExcited': lambda document: any(word in ['excited', 'exciting'] for word in document.split()),
    'hasRidiculous': lambda document: 'ridiculous' in document,
    'hasScary': lambda document: 'scary' in document.split(),
    'hasHurt': lambda document: 'hurt' in document,
    'hasThanks': lambda document: any(word in ['thanks', 'thank you'] for word in document.split()),
    'hasLike': lambda document: 'like' in document.split(),
    'hasDislike': lambda document: 'dislike' in document.split(),
    'hasSave': lambda document: 'save' in document,
    'hasWin': lambda document: any(word in['win', 'won'] for word in document.split()),
    'hasOpportunity': lambda document: 'opportunity' in document,
    'hasConfident': lambda document: 'confident' in document,
    'hasFun': lambda document: 'fun' in document,
    'hasSuper': lambda document: 'super' in document,
    'hasSmile': lambda document: 'smile' in document,
    'hasWow': lambda document: 'wow' in document
}

def extract_features(document):
    features = {}
    for feature, function in all_features.items():
        features[feature] = function(document.lower())
    return features

def read_csv(filename):
    fp = open(filename, 'r')
    reader = csv.reader(fp, delimiter=',', quotechar='"', escapechar='\\')
    return [(row[5], SENTIMENT_MAP[row[0]]) for row in reader]

def train_classifier():
    # read in the tweet csv file with training data
    data = read_csv('trainingandtestdata/training.1600000.processed.noemoticon.csv')
    print('read ' + str(len(data)) + ' tweets for training the classifier')

    training_set = nltk.classify.apply_features(extract_features, data)
    return nltk.NaiveBayesClassifier.train(training_set)

def main():
    classifier = train_classifier()

    # read in test data
    data = read_csv('trainingandtestdata/testdata.manual.2009.06.14.csv')
    print('read ' + str(len(data)) + ' tweets for testing the classifier')

    num_correct = 0
    for tweet in data:
        classification = classifier.classify(extract_features(tweet[0]))
        if classification == tweet[1]:
            num_correct +=1
        print(tweet[0] + ':\t' + classification)

    print(str(float(num_correct) / len(data)) + '% accuracy')
    classifier.show_most_informative_features(32)

    f = open('my_classifier.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()

if __name__ == '__main__':
    main()