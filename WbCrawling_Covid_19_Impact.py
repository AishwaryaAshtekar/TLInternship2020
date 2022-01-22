import math
import os
import re
import string
from collections import Counter

import nltk
import pandas as pd
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from nltk.corpus import stopwords
from warcio.archiveiterator import ArchiveIterator


# Function to identify cosine similarity between docs
def get_cosine(vec1, vec2):
    # Numerator value calculation
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    # Denominator value calculation
    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def get_text_from_html(WNL, contents, eng_stop_words):
    soup = BeautifulSoup(contents, 'html.parser')
    cleaned_text = re.sub(r'[\n\t]', '', soup.text).split(" ")
    cleaned_text = [re.sub(r'[^\w\s]', '', word) for word in cleaned_text if word != ""]
    cleaned_text = [word for word in cleaned_text if word not in eng_stop_words]
    cleaned_text = " ".join([WNL.lemmatize(word.lower()) for word in cleaned_text])
    cleaned_text = re.sub(r'&[@#$%&()0-9]*', r'', cleaned_text)
    cleaned_text = re.sub(r'https?\S+', r'', cleaned_text)
    cleaned_text = re.sub('<[^>]*>', '', cleaned_text)
    cleaned_text = cleaned_text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    return cleaned_text


# Function to extract text from a URL and clean the same
def data_extraction(url, WNL, eng_stop_words):
    return get_text_from_html(WNL, requests.get(url).content, eng_stop_words)


def prepopulate_data(WNL, eng_stop_words, WORD):
    # List of URL's for articles relating to COVID 19 economic impact
    url_list = [
        "https://www.census.gov/library/stories/2021/03/initial-impact-covid-19-on-united-states-economy-more-widespread-than-on-mortality.html",
        "https://www.brookings.edu/research/explaining-the-economic-impact-of-covid-19-core-industries-and-the-hispanic-workforce/",
        "https://www.brookings.edu/research/ten-facts-about-covid-19-and-the-u-s-economy/",
        "https://www.bbc.com/news/business-51706225",
        "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7162753/"]

    # String to concatenate and store all the text from above list of URLs after data cleaning
    final_doc = ""
    for url in url_list:
        final_doc = final_doc + data_extraction(url, WNL, eng_stop_words)

    t1 = Counter(WORD.findall(final_doc))
    print(t1)
    return t1


def get_data_in_stream(file_name):
    if file_name.startswith("http://") or file_name.startswith("https://"):
        stream = requests.get(file_name, stream=True).raw
    else:
        stream = open(file_name, "rb")
    return stream


def main():
    # Take user preference for required result
    while True:
        try:
            cosine_similarity_preference = int(input(
                "How much deeper result you want?\n Please give your scale from 0 to 10\n Accuracy will increase from 0 to 10: "))
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue

        if cosine_similarity_preference < 0 or cosine_similarity_preference > 10:
            print("Sorry, your response must be in range of 0 to 10.")
            continue
        else:
            break
    cosine_similarity_preference = (float)(cosine_similarity_preference / 10)
    print(cosine_similarity_preference)
    print('Final_urls_' + (str)(cosine_similarity_preference * 10) + '.csv')
    # Lemmatization of word
    WNL = nltk.WordNetLemmatizer()

    # Stop words in english language
    eng_stop_words = stopwords.words('english')

    # Word Counter
    WORD = re.compile(r"\w+")

    # Prepopulated Data i.e. dict with word and no of occurances from some articles relating to COVID 19 economic impact
    prepopulated_tokens = prepopulate_data(WNL, eng_stop_words, WORD)

    regex = re.compile("(youtu\.be/|youtube\.com/(watch\?(.*\&)?v=|(embed|v)/))([^?&\"'>]+)")

    file_name = "https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-16/segments/1585370490497.6/warc/CC-MAIN-20200328074047-20200328104047-00000.warc.gz"
    try:
        stream = get_data_in_stream(file_name)
        final_url_output = []
        for record in ArchiveIterator(stream):
            if record.rec_type == "warcinfo" or (not ".com/" in record.rec_headers.get_header("WARC-Target-URI")):
                continue
            contents = (record.content_stream().read().decode("utf-8", "replace"))
            if contents != '' and detect(contents) == 'en':

                contents_cleaned_text = get_text_from_html(WNL, contents, eng_stop_words)

                contents_tokens = Counter(WORD.findall(contents_cleaned_text))
                cosine_similarity = get_cosine(prepopulated_tokens, contents_tokens)

                if cosine_similarity >= (cosine_similarity_preference):
                    print(record.rec_headers.get_header('WARC-Target-URI'))
                    final_url_output.append(record.rec_headers.get_header('WARC-Target-URI'))

                if len(final_url_output) == 1000:
                    break
        dict = {"Url:": final_url_output}
        df = pd.DataFrame(dict)
        curr_path = os.path.abspath(os.getcwd())
        df.to_csv(curr_path + '/Final_urls_' + (str)(cosine_similarity_preference * 10) + '.csv')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
