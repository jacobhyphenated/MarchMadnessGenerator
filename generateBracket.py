import csv
import sys
from random import random

def main(args):
    sortedData = sorted(readRawData(), cmp=sortData)
    for row in sortedData: print(row[TEAM_NAME] + '(' + row[TEAM_SEED] + ') ' + row[TEAM_REGION])
    round1Victors = round1(sortedData)
    roundMap = [('Round 2', RD3_WIN), ('Sweet 16', RD4_WIN), ('Elite Eight', RD5_WIN), ('Final 4', RD6_WIN), ('Championship', RD7_WIN)]
    previousRoundVictors = round1Victors
    for roundName, roundIndex in roundMap:
        previousRoundVictors = roundN(previousRoundVictors, roundIndex, roundName)

def round1(data):
    round1Victors = []
    for i in range(0, len(data), 2):
        if float(data[i][RD2_WIN]) >= random():
            round1Victors.append((data[i], data[i][RD2_WIN]))
        else:
            round1Victors.append((data[i+1], data[i+1][RD2_WIN]))
    print('')
    print('Round 1 Winners')
    for r, v in round1Victors: print(r[TEAM_NAME] + '(' + r[TEAM_SEED] + ') ' + r[TEAM_REGION])
    return round1Victors

def roundN(dataMap, roundIndex, roundName):
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

        print(team1Data[TEAM_NAME] + ' 538 round: ' + str(conditionalWin1) + ' conditional: ' + str(roundWinProb1) + ' actual: ' + str(actualWin1))
        print(team2Data[TEAM_NAME] + ' 538 round: ' + str(conditionalWin2) + ' conditional: ' + str(roundWinProb2) + ' actual: ' + str(actualWin2))

        randomValue = random()
        print('random value:' + str(randomValue))
        if actualWin1 >= randomValue:
            roundVictors.append((team1Data, actualWin1))
        else:
            roundVictors.append((team2Data, actualWin2))
    print('')
    print(roundName + ' Winners')
    for r, v in roundVictors: print(r[TEAM_NAME] + '(' + r[TEAM_SEED] + ') ' + r[TEAM_REGION])
    return roundVictors



'''
Sort the bracket data to be in competition order.
First sort by region: East, West, Midwest, South
Then sort by seed. 1,16,8,9 etc. such that teams that play each other are adjacent
'''
def sortData(line1, line2):
    regionSort = {'East': 0, 'West': 1, 'Midwest': 2, 'South': 3}
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
TEAM_NAME = 12
TEAM_REGION = 14
TEAM_SEED = 15

if __name__ == "__main__":
    main(sys.argv)
