from legacy.TriangleTicTacToe import Game, GetPositionString, Player


class TestLegacyRules:
  def setup_method(self):
    self.player1 = Player("Random", True)
    self.player2 = Player("Random", False)
    self.game = Game(self.player1, self.player2)


  def test_board_connections_are_symmetric(self):
    for origin, destinations in self.game.connections.items():
      for destination in destinations:
        assert origin in self.game.connections[destination]


  def test_all_declared_winning_combinations_win_in_any_order(self):
    for combination in self.game.winnerPositions:
      assert self.game.IsWinner(list(reversed(combination)))


  def test_incomplete_and_non_winning_positions_do_not_win(self):
    assert not self.game.IsWinner(["a", "b", None])
    assert not self.game.IsWinner(["a", "b", "c"])


  def test_placement_allows_every_unoccupied_position(self):
    self.player1.positions = ["a", None, None]
    self.player2.positions = ["b", None, None]

    moves = self.player1.PossibleMoves(self.game, self.player2.positions)

    assert set(moves) == {("x", position) for position in "cdefghi"}


  def test_movement_requires_a_connection_and_empty_destination(self):
    self.player1.positions = ["a", "b", "c"]
    self.player2.positions = ["d", "e", "i"]

    moves = set(
      self.player1.PossibleMoves(self.game, self.player2.positions)
    )

    assert moves == {("a", "f"), ("b", "g"), ("c", "f"), ("c", "h")}
    assert ("a", "d") not in moves  # occupied destination
    assert ("a", "h") not in moves  # destination is not connected


  def test_setting_and_resetting_moves_restores_state(self):
    original = list(self.player1.positions)
    placement = ("x", "a")
    self.player1.SetMove(placement)
    self.player1.ResetMove(placement)
    assert self.player1.positions == original

    self.player1.positions = ["a", "b", "c"]
    original = list(self.player1.positions)
    movement = ("a", "d")
    self.player1.SetMove(movement)
    self.player1.ResetMove(movement)
    assert self.player1.positions == original


  def test_position_string_uses_board_order_and_player_markers(self):
    assert GetPositionString(["a", "i"], ["b", "h"]) == "ABxxxxxBA"
