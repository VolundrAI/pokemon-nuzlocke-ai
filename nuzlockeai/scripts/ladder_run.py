from ..trainerai import GameAIPlayer, BestMovePlayer
from ..utils import PokeCache, build_random_team
from poke_env.player.random_player import RandomPlayer
from poke_env.server_configuration import ServerConfiguration
from poke_env.player_configuration import PlayerConfiguration
from poke_env.teambuilder.teambuilder import Teambuilder
from poke_env.teambuilder.teambuilder_pokemon import TeambuilderPokemon

import asyncio
import json
import pandas as pd
import numpy as np
import requests
import logging
import time
import sys

from typing import List, Tuple, Optional
from tqdm import tqdm

logger = logging.getLogger()
logger.setLevel(90)

logger = logging.getLogger(__name__)
logger.setLevel(90)

server_config= ServerConfiguration(
    "localhost:8192",
    "https://play.pokemonshowdown.com/action.php?"
)

async def challenge_ladder(team_id, team, ladder_matches: int = 25):
    """

    """

    player_config = PlayerConfiguration(team_id, None)
    player = BestMovePlayer(player_configuration=player_config, server_configuration=server_config, battle_format="gen5purehackmons", team=team, log_level=90)

    for _ in range(ladder_matches):
        try:
            await asyncio.wait_for(asyncio.shield(player.ladder(1)), 60*1)
        except asyncio.TimeoutError:
            try:
                await player.stop_listening()
            except:
                pass
            del player
            return "DONE - TIMEOUT"
        except RuntimeError:
            try:
                await player.stop_listening()
            except:
                pass
            del player
            return "DONE - ERRORED"

    try:
        await player.stop_listening()
    except:
        pass
    del player
    return "DONE - COMPLETED"

async def simulate_ladder(cache_path: Optional[str] = "data/pokecache.json"):

    possible_pokemon = [
    "Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Volcarona", "Cobalion", "Terrakion", "Virizion", "Reshiram", "Zekrom", "Kyurem", "Genesect", "Thundurus-Incarnate", "Landorus-Incarnate", "Tornadus-Incarnate", "Darmanitan-Standard", "Keldeo-Ordinary", "Meloetta-Aria", "Basculin-Red-Striped", "Basculin-Blue-Striped"
    ]

    cache = PokeCache(cache_path)

    ladder_challengers = {}
    for i in tqdm(range(0, 100000)):
        team_id = f"Team_{str(i).rjust(7, '0')}"
        team = build_random_team(
            possible_pokemon,
            random_seed=i,
            cache=cache
        )

        ladder_challengers[team_id] = team

    cache.save_to_file(fpath)

    i = 1
    print("Running rounds of challengers to simulate battles...")
    while True:
        print(f"Starting round {i}")
        start = time.time()
        round_challengers = np.random.choice(list(ladder_challengers.keys()), size=250, replace=False)

        results = await asyncio.gather(*[challenge_ladder(team_id, ladder_challengers[team_id], 2) for team_id in round_challengers])

        complete_success = 0
        error_count = 0
        timeout_count = 0
        for r in results:
            if r == "DONE - COMPLETED":
                complete_success += 1
            elif r == "DONE - TIMEOUT":
                timeout_count += 1
            else:
                error_count += 1

        print(f"Ladder matches were a complete success for {100 * complete_success / len(results)}% of competitors")
        print(f"Ladder matches were cut short due to timeouts for {100 * timeout_count / len(results)}% of competitors")
        print(f"Ladder matches were cut short due to errors for {100 * error_count / len(results)}% of competitors")
        print(f"Round {i} finished in {time.time() - start} seconds!")
        print("-------------------------------------------------")
        print()
        i += 1

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(simulate_ladder())
