# Conway-Pool-Process
A multicore processing example of Conway's Game of Life

## Contents

1. [Installation](#Installation)
2. [Usage](#Usage)
3. [API](#API)

### [Installation](#Installation)

You need `numpy` to run this, so go ahead and install it `pip/pip3 install numpy` simple as that. Or whatever your current environment setup is, do the correct installation procedure.

To install the program, simply clone the repository and navigate to the installation location with a terminal. Then call `python main.py`.

### [Usage](#Usage)

To run the program you can call `python main.py [filename]`, the software runs in the terminal and makes use of the size of the terminal to determine how big of a plain to create. To adjust the size of the font in your terminal, use `Ctrl+'+'` and `Ctrl+'-'`.

You can change the size of the terminal at run time, but the changes won't take affect until the next time the software is started.

### [API](#API)

You can create your own patterns to construct as blueprints, they're passed into the `Plain.construct()` method [[source]](./plain.py)

Or you can save them as a `.rle` format file and load them in using the main usage. Or by manually calling `read_rle()` [[source]](./file.py) to create a blueprint and then load it by calling the `Plain.construct()` method.

You calling `tick()` moves the plain through one iteration

See [main.py](./main.py) for a better example of the usage.
