import os
from hatesonar import Sonar

#Natural Language Processing functions
class LanguageProcessor:
    def getOffensiveness(self, string):
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
        return (output)

    def getCaptionAccountData(self, accountData):
        output = []
        #loops through each account in captions array
        for account in accountData[1]: #accountData[1] is an array of account captions
            current_account_output = []
            #writes username
            current_account_output.append(account[0])
            for i in range(1, len(account)):
                current_account_output.append(self.getOffensiveness(account[i]))
            output.append(current_account_output)
        return output

    def __init__(self):
        #Natural Language Processing
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

    def process(self, accountData):
        return self.getCaptionAccountData(accountData)
