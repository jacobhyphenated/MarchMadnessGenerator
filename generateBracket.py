import csv
import sys
import getopt
import json
import random
from collections import OrderedDict
from functools import cmp_to_key

def main(args):
    try:
        opts, _ = getopt.getopt(args[1:], 'ho:s:', ['help', 'output=','seed='])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    outputFormat = 'print'
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-o", "--output"):
            outputFormat = a
        if o in ("-s", "--seed"):
            random.seed(a)

    roundMap = [('Round 2', RD3_WIN), ('Sweet 16', RD4_WIN), ('Elite Eight', RD5_WIN), ('Final 4', RD6_WIN), ('Championship', RD7_WIN)]
    sortedData = sorted(readRawData(), key=cmp_to_key(sortData))
    results = []
    previousRoundVictors = round1(sortedData, results)
    for roundName, roundIndex in roundMap:
        previousRoundVictors = roundN(previousRoundVictors, roundIndex, roundName, results)

    handleResults(results, outputFormat)

def usage():
    print("Tool to help randomly create a March Madness bracket.")
    print("    -h --help\t\tinformation about this command")
    print("    -o --output\t\tOptionally specify an output format. Options are 'print', 'json', 'json-region'. Defaults to print.")
    print("    -s --seed\t\tSpecify the random seed")

"""
Round 1 is easier to calculate than subsequent rounds.
Take a parameter that is the list of rows (sorted) with the necessary data.
return the winning teams for round one in a tuple with the percentage chance of winning.
"""
def round1(data, results):
    round1Victors = []
    for i in range(0, len(data), 2):
        if float(data[i][RD2_WIN]) >= random.random():
            round1Victors.append((data[i], data[i][RD2_WIN]))
        else:
            round1Victors.append((data[i+1], data[i+1][RD2_WIN]))
    results.append(('Round 1', [r for r, v in round1Victors]))
    return round1Victors

"""
Calculating winners for subsequent rounds is more complex. It requires computing
conditional probability based on the chance of winning the previous round.

Parameters
dataMap - list of tuples with the data row and the probability of winning previous round.
roundIndex - Denotes where the win probability is in the CSV file
roundName - the name of this particular round.
results - data structure to store the winning teams in each round
"""
def roundN(dataMap, roundIndex, roundName, results):
    roundVictors = []
    for i in range(0, len(dataMap), 2):
        team1Data, team1PreviousWin = dataMap[i]
        team2Data, team2PreviousWin = dataMap[i+1]

        conditionalWin1 = team1Data[roundIndex]
        roundWinProb1 = float(conditionalWin1) / float(team1PreviousWin)
        conditionalWin2 = team2Data[roundIndex]
        roundWinProb2 = float(conditionalWin2) / float(team2PreviousWin)

        totalProb = roundWinProb1 + roundWinProb2
        actualWin1 = roundWinProb1 / totalProb
        actualWin2 = roundWinProb2 / totalProb

        if actualWin1 >= random.random():
            roundVictors.append((team1Data, actualWin1))
        else:
            roundVictors.append((team2Data, actualWin2))
    results.append((roundName, [r for r, v in roundVictors]))
    return roundVictors

"""
Sort the bracket data to be in competition order.
First sort by region: East, West, Midwest, South
Then sort by seed. 1,16,8,9 etc. such that teams that play each other are adjacent
Note that the region order changes from year to year.
"""
def sortData(line1, line2):
    regionSort = {'West': 3, 'East': 1, 'Midwest': 2, 'South': 0}
    bracketSort = {1: 0, 16: 1, 8: 2, 9: 3, 5: 4, 12: 5, 4: 6, 13: 7, 6: 8, 11: 9, 3: 10, 14: 11, 7: 12, 10: 13, 2: 14, 15: 15 }
    region1 = line1[TEAM_REGION]
    region2 = line2[TEAM_REGION]
    if(region1 != region2):
        return regionSort[region1] - regionSort[region2]
    return bracketSort[int(line1[TEAM_SEED])] - bracketSort[int(line2[TEAM_SEED])]


def readRawData():
    with open('fivethirtyeight_ncaa_forecasts.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        rawForcastData = [row for row in reader]
    return rawForcastData[1:]

def handleResults(results, outputFormat):
    if outputFormat == 'print':
        for roundName, roundResults in results:
            print('')
            print(roundName + ' Winners')
            print('-------------------')
            for r in roundResults: print(r[TEAM_NAME] + '(' + r[TEAM_SEED] + ') ' + r[TEAM_REGION])
    elif outputFormat == 'json-region':
        output = OrderedDict()
        for roundName, roundResults in results:
            roundDict = OrderedDict()
            for r in roundResults:
                region = r[TEAM_REGION]
                name = r[TEAM_NAME] + '(' + r[TEAM_SEED] + ')'
                if region in roundDict: roundDict[region].append(name)
                else: roundDict[region] = [name]
            output[roundName] = roundDict
        print(json.dumps(output, indent=2))
    elif outputFormat == 'json':
        output = OrderedDict()
        for roundName, roundResults in results:
            output[roundName] = [r[TEAM_NAME] + '(' + r[TEAM_SEED] + ') ' + r[TEAM_REGION] for r in roundResults]
        print(json.dumps(output, indent=2))
    else:
        print(outputFormat + ' is not a valid output format')
        sys.exit(1)

# CSV Index Constants
GENDER = 0
FORCAST_DATE = 1
PLAYIN_FLAG = 2
RD1_WIN = 3
RD2_WIN = RD1_WIN + 1
RD3_WIN = RD2_WIN + 1
RD4_WIN = RD3_WIN + 1
RD5_WIN = RD4_WIN + 1
RD6_WIN = RD5_WIN + 1
RD7_WIN = RD6_WIN + 1
TEAM_NAME = 13
TEAM_REGION = 15
TEAM_SEED = 16

if __name__ == "__main__":
    main(sys.argv)
