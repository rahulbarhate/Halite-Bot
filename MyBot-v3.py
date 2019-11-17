import hlt
import logging
from collections import OrderedDict


# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Settler-v3")

logging.info("Starting my Settler bot!")

planned_planets = []

while True:
    game_map = game.update_map()
    command_queue = []

    team_ships = game_map.get_me().all_ships()
    # For every ship that I control
    for ship in team_ships:
        shipid = ship.id
        if ship.docking_status != ship.DockingStatus.UNDOCKED: #If the ship is docked we skip the ship
            # Skip this ship
            continue

        

        # Getting the nearest entities to the ship
        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        # Ordering the entities by distance
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))
        #entities_by_distance - contains planets owned by us or the opponent, enemy ships, empty planets

        #Iterating through the list for ships vs planets
        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not entities_by_distance[distance][0].is_owned()]

        #Iterating through the 'entities_by_distance' and if the entity is a planet and isn't owned we add it to our list

        #Navigating
        #Building lists for finding enemy ships
        #Initially - if an empty planet is encountered, the ships are sent to that planet and we do not care about enemy ships
        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and entities_by_distance[distance][0] not in team_ships]

        #We need to go to the closest entity planet
        if len(closest_empty_planets) > 0:
            target_planet = closest_empty_planets[0]
            if ship.can_dock(target_planet):
                command_queue.append(ship.dock(target_planet))
                #Navigating to the closest planet
            else:
                navigate_command = ship.navigate(
                            ship.closest_point_to(target_planet),
                            game_map,
                            speed=int(hlt.constants.MAX_SPEED),
                            ignore_ships=False)

                if navigate_command:
                        command_queue.append(navigate_command)
                        
            #If there are no empty planets, attack enemy ships            
        elif len(closest_enemy_ships) > 0:
            target_ship = closest_enemy_ships[0]
            navigate_command = ship.navigate(
                        ship.closest_point_to(target_ship),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)

    game.send_command_queue(command_queue)
    # TURN END
# GAME END
                
