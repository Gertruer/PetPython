from collections import Counter
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self):
        self.score = 0
        self.history = []
        self.opponent_history = []

    @abstractmethod
    def move(self):
        pass

    def update_history(self, own_move, opponent_move):
        self.history.append(own_move)
        self.opponent_history.append(opponent_move)

class Cheater(Player):
    def move(self):
        return 'cheat'

class Cooperator(Player):
    def move(self):
        return 'cooperate'

class Copycat(Player):
    def move(self):
        if not self.opponent_history:
            return 'cooperate'
        return self.opponent_history[-1]

class Grudger(Player):
    def move(self):
        if 'cheat' in self.opponent_history:
            return 'cheat'
        return 'cooperate'

class Detective(Player):
    def move(self):
        if len(self.history) < 4:
            return ['cooperate', 'cheat', 'cooperate', 'cooperate'][len(self.history)]
        if 'cheat' in self.opponent_history[:4]:
            return self.opponent_history[-1]
        return 'cheat'
    
class Copykitten(Player):
    def move(self):
        if not self.opponent_history:
            return 'cooperate'
        elif len(self.history) > 3:
            return 'cooperate'
        if 'cheat' in self.opponent_history:
            return 'cheat'
        return self.opponent_history[-1]

class Game:
    def __init__(self, matches=10):
        self.matches = matches
        self.registry = Counter()

    def play(self, player1, player2):
        for _ in range(self.matches):
            move1 = player1.move()
            move2 = player2.move()

            player1.update_history(move1, move2)
            player2.update_history(move2, move1)

            if move1 == 'cooperate' and move2 == 'cooperate':
                player1.score += 2
                player2.score += 2
            elif move1 == 'cheat' and move2 == 'cooperate':
                player1.score += 3
                player2.score -= 1
            elif move1 == 'cooperate' and move2 == 'cheat':
                player1.score -= 1
                player2.score += 3
            elif move1 == 'cheat' and move2 == 'cheat':
                player1.score += 0
                player2.score += 0

        self.registry[type(player1).__name__] += player1.score
        self.registry[type(player2).__name__] += player2.score

    def top3(self):
        top_players = self.registry.most_common(3)
        print("Top 3 players:")
        for player, score in top_players:
            print(f"{player}: {score}")

def main():
    game = Game()

    game.play(Copycat(), Cheater())
    game.play(Copycat(), Cooperator())
    game.play(Copycat(), Grudger())
    game.play(Copycat(), Detective())
    game.play(Copycat(), Copykitten())

    game.play(Grudger(), Cheater())
    game.play(Grudger(), Cooperator())
    game.play(Grudger(), Detective())
    game.play(Grudger(), Copykitten())

    game.play(Cheater(), Cooperator())
    game.play(Cheater(), Detective())
    game.play(Cheater(), Copykitten())

    game.play(Cooperator(), Detective())
    game.play(Cooperator(), Copykitten())

    game.play(Detective(), Copykitten())

    game.top3()

if __name__ == "__main__":
    main()