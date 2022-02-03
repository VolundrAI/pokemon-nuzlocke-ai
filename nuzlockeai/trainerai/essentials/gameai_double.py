from poke_env.player.player import Player
from .essentials_ai_python import get_moveeffect_score, load_moveeffect_map, score_approx_damage, score_calculated_damage
import numpy as np
import asyncio
import nest_asyncio
from poke_env.player.battle_order import DoubleBattleOrder, BattleOrder

nest_asyncio.apply()


def calculate_move_score(
    move,
    user,
    target,
    moveeffect_map,
    battle
) -> int:
    """

    """

    score = 100

    score = get_moveeffect_score(
        score,
        move,
        user,
        target,
        moveeffect_map,
        battle
    )

    if score <= 0:
        #If the score is 0 or less, we skip the rest of the calculations
        return score

    ##Prefer not to use damaging moves when invulnerable
    ##TODO

    ##Perfer a move that goes nicely with choice item if equipped
    ##TODO

    ##If user is asleep, prefer moves that can be used while asleep
    ##TODO

    ##If user is frozen, prefer moves that can be used while frozen
    ##TODO

    ##If target is frozen, prefer moves that don't unthaw them
    ##TODO

    ##Adjust score based on damage of move



    score = asyncio.get_event_loop().run_until_complete(score_calculated_damage(
        score,
        move,
        user,
        target
    ))

    ##Adjust score based on accuracy of move #TODO
    score = int(score * move.accuracy)

    score = max(0, score)

    return score


def get_move_scores(battle, user_moves, user, target, moveeffect_map):
    options = []
    for move in user_moves:
        score = calculate_move_score(
            move,
            user,
            target,
            moveeffect_map,
            battle
        )

        options.append((move, score))

    return options


class GameAIDoublePlayer(Player): #Single Battler

    def teampreview(self, battle):

        return "/team " + "123456"

    def decide_slot_action(self, battle, user_moves, user, moveeffect_map, user_slot):

        options = []

        if battle.opponent_active_pokemon[0] is not None:
            options += [(mv_score, 1) for mv_score in get_move_scores(battle, user_moves, user, battle.opponent_active_pokemon[0], moveeffect_map)]

        if battle.opponent_active_pokemon[1] is not None:
            options += [(mv_score, 2) for mv_score in get_move_scores(battle, user_moves, user, battle.opponent_active_pokemon[1], moveeffect_map)]

        if len(options) == 0:
            max_score = 0
        else:
            max_score = max(options, key=lambda action: action[0][1])[0][1]

        if max_score > 100:
            best_moves = [((move, score), target) for ((move, score), target) in options if score > 100]
            sum_scores = sum([x[0][1] for x in best_moves])

            props = [score / sum_scores for ((move, score), target) in best_moves]

            rnd = np.random.rand()
            for e, p  in enumerate(props):
                if p >= rnd:
                    return self.create_order(best_moves[e][0][0], move_target=best_moves[e][1])
                else:
                    rnd -= p

            return self.create_order(best_moves[e][0][0], move_target=best_moves[e][1])
        elif max_score < 40:
            #If none of the moves are good, we'll choose the best switch our of our other pokemon

            other_options = []
            for e, switch_poke in enumerate(battle.available_switches[user_slot]):
                if battle.opponent_active_pokemon[0] is not None:
                    other_options += [(switch_poke, move, score) for move, score in get_move_scores(battle, switch_poke.moves.values(), switch_poke, battle.opponent_active_pokemon[0], moveeffect_map)]
                if battle.opponent_active_pokemon[1] is not None:
                    other_options += [(switch_poke, move, score) for move, score in get_move_scores(battle, switch_poke.moves.values(), switch_poke, battle.opponent_active_pokemon[1], moveeffect_map)]

            if len(other_options) > 0:
                #Switch to best other poke
                best_option = max(other_options, key=lambda x: x[2])

                if best_option[2] > max_score:
                    return self.create_order(best_option[0])
                elif max_score > 0:
                    only_shot = max(options, key=lambda move: move[0][1])[0][0]
                    return self.create_order(only_shot)
                else:
                    return self.choose_random_move(battle)

            ##If theres no one left to switch to, we just do something random
            return self.choose_random_move(battle)
        else:
            #All the moves are mediocre, so we'll pick a random move weighting them by score
            sum_scores = sum([x[0][1] for x in options])

            props = [score / sum_scores for ((move, score), target) in options]

            rnd = np.random.rand()
            for e, p  in enumerate(props):
                if p >= rnd:
                    return self.create_order(options[e][0][0], move_target=options[e][1])
                else:
                    rnd -= p

            return self.create_order(options[e][0][0], move_target=options[e][1])


    def choose_move(self, battle):
        #Some initial hardcoded loading
        moveeffect_map = load_moveeffect_map("X:/VolundrAI/pokemon-nuzlocke-ai/data/knownmoves.txt")
        # First, for each of the available moves it will calculate a score

        if battle.active_pokemon[0] is not None:
            poke1_action = self.decide_slot_action(battle, battle.available_moves[0], battle.active_pokemon[0], moveeffect_map, 0)
        else:
            poke1_action = None

        if battle.active_pokemon[1] is not None:
            poke2_action = self.decide_slot_action(battle, battle.available_moves[1], battle.active_pokemon[1], moveeffect_map, 1)
        else:
            poke2_action = None

        if poke1_action is None and poke2_action is None:
            return self.choose_random_doubles_move(battle)
        elif poke1_action is None:
            return poke2_action
        elif poke2_action is None:
            return poke1_action
        else:
            if poke1_action is poke2_action or poke1_action == poke2_action:
                return self.choose_random_doubles_move(battle)

            order = DoubleBattleOrder(poke1_action, poke2_action)
            return order
