#query_builder.py
import re
import sqlite3

class QueryBuilder:
    qry = "SELECT * FROM CARDS WHERE "
    cursor = None
    cursor_results = None
    this_criteria = set()
    criteria_groups = set()

    def matches_regex(s,regex):
        regex = re.compile(regex,re.IGNORECASE)
        return regex.search(s) != None

    def attach_connection(conn):
        QueryBuilder.cursor = conn.cursor()
        conn.create_function("REGEX",2,QueryBuilder.matches_regex)

    def add_regex(col,regex):
        QueryBuilder.this_criteria.add('REGEX('+str(col)+',"'+regex.replace('"','""')+'"' + ")")

    def add_equality_operation(col,val,eq):
        QueryBuilder.this_criteria.add(col + eq + str(val))

    def combine_this_criteria():
        QueryBuilder.this_criteria = " AND ".join(list(QueryBuilder.this_criteria))
        if len(QueryBuilder.criteria_groups) > 1:
            QueryBuilder.criteria_groups.add("("+QueryBuilder.this_criteria+")")
        else:
            QueryBuilder.criteria_groups.add(QueryBuilder.this_criteria)
        QueryBuilder.this_criteria = set()

    def make_query():
        QueryBuilder.combine_this_criteria()
        if len(QueryBuilder.criteria_groups) > 1:
            QueryBuilder.qry += "("
            QueryBuilder.qry += " AND ".join(list(QueryBuilder.criteria_groups))
            QueryBuilder.qry += ")"
        else:
            QueryBuilder.qry += list(QueryBuilder.criteria_groups)[0]
        QueryBuilder.print_query()
        QueryBuilder.cursor_results = QueryBuilder.cursor.execute(QueryBuilder.qry)
        QueryBuilder.criteria_groups = set()

    def print_query():
        print(QueryBuilder.qry)
    def print_results():
        for r in QueryBuilder.cursor_results:
            print(r)
        """ columns are in the following order:
        CMC, COLOR_IDENTITY, COLORS, LEGALITIES, LOYALTY, MANA_COST, NAME,
        POWER, PRINTINGS, RULINGS, SUBTYPES, SUPERTYPES, CARD_TEXT, TOUGHNESS,
        TYPE, TYPES """
