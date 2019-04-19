# Battlesnake2019 - Python Snake - The most basic
A simple battlesnake built off the starter snake python template provided for [Battlesnake](http://battlesnake.io).

# Snake Logic
This snake performs the basic functionality to survive. It has no pathing algorithm, but solely relies on moving randomly on the gameboard, avoiding zones that will be deadly or dangerous.

The function for determining the next move location (three possible directions to move) works as follows:
- Check if any of the possible move locations are deadly (move off of map, or into another snake body)
- Determine if any of the remaining move locations are dangerous, and avoid them if possible. (Dangerous is determined as potentially coliding with another snake's head, which the snake's length is larger than my own.)
- From the remaining safe locations, see if any food is present, and go there if it is.

One additional feature that improves it past the most basic survival mode is the ability to look one move ahead. It will perform the above math, to check if the next move location will result in death (going into a dead end). It will avoid that move if possible.


# starter-snake-python
Visit [https://github.com/battlesnakeio/community/blob/master/starter-snakes.md](https://github.com/battlesnakeio/community/blob/master/starter-snakes.md) for API documentation and instructions for running your AI.

This AI client uses the [bottle web framework](http://bottlepy.org/docs/dev/index.html) to serve requests and the [gunicorn web server](http://gunicorn.org/) for running bottle on Heroku. Dependencies are listed in [requirements.txt](requirements.txt).
