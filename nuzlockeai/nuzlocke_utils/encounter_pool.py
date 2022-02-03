import numpy as np
import pandas as pd
from poke_env.teambuilder.teambuilder_pokemon import TeambuilderPokemon
from pydantic import BaseModel
from typing import List, Tuple
import requests
from typing import Optional
from ..utils import PokeCache, get_encounter_basic_info

class Encounter(BaseModel):
    id: str
    pokemon: TeambuilderPokemon
    odds: float
    learnset: List[Tuple[int,str]]

    class Config:
        arbitrary_types_allowed = True


class EncounterPool:
    """
    A class to manage all of the encounters on a single run of a nuzlocke
    """

    def __init__(self, run_df: pd.DataFrame, encounter_df: pd.DataFrame, limit_modes=["a", "b", "c"], cache: Optional[PokeCache] = None, version_name: str = "black-white"):
        """
        Initialize the pool to be empty
        """

        self.limit_mode = np.random.choice(limit_modes)
        self.pool = []
        self.dead_pokemon = []
        self.level_cap = 5

        self.run_df = run_df
        self.encounter_df = encounter_df

        if cache is None:
            cache = PokeCache()

        self.cache = cache

        self.version_name = version_name

        self.build_encounters("START")


    def build_encounters(self, battle_id) -> None:
        """

        """

        for run_ind in self.run_df[self.run_df["BattleID"] == battle_id].index:
            self.level_cap = max(self.level_cap, self.run_df.loc[run_ind, "LevelCap"])

            enc_id = self.run_df.loc[run_ind, "EncounterID"]

            if str(enc_id) != "NaN":

                potential_encounters = []
                for enc_ind in self.encounter_df[self.encounter_df["AreaID"] == enc_id].index:

                    species = self.encounter_df.loc[enc_ind, "EncounterPokemon"]

                    lrange = self.encounter_df.loc[enc_ind, "LevelRange"]
                    level_min = int(lrange.split("-")[0])
                    level_max = int(lrange.split("-")[1])+1
                    level = np.random.randint(level_min, level_max)

                    ivs = [
                        np.random.randint(1, 32)
                        for _ in range(6)
                    ]
                    evs = [1,1,1,1,1,1]

                    possible_abilities, odds_female, moveset = get_encounter_basic_info(species, self.cache, self.version_name)

                    ability = np.random.choice(possible_abilities)

                    gender = "Male" if np.random.rand() >= odds_female else "Female"

                    moves = [m[1].replace("-", "") for m in moveset if m[0] <= level][-4:]

                    encounter_id = str(self.encounter_df.loc[enc_ind, "AreaID"]) + "_" + str(self.encounter_df.loc[enc_ind, "EncounterID"])

                    potential_encounters.append(
                        Encounter(
                            id=encounter_id,
                            pokemon=TeambuilderPokemon(
                                species=species,
                                ability=ability,
                                moves=moves,
                                gender=gender,
                                level=level,
                                evs=evs,
                                ivs=ivs
                            ),
                            odds=self.encounter_df.loc[enc_ind, "Odds"],
                            learnset=moveset
                        )
                    )

                self.add_encounter(potential_encounters)



    def add_encounter(self, potential_encounters: List[Encounter]):
        """
        Out of each potential encounter, it will get one and add it to then pool,
        checking for species, and other limits automatically.
        """

        valid_encounters = []
        for encounter in potential_encounters:
            if encounter.pokemon.species.strip().lower() not in [p.pokemon.species.strip().lower() for p in self.pool] + self.dead_pokemon:
                valid_encounters.append(encounter)
            if "a" in encounter.id:
                if self.limit_mode == "a":
                    valid_encounters.append(encounter)
            if "b" in encounter.id:
                if self.limit_mode == "b":
                    valid_encounters.append(encounter)
            if "c" in encounter.id:
                if self.limit_mode == "c":
                    valid_encounters.append(encounter)

        if len(valid_encounters) == 0:
            return None

        odds = np.array([encounter.odds for encounter in valid_encounters])
        odds = odds / odds.sum() #[0.2, 0.5, 0.3]

        rand = np.random.rand() # 0.79 -> 0.59 -> 0.09

        current_odds = rand
        for e, odd in enumerate(odds):
            if odd <= current_odds:
                current_odds -= odd
            else:
                break

        encounter = valid_encounters[e]

        self.pool.append(encounter)

    def remove_from_pool(self, dead_pokemon: List[str]):
        """
        Pass in a list of fainted pokemon to remove them from the ongoing pool
        """

        self.dead_pokemon += dead_pokemon

        self.pool = [poke for poke in self.pool if poke.pokemon.species.strip().lower() not in self.dead_pokemon]
