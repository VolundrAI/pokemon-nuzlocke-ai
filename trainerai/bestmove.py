from poke_env.player.player import Player

def calc_power(move, current_poke, opponent_poke) -> float:

    power = move.base_power
    power *= opponent_poke.damage_multiplier(move)
    power *= 1.5 if (move.type == current_poke.type_1) else 1.0
    power *= 1.5 if (current_poke.type_2 is not None and move.type == current_poke.type_2) else 1.0

    return power

class BestMovePlayer(Player):
    def choose_move(self, battle):
        # If the player can attack, it will
        if battle.available_moves:

            opponent_poke = battle.opponent_active_pokemon
            current_poke = battle.active_pokemon

            # Finds the best move among available ones
            powers = [(move, calc_power(move, current_poke, opponent_poke)) for move in battle.available_moves]

            best_move = max(powers, key=lambda pair: pair[1])

            return self.create_order(best_move[0])

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)
