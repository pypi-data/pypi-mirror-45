# risk

This project is the python *plug and play* implementation of the game [risk](https://en.wikipedia.org/wiki/Risk_(game)).

## TC1 (reached)

We have reached TC1 when:
- we have created a general structure for the game (folder structure, packages, deployment) (reached)
- we have defined the observation space (reached)
- we have defined the action space (reached)

## TC2 (reached)

We have reached TC2 when:
- We have implemented Version 1 ([v1](./versions.md)) (reached)

## TC3 (due date 21-12-2018)

We have reached TC3 when:
- We have assigned an executor to each of the following bullet points
- We have moved `humain.py` to the environment (there is a `human mode` for that)
- We are able to load and store graphs (either through own implementation or via the [NetworkX](https://networkx.github.io/documentation/networkx-1.10/overview.html) library)
- We have enhanced code readability (refactor classes and functions to be understood more easily)
- We have documented the written code (correlates with the point above)
- We have implemented Version 2 ([v2](./versions.md))

## TC4 (due date 22-03-2019)

We have reached TC4 when:
- We have implemented the actual risk map as our graph
- We have implemented the troop deployement
- We have playermoves consisting of seperate stages
- We have added Tests for our main features

## TC5 (due date xx-xx-2019)

We have reached TC5 when:
- We have implemented the random card reward for a won country

## TC6 (due date xx-xx-2019)

We have reached TC6 when:
- We have implemented the random dice roll to determine the outcome of a fight