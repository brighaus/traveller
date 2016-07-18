# traveller

####Python 3 CRUD system for making science fiction characters and careers based on the Games Designer's Workshop Traveller ruleset.

- Work in progress.
- Includes some crude CLI scripts for creating with characters and services.
- Includes a byte code file database with some premade characters.
- Most classes have self executing suites that demo their API.

####Key players:

- util/data-config.py
  - manages data paths and logging targets. intended to be readonly at runtime.
- util/datamule.py
  - core CRUD API for shelves and pickle
- make_character.py
  - create and save a character from the CLI
  - useage: <projectlocation>$python3 make_character.py