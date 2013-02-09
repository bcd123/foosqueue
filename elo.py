import string
import sys
import argparse

# these are global defaults and should not be changed unless we want
# to re-write history
pointsForNewPlayer = 500.0
eloFormulaK = 50.0
eloFormulaF = 1000.0

def getPlayerPoints(player, pointsMap):
    if player in pointsMap:
        return pointsMap[player][-1]
    else:
        return pointsForNewPlayer

def updatePlayerPoints(player, pointsToAdd, pointsMap):
    if player in pointsMap:
        pointsMap[player].append(getPlayerPoints(player, pointsMap)+pointsToAdd)
    else:
        pointsMap[player] = [pointsForNewPlayer, pointsForNewPlayer + pointsToAdd]

def getTeamPoints(team, pointsMap):
    return (getPlayerPoints(team[0], pointsMap) + getPlayerPoints(team[1], pointsMap)) / 2.0

def computeEloPoints(gameResults):
    # maps player name to list representing that player's points history
    eloPointsByPlayer = {}

    # play each game, updating points appropriately
    for game in gameResults:
        if len(game) != 4:
            print 'Skipping line: ', game
            continue

        winners = game[:2]
        loosers = game[2:]
        winnersInitialTeamPoints = getTeamPoints(winners, eloPointsByPlayer)
        loosersInitialTeamPoints = getTeamPoints(loosers, eloPointsByPlayer)

        eloFormulaD  = winnersInitialTeamPoints-loosersInitialTeamPoints
        eloFormulaWe = 1.0 / (10.0**(-eloFormulaD/eloFormulaF)+1)
        pointsExchanged = round(eloFormulaK * (1.0 - eloFormulaWe))

        print '%s,%s (%d,%d;%d) beat %s,%s (%d,%d;%d) exchanging %d points' % (winners[0], winners[1], 
                                                                               getPlayerPoints(winners[0], eloPointsByPlayer), getPlayerPoints(winners[1], eloPointsByPlayer),
                                                                               winnersInitialTeamPoints, 
                                                                               loosers[0], loosers[1], 
                                                                               getPlayerPoints(loosers[0], eloPointsByPlayer), getPlayerPoints(loosers[1], eloPointsByPlayer),
                                                                               loosersInitialTeamPoints, 
                                                                               pointsExchanged) 

        [updatePlayerPoints(player, pointsExchanged, eloPointsByPlayer) for player in winners]
        [updatePlayerPoints(player, -pointsExchanged, eloPointsByPlayer) for player in loosers]
    
    return eloPointsByPlayer

def loadGameResultsFromFile(fileName):
    """read data from input file; format should be lines like this,
    e.g., copy-pasted from a spreadsheet: winner_name_1 winner_name_2
    looser_name_1 looser_name_2"""
    with open(fileName) as f:
        gameFileLines = f.readlines()
        gameResults = [string.split(line) for line in gameFileLines]
        return gameResults

def printLadder(eloPointsByPlayer):
    """Display points ladder sorted by points"""
    print 'Current Ladder'
    print 'Player\t#Games\tPoints'
    for k,v in sorted(eloPointsByPlayer.iteritems(), key=lambda (k,v): (-v[-1],k)):
        print '%s\t%04d\t%04d' % (k, len(v)-1, v[-1])

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    parser = argparse.ArgumentParser(description='Compute Elo scores for foosball results')
    parser.add_argument("results_filename")
    args = parser.parse_args()
    
    gameResults = loadGameResultsFromFile(args.results_filename)
    eloPointsByPlayer = computeEloPoints(gameResults)
    printLadder(eloPointsByPlayer)

if __name__ == "__main__":
    sys.exit(main())
