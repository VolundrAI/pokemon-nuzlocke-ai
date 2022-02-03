from poke_env.player.player import Player
from .essentials_ai_python import get_moveeffect_score, load_moveeffect_map, score_approx_damage, score_calculated_damage
import numpy as np
import asyncio
import nest_asyncio
nest_asyncio.apply()
from time import time
from poke_env.player.battle_order import BattleOrder
from typing import Optional
from dataclasses import dataclass

@dataclass
class CustomBattleOrder(BattleOrder):
    custom_message: Optional[str] = None

    @property
    def message(self):
        if self.custom_message is None:
            return super().message
        else:
            return self.custom_message


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


class GameAIPlayer(Player): #Single Battler

    def teampreview(self, battle):

        return "/team " + "123456"

    def choose_random_move(self, battle):
        switch = str(np.random.choice(list(battle._team.keys()), 1))
        battle_order = CustomBattleOrder(None, custom_message=f"/choose switch {switch.split(':')[-1].strip()[:-2]}")

        return battle_order

    def choose_move(self, battle):

        move_time = time()


        #Some initial hardcoded loading
        moveeffect_map = load_moveeffect_map("X:/VolundrAI/pokemon-nuzlocke-ai/data/knownmoves.txt")
        # First, for each of the available moves it will calculate a score
        user = battle.active_pokemon
        target = battle.opponent_active_pokemon
        options = []
        for move in battle.available_moves:
            score = calculate_move_score(
                move,
                user,
                target,
                moveeffect_map,
                battle
            )

            options.append((move, score))

        #Based on results of found scores, decide what to do:
        if len(options) == 0:
            max_score = 0
        else:
            max_score = max(options, key=lambda move: move[1])[1]

        if max_score > 100:
            #We found some good moves, let's pick a random move with score > 100, weighted by score
            best_moves = [(move, score) for move,score in options if score > 100]
            sum_scores = sum([x[1] for x in best_moves])

            props = [score / sum_scores for _, score in best_moves]

            rnd = np.random.rand()
            for e, p  in enumerate(props):
                if p >= rnd:
                    return self.create_order(best_moves[e][0])
                else:
                    rnd -= p

            return self.create_order(best_moves[e][0])
        elif max_score < 40:
            #If none of the moves are good, we'll choose the best switch our of our other pokemon

            other_options = []
            for e, switch_id in enumerate(battle._team.keys()):
                switch_poke = battle._team[switch_id]

                if switch_poke.active:
                    continue
                elif switch_poke.fainted:
                    continue

                other_options += [(switch_id, mv, calculate_move_score(mv, switch_poke, target, moveeffect_map, battle)) for _, mv in switch_poke.moves.items()]

            if len(other_options) > 0:
                #Switch to best other poke
                best_option = max(other_options, key=lambda x: x[2])

                if best_option[2] > max_score:
                    battle_order = CustomBattleOrder(None, custom_message=f"/choose switch {best_option[0].split(':')[-1].strip()[:-2]}")

                    return battle_order
                elif max_score > 0:
                    only_shot = max(options, key=lambda move: move[1])[0]
                    return self.create_order(only_shot)
                else:
                    return self.choose_random_move(battle)

            ##If theres no one left to switch to, we just do something random
            return self.choose_random_move(battle)
        else:

            #All the moves are mediocre, so we'll pick a random move weighting them by score
            sum_scores = sum([x[1] for x in options])

            props = [score / sum_scores for _, score in options]

            rnd = np.random.rand()
            for e, p  in enumerate(props):
                if p >= rnd:

                    return self.create_order(options[e][0])
                else:
                    rnd -= p

            return self.create_order(options[e][0])
