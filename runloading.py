import pandas as pd
import numpy as np
from typing import List, Tuple
import asyncio

from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ServerConfiguration

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer
from trainerai import GameAIPlayer

from poke_env.player.utils import cross_evaluate

from poke_env.teambuilder.teambuilder import Teambuilder
from poke_env.teambuilder.teambuilder_pokemon import TeambuilderPokemon


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

async def main(run_df, battle_df, encounter_df, item_df):

    teams = build_teams(battle_df)

    players = [
        GameAIPlayer(server_configuration=server_config, max_concurrent_battles=20, team=team, battle_format="gen8anythinggoes")
        for team in teams
    ]

    cross_evaluation = await cross_evaluate(players, n_challenges=100)

    table = [["-"] + [p.username for p in players]]

    # Adds one line per player with corresponding results
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])

    # Displays results in a nicely formatted table.
    print(tabulate(table))


if __name__ == "__main__":
    run_df, battle_df, encounter_df, item_df = load_run_data("data/PokemonBlackRun.xlsx")

    asyncio.get_event_loop().run_until_complete(main(run_df, battle_df, encounter_df, item_df))
