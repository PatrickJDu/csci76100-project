# csci76100-project
[Demo Video](https://drive.google.com/open?id=1ALGePklEHxupCHI5IPG7ZZuBVvTlw52D)

``` python
# Run genetic algorithm
GameManager.py 1 (DISPLAY_ON/DISPLAY_OFF) (TRAIN/LOAD_POPULATION/LOAD_WEIGHT) (TRAIN BOTH/PREY/HUNTER or LOAD_PREY) (LOAD_HUNTER)

# (DISPLAY_ON/DISPLAY_OFF): 1 to show the window during the run. 0 to hide the window during the run.

# (TRAIN/LOAD_POPULATION/LOAD_WEIGHT) 0 to train the neural network from scratch, 1 to train from a certain generation (Provide a csv file), 2 to use a generation (Provide a csv file)

# (TRAIN BOTH/PREY/HUNTER or LOAD_PREY) If 1 or 2 was not specified in the prevous argument nothing is needed here. However, if there values are provided, a csv file msut be provided to mark the generation seed.

# (LOAD_HUNTER) Same as the last argument.

# Run expectiminimax, outputs the score of the run (prey size - 1).
GameManager.py 0 (DISPLAY_ON/DISPLAY_OFF) (SMART/RANDOM PREY) (SMART/RANDOM HUNTER)

# (DISPLAY_ON/DISPLAY_OFF): 1 to show the window during the run. 0 to hide the window during the run.

# (SMART/RANDOM PREY): For expectiminimax: 1 to use prey heuristics for the prey ai and 0 to use a random choice.

# (SMART/RANDOM HUNTER): For expectiminimax: 1 to use hunter heuristics for the hunter ai and 0 to use a random choice.
```
