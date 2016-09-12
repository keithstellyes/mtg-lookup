# mtg-lookup

This is a Magic: The Gathering card search engine written in Python using
SQLite 3 as a backend. Currently, it is only usable as a command-line
application. This is a rebasing/refactoring in progress of some old code with
many features.

# Features
Currently, it supports only a few criteria searching (like power greater than
X), regex searching of names and card descriptions, among a few other things.
It is currently in the process of being updated with reimplementations of
already written features.

# Upcoming Features
More criteria searching, tag-based searching (Like, has-flying), complex 
boolean searches like returning only cards that are named Jace or are 
instants, or sorceries with CMC less than 4. These features already exist in
the old deprecated code, in fact.

# Setup
mtg-lookup is currently only distributed as Python 3 script and thus requires
a Python 3 interpreter on the machine running mtg-lookup. 

1. Download this repository

2. Run the db-builder with a *Python 3* interpreter in the **scripts/** 
directory. What this does is build the *SQLite* database file for the actual 
mtg-lookup script to search, it builds the database from a JSON file downloaded
from mtgjson.com *(Thanks to all the folks involved with that project!)*

3. Run the script, **mtg_lookup.py** with your Python 3 interpreter. Currently,
it is run only as a command line program and must be sent arguments that way.
See the **syntax** section on the syntax of those arguments passed.

# Syntax

In mtg-lookup, there are 3 types of parameters implemented, each with their
own syntax. There is also print settings

**Integer parameters:**

The keywords are: power, toughness, p, t, and cmc. (p ant t are shorthand for
power and toughness) right after usage of an integer argument, you must define
the equality you're searching for. For example, for all creatures with power
greater than 5, you would pass:

    -power >5

**NOTE:** In most environments, including Windows, Mac OS and Linux > < have a
special meaning, so to pass the above, you must surround the > < with "".

For power in a range 3-5, it is as simple as:

    -p ">2" -p "<6" 

or,

    -p ">=3" -p "<=5"

Also, for exact equality:

    -cmc 5

This will return all cards with a CMC of exactly 5.

**REGEX PARAMETERS**

The keywords are name, text

The syntax is simple:

    -keyword PATTERN

For cards that contain "Jace" in their name:

    -name jace

Also, by default name searches can be passed without the -name parameter The 
above can be written as:

    jace

For creatures with "golgari" in their name and power greater than 3 we can do:

    golgari -p ">3"

**LIST PARAMETERS**
The keywords are printings, colorid, and type

The syntax is simple, for inclusions there is:

    -keyword -i ELEMENT-TO-INCLUDE

Also,

    -keyword ELEMENT-TO-INCLUDE

For exclusions it is:

    -keyword -x ELEMENT-TO-EXCLUDE

**PRINT OPTIONS**
Currently, the only printing option beyond default is count_bare. This is mainly useful for debugging purposes.

It simply returns the number of results

The syntax is:

    -print count_bare
