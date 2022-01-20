from poke_env.player.player import Player
from .essentials_ai_python import get_moveeffect_score, load_moveeffect_map, score_approx_damage, score_calculated_damage
import numpy as np



def calculate_move_score(
    move,
    user,
    target,
    moveeffect_map
) -> int:
    """

    """

    score = 100

    score = get_moveeffect_score(
        score,
        move,
        user,
        target,
        moveeffect_map
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

    score = score_calculated_damage(
        score,
        move,
        user,
        target
    )

    ##Adjust score based on accuracy of move #TODO
    score = int(score * move.accuracy)

    score = max(0, score)

    return score


class GameAIPlayer(Player): #Single Battler

    def teampreview(self, battle):

        return "/team " + "123456"

    def choose_move(self, battle):
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
                moveeffect_map
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
            for e, switch_poke in enumerate(battle.available_switches):
                other_options += [(e, mv, calculate_move_score(mv, switch_poke, target, moveeffect_map)) for _, mv in switch_poke.moves.items()]

            if len(other_options) > 0:
                #Switch to best other poke
                best_option = max(other_options, key=lambda x: x[2])

                if best_option[2] > max_score:
                    return self.create_order(battle.available_switches[best_option[0]])
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
