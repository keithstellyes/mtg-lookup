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

More criteria searching, tag-based searching (Like, has-flying)

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
special meaning, so to pass the above, you must surround the > < with "" or,
escape it with a \.

For power in a range 3-5, it is as simple as:

    -p ">2" -p "<6" 

or,

    -p ">=3" -p "<=5"

or,
    -p \\>2 -p \\<6

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

The keywords are printings, colorid, format and type

The syntax is simple, for inclusions there is:

    -keyword -i ELEMENT-TO-INCLUDE

Also,

    -keyword ELEMENT-TO-INCLUDE

For exclusions it is:

    -keyword -x ELEMENT-TO-EXCLUDE

**PRINT OPTIONS**

Currently, there are two printing options (not including the default one):

count_bare and custom

*count_bare:*

It simply returns the number of results

The syntax is:

    -print count_bare

*custom:*

Loads a custom print formatting as defined by a file. See Custom card printing.

    -print custom file-path-of-formatting-file

# Custom card printing

mtg-lookup also supports custom print outputting as defined by a text file.

The syntax is simple: {SQLite column name} to be replaced by it. See the 
examples examples-of-custom-card-output/ folder for examples. Currently, lists
are stored as ; separated lists with ; at each end, meaning, putting in {FORMAT}
will output an ugly list with semi-colons between the elements and at the 
beginning and end.

# Boolean operations

    -bool "OPERATION" CRITERIA-GROUP-0 , CRITERIA-GROUP-1

mtg-lookup's uses a "Criteria group" model. A standard search that does not use
boolean operators only has a single criteria group. | is used to represent OR,
and & represents AND.

Currently, it only supports up to 10 criteria groups, starting with criteria 0.
It is best explained by example.

For example, to search for blue instants that cost less than 4 mana, or Jace 
planeswalker cards, we would do the following:

    mtg_lookup.py -bool "0|1" -type Jace , -type instant -cmc "<4"

**Explanation:**
    -bool "0|1" 
That translates to CRITERIA-GROUP-0 OR CRITERIA-GROUP-1 . In order for a
card to be matched by a criteria group, it must match all of its parameters.

    ,

This separates the criteria groups.

In that example, the criteria groups are:

    -type Jace

and

    -type instant cmc "<4"
