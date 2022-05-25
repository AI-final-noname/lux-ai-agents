import math
import sys
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate
import random

DIRECTIONS = Constants.DIRECTIONS
game_state = None


def agent(observation, configuration):
    global game_state

    ### Do not edit ###
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player
    else:
        game_state._update(observation["updates"])

    actions = []

    ### AI Code goes down here! ###
    game_map = game_state.map
    player = game_state.players[observation.player]

    worker_weight = [8, 1, 1]  # Move, Pillage, Build City Tiles
    move_weight = [1, 1, 1, 1, 1]  # Move to five of the directions
    city_weight = [2, 1, 2]  # Build worker, Build cart, Research
    directions = [Constants.DIRECTIONS.NORTH, Constants.DIRECTIONS.SOUTH,
                  Constants.DIRECTIONS.EAST, Constants.DIRECTIONS.WEST, Constants.DIRECTIONS.CENTER]

    # Randomly select an action from all the available actions, according to the weight.
    # TODO: Add conditions of whether an unit can step onto the cell
    # TODO: Add conditions of whether a city tile can build something
    for unit in player.units:
        if unit.is_worker() and unit.can_act():
            worker_weight[2] = 1 if unit.can_build(
                game_map) and unit.get_cargo_space_left() == 0 else 0
            action = random.choices(
                [x for x in range(3)], weights=worker_weight)[0]
            if action == 0:  # Move
                direction = random.choices(
                    directions, weights=move_weight)[0]
                actions.append(unit.move(direction))
            elif action == 1:  # Pillage
                actions.append(unit.pillage())
            else:  # Build City Tiles
                actions.append(unit.build_city())
        if unit.is_cart() and unit.can_act():
            direction = random.choices(
                directions, weights=move_weight)[0]
            actions.append(unit.move(direction))

    for id, city in player.cities.items():
        for tile in city.citytiles:
            if tile.can_act():
                action = random.choices(
                    [x for x in range(3)], weights=city_weight)[0]
                if action == 0:  # Build Worker
                    actions.append(tile.build_worker())
                elif action == 1:  # Build Cart
                    actions.append(tile.build_cart())
                else:  # Research
                    actions.append(tile.research())

    return actions
