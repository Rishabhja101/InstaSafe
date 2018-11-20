import os
import requests
import math

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

    def getImageAccountData(self, accountData):
        output_array = []
        for account in accountData[0]:
            current_account_classifications = []
            #append username
            current_account_classifications.append(account[0])
            #loops through all posts in account
            #since the loop goes by twos, account[i] = the post url --and-- account[i - 1] = the date of the post
            for i in range(2, len(account), 2):
                #writes date
                current_account_classifications.append(account[i - 1]) # account[i - 1] is the date of the post

                #gets raw image data
                rawImageData = self.getRawImageData(account[i]) # account[i] is the post url

                #gets threat level of image
                threatLevel = float(self.assessViolence(rawImageData))
                #rounds threat level to 2 decimals
                threatLevel = round(threatLevel, 2)

                #writes threat level to file
                current_account_classifications.append(str(threatLevel))
            output_array.append(current_account_classifications)
        return output_array

    def classify(self, accountData):
        return self.getImageAccountData(accountData)

    def __init__(self):
        #Image Classification
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
