import os
import requests
import math
import threading
from threading import Thread

class ImageClassifier:
    def formatTag(self, tag):
        line = tag[17:len(tag)]
        split_text = line.split("\"")
        line_final = split_text[3].replace(" ", "_") + " " + '{0:.{1}f}'.format(float(split_text[0].replace(",", "")), 2)
        return line_final

    def getRawImageData(self, image):
        url = "http://api.imagga.com/v1/tagging"
        querystring = {"url":image,"version":"2"}
        headers = {
            'accept': "application/json",
            'authorization': "Basic YWNjXzU0ZGExZjg4Y2ZjYjgzMDphMzUwNTFhZThhZTVjMjExMmI4ZThlNmY1ZDRmODRkMw=="
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        output_raw = response.text
        output_formatted = ""
        output_raw_split = output_raw.split("}")
        for i in range (1, len(output_raw_split) - 3):
            tag_formatted = self.formatTag(output_raw_split[i])
            #if float(tag_formatted.split(" ")[1]) >= 10.00:
            output_formatted += tag_formatted + ","
        output_list = output_formatted.split(",")
        output_list.pop()
        return output_list

    def assessViolence(self, array):
        threat_level = 0
        flag_words = open("violentTags.txt", "r").read().split(", ")
        for i in range (0, 10):
            for n in range (0, len(flag_words)):
                if flag_words[n] in array[i].split(" ")[0]:
                    threat_level += float(array[i].split(" ")[1])
        if threat_level > 0:
            return '{0:.{1}f}'.format(math.log10(threat_level) * 25, 2)
        else:
            return 0
        #return threat_level / 10

    def assessImages(self, rawImageData):
        urls = open(rawImageData, "r").read().split(", ")
        for i in range (0, len(urls)):
            print(self.assessViolence(self.getRawImageData(urls[i])))

    def assessSingleImage(self, account, i, current_account_classifications):
            #writes date
            current_account_classifications[i - 1] = account[i - 1] # account[i - 1] is the date of the post

            #gets raw image data
            rawImageData = self.getRawImageData(account[i]) # account[i] is the post url

            #gets threat level of image
            threatLevel = float(self.assessViolence(rawImageData))
            #rounds threat level to 2 decimals
            threatLevel = round(threatLevel, 2)

            #writes threat level to file
            current_account_classifications[i] = str(threatLevel)

    def getSingleAccountData(self, account, output_array):
        current_account_classifications = [None] * len(account)
        #append username
        current_account_classifications[0] = account[0]

        #create an empty list of threads
        threads = []

        #loops through all posts in account
        #since the loop goes by twos, account[i] = the post url --and-- account[i - 1] = the date of the post
        for i in range(2, len(account), 2):
            #create a thread for each image to classify each image for an account at the same time
            threads.append(Thread(target = self.assessSingleImage, args = (account, i, current_account_classifications,)))
            threads[int(i / 2 - 1)].start()

        #wait for threads to finish
        for i in range(1, len(threads)):
            threads[i].join()
            
        #append the risk level for the account to the output array
        output_array.append(current_account_classifications)

    def getImageAccountData(self, accountData):
        threads_a = []
        output_array = []
        count = 0

        #loop though each account
        for account in accountData[0]:
            threads_a.append(Thread(target = self.getSingleAccountData, args = (account, output_array,)))
            threads_a[count].start()
            count += 1

        #wait for threads to finish
        for i in range(0, count):
            threads_a[i].join()

        return output_array

    def classify(self, accountData):
        return self.getImageAccountData(accountData)

    def __init__(self):
        #Image Classification
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
