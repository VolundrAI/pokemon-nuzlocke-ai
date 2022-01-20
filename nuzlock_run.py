from nuzlocke.encounter_pool import EncounterPool
from trainerai import GameAIPlayer, BestMovePlayer
from poke_env.player.random_player import RandomPlayer
from poke_env.server_configuration import ServerConfiguration
from poke_env.player_configuration import PlayerConfiguration
import asyncio
import pandas as pd
import numpy as np

from poke_env.teambuilder.teambuilder import Teambuilder
from poke_env.teambuilder.teambuilder_pokemon import TeambuilderPokemon

from bs4 import BeautifulSoup
from glob import glob

from typing import List, Tuple

server_config= ServerConfiguration(
    "localhost:8192",
    "https://play.pokemonshowdown.com/action.php?"
)


def load_run_data(fpath: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """

    """

    run_df = pd.read_excel(fpath, sheet_name="Run")
    battle_df = pd.read_excel(fpath, sheet_name="Trainers")
    encounter_df = pd.read_excel(fpath, sheet_name="Encounters")
    item_df = pd.read_excel(fpath, sheet_name="Items")

    return run_df, battle_df, encounter_df, item_df


def build_teams(battle_df) -> List[str]:
    """

    """

    teams = []
    for ind in battle_df.index:
        battle_id = battle_df.loc[ind, "BattleID"]
        trainer_name = battle_df.loc[ind, "TrainerName"]

        team = []
        for p in range(1, 7):
            species = battle_df.loc[ind, f"Pokemon{p}"]
            if str(species).strip().lower() == str(np.nan).strip().lower():
                break
            gender = battle_df.loc[ind, f"Pokemon{p}Gender"]
            level = battle_df.loc[ind, f"Pokemon{p}Level"]
            ability = battle_df.loc[ind, f"Pokemon{p}Ability"]
            moves = [
                None if str(battle_df.loc[ind, f"Pokemon{p}Attack1"]).lower() == "nan" else battle_df.loc[ind, f"Pokemon{p}Attack1"],
                None if str(battle_df.loc[ind, f"Pokemon{p}Attack2"]).lower() == "nan" else battle_df.loc[ind, f"Pokemon{p}Attack2"],
                None if str(battle_df.loc[ind, f"Pokemon{p}Attack3"]).lower() == "nan" else battle_df.loc[ind, f"Pokemon{p}Attack3"],
                None if str(battle_df.loc[ind, f"Pokemon{p}Attack4"]).lower() == "nan" else battle_df.loc[ind, f"Pokemon{p}Attack4"],
            ]

            moves = [m for m in moves if m is not None]

            item = None if str(battle_df.loc[ind, f"Pokemon{p}Item"]).lower() == "nan" else battle_df.loc[ind, f"Pokemon{p}Item"]

            tb_pokemon = TeambuilderPokemon(
                species=species,
                item=item,
                ability=ability,
                moves=moves,
                gender=gender,
                level=level,
                evs=[1,1,1,1,1,1],
                ivs=[1,1,1,1,1,1]
            )

            team.append(tb_pokemon)

        showdown_team = Teambuilder.join_team(team)
        teams.append(showdown_team)

    return teams

def team_build(model, encounter_pool, enemy_team) -> str:
    """

    """

    team = list(np.random.choice(encounter_pool.pool, min(len(encounter_pool.pool), 6), replace=False))

    for poke in team:
        if poke.pokemon.level == encounter_pool.level_cap:
            continue

        poke.pokemon.level = encounter_pool.level_cap

        poke.pokemon.moves = [m[1].replace("-", "") for m in poke.learnset if int(m[0]) <= int(poke.pokemon.level)][-4:]

        #TODO: Add support for evolution

    showdown_team = Teambuilder.join_team([poke.pokemon for poke in team])

    return showdown_team

def find_dead_pokemon(our_name):
    f = sorted(glob(f"replays/{our_name}*.html"))[-1]
    # Opening the html file
    HTMLFile = open(f, "r")
    # Reading the file
    index = HTMLFile.read()
    # Creating a BeautifulSoup object and specifying the parser
    S = BeautifulSoup(index, 'html5lib')

    dead_pokemon = []
    battle_log = S.find('script', attrs = {'class':'battle-log-data'})
    for line in str(battle_log).split("\n"):
        if "|faint|p1a" in line:
            dead_pokemon.append(line.split(":")[1].strip().lower())

    return dead_pokemon


async def do_run(run_df, battle_df, encounter_df, item_df) -> bool:

    team_build_model = None
    battle_model = None

    teams = build_teams(battle_df)
    encounter_pool = EncounterPool(run_df, encounter_df)

    #Do each battle in order from start to finish
    for battle in battle_df.index:
        battle_id = battle_df.loc[battle, "BattleID"]
        enemy_name = battle_df.loc[battle, "TrainerName"]
        enemy_team = teams[battle]

        #If the battle isn't for our starter, skip it
        if any([case in battle_id for case in ["a", "b", "c"]]) and encounter_pool.limit_mode not in battle_id:
            continue

        #In the future, also skip optional battles
        print(f"Preparing team for battle {battle_id} against {enemy_name}")
        our_team = team_build(team_build_model, encounter_pool, enemy_team)
        print(f"Team prepared for battle!")
        print(our_team)

        enemy_name = (battle_id + enemy_name).replace(" ", "")[:18]
        our_name = f"VolundrAI_{battle_id}"

        enemy_player_config = PlayerConfiguration(enemy_name, None)
        our_player_config = PlayerConfiguration(our_name, None)

        enemy_player = GameAIPlayer(player_configuration=enemy_player_config, server_configuration=server_config, max_concurrent_battles=25, battle_format="gen7anythinggoes", team=enemy_team)
        our_player = BestMovePlayer(player_configuration=our_player_config, save_replays=True, server_configuration=server_config, max_concurrent_battles=25, battle_format="gen7anythinggoes", team=our_team)

        print("Starting Battle...")
        await our_player.battle_against(enemy_player, n_battles=1)

        if our_player.n_won_battles == 1:
            print("Battle was a success!")
            #We won!
            #Now we need to find our losses and remove from the pool

            #Dig into recent_battle to find which pokemon fainted
            dead_pokemon = find_dead_pokemon(our_name)
            print(f"We had the following losses: {dead_pokemon}")

            #remove fainted pokemon from the pool
            encounter_pool.remove_from_pool(dead_pokemon)

            print("Dead Pokemon:", encounter_pool.dead_pokemon)
            print("Remaining Pokemon:", encounter_pool.pool)

            #Add new encounters that can be seen after this battle
            print("Searching for new pokemon after the battle...")
            encounter_pool.build_encounters(battle_id)

        else:
            dead_pokemon = find_dead_pokemon(our_name)
            print(f"We had the following losses: {dead_pokemon}")

            encounter_pool.remove_from_pool(dead_pokemon)

            print("Dead Pokemon:", encounter_pool.dead_pokemon)
            print("Remaining Pokemon:", encounter_pool.pool)

            print(f"The run has failed here, at battle number: {battle_id}")
            return False
        print("-----------------------------------------------------------")
        print()
        print()

if __name__ == "__main__":
    run_df, battle_df, encounter_df, item_df = load_run_data("data/PokemonBlackRun.xlsx")

    asyncio.get_event_loop().run_until_complete(do_run(run_df, battle_df, encounter_df, item_df))
