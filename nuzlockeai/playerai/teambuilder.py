import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from typing import List, Tuple, Optional
from tqdm import tqdm
from copy import deepcopy
from ..utils import build_random_team

import pandas as pd
import numpy as np

def is_pokemon_included(pokemon:str, team:str) -> int:
    """
    A helper function to check if a pokemon is in a certain team

    Returns 1 if the pokemon is in the team, 0 otherwise
    """
    if pokemon.strip().lower() in team:
        return 1
    else:
        return 0

def train_model(data_directory: str):
    """

    """

    possible_pokemon = [
        "Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Volcarona", "Cobalion", "Terrakion", "Virizion", "Reshiram", "Zekrom", "Kyurem", "Genesect", "Thundurus-Incarnate", "Landorus-Incarnate", "Tornadus-Incarnate", "Darmanitan-Standard", "Keldeo-Ordinary", "Meloetta-Aria", "Basculin-Red-Striped", "Basculin-Blue-Striped"
    ]

    cache = PokeCache(fpath=f"{data_directory}/pokecache.json")

    elo_data = pd.read_excel(f"{data_directory}/gen5hackmon_adjustedelo.xlsx")
    elo_data = elo_data.dropna()

    elo_data["Team"] = [
        build_random_team(possible_pokemon, random_seed=int(team_id.split("_")[1]), cache=cache)
        for team_id in elo_data["Username"]
    ]

    for pokemon in possible_pokemon:
        elo_data[f"Contains_{pokemon}"] = [is_pokemon_included(pokemon, team) for team in elo_data["Team"]]

    elo_data = elo_data.sample(frac=1.0)

    X = elo_data[[col for col in elo_data.columns if "Contains_" in col]]
    Y = (elo_data["AdjustedELO"] - elo_data["AdjustedELO"].mean()) / elo_data["AdjustedELO"].std()

    X_train = X.iloc[:90000, :]
    X_val = X.iloc[90000:, :]

    Y_train = Y.iloc[:90000]
    Y_val = Y.iloc[90000:]

    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
      # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
        try:
            tf.config.set_logical_device_configuration(
                gpus[0],
                [tf.config.LogicalDeviceConfiguration(memory_limit=4096)])
            logical_gpus = tf.config.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Virtual devices must be set before GPUs have been initialized
            print(e)

    model = Sequential()

    model.add(Dense(64, input_shape=(157,)))
    model.add(Dropout(0.25))
    model.add(BatchNormalization())
    model.add(Dense(32))
    model.add(Dropout(0.25))
    model.add(BatchNormalization())
    model.add(Dense(1))

    model.compile(loss="mse", optimizer="adam")

    model.fit(
        X_train,
        Y_train,
        epochs=10,
        validation_data=(X_val, Y_val)
    )

    return model

def fitness_function(team, possible_pokemon, model) -> float:
    team_row = [1 if (p in team) else 0 for p in possible_pokemon]

    score = model.predict(np.array(team_row).reshape(1, -1)).squeeze()*elo_data["AdjustedELO"].std() + elo_data["AdjustedELO"].mean()

    return score

def find_best_team(pop_size, possible_pokemon, model):
    team_data = []
    print("Building Initial Population...")
    for _ in tqdm(range(pop_size)):
        team = np.random.choice(possible_pokemon, size=6, replace=True)
        fitness_score = fitness_function(team, possible_pokemon, model)

        team_data.append((team, fitness_score))

    team_info = pd.DataFrame(columns=["Team", "Score"], data=team_data)
    team_info = team_info.sort_values(by=["Score"], ascending=False)

    print("Finding Initial seed for Generation 1...")
    seed_population = team_info.head(pop_size // 6)
    best_team = seed_population.iloc[0, 0]
    best_score = seed_population["Score"].max()

    return mutate_team(seed_population, best_team, best_score, pop_size, 1, possible_pokemon, model)

def mutate_team(seed_population, best_team, best_score, pop_size, depth, possible_pokemon, model):
    team_data = []
    print(f"Mutating Generation {depth}...")
    for team in tqdm(seed_population["Team"]):
        new_pokemon = np.random.choice([p for p in possible_pokemon if p not in team])

        for i in range(6):
            temp_team = deepcopy(team)
            temp_team[i] = new_pokemon

            fitness_score = fitness_function(temp_team, possible_pokemon, model)
            team_data.append((temp_team, fitness_score))

    team_info = pd.DataFrame(columns=["Team", "Score"], data=team_data)
    team_info = team_info.sort_values(by=["Score"], ascending=False)

    best_new_team = team_info.iloc[0, 0]
    best_new_score = team_info["Score"].max()

    if best_new_score < best_score:
        return best_team
    elif depth > 20:
        return best_new_team
    else:
        best_team = best_new_team
        best_score = best_new_score
        seed_population = team_info.head(pop_size // 6)

        return mutate_team(seed_population, best_team, best_score, pop_size, depth+1, possible_pokemon, model)
