import nuzlockeai
import asyncio

if __name__ == "__main__":

    cache_path = "data/pokecache.json"
    cache = nuzlockeai.PokeCache(cache_path)

    run_df, battle_df, encounter_df, item_df = nuzlockeai.load_run_data("data/PokemonBlackRun.xlsx")

    asyncio.get_event_loop().run_until_complete(nuzlockeai.do_run(run_df, battle_df, encounter_df, item_df, replay_path="replays", cache=cache))
