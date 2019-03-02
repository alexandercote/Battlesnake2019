import json
import os
import random
import bottle

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
    data = bottle.request.json
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

    print(json.dumps(data))

    # Initial direction choice
    directions = ['up', 'down', 'left', 'right']
    random_selected_direction = random.choice(directions)

    myhead_x = int(data['you']['body'][0]['x'])
    myhead_y = int(data['you']['body'][0]['y'])

    # 1st check if move is deadly
    # 2nd check if move is dangerous
    # -> another snake head could move there

    for direction in directions



    return move_response(random_selected_direction)



def check_move_isdeadly(data, direction):
    # check not going outside of border of map
    # check not running into another snake

    myhead_x = int(data['you']['body'][0]['x'])
    myhead_y = int(data['you']['body'][0]['y'])
    new_x = myhead_x + Directions_dict[direction][0]  # take the head of my snake, and add the x direction 
    new_y = myhead_y + Directions_dict[direction][1]  # take the head of my snake, and add the y direction 

    return True

def check_move_isdangerous(data, direction):
    # check not running into where another snake could be
    # -> Head on collision of unequal length snakes - shorter snake dies.
    # -> Head on collision of equal length snakes - both snakes die.

    myhead_x = int(data['you']['body'][0]['x'])
    myhead_y = int(data['you']['body'][0]['y'])
    new_x = myhead_x + Directions_dict[direction][0]  # take the head of my snake, and add the x direction 
    new_y = myhead_y + Directions_dict[direction][1]  # take the head of my snake, and add the y direction

    return True


@bottle.post('/end')
def end():
    data = bottle.request.json
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
