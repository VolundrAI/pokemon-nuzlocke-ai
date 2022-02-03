from .pokecache import PokeCache, get_pokedex_entry, get_species_entry

from poke_env.teambuilder.teambuilder import Teambuilder
from poke_env.teambuilder.teambuilder_pokemon import TeambuilderPokemon
from typing import List, Tuple, Optional

import numpy as np

def build_random_team(
    possible_pokemon: List[str],
    level_options: List[int] = [80], #[5, 14, 20, 23, 27, 31, 35, 39, 43, 50],
    random_seed: Optional[int] = None,
    cache: Optional[PokeCache] = None,
    banned_abilities: List[str] = ["competitive", "slush-rush", "weak-armor"],
    gen_tag: str = "black-white"
) -> str:
    """

    """

    if cache is None:
        cache = PokeCache()

    rng = np.random.default_rng(seed=random_seed)

    team_size = rng.integers(low=1, high=6+1, size=1)
    poke_selection = rng.choice(possible_pokemon, team_size, replace=False)
    level = rng.choice(level_options)

    team = []
    for poke in poke_selection:
        #Update the cache for this pokemon
        get_pokedex_entry(poke, cache)
        get_species_entry(poke, cache)

        #Select a random ability out of the options
        possible_abilities = [
            a["ability"]["name"]
            for a in cache.dex_cache[poke.strip().lower()]["abilities"]
            if (not a["is_hidden"]) and(a["ability"]["name"] not in banned_abilities)
        ]
        ability = rng.choice(possible_abilities)

        #Select a random set of moves for the pokemon
        moveset =  []
        for move in cache.dex_cache[poke.strip().lower()]["moves"]:
            for v_details in move["version_group_details"]:
                if v_details["version_group"]["name"] == gen_tag:
                    moveset.append((v_details["level_learned_at"], move["move"]["name"]))
        moveset = [m[1] for m in moveset if m[0] <= level]
        if len(moveset) < 4:
            raise RuntimeError(f"Error in loading moveset for: {poke}")
        moveset = list(set(moveset))
        moves = rng.choice(moveset, replace=False, size=4)

        #Select a random gender given the weighted odds of the pokemon
        odds_female = cache.species_cache[generic_name]["gender_rate"] / 8
        gender = "Male" if np.random.rand() >= odds_female else "Female"

        #Generate evs and ivs of the pokemon
        evs = [1,1,1,1,1,1]
        ivs = rng.integers(1, 32, size=6)

        #Construct the pokemon out of the randomly selected options
        pokemon = TeambuilderPokemon(
            species=poke.strip().lower(),
            ability=ability,
            moves=moves,
            gender=gender,
            level=level,
            evs=evs,
            ivs=ivs
        )

        team.append(pokemon)

    #Create a showdown-readable team out of the team
    showdown_team = Teambuilder.join_team(team)

    return showdown_team
