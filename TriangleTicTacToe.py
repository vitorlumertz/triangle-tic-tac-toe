import random
import time
import json


def RemoveNones(t: tuple):
  return [val for val in t if val is not None]


def GetPositionString(p1Positions, p2Positions):
  posString = ''
  boardPositions = 'abcdefghi'
  for c in boardPositions:
    if c in p1Positions:
      posString += 'A'
    elif c in p2Positions:
      posString += 'B'
    else:
      posString += 'x'

  return posString


class Player:
  def __init__(self, level, isP1, bestMovesFileName='BestMoves.json'):
    self.positions = [None for i in range(3)]
    self.level = level
    self.isP1 = isP1
    self.bestMoves = None
    if level == 'FastAdvanced':
      file = open(bestMovesFileName)
      bestMoves = json.load(file)
      self.bestMoves = bestMoves


  def PossibleMoves(self, game, opponentPositions):
    impossiblePositions = RemoveNones(self.positions + opponentPositions)

    if None in self.positions:
      possibleMoves = [('x', p) for p in game.positions if p not in impossiblePositions]
      return possibleMoves

    possibleMoves = list()
    for oldPosition in self.positions:
      pieceMoves = [(oldPosition, newPosition) for newPosition in game.connections[oldPosition] if newPosition not in impossiblePositions]
      possibleMoves.extend(pieceMoves)
    return possibleMoves


  def SetMove(self, move):
    oldPosition = move[0]
    newPosition = move[1]

    if oldPosition == 'x':
      i = self.positions.index(None)
    else:
      i = self.positions.index(oldPosition)

    self.positions[i] = newPosition


  def ResetMove(self, move):
    oldPosition = move[0]
    newPosition = move[1]

    i = self.positions.index(newPosition)

    if oldPosition == 'x':
      self.positions[i] = None
    else:
      self.positions[i] = oldPosition


  def __twoMovesFilter(self, game, opponent):
    possibleMoves = self.PossibleMoves(game, opponent.positions)
    filteredPossibleMoves = list()

    for move in possibleMoves:
      self.SetMove(move)

      if game.IsWinner(self.positions):
        self.ResetMove(move)
        return [move]
      else:
        opponentPms = opponent.PossibleMoves(game, self.positions)
        for m in opponentPms:
          opponent.SetMove(m)
          if game.IsWinner(opponent.positions):
            opponent.ResetMove(m)
            break
          opponent.ResetMove(m)
        else:
          filteredPossibleMoves.append(move)

      self.ResetMove(move)

    if len(filteredPossibleMoves) == 0:
      return [possibleMoves[0]]

    return filteredPossibleMoves


  def RandomMove(self, game, opponent):
    possibleMoves = self.PossibleMoves(game, opponent.positions)
    move = random.choice(possibleMoves)
    self.SetMove(move)
    return move


  def BestMoves(self, game, opponent):
    possibleMoves = self.__twoMovesFilter(game, opponent)
    if len(possibleMoves) == 1:
      bestMoves = [possibleMoves[0]]
      return bestMoves

    maxEval = float('-inf')
    minEval = float('inf')
    bestMoves = list()

    for move in possibleMoves:
      print(move)
      self.SetMove(move)

      eval = minimax(game, 14, float('-inf'), float('inf'), not self.isP1)
      print(eval)
      if self.isP1:
        if eval == maxEval:
          bestMoves.append(move)
        elif eval > maxEval:
          maxEval = eval
          bestMoves = [move]
      else:
        if eval == minEval:
          bestMoves.append(move)
        elif eval < minEval:
          minEval = eval
          bestMoves = [move]

      self.ResetMove(move)

    return bestMoves


  def FastBestMoves(self, opponent):
    p1Positions = self.positions
    p2Positions = opponent.positions
    if not self.isP1:
      p1Positions = opponent.positions
      p2Positions = self.positions

    posString = GetPositionString(p1Positions, p2Positions)
    if self.isP1:
      return self.bestMoves[posString]['P1']
    else:
      return self.bestMoves[posString]['P2']


  def Move(self, game, opponent):
    if self.level == 'Random':
      self.RandomMove(game, opponent)

    if self.level == 'Advanced':
      bestMoves = self.BestMoves(game, opponent)
      move = random.choice(bestMoves)
      self.SetMove(move)
      return move

    if self.level == 'FastAdvanced':
      bestMoves = self.FastBestMoves(opponent)
      move = tuple(random.choice(bestMoves))
      self.SetMove(move)
      return move


