import json
import os
import random
import bottle
import sys

from api import ping_response, start_response, move_response, end_response

# direction dictionary
Directions_dict = {'right': [1,0], 'left':[-1,0], 'up':[0,-1], 'down':[0,1]}


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    #data = bottle.request.json
    #print(json.dumps(data))

    color = "#8B008B"   # dark magenta
    head = "pixel"
    tail = "sharp"

    return start_response(color, head, tail)


@bottle.post('/move')
def move():
    data = bottle.request.json
    """
    DATA JSON FORMAT:
    {
        "game": {
            "id": "game-id-string"
        },
        "turn": "int",
        "board": {
            "height": "int",
            "width": "int",
            "food": [{
            "x": "int",
            "y": "int"
            }],
            "snakes": [{
            "id": "int",
            "name": "string",
            "health": "int",
            "body": [{
                "x": "int",
                "y": "int"
            }]
            }]
        },
        "you": {
            "id": "int",
            "name": "string",
            "health": "int",
            "body": [{
            "x": "int",
            "y": "int"
            }]
        }
    }
    """

    #print(json.dumps(data))

    # Initial direction choice
    directions = ['up', 'down', 'left', 'right']
    print("New Move!")
    # 1st check if move is deadly
    # 2nd check if move is dangerous
    # -> another snake head could move there

    death_directions = []
    dangerous_directions = []
    potential_directions = []
    safe_directions = []

    for direction in directions:
        if check_move_isdeadly(data, direction):
            print("Moving in " + direction + " is deadly!")
            sys.stdout.flush()
            death_directions.append(direction)
        else:
            potential_directions.append(direction)

    if( len(death_directions) == 4): # all 4 directions are death.
        return move_response(random.choice(directions)) # doesn't matter. Dead anyway.

    for direction in potential_directions:
        if check_move_isdangerous(data, direction):
            print("Moving in " + direction + " is dangerous!")
            sys.stdout.flush()
            dangerous_directions.append(direction)
        else:
            safe_directions.append(direction)
    
    # find food
    for direction in safe_directions:
        print("Moving in " + direction + " is safe!")
        if check_move_food(data, direction):
            return move_response(direction)

    if( len(safe_directions) == 0): # no directions is explicitely safe, go random dangerous.
        movedir = random.choice(dangerous_directions)
        print("Moving in direction " + movedir)
        sys.stdout.flush()
        return move_response(movedir)
    else: #have some safe direction
        movedir = random.choice(safe_directions)
        print("Moving in direction " + movedir)
        sys.stdout.flush()
        return move_response(movedir)

    
    return move_response('up')

def check_move_food(data, direction):
    myhead_x = int(data['you']['body'][0]['x'])
    myhead_y = int(data['you']['body'][0]['y'])
    new_x = myhead_x + int(Directions_dict[direction][0])  # take the head of my snake, and add the x direction 
    new_y = myhead_y + int(Directions_dict[direction][1])  # take the head of my snake, and add the y direction 

    for food in data['board']['food']:
        if (int(food['x']) == new_x and int(food['y']) == new_y):
            return True
    
    return False

def check_move_isdeadly(data, direction):
    # check not going outside of border of map
    # check not running into another snake

    # establish head position, and next position
    myhead_x = int(data['you']['body'][0]['x'])
    myhead_y = int(data['you']['body'][0]['y'])
    new_x = myhead_x + int(Directions_dict[direction][0])  # take the head of my snake, and add the x direction 
    new_y = myhead_y + int(Directions_dict[direction][1])  # take the head of my snake, and add the y direction 

    # 1 checking new x is on the board
    if new_x not in range(data['board']['width']):
        return True
    if new_y not in range(data['board']['height']):
        return True
    
    # 2 check not running into another snake body
    for snake_body in data['board']['snakes']:
        for index, spot in enumerate(snake_body['body']):
            if (new_x == spot["x"] and new_y == spot["y"]):
                if(index == len(snake_body['body']) -1 ): # end of the snake, hope the snake moves and its safe.
                    continue
                else:
                    return True     

    return False # move is not deadly


def check_move_isdangerous(data, direction):
    # check not running into where another snake could be
    # -> Head on collision of unequal length snakes - shorter snake dies.
    # -> Head on collision of equal length snakes - both snakes die.

    myhead_x = int(data['you']['body'][0]['x'])
    myhead_y = int(data['you']['body'][0]['y'])
    new_x = myhead_x + int(Directions_dict[direction][0])  # take the head of my snake, and add the x direction 
    new_y = myhead_y + int(Directions_dict[direction][1])  # take the head of my snake, and add the y direction
    print("Testing newx = " + str(new_x) + " and newy = " + str(new_y))

    # 1 Head Colisions
    snake_move_points_x = []
    snake_move_points_y = []
    # get a list of snake heads and
    # create potential move areas around head (include death moves for their heads, won't matter for my snake.)
    for snake in data['board']['snakes']:
        if(data['you']['name'] == snake['name']):
            print("Found my snake in the list")
            continue
        snake_head = snake['body'][0]
        print(snake_head)
        if(len(snake['body']) >= len(data['you']['body']) ): # can possibly die from this movement.
            snake_move_points_x.append( int(snake_head['x']) + 1 ) # right
            snake_move_points_x.append( int(snake_head['x']) - 1 ) # left
            snake_move_points_x.append( int(snake_head['x']) + 0 ) # up
            snake_move_points_x.append( int(snake_head['x']) + 0 ) # down
            snake_move_points_y.append( int(snake_head['y']) + 0 ) # right
            snake_move_points_y.append( int(snake_head['y']) + 0 ) # left
            snake_move_points_y.append( int(snake_head['y']) - 1 ) # up
            snake_move_points_y.append( int(snake_head['y']) + 1 ) # down

    print(snake_move_points_x)
    print(snake_move_points_y)
    for index,point in enumerate(snake_move_points_x):
        if new_x == snake_move_points_x[index] and new_y == snake_move_points_y[index]:
            return True  # point in is potential zones for other snake to move to. consider it dangerous.

    # 2 Consider small dead ends
        # TODO: Add more code here

    return False


@bottle.post('/end')
def end():
    #data = bottle.request.json
    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
