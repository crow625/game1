# game1
My first game in Python. Inspired by Fire Emblem, Civ.

The goal is for a top-down, turn-based strategic game, like Fire Emblem or Civilization. 

The game board will be read from a text file or potentially randomly generated in the future.
There are currently four different types of terrain: grassland, desert, mountain, and water.
The maps will be symmetrical for both players: either rotationally symmetric or mirrored.

The game will take place in two phases: in the first phase, you survey the map and decide which units you want to use.
Each player will get a set number of units they can choose: probably around 5 or 6, depending on the size of the maps.
Every unit has different stats: Attack, defense, and a different movement cost on each terrain.
Some units will be better suited to different maps, and offense/defense.
There will be a library in-game with each unit's stats.
Neither player will know which units the other has picked until every unit has been chosen.

In the second phase, the players take turns moving their units and attacking the enemy's units.
The win condition has yet to be determined, but the plan is that each player has 2 forts in the corners of the map, 
and winning will be some combination of defending your forts while capturing one of the opponent's.
The goal is that gameplay will be equally split between offense and defense.
