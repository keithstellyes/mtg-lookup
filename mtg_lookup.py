#LICENSE: See LICENSE.txt
"""
AUTHOR: Keith Stellyes

This was originally written in a completly different way. This old code is not
public. This is the rebase, the refactored, the rebirth of that old project.

This is an MTG search engine backend that can be used as a command line app,
or be easily reworked as part of a website, or other things. It supports many
things like:

Regex searching of names, complex boolean sequences, and other criterias simply
not possible with Gatherer or magiccards.info

See the roadmap file for more info of where I intend to take this next.
"""
import os
import os.path
import sqlite3
import sys
from modules.query_builder import QueryBuilder as qb
from modules.arg_parser import parse_args

data_db_file = os.getcwd() + "/" + "data/data.db"

if not os.path.isfile(data_db_file):
    print("ERROR")
    print("Looked for database file at")
    print(data_db_file)
    print("But, it was not found. Please rebuild using build_db_from_json")
    print("It can be found in the scripts/db-builder/ directory.")
    print("Exiting.")
    sys.exit(1)

conn = sqlite3.connect(data_db_file)
qb.attach_connection(conn)

parse_args()
qb.make_query()
qb.print_results()
#data = qb.fetchall()
