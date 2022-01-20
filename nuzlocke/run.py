from .encounter_pool import EncounterPool
from ..trainerai import Gen5AIPlayer
from ..playerai import PlayerAI

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

def teambuild(model, encounter_pool, enemy_team) -> str:
    """

    """



async def do_run(run_df, battle_df, encounter_df, item_df) -> bool:

    team_build_model = None
    battle_model = None

    teams = build_teams(battle_df)
    encounter_pool = EncounterPool()

    #Do each battle in order from start to finish
    for battle in battle_df.index:
        battle_id = battle_df.loc[battle, "BattleID"]
        enemy_team = teams[battle]

        #If the battle isn't for our starter, skip it
        if encounter_pool.limit_mode not in battle_id:
            continue

        #In the future, also skip optional battles
        our_team = team_build(team_build_model, encounter_pool, enemy_team)

        enemy_player = Gen5AIPlayer(team=enemy_team) #Add the name as a username for style points

        our_player = PlayerAI(team=our_team) #Add the nickname as well

        await our_player.battle_against(enemy_player, n_battles=1)

        if our_player.n_won_battles == 1:
            #We won!
            #Now we need to find our losses and remove from the pool

            recent_battle = our_player.battles[-1]
            #Dig into recent_battle to find which pokemon fainted
            dead_pokemon = []

            #remove fainted pokemon from the pool
            encounter_pool.remove_from_pool(dead_pokemon)

            if battle_id in run_df.index:
                unlocked_encounters = list(run_df.loc[battle_id, "EncounterID"])

                relevant_encounter_df = encounter_df[encounter_df["AreaID"].isin(unlocked_encounters)]

                #Transform this dataframe into a list of Encounter objects

        else:
            print(f"The run has failed here, at battle number: {battle}")
            return False
