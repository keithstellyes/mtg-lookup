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
