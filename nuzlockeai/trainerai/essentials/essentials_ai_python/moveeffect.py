from poke_env.environment.move import Move
from poke_env.environment.move_category import MoveCategory
from poke_env.environment.status import Status
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.abstract_battle import AbstractBattle
from poke_env.environment.pokemon_gender import PokemonGender
from poke_env.environment.pokemon_type import PokemonType
from poke_env.environment.effect import Effect
from poke_env.environment.side_condition import SideCondition
from poke_env.environment.weather import Weather
from poke_env.environment.field import Field
from poke_env.environment.double_battle import DoubleBattle

moveeffect_dict = {}

def moveeffect_000(score, move, user, target, battle) -> int:
    """
    Move Effect Name: Default

    When a move has no effect, or the id is unknown, this effect will be used.
    """

    return score
moveeffect_dict["000"] = moveeffect_000

def moveeffect_001(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Splash

    Splash has no use, so the AI should never use it.
    """

    score = 0

    return score
moveeffect_dict["001"] = moveeffect_001

def moveeffect_002(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Struggle

    If the AI is forced to use only struggle it should switch, so the score is 0
    """

    score = 0

    return score
moveeffect_dict["002"] = moveeffect_002

def moveeffect_003(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Sleep

    This effect is triggered when the move can cause the target to sleep.

    #TODO: Adjust conditions for checking whether the opponent can sleep instead of just "are they already asleep"
    """

    if target.status is None: #TODO: replace to check if target can sleep (all situations)
        score += 30

        if target.effects.get(Effect.YAWN, None) is not None:
            score -= 30
        if ("marvelscale" in target.possible_abilities and target.ability is None) or target.ability == "marvelscale":
            score -= 30
        for _, mv in target.moves.items():
            if mv.sleep_usable:
                score -= 50
                break
    else:
        if move.category == MoveCategory.STATUS:
            score -= 90

    return score
moveeffect_dict["003"] = moveeffect_003

def moveeffect_004(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Yawn

    This effect is triggered when the move can cause the target to become drowsy.

    #TODO: Adjust conditions for checking whether the opponent can sleep instead of just "are they already asleep"
    """

    if target.effects.get(Effect.YAWN, None) is None and target.status is None: #TODO: replace to check if target can sleep (all situations)
        score += 30

        if ("marvelscale" in target.possible_abilities and target.ability is None) or target.ability == "marvelscale":
            score -= 30
        for _, mv in target.moves.items():
            if mv.sleep_usable:
                score -= 50
                break
    else:
        score -= 100

    return score
moveeffect_dict["004"] = moveeffect_004

def moveeffect_005(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Poison

    This effect is triggered when the move can cause the target to become poisened.

    #TODO: Adjust conditions for checking whether the opponent can be poisened instead of just "are they already poisened"
    """

    if target.status is None: #TODO: replace to check if target can be inflicted (all situations)
        score += 30

        if target.effects.get(Effect.YAWN, None) is not None:
            score -= 40

        if target.current_hp_fraction <= 1.0/4:
            score += 30

        if target.current_hp_fraction <= 1.0/8:
            score += 50

        if ("marvelscale" in target.possible_abilities and target.ability is None) or target.ability == "marvelscale":
            score -= 40
        if ("guts" in target.possible_abilities and target.ability is None) or target.ability == "guts":
            score -= 40
        if ("toxicboost" in target.possible_abilities and target.ability is None) or target.ability == "toxicboost":
            score -= 40
    else:
        if move.category == MoveCategory.STATUS:
            score -= 90

    return score
moveeffect_dict["005"] = moveeffect_005

def moveeffect_006(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Toxic

    This effect is triggered when the move can cause the target to become badly poisened.
    """

    score = moveeffect_005(score, move, user, target, battle)

    return score
moveeffect_dict["006"] = moveeffect_006

def moveeffect_007(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Simple Paralysis

    This effect is triggered when the move can cause the target to become paralyzed.

    #TODO: Adjust conditions for checking whether the opponent can be paralyzed instead of just "are they already paralyzed"
    """

    if target.status is None: #TODO: replace to check if target can be inflicted (all situations)
        score += 30

        try:
            speed = target.stats["spe"]
        except AttributeError:
            speed = None

        if speed is None:
            #Use species base speed as a guestimate
            if target.base_stats["spe"] > user.base_stats["spe"]:
                score += 30
            else:
                score -= 40
        else:
            if target.stats["spe"] > user.stats["spe"]:
                score += 30
            else:
                score -= 40

        if ("marvelscale" in target.possible_abilities and target.ability is None) or target.ability == "marvelscale":
            score -= 40
        if ("guts" in target.possible_abilities and target.ability is None) or target.ability == "guts":
            score -= 40
        if ("quickfeet" in target.possible_abilities and target.ability is None) or target.ability == "quickfeet":
            score -= 40
    else:
        if move.category == MoveCategory.STATUS:
            score -= 90

    return score
moveeffect_dict["007"] = moveeffect_007

def moveeffect_008(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Paralysis + rain perfect accuracy

    This effect is triggered when the move can cause the target to become paralyzed
    """

    score = moveeffect_007(score, move, user, target, battle)

    return score
moveeffect_dict["008"] = moveeffect_008

def moveeffect_009(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Paralysis + flinch

    This effect is triggered when the move can cause the target to become paralyzed
    """

    score = moveeffect_007(score, move, user, target, battle)

    return score
moveeffect_dict["009"] = moveeffect_009

def moveeffect_00A(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Simple Burn

    This effect is triggered when the move can cause the target to become burned.

    #TODO: Adjust conditions for checking whether the opponent can be burned instead of just "are they already burned"
    """

    if target.status is None: #TODO: replace to check if target can be inflicted (all situations)
        score += 30

        if ("marvelscale" in target.possible_abilities and target.ability is None) or target.ability == "marvelscale":
            score -= 40
        if ("guts" in target.possible_abilities and target.ability is None) or target.ability == "guts":
            score -= 40
        if ("quickfeet" in target.possible_abilities and target.ability is None) or target.ability == "quickfeet":
            score -= 40
        if ("flareboost" in target.possible_abilities and target.ability is None) or target.ability == "flareboost":
            score -= 40
    else:
        if move.category == MoveCategory.STATUS:
            score -= 90

    return score
moveeffect_dict["00A"] = moveeffect_00A

def moveeffect_00B(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Burn + Flinch

    This effect is triggered when the move can cause the target to become burned.
    """

    score = moveeffect_00A(score, move, user, target, battle)

    return score
moveeffect_dict["00B"] = moveeffect_00B

def moveeffect_00C(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Simple Freeze

    This effect is triggered when the move can cause the target to become frozen.

    #TODO: Adjust conditions for checking whether the opponent can be frozen instead of just "are they already frozen"
    """

    if target.status is None: #TODO: replace to check if target can be inflicted (all situations)
        score += 30

        if ("marvelscale" in target.possible_abilities and target.ability is None) or target.ability == "marvelscale":
            score -= 20

    else:
        if move.category == MoveCategory.STATUS:
            score -= 90

    return score
moveeffect_dict["00C"] = moveeffect_00C

def moveeffect_00D(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Freeze + hail perfect accuracy

    This effect is triggered when the move can cause the target to become frozen.
    """

    score = moveeffect_00C(score, move, user, target, battle)

    return score
moveeffect_dict["00D"] = moveeffect_00D

def moveeffect_00E(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Freeze + flinch

    This effect is triggered when the move can cause the target to become frozen.
    """

    score = moveeffect_00C(score, move, user, target, battle)

    return score
moveeffect_dict["00E"] = moveeffect_00E

def moveeffect_00F(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Flinch

    This effect is triggered when the move can cause the target to flinch
    """

    score += 60

    if ("innerfocus" in target.possible_abilities and target.ability is None) or target.ability == "innerfocus":
        score -= 30
    elif target.effects.get(Effect.SUBSTITUTE, None) is not None:
        score -= 30

    return score
moveeffect_dict["00F"] = moveeffect_00F

def moveeffect_010(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Flinch + Extra damage to Minimize

    This effect is triggered when the move can cause the target to flinch and
    does extra damage to minimized opponents

    #TODO: Minimize isn't currently an Effect. Raised issue on poke-env github:
    https://github.com/hsahovic/poke-env/issues/251
    """

    score += 30

    if ("innerfocus" in target.possible_abilities and target.ability is None) or target.ability == "innerfocus":
        score -= 30
    elif target.effects.get(Effect.SUBSTITUTE, None) is not None:
        score -= 30

    #if target.effects.get(Effect.MINIMIZE, None) is not None: #TODO: Effect.Minimize doesn't exist!
    #    score += 30

    return score
moveeffect_dict["010"] = moveeffect_010

def moveeffect_011(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Flinch + Only when user is sleeping (Snore)

    This effect is triggered when the move can cause the target to flinch and is
    only usable while sleeping
    """

    if user.status == Status.SLP:
        score += 130

        if ("innerfocus" in target.possible_abilities and target.ability is None) or target.ability == "innerfocus":
            score -= 30
        elif target.effects.get(Effect.SUBSTITUTE, None) is not None:
            score -= 30
    else:
        score = 0

    return score
moveeffect_dict["011"] = moveeffect_011

def moveeffect_012(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: First turn only Flinch (Fake out)

    This effect is triggered when the move can cause the target to flinch and is
    only usable the first turn that the pokemon is out
    """

    if user.first_turn:
        score += 60

        if ("innerfocus" in target.possible_abilities and target.ability is None) or target.ability == "innerfocus":
            score -= 30
        elif target.effects.get(Effect.SUBSTITUTE, None) is not None:
            score -= 30
    else:
        score = 0

    return score
moveeffect_dict["012"] = moveeffect_012

def moveeffect_013(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Confuse

    This effect is triggered when the move can cause the target to become confused

    #TODO: Replace main condition with a better canConfuse function
    """

    if target.effects.get(Effect.CONFUSION, None) is None: ##TODO
        score += 30

    else:
        if move.category == MoveCategory.STATUS:
            score -= 90

    return score
moveeffect_dict["013"] = moveeffect_013

def moveeffect_014(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Confuse (Chatter)

    This effect is triggered when the move can cause the target to become confused
    """

    score = moveeffect_013(score, move, user, target, battle)

    return score
moveeffect_dict["014"] = moveeffect_014

def moveeffect_015(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Confuse + Perfect accuracy in rain + 50% accuracy in sun (Hurricane) + Hits flying

    This effect is triggered when the move can cause the target to become confused
    """

    score = moveeffect_013(score, move, user, target, battle)

    return score
moveeffect_dict["015"] = moveeffect_015

def moveeffect_016(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Attract

    This effect is triggered when the move can cause the target to become attracted
    """

    can_attract = True
    if (user.gender == target.gender) or (user.gender == PokemonGender.NEUTRAL) or (target.gender == PokemonGender.NEUTRAL):
        can_attract = False
        score -= 90
    elif target.effects.get(Effect.ATTRACT, None) is not None:
        can_attract = False
        score -= 80
    elif ("oblivious" in target.possible_abilities and target.ability is None) or target.ability == "oblivious":
        score -= 80
        can_attract = False

    if can_attract and target.item == "destinyknot":
        score -= 30

    return score
moveeffect_dict["016"] = moveeffect_016

def moveeffect_017(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: TriAttack

    This effect is triggered when the move can cause the target to become burned/parad/frozen
    """

    if target.status is None:
        score += 30

    return score
moveeffect_dict["017"] = moveeffect_017

def moveeffect_018(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Cures user of Burn,Poison,PARALYSIS (Refresh)

    This effect is triggered when the move heals the user's burn, para, or poison
    """

    if user.status == Status.PSN or user.status == Status.TOX:
        score += 40

        if user.current_hp_fraction < 1.0/8:
            score += 60
        elif user.current_hp < (user.status_counter + 1) * user.max_hp / 16:
            score += 60
    elif (user.status == Status.BRN) or (user.status == Status.PAR):
        score += 40
    else:
        score -= 90

    return score
moveeffect_dict["018"] = moveeffect_018

def moveeffect_019(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Cures party of permanent status conditions

    This effect is triggered when the move heals the party's status conditions
    """

    if isinstance(battle, DoubleBattle):
        switches = battle.available_switches[0]
    else:
        switches = battle.available_switches
    statuses = len(
        [
            poke
            for poke in switches + [user]
            if poke.status not in [None, Status.FNT]
        ]
    )

    if statuses == 0:
        score -= 80
    else:
        score += 20*statuses

    return score
moveeffect_dict["019"] = moveeffect_019

def moveeffect_01A(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Protects party from status conditions (Safeguard)
    """

    if user.effects.get(Effect.SAFEGUARD, None) is not None:
        score -= 80
    elif user.status is not None:
        score -= 40
    else:
        score += 30

    return score
moveeffect_dict["01A"] = moveeffect_01A

def moveeffect_01B(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Passes own status condition onto the target (Psycho Shift)
    """

    if user.status is None:
        score -= 90
    else:
        score += 40

    return score
moveeffect_dict["01B"] = moveeffect_01B

def moveeffect_01C(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user attack by one stage
    """

    if move.category == MoveCategory.STATUS:
        if user.boosts.get("atk", 0) == 6:
            score -= 90
        else:
            score -= 20 * user.boosts.get("atk", 0)

            has_phys = False
            for _, mv in user.moves.items():
                if mv.category == MoveCategory.PHYSICAL:
                    has_phys = True
                    break

            if has_phys:
                score += 20
            else:
                score -= 90
    else:
        if user.boosts.get("atk", 0) < 0:
            score += 20

        has_phys = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.PHYSICAL:
                has_phys = True
                break

        if has_phys:
            score += 20

    return score
moveeffect_dict["01C"] = moveeffect_01C

def moveeffect_01D(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user defense by one stage
    """

    if move.category == MoveCategory.STATUS:
        if user.boosts.get("def", 0) == 6:
            score -= 90
        else:
            score -= 20 * user.boosts.get("def", 0)
    else:
        if user.boosts.get("def", 0) < 0:
            score += 20

    return score
moveeffect_dict["01D"] = moveeffect_01D

def moveeffect_01E(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user defense by one stage
    """

    score = moveeffect_01D(score, move, user, target, battle)

    return score
moveeffect_dict["01E"] = moveeffect_01E

def moveeffect_01F(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user speed by one stage
    """

    if move.category == MoveCategory.STATUS:
        if user.boosts.get("spe", 0) == 6:
            score -= 90
        else:
            score -= 10 * user.boosts.get("spe", 0)

            try:
                speed = target.stats["spe"]
            except AttributeError:
                speed = None

            if speed is None:
                #Use species base speed as a guestimate
                if (target.base_stats["spe"] > user.base_stats["spe"]) and (target.base_stats["spe"] < 2*user.base_stats["spe"]):
                    score += 30
            else:
                if (target.stats["spe"] > user.stats["spe"]) and (target.stats["spe"] < 2*user.stats["spe"]):
                    score += 30
    else:
        if user.boosts.get("spe", 0) < 0:
            score += 20

    return score
moveeffect_dict["01F"] = moveeffect_01F

def moveeffect_020(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user special attack by one stage
    """

    if move.category == MoveCategory.STATUS:
        if user.boosts.get("spa", 0) == 6:
            score -= 90
        else:
            score -= 20 * user.boosts.get("spa", 0)

            has_spec = False
            for _, mv in user.moves.items():
                if mv.category == MoveCategory.SPECIAL:
                    has_spec = True
                    break

            if has_spec:
                score += 20
            else:
                score -= 90
    else:
        if user.boosts.get("spa", 0) < 0:
            score += 20

        has_spec = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.SPECIAL:
                has_spec = True
                break

        if has_spec:
            score += 20

    return score
moveeffect_dict["020"] = moveeffect_020

def moveeffect_021(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user special defense by one stage and powers next electric move
    (Charge)
    """

    for _, mv in user.moves.items():
        if move.category == MoveCategory.STATUS:
            continue
        if move.type != PokemonType.ELECTRIC:
            continue
        score += 20
        break

    if move.category == MoveCategory.STATUS:
        if user.boosts.get("spd", 0) == 6:
            score -= 90
        else:
            score -= 20 * user.boosts.get("spd", 0)
    else:
        if user.boosts.get("spd", 0) < 0:
            score += 20

    return score
moveeffect_dict["021"] = moveeffect_021

def moveeffect_022(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user evasion by one stage
    """

    if move.category == MoveCategory.STATUS:
        if user.boosts.get("evasion", 0) == 6:
            score -= 90
        else:
            score -= 10 * user.boosts.get("evasion", 0)
    else:
        if user.boosts.get("evasion", 0) < 0:
            score += 20

    return score
moveeffect_dict["022"] = moveeffect_022

def moveeffect_023(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's crit ratio (FocusEnergy)
    """

    if move.category == MoveCategory.STATUS:
        if user.effects.get(Effect.FOCUS_ENERGY, None) is not None:
            score -= 80
        else:
            score += 30
    else:
        if user.effects.get(Effect.FOCUS_ENERGY, None) is None:
            score += 30

    return score
moveeffect_dict["023"] = moveeffect_023

def moveeffect_024(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's attack and defense by one stage (Bulk Up)
    """

    if user.boosts.get("atk", 0) == 6 and  user.boosts.get("def", 0) == 6:
        score -= 90
    else:
        score -= 10 * user.boosts.get("atk", 0)
        score -= 10 * user.boosts.get("def", 0)

        has_phys = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.PHYSICAL:
                has_phys = True
                break

        if has_phys:
            score += 20
        else:
            score -= 90

    return score
moveeffect_dict["024"] = moveeffect_024

def moveeffect_025(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's attack, defense, and accuracy by one stage (Coil)
    """

    if user.boosts.get("atk", 0) == 6 and user.boosts.get("def", 0) == 6 and user.boosts.get("accuracy", 0) == 6:
        score -= 90
    else:
        score -= 10 * user.boosts.get("atk", 0)
        score -= 10 * user.boosts.get("def", 0)
        score -= 10 * user.boosts.get("accuracy", 0)

        has_phys = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.PHYSICAL:
                has_phys = True
                break

        if has_phys:
            score += 20
        else:
            score -= 90

    return score
moveeffect_dict["025"] = moveeffect_025

def moveeffect_026(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's attack and speed by one stage (Dragon Dance)
    """

    if user.first_turn:
        score += 40

    if user.boosts.get("atk", 0) == 6 and user.boosts.get("spe", 0) == 6:
        score -= 90
    else:
        score -= 10 * user.boosts.get("atk", 0)
        score -= 10 * user.boosts.get("spe", 0)

        has_phys = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.PHYSICAL:
                has_phys = True
                break

        if has_phys:
            score += 20
        else:
            score -= 90

        try:
            speed = target.stats["spe"]
        except AttributeError:
            speed = None

        if speed is None:
            #Use species base speed as a guestimate
            if (target.base_stats["spe"] > user.base_stats["spe"]) and (target.base_stats["spe"] < 2*user.base_stats["spe"]):
                score += 20
        else:
            if (target.stats["spe"] > user.stats["spe"]) and (target.stats["spe"] < 2*user.stats["spe"]):
                score += 20

    return score
moveeffect_dict["026"] = moveeffect_026

def moveeffect_027(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's attack and special attack by one stage (Work Up)
    """

    if user.boosts.get("atk", 0) == 6 and user.boosts.get("spa", 0) == 6:
        score -= 90
    else:
        score -= 10 * user.boosts.get("atk", 0)
        score -= 10 * user.boosts.get("spa", 0)

        has_damage = False
        for _, mv in user.moves.items():
            if mv.category != MoveCategory.STATUS:
                has_damage = True
                break

        if has_damage:
            score += 20
        else:
            score -= 90

    return score
moveeffect_dict["027"] = moveeffect_027

def moveeffect_028(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's attack and special attack by one stage (Growth)
    Effect is doubled in Sunlight.
    """

    score = moveeffect_027(score, move, user, target, battle)

    if battle.weather.get(Weather.SUNNYDAY, None) is not None:
        score += 20
    elif battle.weather.get(Weather.DESOLATELAND, None) is not None:
        score += 20

    return score
moveeffect_dict["028"] = moveeffect_028

def moveeffect_029(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's attack and accuracy by one stage (Hone Claws)
    """

    if user.boosts.get("atk", 0) == 6 and user.boosts.get("accuracy", 0) == 6:
        score -= 90
    else:
        score -= 10 * user.boosts.get("atk", 0)
        score -= 10 * user.boosts.get("accuracy", 0)

        has_damage = False
        for _, mv in user.moves.items():
            if mv.category != MoveCategory.PHYSICAL:
                has_damage = True
                break

        if has_damage:
            score += 20
        else:
            score -= 90

    return score
moveeffect_dict["029"] = moveeffect_029

def moveeffect_02A(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's defense and special defense by one stage (Cosmic Power)
    """

    if user.boosts.get("def", 0) == 6 and user.boosts.get("spd", 0) == 6:
        score -= 90
    else:
        score -= 10 * user.boosts.get("def", 0)
        score -= 10 * user.boosts.get("spd", 0)

    return score
moveeffect_dict["02A"] = moveeffect_02A

def moveeffect_02B(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's special attack, special defense, and speed by one stage (Quiver Dance)
    """

    if user.boosts.get("spa", 0) == 6 and user.boosts.get("spe", 0) == 6 and user.boosts.get("spd", 0) == 6:
        score -= 90
    else:
        score -= 10 * user.boosts.get("spa", 0)
        score -= 10 * user.boosts.get("spe", 0)
        score -= 10 * user.boosts.get("spd", 0)

        has_spec = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.SPECIAL:
                has_spec = True
                break

        if has_spec:
            score += 20
        else:
            score -= 90

        try:
            speed = target.stats["spe"]
        except AttributeError:
            speed = None

        if speed is None:
            #Use species base speed as a guestimate
            if (target.base_stats["spe"] > user.base_stats["spe"]) and (target.base_stats["spe"] < 2*user.base_stats["spe"]):
                score += 20
        else:
            if (target.stats["spe"] > user.stats["spe"]) and (target.stats["spe"] < 2*user.stats["spe"]):
                score += 20

    return score
moveeffect_dict["02B"] = moveeffect_02B

def moveeffect_02C(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's special attack and special defense (Calm Mind)
    """

    if user.first_turn:
        score += 40

    if user.boosts.get("spa", 0) == 6 and user.boosts.get("spd", 0) == 6:
        score -= 90
    else:
        score -= 10 * user.boosts.get("spa", 0)
        score -= 10 * user.boosts.get("spd", 0)

        has_spec = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.SPECIAL:
                has_spec = True
                break

        if has_spec:
            score += 20
        else:
            score -= 90

    return score
moveeffect_dict["02C"] = moveeffect_02C

def moveeffect_02D(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's stats by 1 each (Ancient Power)
    """

    for stat in ["atk", "def", "spa", "spd", "spe"]:
        if user.boosts.get(stat, 0) < 0:
            score += 10

    has_damaging = False
    for _, mv in user.moves.items():
        if mv.category != MoveCategory.STATUS:
            has_damaging = True
            break

    if has_damaging:
        score += 20

    return score
moveeffect_dict["02D"] = moveeffect_02D

def moveeffect_02E(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's attack by two (Swords Dance)
    """

    if move.category == MoveCategory.STATUS:
        if user.first_turn:
            score += 40

        if user.boosts.get("atk", 0) == 6:
            score -= 90
        else:
            score -= 20 * user.boosts.get("atk", 0)

            has_phys = False
            for _, mv in user.moves.items():
                if mv.category == MoveCategory.PHYSICAL:
                    has_phys = True
                    break

            if has_phys:
                score += 20
            else:
                score -= 90
    else:
        if user.first_turn:
            score += 10

        if user.boosts.get("atk", 0) < 0:
            score += 20

        has_phys = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.PHYSICAL:
                has_phys = True
                break

        if has_phys:
            score += 20

    return score
moveeffect_dict["02E"] = moveeffect_02E

def moveeffect_02F(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's defense by two (Iron Defense)
    """

    if move.category == MoveCategory.STATUS:
        if user.first_turn:
            score += 40

        if user.boosts.get("def", 0) == 6:
            score -= 90
        else:
            score -= 20 * user.boosts.get("def", 0)
    else:
        if user.first_turn:
            score += 10

        if user.boosts.get("atk", 0) < 0:
            score += 20

    return score
moveeffect_dict["02F"] = moveeffect_02F

def moveeffect_030(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's speed by two (Agility)
    """

    if move.category == MoveCategory.STATUS:
        if user.first_turn:
            score += 20

        if user.boosts.get("spe", 0) == 6:
            score -= 90
        else:
            score -= 10 * user.boosts.get("spe", 0)

            try:
                speed = target.stats["spe"]
            except AttributeError:
                speed = None

            if speed is None:
                #Use species base speed as a guestimate
                if (target.base_stats["spe"] > user.base_stats["spe"]) and (target.base_stats["spe"] < 2*user.base_stats["spe"]):
                    score += 30
            else:
                if (target.stats["spe"] > user.stats["spe"]) and (target.stats["spe"] < 2*user.stats["spe"]):
                    score += 30
    else:
        if user.first_turn:
            score += 10

        if user.boosts.get("spe", 0) < 0:
            score += 20

    return score
moveeffect_dict["030"] = moveeffect_030

def moveeffect_031(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's speed by two and reduce weight by 100kg. (Autotomize)
    """

    score = moveeffect_030(score, move, user, target, battle)

    return score
moveeffect_dict["031"] = moveeffect_031

def moveeffect_032(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's special attack by two (Nasty Plot)
    """

    if move.category == MoveCategory.STATUS:
        if user.first_turn:
            score += 40

        if user.boosts.get("spa", 0) == 6:
            score -= 90
        else:
            score -= 20 * user.boosts.get("spa", 0)

        has_spec = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.SPECIAL:
                has_spec = True
                break

        if has_spec:
            score += 20
        else:
            score -= 90


    else:
        if user.first_turn:
            score += 10

        if user.boosts.get("spa", 0) < 0:
            score += 20

        has_spec = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.SPECIAL:
                has_spec = True
                break

        if has_spec:
            score += 20

    return score
moveeffect_dict["032"] = moveeffect_032

def moveeffect_033(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's special defense by two (Amnesia)
    """

    if move.category == MoveCategory.STATUS:
        if user.first_turn:
            score += 40

        if user.boosts.get("spd", 0) == 6:
            score -= 90
        else:
            score -= 20 * user.boosts.get("spd", 0)
    else:
        if user.first_turn:
            score += 10

        if user.boosts.get("spd", 0) < 0:
            score += 20

    return score
moveeffect_dict["033"] = moveeffect_033

def moveeffect_034(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's evasion by two and minimizes (Minimize)
    """

    if move.category == MoveCategory.STATUS:
        if user.first_turn:
            score += 40

        if user.boosts.get("evasion", 0) == 6:
            score -= 90
        else:
            score -= 10 * user.boosts.get("evasion", 0)
    else:
        if user.first_turn:
            score += 10

        if user.boosts.get("evasion", 0) < 0:
            score += 20

    return score
moveeffect_dict["034"] = moveeffect_034

def moveeffect_035(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's attack, special attack, and speed by two.
    Decreases user's defense and special defense by one. (Shell Smash)
    """

    score -= 20 * user.boosts.get("atk", 0)
    score -= 20 * user.boosts.get("spa", 0)
    score -= 20 * user.boosts.get("spe", 0)
    score += 10 * user.boosts.get("def", 0)
    score += 10 * user.boosts.get("spd", 0)

    has_damage = False
    for _, mv in user.moves.items():
        if mv.category != MoveCategory.STATUS:
            has_damage = True
            break

    if has_damage:
        score += 20

    return score
moveeffect_dict["035"] = moveeffect_035

def moveeffect_036(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's speed by two and attack by one (Shift Gear)
    """

    if user.boosts.get("spe", 0) == 6 and user.boosts.get("atk", 0) == 6:
        score -= 90
    else:
        score -= 10 * user.boosts.get("atk", 0)
        score -= 10 * user.boosts.get("spe", 0)

        has_phys = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.PHYSICAL:
                has_phys = True
                break

        if has_phys:
            score += 20
        else:
            score -= 90

        try:
            speed = target.stats["spe"]
        except AttributeError:
            speed = None

        if speed is None:
            #Use species base speed as a guestimate
            if (target.base_stats["spe"] > user.base_stats["spe"]) and (target.base_stats["spe"] < 2*user.base_stats["spe"]):
                score += 30
        else:
            if (target.stats["spe"] > user.stats["spe"]) and (target.stats["spe"] < 2*user.stats["spe"]):
                score += 30

    return score
moveeffect_dict["036"] = moveeffect_036

def moveeffect_037(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases a random stat by two stages (Acupressure)
    """

    avg_stat = 0
    can_change = False

    for stat in ["atk", "def", "spa", "spd", "spe", "evasion", "accuracy"]:
        if target.boosts.get(stat, 0) == 6:
            continue
        can_change = True
        avg_stat -= target.boosts.get(stat, 0)

    if can_change:
        avg_stat = avg_stat // 2
        score += avg_stat * 10
    else:
        score -= 90

    return score
moveeffect_dict["037"] = moveeffect_037

def moveeffect_038(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's defense by three (Cotton Guard)
    """

    if move.category == MoveCategory.STATUS:
        if user.boosts.get("def", 0) == 6:
            score -= 90
        else:
            if user.first_turn:
                score += 40

            score -= 30 * user.boosts.get("def", 0)
    else:
        if user.first_turn:
            score += 10
        if user.boosts.get("def", 0) < 0:
            score += 30

    return score
moveeffect_dict["038"] = moveeffect_038

def moveeffect_039(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user's special attack by three (Tail Glow)
    """

    if move.category == MoveCategory.STATUS:
        if user.boosts.get("spa", 0) == 6:
            score -= 90
        else:
            if user.first_turn:
                score += 40

            score -= 30 * user.boosts.get("spa", 0)

            has_spec = False
            for _, mv in user.moves.items():
                if mv.category == MoveCategory.SPECIAL:
                    has_spec = True
                    break

            if has_spec:
                score += 20
            else:
                score -= 90
    else:
        if user.first_turn:
            score += 10
        if user.boosts.get("spa", 0) < 0:
            score += 30

        has_spec = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.SPECIAL:
                has_spec = True
                break

        if has_spec:
            score += 30

    return score
moveeffect_dict["039"] = moveeffect_039

def moveeffect_03A(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Maxs attack but cuts HP in half max (Belly Drum)
    """

    if user.boosts.get("atk", 0) == 6 or user.current_hp_fraction <= 0.5:
        score -= 100
    else:
        score += (6 - user.boosts.get("atk", 0))*10

        has_phys = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.PHYSICAL:
                has_phys = True
                break

        if has_phys:
            score += 40
        else:
            score -= 90

    return score
moveeffect_dict["03A"] = moveeffect_03A

def moveeffect_03B(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases user's attack and defense by one stage (Superpower)
    """

    avg = user.boosts.get("atk", 0)*10
    avg += user.boosts.get("def", 0)*10

    score += avg // 2

    return score
moveeffect_dict["03B"] = moveeffect_03B

def moveeffect_03C(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases user's defense and special defense by one stage (Close Combat)
    """

    avg = user.boosts.get("def", 0)*10
    avg += user.boosts.get("spd", 0)*10

    score += avg // 2

    return score
moveeffect_dict["03C"] = moveeffect_03C

def moveeffect_03D(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases user's defense, special defense, and speed by one stage (V-Create)
    """

    avg = user.boosts.get("def", 0)*10
    avg += user.boosts.get("spd", 0)*10
    avg += user.boosts.get("spe", 0)*10

    score += avg // 3

    return score
moveeffect_dict["03D"] = moveeffect_03D

def moveeffect_03E(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases user's speed by one stage (Hammer Arm)
    """

    score += user.boosts.get("spe", 0)*10

    return score
moveeffect_dict["03E"] = moveeffect_03E

def moveeffect_03F(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases user's special attack by two stages
    """

    score += user.boosts.get("spa", 0)*10

    return score
moveeffect_dict["03F"] = moveeffect_03F

def moveeffect_040(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases target's spa by 1, and confuses (Flatter)

    #TODO: Improve the check if target can be confused!
    """

    if target.effects.get(Effect.CONFUSED, None) is not None:
        score -= 90
    elif target.boosts.get("spa", 0) < 0:
        score += 30

    return score
moveeffect_dict["040"] = moveeffect_040

def moveeffect_041(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases target's atk by 2, and confuses (Swagger)

    #TODO: Improve the check if target can be confused!
    """

    if target.effects.get(Effect.CONFUSED, None) is not None:
        score -= 90
    elif target.boosts.get("atk", 0) < 0:
        score += 30

    return score
moveeffect_dict["041"] = moveeffect_041

def moveeffect_042(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's atk by 1

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("atk", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            score += 20*target.boosts.get("atk", 0)

        has_phys = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.PHYSICAL:
                has_phys = True
                break

        if has_phys:
            score += 20
        else:
            score -= 90
    else:
        if target.boosts.get("atk", 0) > 0:
            score += 20

        has_phys = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.PHYSICAL:
                has_phys = True
                break

        if has_phys:
            score += 20

    return score
moveeffect_dict["042"] = moveeffect_042

def moveeffect_043(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's def by 1

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("def", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            score += 20*target.boosts.get("def", 0)
    else:
        if target.boosts.get("def", 0) > 0:
            score += 20

    return score
moveeffect_dict["043"] = moveeffect_043

def moveeffect_044(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's speed by 1

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("spe", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            score += 10*target.boosts.get("spe", 0)

            try:
                speed = target.stats["spe"]
            except AttributeError:
                speed = None

            if speed is None:
                #Use species base speed as a guestimate
                if (target.base_stats["spe"] > user.base_stats["spe"]) and (target.base_stats["spe"] < 2*user.base_stats["spe"]):
                    score += 30
            else:
                if (target.stats["spe"] > user.stats["spe"]) and (target.stats["spe"] < 2*user.stats["spe"]):
                    score += 30
    else:
        if target.boosts.get("spe", 0) > 0:
            score += 20

    return score
moveeffect_dict["044"] = moveeffect_044

def moveeffect_045(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's spa by 1

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("spa", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            score += 20*target.boosts.get("spa", 0)

        has_spec = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.SPECIAL:
                has_spec = True
                break

        if has_spec:
            score += 20
        else:
            score -= 90
    else:
        if target.boosts.get("spa", 0) > 0:
            score += 20

        has_spec = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.SPECIAL:
                has_spec = True
                break

        if has_spec:
            score += 20

    return score
moveeffect_dict["045"] = moveeffect_045

def moveeffect_046(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's spd by 1

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("spd", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            score += 20*target.boosts.get("spd", 0)
    else:
        if target.boosts.get("spd", 0) > 0:
            score += 20

    return score
moveeffect_dict["046"] = moveeffect_046

def moveeffect_047(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's accuracy by 1

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("accuracy", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            score += 10*target.boosts.get("accuracy", 0)
    else:
        if target.boosts.get("accuracy", 0) > 0:
            score += 20

    return score
moveeffect_dict["047"] = moveeffect_047

def moveeffect_048(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's evasion by 1/2 stages

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("evasion", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            score += 10*target.boosts.get("evasion", 0)
    else:
        if target.boosts.get("evasion", 0) > 0:
            score += 20

    return score
moveeffect_dict["048"] = moveeffect_048

def moveeffect_049(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's evasion by 1 and clears entry hazards

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("evasion", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            score += 10*target.boosts.get("evasion", 0)
    else:
        if target.boosts.get("evasion", 0) > 0:
            score += 20

    if battle.opponent_side_conditions.get(SideCondition.AURORA_VEIL, None) is not None:
        score += 30
    elif battle.opponent_side_conditions.get(SideCondition.REFLECT, None) is not None:
        score += 30
    elif battle.opponent_side_conditions.get(SideCondition.LIGHT_SCREEN, None) is not None:
        score += 30
    elif battle.opponent_side_conditions.get(SideCondition.MIST, None) is not None:
        score += 30
    elif battle.opponent_side_conditions.get(SideCondition.SAFEGUARD, None) is not None:
        score += 30

    if battle.opponent_side_conditions.get(SideCondition.SPIKES, None) is not None:
        score -= 30
    elif battle.opponent_side_conditions.get(SideCondition.TOXIC_SPIKES, None) is not None:
        score -= 30
    elif battle.opponent_side_conditions.get(SideCondition.STEALTH_ROCK, None) is not None:
        score -= 30

    return score
moveeffect_dict["049"] = moveeffect_049

def moveeffect_04A(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases user's atk/def by 1
    """

    avg = user.boosts.get("atk", 0)*10
    avg += user.boosts.get("def", 0)*10

    score += avg // 2

    return score
moveeffect_dict["04A"] = moveeffect_04A

def moveeffect_04B(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's atk by 2

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("atk", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            score += 20*target.boosts.get("atk", 0)
            if user.first_turn:
                score += 40

            has_phys = False
            for _, mv in user.moves.items():
                if mv.category == MoveCategory.PHYSICAL:
                    has_phys = True
                    break

            if has_phys:
                score += 20
            else:
                score -= 90
    else:
        if user.first_turn:
            score += 10

        if target.boosts.get("atk", 0) > 0:
            score += 20

        has_phys = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.PHYSICAL:
                has_phys = True
                break

        if has_phys:
            score += 20

    return score
moveeffect_dict["04B"] = moveeffect_04B

def moveeffect_04C(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's def by 2

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("def", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            if user.first_turn:
                score += 40

            score += 20*target.boosts.get("def", 0)
    else:
        if user.first_turn:
            score += 10

        if target.boosts.get("def", 0) > 0:
            score += 20

    return score
moveeffect_dict["04C"] = moveeffect_04C

def moveeffect_04D(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's speed by 2

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("spe", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            if user.first_turn:
                score += 20

            score += 20*target.boosts.get("spe", 0)

            try:
                speed = target.stats["spe"]
            except AttributeError:
                speed = None

            if speed is None:
                #Use species base speed as a guestimate
                if (target.base_stats["spe"] > user.base_stats["spe"]) and (target.base_stats["spe"] < 2*user.base_stats["spe"]):
                    score += 30
            else:
                if (target.stats["spe"] > user.stats["spe"]) and (target.stats["spe"] < 2*user.stats["spe"]):
                    score += 30
    else:
        if user.first_turn:
            score += 10
        if target.boosts.get("spe", 0) > 0:
            score += 30

    return score
moveeffect_dict["04D"] = moveeffect_04D

def moveeffect_04E(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's spa by 2, only if opposite gender

    #TODO Improve check if target can have stats lowered!
    """

    if (user.gender == target.gender) or (user.gender == PokemonGender.NEUTRAL) or (target.gender == PokemonGender.NEUTRAL):
        score -= 90
    elif ("oblivious" in target.possible_abilities and target.ability is None) or target.ability == "oblivious":
        score -= 90
    elif move.category == MoveCategory.STATUS:
        if target.boosts.get("spa", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            if user.first_turn:
                score += 40
            score += 20*target.boosts.get("spa", 0)

            has_spec = False
            for _, mv in user.moves.items():
                if mv.category == MoveCategory.SPECIAL:
                    has_spec = True
                    break

            if has_spec:
                score += 20
            else:
                score -= 90
    else:
        if user.first_turn:
            score += 10

        if target.boosts.get("spa", 0) > 0:
            score += 20

        has_spec = False
        for _, mv in user.moves.items():
            if mv.category == MoveCategory.SPECIAL:
                has_spec = True
                break

        if has_spec:
            score += 30

    return score
moveeffect_dict["04E"] = moveeffect_04E

def moveeffect_04F(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Decreases target's spd by 2

    #TODO Improve check if target can have stats lowered!
    """

    if move.category == MoveCategory.STATUS:
        if target.boosts.get("spd", 0) == -6: #TODO improve to check abilities and items
            score -= 90
        else:
            if user.first_turn:
                score += 40

            score += 20*target.boosts.get("spd", 0)
    else:
        if user.first_turn:
            score += 10
        if target.boosts.get("spd", 0) > 0:
            score += 20

    return score
moveeffect_dict["04F"] = moveeffect_04F

def moveeffect_050(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Reset all opponents stat changes to 0 (Clear Smog)
    """

    if target.effects.get(Effect.SUBSTITUTE, None) is not None:
        score -= 90
    else:
        avg = 0
        any_change = False

        for stat in ["atk", "def", "spa", "spd", "spe", "evasion", "accuracy"]:
            if target.boosts.get(stat, 0) == 0:
                continue
            else:
                any_change = True
                avg += target.boosts.get(stat)

        if any_change:
            score += avg*10
        else:
            score -= 90

    return score
moveeffect_dict["050"] = moveeffect_050

def moveeffect_051(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Resets all stat stages for all battlers to 0. (Haze)
    """

    avg = 0

    for stat in ["atk", "def", "spa", "spd", "spe", "evasion", "accuracy"]:
        avg += target.boosts.get(stat, 0)
        avg -= user.boosts.get(stat, 0)

    score += avg*10

    return score
moveeffect_dict["051"] = moveeffect_051

def moveeffect_052(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: User and target swap their Attack and Special Attack stat stages. (Power Swap)
    """
    aatk = user.boosts.get("atk", 0)
    aspa = user.boosts.get("spa", 0)

    oatk = target.boosts.get("atk", 0)
    ospa = target.boosts.get("spa", 0)

    if aatk >= oatk and aspa >= ospa:
        score -= 80
    else:
        score += (oatk - aatk)*10
        score += (ospa - aspa)*10

    return score
moveeffect_dict["052"] = moveeffect_052

def moveeffect_053(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: User and target swap their Defense and Special Defense stat stages. (Guard Swap)
    """
    adef = user.boosts.get("def", 0)
    aspd = user.boosts.get("spd", 0)

    odef = target.boosts.get("def", 0)
    ospd = target.boosts.get("spd", 0)

    if adef >= odef and aspd >= ospd:
        score -= 80
    else:
        score += (odef - adef)*10
        score += (ospd - aspd)*10

    return score
moveeffect_dict["053"] = moveeffect_053

def moveeffect_054(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: User and target swap all their stat stages. (Heart Swap)
    """

    us = 0
    them = 0
    for stat in ["atk", "def", "spa", "spd", "spe", "evasion", "accuracy"]:
        them += target.boosts.get(stat, 0)
        us += user.boosts.get(stat, 0)
    score += (them - user)*10

    return score
moveeffect_dict["054"] = moveeffect_054

def moveeffect_055(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: User copies the target's stat stages. (Psych Up)
    """

    equal = True

    for stat in ["atk", "def", "spa", "spd", "spe", "evasion", "accuracy"]:
        diff = target.boosts.get(stat, 0) - user.boosts.get(stat, 0)
        score += diff*10

        if diff != 0:
            equal = False

    if equal:
        score -= 80

    return score
moveeffect_dict["055"] = moveeffect_055

def moveeffect_056(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: For 5 rounds, user's and ally's stat stages cannot be lowered by foes. (Mist)
    """

    if user.effects.get(Effect.MIST, None) is not None:
        score -= 80

    return score
moveeffect_dict["056"] = moveeffect_056

def moveeffect_057(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Swaps the user's Attack and Defense stats. (Power Trick)
    """

    aatk = user.stats.get("atk", 0)
    adef = user.stats.get("def", 0)

    if aatk == adef or user.effects.get(Effect.POWER_TRICK, None) is not None:
        score -= 90
    elif adef > aatk:
        score += 30
    else:
        score -= 30

    return score
moveeffect_dict["057"] = moveeffect_057

def moveeffect_058(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Averages the user's and target's Attack/Special Attack.
    """

    aatk = user.base_stats.get("atk", 0)
    aspa = user.base_stats.get("spa", 0)

    oatk = target.base_stats.get("atk", 0)
    ospa = target.base_stats.get("spa", 0)

    if aatk<oatk and aspa<ospa:
        score += 50
    elif aatk+aspatk<ospa+oatk:
        score += 30
    else:
        score -= 50

    return score
moveeffect_dict["058"] = moveeffect_058

def moveeffect_059(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Averages the user's and target's Defense/Special Defense.
    """

    adef = user.base_stats.get("def", 0)
    aspd = user.base_stats.get("spd", 0)

    odef = target.base_stats.get("def", 0)
    ospd = target.base_stats.get("spd", 0)

    if adef<odef and aspd<ospd:
        score += 50
    elif adef+aspd<odef+ospd:
        score += 30
    else:
        score -= 50

    return score
moveeffect_dict["059"] = moveeffect_059

def moveeffect_05A(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Averages the user's and target's current HP. (Pain Split)
    """

    if target.effects.get(Effect.SUBSTITUTE, None) is not None:
        score -= 90
    elif user.current_hp_fraction > (user.current_hp_fraction+target.current_hp_fraction)/2:
        score -= 90
    else:
        score += 40

    return score
moveeffect_dict["05A"] = moveeffect_05A

def moveeffect_05B(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: For 4 rounds, doubles the Speed of all battlers on the user's side. (Tailwind)
    """

    if battle.side_conditions.get(SideCondition.TAILWIND, None) is not None:
        score -= 90

    return score
moveeffect_dict["05B"] = moveeffect_05B

def moveeffect_05C(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    This move turns into the last move used by the target, until user switches out. (Mimic)

    #TODO: Check for pokemon's last move
    """

    #TODO: Check for last move

    return score
moveeffect_dict["05C"] = moveeffect_05C

def moveeffect_05D(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    This move permanently turns into the last move used by the target. (Sketch)

    #TODO: Check for pokemon's last move
    """

    #TODO: Check for last move

    return score
moveeffect_dict["05D"] = moveeffect_05D

def moveeffect_05E(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Changes user's type to that of a random user's move, except a type the user
    already has (even partially), OR changes to the user's first move's type.
    (Conversion)
    """

    has_possible = False

    for _, move in user.moves.items():
        if move.type in user.types:
            continue

    if not has_possible:
        score -= 90

    return score
moveeffect_dict["05E"] = moveeffect_05E

def moveeffect_05F(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Changes user's type to a random one that resists/is immune to the last move
    used by the target. (Conversion 2)

    #TODO: Check for pokemon's last move
    """


    #TODO: Check for last move

    return score
moveeffect_dict["05F"] = moveeffect_05F

def moveeffect_060(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Changes user's type depending on the environment. (Camouflage)

    #TODO: Check if pokemon can switch type
    """

    new_type = PokemonType.NORMAL
    if battle.fields.get(Field.ELECTRIC_TERRAIN, None) is not None:
        new_type = PokemonType.ELECTRIC
    if battle.fields.get(Field.GRASSY_TERRAIN, None) is not None:
        new_type = PokemonType.GRASS
    if battle.fields.get(Field.MISTY_TERRAIN, None) is not None:
        new_type = PokemonType.FAIRY
    if battle.fields.get(Field.PSYCHIC_TERRAIN, None) is not None:
        new_type = PokemonType.PSYCHIC

    #TODO: Check if pokemon can switch type

    if new_type in user.types:
        score -= 90

    return score
moveeffect_dict["060"] = moveeffect_060

def moveeffect_060(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Changes user's type depending on the environment. (Camouflage)

    #TODO: Check if pokemon can switch type
    """

    new_type = PokemonType.NORMAL
    if battle.fields.get(Field.ELECTRIC_TERRAIN, None) is not None:
        new_type = PokemonType.ELECTRIC
    if battle.fields.get(Field.GRASSY_TERRAIN, None) is not None:
        new_type = PokemonType.GRASS
    if battle.fields.get(Field.MISTY_TERRAIN, None) is not None:
        new_type = PokemonType.FAIRY
    if battle.fields.get(Field.PSYCHIC_TERRAIN, None) is not None:
        new_type = PokemonType.PSYCHIC

    #TODO: Check if pokemon can switch type

    if new_type in user.types:
        score -= 90

    return score
moveeffect_dict["060"] = moveeffect_060

def moveeffect_061(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Target becomes Water type. (Soak)

    #TODO: Check if pokemon can switch type
    """

    #TODO: Check if pokemon can switch type

    if PokemonType.WATER in target.types:
        score -= 90

    return score
moveeffect_dict["061"] = moveeffect_061

def moveeffect_062(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    User copes target's types. (Reflect Type)

    #TODO: Check if pokemon can switch type
    """

    #TODO: Check if pokemon can switch type

    if all(sorted(user.types) == sorted(target.types)):
        score -= 90

    return score
moveeffect_dict["062"] = moveeffect_062

def moveeffect_063(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Target's ability becomes Simple. (Simple Beam)

    #TODO: Check if pokemon can switch ability
    """

    #TODO: Check if pokemon can switch ability

    if ("simple" in target.possible_abilities and target.ability is None) or target.ability == "simple":
        score -= 90
    elif ("truant" in target.possible_abilities and target.ability is None) or target.ability == "truant":
        score -= 90

    return score
moveeffect_dict["063"] = moveeffect_063

def moveeffect_064(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Target's ability becomes Insomnia. (Worry Seed)

    #TODO: Check if pokemon can switch ability
    """

    #TODO: Check if pokemon can switch ability

    if ("insomnia" in target.possible_abilities and target.ability is None) or target.ability == "insomnia":
        score -= 90
    elif ("truant" in target.possible_abilities and target.ability is None) or target.ability == "truant":
        score -= 90

    return score
moveeffect_dict["064"] = moveeffect_064

def moveeffect_065(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    User copies target's ability. (Role Play)

    #TODO: Check if pokemon can switch ability
    """

    score -= 40


    if ("slowstart" in target.possible_abilities and target.ability is None) or target.ability == "slowstart":
        score -= 90
    elif ("truant" in target.possible_abilities and target.ability is None) or target.ability == "truant":
        score -= 90
    elif ("multitype" in target.possible_abilities and target.ability is None) or target.ability == "multitype":
        score -= 90
    elif ("forecast" in target.possible_abilities and target.ability is None) or target.ability == "forecast":
        score -= 90
    elif ("illusion" in target.possible_abilities and target.ability is None) or target.ability == "illusion":
        score -= 90
    elif ("imposter" in target.possible_abilities and target.ability is None) or target.ability == "imposter":
        score -= 90
    elif ("flowergift" in target.possible_abilities and target.ability is None) or target.ability == "flowergift":
        score -= 90
    elif ("trace" in target.possible_abilities and target.ability is None) or target.ability == "trace":
        score -= 90
    elif ("wonderguard" in target.possible_abilities and target.ability is None) or target.ability == "wonderguard":
        score -= 90
    elif ("zenmode" in target.possible_abilities and target.ability is None) or target.ability == "zenmode":
        score -= 90
    elif ("rkssystem" in target.possible_abilities and target.ability is None) or target.ability == "rkssystem":
        score -= 90
    elif (user.ability in target.possible_abilities and target.ability is None) or target.ability == user.ability:
        score -= 90

    return score
moveeffect_dict["065"] = moveeffect_065

def moveeffect_066(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Target copies user's ability. (Entrainment)

    #TODO: Check if pokemon can switch ability
    """

    score -= 40

    if target.effects.get(Effect.SUBSTITUTE, None) is not None:
        score -= 90


    if ("slowstart" in target.possible_abilities and target.ability is None) or target.ability == "slowstart":
        score -= 90
    elif ("truant" in target.possible_abilities and target.ability is None) or target.ability == "truant":
        score -= 90
    elif ("multitype" in target.possible_abilities and target.ability is None) or target.ability == "multitype":
        score -= 90
    elif ("forecast" in target.possible_abilities and target.ability is None) or target.ability == "forecast":
        score -= 90
    elif ("illusion" in target.possible_abilities and target.ability is None) or target.ability == "illusion":
        score -= 90
    elif ("imposter" in target.possible_abilities and target.ability is None) or target.ability == "imposter":
        score -= 90
    elif ("flowergift" in target.possible_abilities and target.ability is None) or target.ability == "flowergift":
        score -= 90
    elif ("trace" in target.possible_abilities and target.ability is None) or target.ability == "trace":
        score -= 90
    elif ("wonderguard" in target.possible_abilities and target.ability is None) or target.ability == "wonderguard":
        score -= 90
    elif ("zenmode" in target.possible_abilities and target.ability is None) or target.ability == "zenmode":
        score -= 90
    elif ("rkssystem" in target.possible_abilities and target.ability is None) or target.ability == "rkssystem":
        score -= 90
    elif (user.ability in target.possible_abilities and target.ability is None) or target.ability == user.ability:
        score -= 90

    return score
moveeffect_dict["066"] = moveeffect_066

def moveeffect_0BE(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Multihit poison

    This effect is triggered when the move can cause the target to become poisened.
    """

    score = moveeffect_005(score, move, user, target, battle)

    return score
moveeffect_dict["0BE"] = moveeffect_0BE

def moveeffect_0C5(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Two turn paralysis (freeze shock)

    This effect is triggered when the move can cause the target to become paralyzed
    """

    score = moveeffect_007(score, move, user, target, battle)

    return score
moveeffect_dict["0C5"] = moveeffect_0C5

def moveeffect_0C6(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Two turn burn (Ice Burn)

    This effect is triggered when the move can cause the target to become burned.
    """

    score = moveeffect_00A(score, move, user, target, battle)

    return score
moveeffect_dict["0C6"] = moveeffect_0C6

def moveeffect_0C8(score: int, move: Move, user: Pokemon, target: Pokemon, battle: AbstractBattle) -> int:
    """
    Move Effect Name: Increases user defense by one stage on first turn (Skull Bash)
    """

    score = moveeffect_01D(score, move, user, target, battle)

    return score
moveeffect_dict["0C8"] = moveeffect_0C8
