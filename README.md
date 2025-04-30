# Wilderness Survival System

## Description

The Wilderness Survival System (WSS) is a "game" which emulates surviving in an
unknown wilderness. Players are placed randomly on the west side of the map and
make decisions to try and get to the east side of the map. After the players are
placed, the game runs itself (similar to John Conway's Game of Life).

## Developing

To start developing, clone this repo, make a venv, and install from
`requirements.txt`

To do that, run the following commands from the root directory:

```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Usage

To play the game, after installing requirements (see [here](#developing)),
simply run the following command:

```
python wss.py
```

To demo the procedural map generation, use the following:

```
python wss.py --demo-terrain
```
