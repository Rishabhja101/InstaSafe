import os
import threading
from threading import Thread
from hatesonar import Sonar

#Natural Language Processing functions
class LanguageProcessor:
    def getOffensiveness(self, string, output_a):
        sonar = Sonar()
        data_raw = str(sonar.ping(string))
        data_raw_split = data_raw.split(": [{")[1].split("}]}")[0].replace("'class_name': '", "").replace("', 'confidence':", "").split("}, {")
        output = data_raw_split[0].split(" ")[0] + " "
        if "e" in data_raw_split[0].split(" ")[1]:
            output += "0.00"
        else:
            output += str('{0:.{1}f}'.format(float(data_raw_split[0].split(" ")[1]) * 100, 2)) + " "
        output += data_raw_split[1].split(" ")[0] + " "
        if "e" in data_raw_split[1].split(" ")[1]:
            output += "0.00"
        else:
            output += str('{0:.{1}f}'.format(float(data_raw_split[1].split(" ")[1]) * 100, 2)) + " "
        output += data_raw_split[2].split(" ")[0] + " "
        if "e" in data_raw_split[2].split(" ")[1]:
            output += "0.00"
        else:
            output += str('{0:.{1}f}'.format(float(data_raw_split[2].split(" ")[1]) * 100, 2))
        output_a.append(output)

    def getSingleAccountData(self, account, output, x):
        current_account_output = []
        #writes username
        current_account_output.append(account[0])
        threads = [None] * (len(account) - 1)
        output_a = []
        for i in range(1, len(account)):
#            self.getOffensiveness(account[i], output_a)
            threads[i - 1] = Thread(target = self.getOffensiveness, args = (account[i], output_a,))
            threads[i - 1].start()
        for i in range(0, len(threads)):
            threads[i].join()
        current_account_output.append(output_a)
        output[x] = current_account_output

    def getCaptionAccountData(self, accountData):
        threads = [None] * len(accountData[1])
        output = [None] * len(accountData[1])
        #loops through each account in captions array
        #for account in accountData[1]: #accountData[1] is an array of account captions
        for i in range (0, len(accountData[1])):
            threads[i] = Thread(target = self.getSingleAccountData, args = (accountData[1][i], output, i,))
            threads[i].start()
        for i in range (0, len(threads)):
            threads[i].join()
        return output

    def __init__(self):
        #Natural Language Processing
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

    def process(self, accountData):
        return self.getCaptionAccountData(accountData)
