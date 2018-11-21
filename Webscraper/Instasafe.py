import os
from InstagramScraper import InstagramScraper
from ImageClassifier import ImageClassifier
from LanguageProcessor import LanguageProcessor

#set all file paths relative to the location of this program
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#Instagram Scraping
instaScraper = InstagramScraper()
account_data = instaScraper.scrape("usernames.txt")

#Image Classification
imageClassifier = ImageClassifier()
image_classifier_output = imageClassifier.classify(account_data)
print(image_classifier_output)

#Natural Language Processing
languageProcessor = LanguageProcessor()
language_processor_output = languageProcessor.process(account_data)
print(language_processor_output)