class Game:
  def __init__(self, player1: Player, player2: Player):
    self.player1 = player1
    self.player2 = player2

    self.positions = (
      'a',
      'b',
      'c',
      'd',
      'e',
      'f',
      'g',
      'h',
      'i',
    )

    self.connections = {
      'a': ('d', 'f', 'i'),
      'b': ('d', 'e', 'g'),
      'c': ('e', 'f', 'h'),
      'd': ('a', 'b', 'g', 'h'),
      'e': ('b', 'c', 'h', 'i'),
      'f': ('a', 'c', 'g', 'i'),
      'g': ('b', 'd', 'f', 'h', 'i'),
      'h': ('c', 'd', 'e', 'g', 'i'),
      'i': ('a', 'e', 'f', 'g', 'h'),
    }

    self.winnerPositions = [
      ('a', 'b', 'd'),
      ('b', 'c', 'e'),
      ('a', 'c', 'f'),
      ('a', 'e', 'i'),
      ('b', 'f', 'g'),
      ('c', 'd', 'h'),
      ('d', 'g', 'i'),
      ('e', 'g', 'h'),
      ('f', 'h', 'i'),
    ]


  def IsWinner(self, positions) -> bool:
    if None in positions:
      return False

    positions = tuple(sorted(positions))
    if positions in self.winnerPositions:
      return True
    return False


  def IsP1Winner(self) -> bool:
    return self.IsWinner(self.player1.positions)


  def IsP2Winner(self) -> bool:
    return self.IsWinner(self.player2.positions)


  def Evaluation(self):
    if self.IsP1Winner():
      return 1
    elif self.IsP2Winner():
      return -1
    else:
      return 0


def minimax(game: Game, depth, alpha, beta, isMaxPlayer):
  if depth == 0:
    return game.Evaluation()
  if game.IsP1Winner():
    return 1 + depth
  if game.IsP2Winner():
    return -(1 + depth)

  if isMaxPlayer:
    maxEval = float('-inf')
    possibleMoves = game.player1.PossibleMoves(game, game.player2.positions)

    for move in possibleMoves:
      game.player1.SetMove(move)
      eval = minimax(game, depth-1, alpha, beta, False)
      game.player1.ResetMove(move)
      maxEval = max(maxEval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        break
    return maxEval

  else:
    minEval = float('inf')
    possibleMoves = game.player2.PossibleMoves(game, game.player1.positions)

    for move in possibleMoves:
      game.player2.SetMove(move)
      eval = minimax(game, depth-1, alpha, beta, True)
      game.player2.ResetMove(move)
      minEval = min(minEval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        break
    return minEval


##########################################################################################


def AIvsAI(p1Level, p2Level, maxMoves=10):
  p1 = Player(p1Level, True)
  p2 = Player(p2Level, False)
  game = Game(p1,p2)

  # p1.SetMove(('x', 'a'))
  # p2.SetMove(('x', 'i'))

  for i in range(maxMoves):
    ini = time.time()
    print('\nPlayer 1:')
    move = p1.Move(game, p2)
    print('Best Move:', move)
    print(time.time() - ini)
    if game.IsP1Winner():
      print(p1.positions)
      print('Player 1 Win!')
      break

    ini = time.time()
    print('\nPlayer 2:')
    move = p2.Move(game, p1)
    print('Best Move:', move)
    print(time.time() - ini)
    if game.IsP2Winner():
      print(p2.positions)
      print('Player 2 Win!')
      break


def HumanVsAi(level):
  p1 = Player('Random', True)
  p2 = Player(level, False)
  game = Game(p1,p2)
  roundNumber = 1

  while True:
    possibleMoves = p1.PossibleMoves(game, p2.positions)

    while True:
      if roundNumber <= 3:
        print(f'\nRound {roundNumber} - Place a new piece')
        newPosition = input('Enter the position (a-i): ').strip().lower()
        move = ('x', newPosition)
      else:
        print(f'\nRound {roundNumber} - Move one of your pieces')
        oldPosition = input('Move from: ').strip().lower()
        newPosition = input('Move to: ').strip().lower()
        move = (oldPosition, newPosition)

      if move in possibleMoves:
        break

      if roundNumber <= 3:
        print('Invalid move. Please choose an available position from a to i.')
      else:
        print('Invalid move. Choose one of your pieces and an available connected position.')

    p1.SetMove(move)
    if game.IsP1Winner():
      print(p1.positions)
      print('Player 1 Win!')
      break

    move = p2.Move(game, p1)
    if move[0] == 'x':
      print(f'AI placed a new piece at {move[1]}.')
    else:
      print(f'AI moved a piece from {move[0]} to {move[1]}.')
    if game.IsP2Winner():
      print(p2.positions)
      print('Player 2 Win!')
      break

    roundNumber += 1


if __name__ == '__main__':
  #AIvsAI('FastAdvanced', 'FastAdvanced')
  HumanVsAi('FastAdvanced')
