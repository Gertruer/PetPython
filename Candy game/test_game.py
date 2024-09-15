import unittest
from Candy import *

class TestCandyGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.cheater = Cheater()
        self.cooperator = Cooperator()
        self.copycat = Copycat()
        self.grudger = Grudger()
        self.detective = Detective()
        self.copykitten = Copykitten()

    def test_cheater_behavior(self):
       for _ in range(10):
           self.assertEqual(self.cheater.move(), 'cheat')

    def test_cooperator_behavior(self):
       for _ in range(10):
           self.assertEqual(self.cooperator.move(), 'cooperate')

    def test_copycat_behavior(self):
        self.copycat.update_history(self.copycat.move(), 'cheat')

        opponent_moves = ['cooperate', 'cheat', 'cooperate', 'cooperate', 'cheat']
        for opponent_move in opponent_moves:
            copycat_move = self.copycat.move()
            self.assertEqual(copycat_move, self.copycat.opponent_history[-1], 
                            f"Copycat should copy opponent's move: expected {opponent_move}, but got {copycat_move}")
            self.copycat.update_history(copycat_move, opponent_move)


    def test_grudger_behavior(self):
        for _ in range(5):
            grudger_move = self.grudger.move()
            self.assertEqual(grudger_move, 'cooperate')
            self.grudger.update_history(grudger_move, 'cooperate')
        
        self.grudger.update_history(grudger_move, 'cheat') #Mistake
        for _ in range(3):
            grudger_move = self.grudger.move()
            self.assertEqual(grudger_move, 'cheat', 
                            f"Grudger does not forgive mistakes (and cheaters)")
            self.grudger.update_history(grudger_move, 'cooperate')


    def test_detective_behavior(self):
        expected_moves = ['cooperate', 'cheat', 'cooperate', 'cooperate']
        for expected_move in expected_moves:
            actual_move = self.detective.move()
            self.assertEqual(actual_move, expected_move, 
                            f"Expected {expected_move}, but got {actual_move}")
            self.detective.update_history(actual_move, 'cooperate') 

        self.assertEqual(self.detective.move(), 'cheat', 
                     "Detective should cheat after 4 moves if opponent always cooperated")
        #Reset move detective
        self.detective = Detective()
        for _ in range(4):
            self.detective.update_history(self.detective.move(), 'cheat')
        
        opponent_moves = ['cooperate', 'cooperate', 'cheat', 'cooperate']
        for opponent_move in opponent_moves:
            detective_move = self.detective.move()
            self.assertEqual(detective_move, self.detective.opponent_history[-1], 
                            f"Detective should copy opponent's move: expected {opponent_move}, but got {detective_move}")
            self.detective.update_history(detective_move, opponent_move)

    def test_copykitten_behavior(self):
        self.assertEqual(self.copykitten.move(), 'cooperate')
        self.copykitten.update_history(self.copykitten.move(), 'cheat') 
        for _ in range(3):
            copykitten_move = self.copykitten.move()
            self.assertEqual(copykitten_move, 'cheat')
            self.copykitten.update_history(copykitten_move, 'cooperate') 

        opponent_moves = ['cheat', 'cheat', 'cooperate']
        for opponent_move in opponent_moves:
            copykitten_move = self.copykitten.move()
            self.assertEqual(copykitten_move, 'cooperate')
            self.copykitten.update_history(copykitten_move, opponent_move)

        #Restart move copykitten
        self.copykitten = Copykitten()
        for _ in range(6):
            self.assertEqual(self.copykitten.move(), 'cooperate')
            self.copykitten.update_history(self.copykitten.move(), 'cooperate')

    def test_score_calculation(self):
        self.game.play(self.cheater, self.cooperator)
        self.assertEqual(self.cooperator.score, -10)
        self.assertEqual(self.cheater.score, 30)
        
        self.game.play(self.copycat, self.detective)
        self.assertEqual(self.copycat.score, 18)
        self.assertEqual(self.detective.score, 18)
        
    def test_game_length(self):
        self.assertEqual(self.game.matches, 10)

        self.game.matches = 5
        self.game.play(self.copycat, self.detective)
        self.assertEqual(self.game.matches, 5)
        self.assertEqual(self.copycat.score, 8)
        self.assertEqual(self.detective.score, 8)

    def test_game_registry_update(self):
        self.game = Game(matches=5)
        self.game.play(self.cheater, self.cooperator)
        self.assertEqual(self.game.registry['Cheater'], 15)  # 3 points per round * 5 rounds
        self.assertEqual(self.game.registry['Cooperator'], -5)  # -1 point per round * 5 rounds

    def test_player_history_update(self):
        self.game.play(self.cheater, self.cooperator)
        for _ in range(10):
            self.assertEqual(self.cheater.opponent_history[-1], 'cooperate')
            self.assertEqual(self.cooperator.opponent_history[-1], 'cheat')
    
    def test_game_results(self):
        game = Game()
        player_classes = [Cheater, Cooperator, Copycat, Grudger, Detective, Copykitten]  

        for player1_class, player2_class in itertools.combinations(player_classes, 2):
            player1 = player1_class()
            player2 = player2_class()
            game.play(player1, player2)

        top_3 = game.top3()
        self.assertEqual(len(top_3), 3, "Top 3 should contain exactly 3 elements")

        self.assertTrue(top_3[0][1] >= top_3[1][1] >= top_3[2][1], 
                    "Top 3 should be sorted in descending order by score")
        
        expected_winners = ["Copycat", "Copykitten", "Cheater"] 
        actual_winners = [player for player, _ in top_3]
        for winner in expected_winners:
            self.assertIn(winner, actual_winners, 
                        f"{winner} should be in the top 3")



if __name__ == "__main__":
    unittest.main()