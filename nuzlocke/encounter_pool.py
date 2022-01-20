import numpy as np
from poke_env.environment.pokemon import Pokemon
from pydantic import BaseModel
from typing import List

class Encounter(BaseModel):
    id: str
    pokemon: Pokemon
    odds: float


class EncounterPool:
    """
    A class to manage all of the encounters on a single run of a nuzlocke
    """

    def __init__(self, limit_mode="a"):
        """
        Initialize the pool to be empty
        """

        self.limit_mode = limit_mode
        self.pool = []


    def add_encounter(self, potential_encounters: List[Encounter]):
        """
        Out of each potential encounter, it will get one and add it to then pool,
        checking for species, and other limits automatically.
        """

        valid_encounters = []
        for encounter in potential_encounters:
            if encounter not in self.pool:
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

        self.pool.append(encounter.pokemon)

    def remove_from_pool(self, dead_pokemon: List[Pokemon]):
        """
        Pass in a list of fainted pokemon to remove them from the ongoing pool
        """

        self.pool = [poke for poke in self.pool if poke not in dead_pokemon]
