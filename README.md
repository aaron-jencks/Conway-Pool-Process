# Conway-Pool-Process
A multicore processing example of Conway's Game of Life

## Contents

1. [Installation](#Installation)
2. [Usage](#Usage)
3. [API](#API)

### [Installation](#Installation)

To install the program, simply clone the repository and navigate to the installation location with a terminal. Then call `python main.py`.

### [Usage](#Usage)

To run the program you can call `python main.py`, the software runs in the terminal and makes use of the size of the terminal to determine how big of a plain to create. To adjust the size of the font in your terminal, use `Ctrl+'+'` and `Ctrl+'-'`.

You can change the size of the terminal at run time, but the changes won't take affect until the next time the software is started.

### [API](#API)

You can create your own patterns to construct as blueprints, they're passed into the `Plain.construct()` method [[source]](./plain.py)

You calling `tick()` moves the plain through one iteration

See [main.py](./main.py) for a better example of the usage.
