from poke_env.environment.move import Move
from poke_env.environment.move_category import MoveCategory
from poke_env.environment.pokemon import Pokemon
from poke_env.data import TYPE_CHART

from .moveeffect import moveeffect_dict, moveeffect_000
from functools import lru_cache
from typing import Dict
import requests

@lru_cache
def load_moveeffect_map(move_db: str) -> Dict[str, str]:

    moveeffect_map = {}
    with open(move_db, "r", encoding="utf-8") as f:
        for line in f:
            clean_line = line.strip()

            if clean_line[0] == "#":
                continue
            if clean_line == "":
                continue

            try:
                move_name = clean_line.split(",")[1]
                move_effect = clean_line.split(",")[3]
            except IndexError as e:
                continue

            moveeffect_map[move_name] = move_effect

    return moveeffect_map

def get_moveeffect_score(
    initial_score: int,
    move: Move,
    user: Pokemon,
    target: Pokemon,
    moveeffect_map: Dict[str,str],
) -> int:
    """

    """

    score = initial_score

    me_key = move.id.replace(" ", "").upper()

    if me_key not in moveeffect_map.keys():
        pass
        #print(f"Unknown Move: {me_key}")

    move_effect_id = moveeffect_map.get(me_key, "000")

    if move_effect_id not in moveeffect_dict.keys():
        pass
        #print(f"Unknown Move Effect: {move_effect_id}")

    move_effect_func = moveeffect_dict.get(move_effect_id, moveeffect_000)
    score = move_effect_func(score, move, user, target)

    return score

def score_approx_damage(
    score: int,
    move: Move,
    user: Pokemon,
    target: Pokemon
) -> int:
    """

    """

    if score <= 0:
        return 0

    multiplier = 1.0
    if move.type in user.types:
        multiplier *= 1.5

    for tp in target.types:
        if tp is None:
            continue
        multiplier *= TYPE_CHART[move.type.name][tp.name]

    if target.ability == "levitate" and move.type.name == "GROUND":
        multiplier *= 0

    damage = move.base_power * multiplier

    if move.category == MoveCategory.SPECIAL:
        attack = user.base_stats["atk"]
        defense = target.base_stats["def"]

        atk_stat = "atk"
        def_stat = "def"
    elif move.category == MoveCategory.SPECIAL:
        attack = user.base_stats["spa"]
        defense = target.base_stats["spd"]

        atk_stat = "spa"
        def_stat = "spd"
    else:
        return 0

    standard_stages = [2/8, 2/7, 2/6, 2/5, 2/4, 2/3, 2/2, 3/2, 4/2, 5/2, 6/2, 7/2, 8/2]
    acceva_stages = [3/9, 3/8, 3/7, 3/6, 3/5, 3/4, 3/3, 4/3, 5/3, 6/3, 7/3, 8/3, 9/3]

    attack = standard_stages[user.boosts.get(atk_stat, 0) + 6] * attack
    defense = standard_stages[target.boosts.get(def_stat, 0) + 6] * defense

    damage *= (attack / defense)

    score = int((2*score*damage)/(score + damage))

    return score

def score_calculated_damage(
    score: int,
    move: Move,
    user: Pokemon,
    target: Pokemon
) -> int:
    """

    """

    if move.category == MoveCategory.STATUS:
        return score

    api1_url = "http://localhost:8193/calculate"
    api2_url = "http://localhost:8194/calculate"
    api3_url = "http://localhost:8195/calculate"


    def clean_species(species_name):
        if "gastrodon" in species_name:
            return "gastrodon"
        if "aegislash" in species_name:
            return "aegislash-both"

        return species_name


    payload = {
        "attackingPokemon": clean_species(user.species),
        "attackingPokemonOptions":{
            "level":user.level,
            "ivs": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spa": 0,
                "spd": 0,
                "spe": 0
            },
            "evs": {
                "hp": 0,
                "atk": 0,
                "def": 0,
                "spa": 0,
                "spd": 0,
                "spe": 0
            },
            "ability":user.ability,
            "moves":[move for move in user.moves],
            "boosts":{
                "hp": 0,
                "atk": user.boosts.get("atk", 0),
                "def": user.boosts.get("atk", 0),
                "spa": user.boosts.get("atk", 0),
                "spd": user.boosts.get("atk", 0),
                "spe": user.boosts.get("atk", 0)
            }
        },
        "defendingPokemon": clean_species(target.species),
        "defendingPokemonOptions":{
            "level":target.level,
            "ivs": {
                "hp": 31,
                "atk": 31,
                "def": 31,
                "spa": 31,
                "spd": 31,
                "spe": 31
            },
            "evs": {
                "hp": 31,
                "atk": 31,
                "def": 31,
                "spa": 31,
                "spd": 31,
                "spe": 31
            },
            "ability":target.ability if target.ability is not None else target.possible_abilities[0],
            "moves":[move for move in target.moves],
            "boosts":{
                "hp": 0,
                "atk": target.boosts.get("atk", 0),
                "def": target.boosts.get("atk", 0),
                "spa": target.boosts.get("atk", 0),
                "spd": target.boosts.get("atk", 0),
                "spe": target.boosts.get("atk", 0)
            }
        },
        "moveName":move.id
    }

    if(target.item is not None and str(target.item) != "unknown_item"):
        payload["defendingPokemonOptions"]["item"] = target.item
    if(user.item is not None and str(user.item) != "unknown_item"):
        payload["attackingPokemonOptions"]["item"] = user.item


    try:
        resp = requests.get(api1_url, json=payload)
    except:
        try:
            resp = requests.get(api2_url, json=payload)
        except:
            resp = requests.get(api3_url, json=payload)


    if resp.status_code == 200:
        damage = resp.json()["damage"]
        if not isinstance(damage, list):
            damage = [damage for _ in range(16)]

        max_health = resp.json()["defender"]["originalCurHP"] * target.current_hp_fraction

        #A 2-hit KO averages a score of 100
        damage_score = (sum([d/max_health for d in damage]) / 16) * 100 * 4

        score = (2*score*damage_score) / (score + damage_score)

    else:
        print(f"Calculation API Error: {resp.status_code}")
        print("------------------------------------------")
        print("Move ID:", move.id)
        print("User Species:", user.species)
        print("Enemy Species:", target.species)
        print("User Moves:", [move for move in user.moves])
        print("Enemy Moves:", [move for move in target.moves])
        print("User Ability:", user.ability)
        print("Enemy Ability:", target.ability if target.ability is not None else target.possible_abilities[0])
        print("User Item:", user.item)
        print("Enemy Item:", target.item if (target.item is not None and str(target.item) != "unknown_item") else None)
        print("------------------------------------------")
        print(resp.content)
        raise RuntimeError(f"Response code: {resp.status_code}")

    return score
