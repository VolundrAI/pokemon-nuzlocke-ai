import requests
import json

from typing import List, Tuple, Optional

class PokeCache:
    """

    """

    def __init__(self, fpath: Optional[str] = None):
        """

        """

        self.dex_cache = {}
        self.species_cache = {}

        if fpath is not None:
            self.load_from_file(fpath)

    def load_from_file(self, fpath: str):
        """

        """
        with open(fpath, "r") as f:
            contents = f.read()
            cache = json.loads(contents)

        self.dex_cache = cache["pokedex"]
        self.species_cache = cache["species"]

    def save_to_file(self, fpath: str):
        """

        """

        with open(fpath, "w") as f:
            output = {}
            output["pokedex"] = self.dex_cache
            output["species"] = self.species_cache

            contents = json.dumps(output)
            f.write(contents)

def get_pokedex_entry(poke: str, cache: PokeCache) -> None:
    """

    """

    if poke.strip().lower() not in cache.dex_cache.keys():
        pokedex_url = f"https://pokeapi.co/api/v2/pokemon/{poke.strip().lower()}/"
        pokedex_entry_response = requests.get(pokedex_url)

        if pokedex_entry_response.status_code != 200:
            print(pokedex_entry_response.status_code)
            print(pokedex_entry_response.content)
            raise RuntimeError(f"Error when trying to pull pokedex data for: {poke}")

        pokedex_entry = pokedex_entry_response.json()

        cache.dex_cache[poke.strip().lower()] = pokedex_entry

def get_species_entry(poke: str, cache: PokeCache) -> None:
    """

    """

    if poke.strip().lower() not in cache.dex_cache.keys():
        get_pokedex_entry(poke, cache)

    generic_name = cache.dex_cache[poke.strip().lower()]["species"]["name"]
    if generic_name not in cache.species_cache.keys():
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{generic_name}/"
        species_response = requests.get(species_url)

        if species_response.status_code != 200:
            print(species_response.status_code)
            print(species_response.content)
            raise RuntimeError(f"Error when trying to pull species data for: {generic_name}")

        species_entry = species_response.json()

        cache.species_cache[generic_name] = species_entry

def get_encounter_basic_info(poke: str, cache: PokeCache, version_name: str = "black-white", move_method: str = "level-up", banned_abilities: List[str] = ["competitive", "slush-rush", "weak-armor"]) -> Tuple[List[str], float, List[str]]:
    """
    Get the basic details of an encountered pokemon from the pokeAPI.
    (Abilities, Odds Female, and Level-up Learnset)
    """

    get_pokedex_entry(poke, cache)
    get_species_entry(poke, cache)

    possible_abilities = [
        a["ability"]["name"]
        for a in cache.dex_cache[poke.strip().lower()]["abilities"]
        if (not a["is_hidden"]) and(a["ability"]["name"] not in banned_abilities)
    ]

    generic_name = cache.dex_cache[poke.strip().lower()]["species"]["name"]
    odds_female = cache.species_cache[generic_name]["gender_rate"] / 8

    moveset =  []
    for move in cache.dex_cache[poke.strip().lower()]["moves"]:
        for v_details in move["version_group_details"]:
            if v_details["version_group"]["name"] == version_name:
                moveset.append((v_details["level_learned_at"], move["move"]["name"]))

    moveset = sorted(moveset, key=lambda x: x[0])

    return possible_abilities, odds_female, moveset
