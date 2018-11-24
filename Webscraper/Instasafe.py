import os
import threading
from threading import Thread
from InstagramScraper import InstagramScraper
from ImageClassifier import ImageClassifier
from LanguageProcessor import LanguageProcessor

class Instasafe:
    #Image Classification
    def imageClassification(self, account_data, output):
        imageClassifier = ImageClassifier()
        image_classifier_output = imageClassifier.classify(account_data)
        output.append(image_classifier_output)
        print(image_classifier_output)

    #Natural Language Processing
    def naturalLanguageProcessing(self, account_data, output):
        languageProcessor = LanguageProcessor()
        language_processor_output = languageProcessor.process(account_data)
        output.append(language_processor_output)
        print(language_processor_output)

    def run(self):
        #set all file paths relative to the location of this program
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        #Instagram Scraping
        instaScraper = InstagramScraper()
        account_data = instaScraper.scrape("usernames.txt")

        print("Instagram Scraping Complete")

        #initialize output variables for image classification and natural language processing
        image_classifier_output_raw = []
        language_processor_output_raw = []

        #create a thread for image classigication
        thread_imageClassification = Thread(target = self.imageClassification, args = (account_data, image_classifier_output_raw,))
        thread_imageClassification.start()

        #create a thread for natural language processing
        thread_naturalLanguageProcessing = Thread(target = self.naturalLanguageProcessing, args = (account_data, language_processor_output_raw,))
        thread_naturalLanguageProcessing.start()

        #wait for all image classification and natural language processing to finish running
        thread_imageClassification.join()
        thread_naturalLanguageProcessing.join()

        image_classifier_output = image_classifier_output_raw[0]
        language_processor_output = language_processor_output_raw[0]

        print(image_classifier_output)
        print(language_processor_output)
