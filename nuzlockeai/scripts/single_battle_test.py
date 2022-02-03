from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ServerConfiguration
from poke_env.player.random_player import RandomPlayer
from poke_env.player.player import Player

import asyncio
from time import time

from ..trainerai import BestMovePlayer, HighPowerPlayer, SwitchBestMovePlayer, GameAIPlayer

server_config= ServerConfiguration(
    "localhost:8192",
    "https://play.pokemonshowdown.com/action.php?"
)

async def main():
    """

    """
    battle_format = "gen5anythinggoes"

    battle_time = time()

    team1 = """
P1 (Pansear) @ Eviolite
Ability: Gluttony
EVs: 252 HP
IVs: 0 Atk
- Acrobatics
- Crunch
- Fire Blast
- Fire Punch

P2 (Pansear) @ Eviolite
Ability: Gluttony
EVs: 252 HP
IVs: 0 Atk
- Acrobatics
- Crunch
- Fire Blast
- Fire Punch

P3 (Pansear) @ Eviolite
Ability: Gluttony
EVs: 252 HP
IVs: 0 Atk
- Acrobatics
- Crunch
- Fire Blast
- Fire Punch
"""

    team2 = """
Oshawott @ Eviolite
Ability: Torrent
EVs: 252 HP
IVs: 0 Atk
- Aqua Jet
- Protect
- Ice Beam
- Surf

Pansage @ Leftovers
Ability: Gluttony
EVs: 252 HP / 252 Spe
IVs: 0 Atk
- Acrobatics
- Energy Ball
- Grass Knot
- Leech Seed
"""


    p1 = GameAIPlayer(server_configuration=server_config, team=team1, max_concurrent_battles=1, battle_format=battle_format)
    p2 = BestMovePlayer(server_configuration=server_config, team=team2, max_concurrent_battles=1, battle_format=battle_format)

    await p1.battle_against(p2, n_battles=1)

    print(f"Full battle took {time() - battle_time} seconds to run!")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
