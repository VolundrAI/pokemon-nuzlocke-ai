from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer
from poke_env.player.battle_order import DoubleBattleOrder
from poke_env.server_configuration import ServerConfiguration
import asyncio

def calc_power(move, current_poke, opponent_poke) -> float:

    power = move.base_power
    power *= opponent_poke.damage_multiplier(move)
    power *= 1.5 if (move.type == current_poke.type_1) else 1.0
    power *= 1.5 if (current_poke.type_2 is not None and move.type == current_poke.type_2) else 1.0

    return power

class BestMoveDoublePlayer(Player):
    def choose_move(self, battle):
        # If the player can attack, it will
        if battle.available_moves:
            if battle.active_pokemon[0] is not None:
                current_poke = battle.active_pokemon[0]
                poke_moves = battle.available_moves[0]

                # Finds the best move among available ones
                if battle.opponent_active_pokemon[0] is not None:
                    target1_powers = [(move, calc_power(move, current_poke, battle.opponent_active_pokemon[0])) for move in poke_moves]
                    if len(target1_powers) == 0:
                        best_move1 = (None, -1)
                    else:
                        best_move1 = max(target1_powers, key=lambda pair: pair[1])
                else:
                    best_move1 = (None, -1)

                if battle.opponent_active_pokemon[1] is not None:
                    target2_powers = [(move, calc_power(move, current_poke, battle.opponent_active_pokemon[1])) for move in poke_moves]
                    if len(target2_powers) == 0:
                        best_move2 = (None, -1)
                    else:
                        best_move2 = max(target2_powers, key=lambda pair: pair[1])
                else:
                    best_move2 = (None, -1)

                if best_move1[1] > best_move2[1]:
                    best_move = best_move1[0]
                    target = 1
                else:
                    best_move = best_move2[0]
                    target = 2

                if best_move is None:
                    return self.choose_random_doubles_move(battle)

                poke1_move_order = self.create_order(best_move, move_target=target)
            else:
                poke1_move_order = None

            if battle.active_pokemon[1] is not None:
                current_poke = battle.active_pokemon[1]
                poke_moves = battle.available_moves[1]

                # Finds the best move among available ones
                if battle.opponent_active_pokemon[0] is not None:
                    target1_powers = [(move, calc_power(move, current_poke, battle.opponent_active_pokemon[0])) for move in poke_moves]
                    if len(target1_powers) == 0:
                        best_move1 = (None, -1)
                    else:
                        best_move1 = max(target1_powers, key=lambda pair: pair[1])
                else:
                    best_move1 = (None, -1)

                if battle.opponent_active_pokemon[1] is not None:
                    target2_powers = [(move, calc_power(move, current_poke, battle.opponent_active_pokemon[1])) for move in poke_moves]
                    if len(target2_powers) == 0:
                        best_move2 = (None, -1)
                    else:
                        best_move2 = max(target2_powers, key=lambda pair: pair[1])
                else:
                    best_move2 = (None, -1)

                if best_move1[1] > best_move2[1]:
                    best_move = best_move1[0]
                    target = 1
                else:
                    best_move = best_move2[0]
                    target = 2

                if best_move is None:
                    return self.choose_random_doubles_move(battle)

                poke2_move_order = self.create_order(best_move, move_target=target)
            else:
                poke2_move_order = None

            if poke1_move_order is None and poke2_move_order is None:
                return self.choose_random_doubles_move(battle)
            elif poke1_move_order is None:
                return poke2_move_order
            elif poke2_move_order is None:
                return poke1_move_order
            else:
                return DoubleBattleOrder(poke1_move_order, poke2_move_order)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_doubles_move(battle)


async def main():
    server_config= ServerConfiguration(
        "localhost:8192",
        "https://play.pokemonshowdown.com/action.php?"
    )

    opponent = RandomPlayer(server_configuration=server_config, max_concurrent_battles=20, battle_format="gen8randomdoublesbattle")

    player = BestMoveDoublePlayer(server_configuration=server_config, max_concurrent_battles=20, battle_format="gen8randomdoublesbattle")

    res = await player.battle_against(opponent, 100)

    print(f"BestMove Double Battler Win Ratio: {player.n_won_battles / player.n_finished_battles}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
