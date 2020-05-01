import re
from itertools import tee, islice

from unidecode import unidecode

minNgramLength = 1
maxNgramLength = 3


def ngrams_per_line(doc):
    # analyze each line of the input string seperately
    for ln in doc.split(','):
        # tokenize the input string (customize the regex as desired)
        terms = re.findall(u'(?u)\\b\\w+\\b', ln)

        # loop ngram creation for every number between min and max ngram length
        for ngramLength in range(minNgramLength, maxNgramLength + 1):

            # find and return all ngrams
            # for ngram in zip(*[terms[i:] for i in range(3)]): <-- solution without a generator (works the same but has higher memory usage)
            for ngram in zip(*[islice(seq, i, len(terms)) for i, seq in
                               enumerate(tee(terms, ngramLength))]):  # <-- solution using a generator
                ngram = ' '.join(ngram)
                yield ngram


def preprocess_text(line):
    text = line.rsplit(",", 1)[0].strip(" \n\r\t")
#     text = unidecode(text)
    text = re.sub("(?<=[a-z])[-]?(?=[0-9A-Z])", " ", text)
    text = re.sub("(?<=[0-9])(?=[A-Z][a-z]+)", " ", text)
    return text.lower()


if __name__ == "__main__":
    print(preprocess_text("Danang University of Science and Technology550000, Viet Nam"))
    # result = list(
    #     ngrams_per_line(preprocess_text("Ho Chi Minh City University of Techology700000, Viet Nam")))
    # print("-" * 20)
    # print(result)
