from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ServerConfiguration
from poke_env.player.random_player import RandomPlayer
from poke_env.player.player import Player
from poke_env.player.utils import cross_evaluate
import asyncio
from tabulate import tabulate
from time import time

from trainerai import BestMovePlayer, HighPowerPlayer, SwitchBestMovePlayer, GameAIPlayer

server_config= ServerConfiguration(
    "localhost:8192",
    "https://play.pokemonshowdown.com/action.php?"
)


async def main():
    """

    """
    battle_format = "gen8randombattle"


    players = [
        GameAIPlayer(server_configuration=server_config, max_concurrent_battles=25, battle_format=battle_format),
        GameAIPlayer(server_configuration=server_config, max_concurrent_battles=25, battle_format=battle_format),
        RandomPlayer(server_configuration=server_config, max_concurrent_battles=25, battle_format=battle_format),
        RandomPlayer(server_configuration=server_config, max_concurrent_battles=25, battle_format=battle_format),
        BestMovePlayer(server_configuration=server_config, max_concurrent_battles=25, battle_format=battle_format),
        BestMovePlayer(server_configuration=server_config, max_concurrent_battles=25, battle_format=battle_format),
        HighPowerPlayer(server_configuration=server_config, max_concurrent_battles=25, battle_format=battle_format),
        HighPowerPlayer(server_configuration=server_config, max_concurrent_battles=25, battle_format=battle_format),
        SwitchBestMovePlayer(server_configuration=server_config, max_concurrent_battles=25, battle_format=battle_format),
        SwitchBestMovePlayer(server_configuration=server_config, max_concurrent_battles=25, battle_format=battle_format),
    ]


    cross_evaluation = await cross_evaluate(players, n_challenges=100)

    table = [["-"] + [p.username for p in players]]

    # Adds one line per player with corresponding results
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])

    # Displays results in a nicely formatted table.
    print(tabulate(table))

if __name__ == "__main__":
    st = time()
    asyncio.get_event_loop().run_until_complete(main())
    print(f"Took {time() - st} seconds!")
