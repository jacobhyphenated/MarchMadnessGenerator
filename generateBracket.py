import csv
import sys
from random import random

def main(args):
    roundMap = [('Round 2', RD3_WIN), ('Sweet 16', RD4_WIN), ('Elite Eight', RD5_WIN), ('Final 4', RD6_WIN), ('Championship', RD7_WIN)]
    sortedData = sorted(readRawData(), cmp=sortData)
    previousRoundVictors = round1(sortedData)
    for roundName, roundIndex in roundMap:
        previousRoundVictors = roundN(previousRoundVictors, roundIndex, roundName)

def round1(data):
    """
    Round 1 is easier to calculate than subsequent rounds.
    Take a parameter that is the list of rows (sorted) with the necessary data.
    return the winning teams for round one in a tuple with the percentage chance of winning.
    """
    round1Victors = []
    for i in range(0, len(data), 2):
        if float(data[i][RD2_WIN]) >= random():
            round1Victors.append((data[i], data[i][RD2_WIN]))
        else:
            round1Victors.append((data[i+1], data[i+1][RD2_WIN]))
    print('')
    print('Round 1 Winners')
    print('-------------------')
    for r, v in round1Victors: print(r[TEAM_NAME] + '(' + r[TEAM_SEED] + ') ' + r[TEAM_REGION])
    return round1Victors

def roundN(dataMap, roundIndex, roundName):
    """
    Calculating winners for subsequent rounds is more complex. It requires computing
    conditional probability based on the chance of winning the previous round.
    Prints the results at the end of the computation.

    Parameters
    dataMap - list of tuples with the data row and the probability of winning previous round.
    roundIndex - Denotes where the win probability is in the CSV file
    roundName - the name of this particular round.
    """
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

        if actualWin1 >= random():
            roundVictors.append((team1Data, actualWin1))
        else:
            roundVictors.append((team2Data, actualWin2))
    print('')
    print(roundName + ' Winners')
    print('-------------------')
    for r, v in roundVictors: print(r[TEAM_NAME] + '(' + r[TEAM_SEED] + ') ' + r[TEAM_REGION])
    return roundVictors

def sortData(line1, line2):
    """
    Sort the bracket data to be in competition order.
    First sort by region: East, West, Midwest, South
    Then sort by seed. 1,16,8,9 etc. such that teams that play each other are adjacent
    """
    regionSort = {'West': 0, 'East': 1, 'Midwest': 3, 'South': 2}
    bracketSort = {1: 0, 16: 1, 8: 2, 9: 3, 5: 4, 12: 5, 4: 6, 13: 7, 6: 8, 11: 9, 3: 10, 14: 11, 7: 12, 10: 13, 2: 14, 15: 15 }
    region1 = line1[TEAM_REGION]
    region2 = line2[TEAM_REGION]
    if(region1 != region2):
        return regionSort[region1] - regionSort[region2]
    return bracketSort[int(line1[TEAM_SEED])] - bracketSort[int(line2[TEAM_SEED])]


def readRawData():
    with open('fivethirtyeight_ncaa_forecasts.csv', 'rb') as f:
        reader = csv.reader(f)
        rawForcastData = [row for row in reader]
    return rawForcastData[1:]


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
