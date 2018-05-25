[![Businge Scott](https://img.shields.io/badge/Businge%20Scott-Checkpoint1-green.svg)]()
[![Build Status](https://travis-ci.org/scott45/checkpoint-1A.svg?branch=master)](https://travis-ci.org/scott45/checkpoint-1A)
[![Coverage Status](https://coveralls.io/repos/github/scott45/checkpoint-1A/badge.svg)](https://coveralls.io/github/scott45/checkpoint-1A)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)]()

# Amity Room Allocation System.

>Done in fulfillment of the first checkpoint as a requirement in the Andela developer fellowship program.

#1. Problem definition.

The system serves to automate allocation of rooms (which can be either living spaces or offices) to fellows and staff at Andela.

**Who? Fellows and staff at one of Andela's facility called Amity.**

Fellows and staff at Andela are the targeted users of the system.

**What? A room allocation system**

Objective is to have a room allocation system that enables the addition of staff and fellows and automatically allocated them to available rooms.

>An office can contain a maximum of 6 people while a living space takes in a maximum of 4 people.

**Where? Office spaces and living spaces.**

The system manages office spaces as well as living spaces and ensures they are allocated randomly.

**When? On adding a person andon request to occupy a space through reallocation.**

The spaces mentioned above need to be allocated when vacant or occupied and/or reallocated as well as give status on their status when required.
The system serves to also tell how many people are in a given space at any given time.

**Why? To ensure allocation and reallocation of rooms to the fellow and staff.**

The criteria set to solve the problem is to ensure the rooms can and will be allocated on request to get a new space whether office space or living space.
There is also the need to have a way of determing how many people are at a particular space from time to time.


#2. Commands.

Command | Argument | Example
--- | --- | ---
create_room | L or O | create_room O try-it
add_person | (first_name) (last_name) (person_type) [--accomodate] |add_person yours here Fellow --accomodate=Y
reallocate_person | (identifier) (new_room_name) | reallocate_person S1 room
load_people | (filename) | load_people ccreated.txt
print_allocations| [--o=filename] | print_allocations --o=allocations
print_unallocated| [--o=filename] | print_unallocated --o=allocations
print_room | (room_name) | print_room try-it
save_state | [--db=sqlite_database]| save_state --db=database
load_state |(sqlite_database)|load_state my_dbname

#3. Installation and set up.

1. First clone this repository to your local machine using `git clone https://github.com/scott45/checkpoint1.git

3. Create a **virtualenv** on your machine and install the dependencies via `pip install -r requirements.txt` and activate it.

4. cd into the **amityapp** folder and run `python main.py`

#5. Usage video

The following screencast shows how to run the different commands. Check it out:

[![asciicast](https://asciinema.org/a/641tt6m2ljcn5jun51xyrjpwr.png)](https://asciinema.org/a/641tt6m2ljcn5jun51xyrjpwr)

#6. Running Tests.

To run nosetests ensure that you are within the *virtual environment* and have the following installed:

1. *nose*

2. *coveralls*

3. *coverage*

After ensuring the above are installed within the **amity folder** run :

`nosetests --with-coverage` and

`coverage report`

To run tests and view coverage.

#7. IceBox (to-do's).

1. Integrate CI & CD.


## Credits

1. [Businge Scott](https://github.com/scott45)

2. The amazing [Andela](https://www.andela.com) community.

## License

### The MIT License (MIT)

Copyright (c) 2017 [BUSINGE SCOTT [ANDELA]]

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.
