from poke_env.player.player import Player
from poke_env.player.battle_order import BattleOrder
from time import time
import numpy as np
from dataclasses import dataclass

from typing import Optional

def calc_power(move, current_poke, opponent_poke) -> float:

    power = move.base_power
    power *= opponent_poke.damage_multiplier(move)
    power *= 1.5 if (move.type == current_poke.type_1) else 1.0
    power *= 1.5 if (current_poke.type_2 is not None and move.type == current_poke.type_2) else 1.0

    return power

@dataclass
class CustomBattleOrder(BattleOrder):
    custom_message: Optional[str] = None

    @property
    def message(self):
        if self.custom_message is None:
            return super().message
        else:
            return self.custom_message


class BestMovePlayer(Player):
    def choose_move(self, battle):
        # If the player can attack, it will

        move_time = time()
        if battle.available_moves:

            opponent_poke = battle.opponent_active_pokemon
            current_poke = battle.active_pokemon

            # Finds the best move among available ones
            powers = [(move, calc_power(move, current_poke, opponent_poke)) for move in battle.available_moves]

            best_move = max(powers, key=lambda pair: pair[1])

            #print(f"{self._username} decided move in {time() - move_time} seconds for turn no. {battle.turn}!")

            return self.create_order(best_move[0])

        # If no attack is available, a random switch will be made
        else:
            #print(f"{self._username} decided move in {time() - move_time} seconds for turn no. {battle.turn}!")
            switch = str(np.random.choice(list(battle._team.keys()), 1))
            battle_order = CustomBattleOrder(None, custom_message=f"/choose switch {switch.split(':')[-1].strip()[:-2]}")

            return battle_order
