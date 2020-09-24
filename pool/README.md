Pool
====
Pool stuff

Collisions
----------
### Non-relativistic
Just calculate the new velocities using Newton's laws + conservation of energy  
Assume balls are incompressible


### Collision Logic
#### Overlaps
Algorithm for when balls overlap:
 - Step back until balls are just touching, fraction *f* of a timestep
 - Calculate new velocities
 - Step forward (1 - *f*) of a timestep

#### Multiple Collisions
It's hard to simulate one-on-two collisions numerically
Q: do we deal with all collisions at once, or them one at a time?
Both lead to unphyiscal results...
[Here's a link](https://stackoverflow.com/questions/16423466/how-to-handle-multiple-simultaneous-elastic-collisions)
Probably need to read up on algorithms and pick a good one
