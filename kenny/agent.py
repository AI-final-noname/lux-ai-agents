import math, sys
from tkinter import UNITS

from soupsieve import closest
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux.game_objects import Unit,Player
from lux import annotate
import random

DIRECTIONS = Constants.DIRECTIONS
game_state = None

def get_closest_tile(unit,tiles):
    closest_dis = math.inf
    closest_tile = None

    for tile in tiles:
        dis = tile.pos.distance_to(unit.pos)
        if dis < closest_dis:
            closest_dis = dis
            closest_tile = tile
    
    return closest_tile

def get_closest_city_tile(unit, city_tiles):
    closest_dis = math.inf
    closest_tile = None

    for city_tile in city_tiles:
        dis = city_tile.pos.distance_to(unit.pos)
        if dis < closest_dis:
            closest_dis = dis
            closest_tile = city_tile
    
    return closest_tile

def near_to_night(game_state):
    return game_state.turn % 40 > 25

def random_choose_dir():
    r = random.random()
    if r <= 0.2:
        return DIRECTIONS.CENTER
    elif r <= 0.4:
        return DIRECTIONS.EAST
    elif r <= 0.6:
        return DIRECTIONS.WEST
    elif r <= 0.8:
        return DIRECTIONS.NORTH
    else:
        return DIRECTIONS.SOUTH

def get_closest_worker(unit, workers):
    closest_worker = None
    closest_dis = math.inf

    for worker in workers:
        dis = unit.pos.distance_to(worker.pos)
        if dis < closest_dis:
            closest_dis = dis
            closest_worker = worker
    
    return closest_worker

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
    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]
    width, height = game_state.map.width, game_state.map.height
    game_map = game_state.map

    resource_tiles: list[Cell] = []
    for y in range(height):
        for x in range(width):
            cell = game_state.map.get_cell(x, y)
            if cell.has_resource():
                resource_tiles.append(cell)
    
    city_tiles: list[Cell] = []

    for k, city in player.cities.items():
        city__tiles = city.citytiles
        for city_tile in city__tiles:
            city_tiles.append(city_tile)


    workers: list[Unit] = []
    carts: list[Unit] = []

    for unit in player.units:
        if unit.is_worker():
            workers.append(unit)
        elif unit.is_cart():
            carts.append(unit)

    # we iterate over all our units and do something with them
    for worker in workers:
        if worker.can_act():
            if near_to_night(game_state):
                closest_city_tile = get_closest_city_tile(worker,city_tiles)
                actions.append(worker.move(worker.pos.direction_to(closest_city_tile.pos)))
            elif worker.get_cargo_space_left() == 0:
                if worker.can_build(game_map):
                    actions.append(worker.build_city())
                else:
                    actions.append(worker.move(random_choose_dir()))
            elif game_map.get_cell_by_pos(worker.pos).has_resource():
                actions.append(worker.move(DIRECTIONS.CENTER))
            else:
                closest_resource_tile = get_closest_tile(worker,resource_tiles)
                actions.append(worker.move(worker.pos.direction_to(closest_resource_tile.pos)))

    for cart in carts:
        if cart.can_act():
            if cart.get_cargo_space_left() == 0 or near_to_night(game_state):
                closest_city_tile = get_closest_city_tile(cart,city_tiles)
                actions.append(cart.move(cart.pos.direction_to(closest_city_tile.pos)))
            else:
                closest_worker = get_closest_worker(cart,workers)
                actions.append(cart.move(cart.pos.direction_to(closest_worker.pos)))

    for city_tile in city_tiles:
        if player.research_points > 200:
            if len(workers) > len(carts)*3:
                actions.append(city_tile.build_cart())
            else:
                actions.append(city_tile.build_worker())
        else:
            if len(workers) > 10:
                actions.append(city_tiles.research())
            else:
                if len(workers) > len(carts)*3:
                    actions.append(city_tile.build_cart())
                else:
                    actions.append(city_tile.build_worker())

    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))
    
    return actions
