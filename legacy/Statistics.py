from legacy.TriangleTicTacToe import *
from itertools import product
import json


def GeneratePositions():
  characters = ['x', 'A', 'B']
  positions = set()

  for combination in product(characters, repeat=9):
    string = ''
    for c in combination:
      string += c
    numA = string.count('A')
    numB = string.count('B')
    diff = numA - numB
    if (numA <= 3) and (numB <= 3) and (diff >= 0) and (diff <= 1):
      positions.add(string)

  return positions


def GetGameFromPositionString(posString):
  p1 = Player('Advanced', True)
  p2 = Player('Advanced', False)
  game = Game(p1,p2)

  boardPositions = 'abcdefghi'

  for i, c in enumerate(posString):
    if c == 'A':
      p1.SetMove(('x', boardPositions[i]))
    elif c == 'B':
      p2.SetMove(('x', boardPositions[i]))

  return game


def GetBestMoves():
  bestMoves = dict()
  positions = GeneratePositions()
  for p in positions:
    game = GetGameFromPositionString(p)
    p1 = game.player1
    p2 = game.player2

    if game.IsP1Winner():
      bestMoves.update({p: {'P1': 'Winner', 'P2': 'Loser'}})
      continue

    if game.IsP2Winner():
      bestMoves.update({p: {'P1': 'Loser', 'P2': 'Winner'}})
      continue

    numA = p.count('A')
    numB = p.count('B')

    Round = 'Both'
    if numA > numB:
      Round = 'P2'
    elif numA < 3:
      Round = 'P1'

    p1BestMoves = None
    p2BestMoves = None
    if (Round == 'P1') or (Round == 'Both'):
      p1BestMoves = p1.BestMoves(game, p2)
    if (Round == 'P2') or (Round == 'Both'):
      p2BestMoves = p2.BestMoves(game, p1)

    bestMoves.update({p: {'P1': p1BestMoves, 'P2': p2BestMoves}})
    print(p, bestMoves[p])

  return bestMoves


def SaveBestMoves():
  bestMoves = GetBestMoves()
  bestMovesString = json.dumps(bestMoves, sort_keys=True, indent=2)
  file = open('BestMoves2.json', 'a')
  file.write(bestMovesString)
  file.close()


if __name__ == '__main__':
  SaveBestMoves()
