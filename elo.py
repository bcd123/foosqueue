import string

# these are global defaults and should not be changed unless we want
# to re-write history
pointsForNewPlayer = 500.0
eloFormulaK = 50.0
eloFormulaF = 1000.0

# maps player name to list representing that player's points history
eloPointsByPlayer = {}

# read data from input file
# format should be lines like this, e.g., copy-pasted from a spreadsheet
# winner_name_1 winner_name_2 looser_name_1 looser_name_2
f = open('eloInput.txt')
gameFileLines = f.readlines()
f.close()

games = [string.split(line) for line in gameFileLines]

def getPlayerPoints(player):
    if player in eloPointsByPlayer:
        return eloPointsByPlayer[player][-1]
    else:
        return pointsForNewPlayer

def updatePlayerPoints(player, pointsToAdd):
    if player in eloPointsByPlayer:
        eloPointsByPlayer[player].append(getPlayerPoints(player)+pointsToAdd)
    else:
        eloPointsByPlayer[player] = [pointsForNewPlayer, pointsForNewPlayer + pointsToAdd]

def getTeamPoints(team):
    return (getPlayerPoints(team[0]) + getPlayerPoints(team[1])) / 2.0

# play each game, updating points appropriately
for game in games:
    if len(game) != 4:
        print 'Skipping line: ', game
        continue

    winners = game[:2]
    loosers = game[2:]
    winnersInitialTeamPoints = getTeamPoints(winners)
    loosersInitialTeamPoints = getTeamPoints(loosers)

    eloFormulaD  = winnersInitialTeamPoints-loosersInitialTeamPoints
    eloFormulaWe = 1.0 / (10.0**(-eloFormulaD/eloFormulaF)+1)
    pointsExchanged = round(eloFormulaK * (1.0 - eloFormulaWe))

    print '%s,%s (%d,%d;%d) beat %s,%s (%d,%d;%d) exchanging %d points' % (winners[0], winners[1], 
                                                                           getPlayerPoints(winners[0]), getPlayerPoints(winners[1]),
                                                                           winnersInitialTeamPoints, 
                                                                           loosers[0], loosers[1], 
                                                                           getPlayerPoints(loosers[0]), getPlayerPoints(loosers[1]),
                                                                           loosersInitialTeamPoints, 
                                                                           pointsExchanged) 

    [updatePlayerPoints(player, pointsExchanged) for player in winners]
    [updatePlayerPoints(player, -pointsExchanged) for player in loosers]

# display final points scoreboard (sorted by latest ranking)
print 'Current Ladder'
print 'Player\t#Games\tPoints'
for k,v in sorted(eloPointsByPlayer.iteritems(), key=lambda (k,v): (-v[-1],k)):
    print '%s\t%04d\t%04d' % (k, len(v)-1, v[-1])


