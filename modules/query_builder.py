#LICENSE: See LICENSE.txt
#query_builder.py
import re
import sqlite3

class QueryBuilder:
    qry = "SELECT * FROM CARDS WHERE "
    cursor = None
    cursor_results = None
    this_criteria = set()
    #criteria_groups = set()
    criteria_groups = []
    print_setting = ""
    custom_print_str = ""
    bool_operation = None
    debug_options = {"PRINT_QUERY":False}

    #returns True on success, False on failure
    def push_bool_operation(s):
        valid_chars = "0123456789()&| "
        for c in s:
            if c not in valid_chars:
                return False
        QueryBuilder.bool_operation = s.replace("&", " AND ")
        QueryBuilder.bool_operation = QueryBuilder.bool_operation.replace("|"," OR ")
        for n in range(10):
            sn = str(n)
            snn = '{' + sn + '}'
            QueryBuilder.bool_operation = QueryBuilder.bool_operation.replace(sn,snn)

    def matches_regex(s,regex):
        regex = re.compile(regex,re.IGNORECASE)
        return regex.search(s) != None

    def list_has(col,incl,excl):
        try:
            col = col.lower()
            incll = incl.split(";")
            excll = excl.split(";")
            for el in excll:
                el = el.lower()
                el = ";" + el + ";"
                if el in col and el != ";;":
                    return False
            for el in incll:
                el = el.lower()
                el = ";" + el + ";"
                if el not in col and el != ";;":
                    return False
            return True
        except Exception as e:
            #print(e)
            return False

    def attach_connection(conn):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        conn.row_factory = dict_factory
        QueryBuilder.cursor = conn.cursor()
        conn.create_function("REGEX",2,QueryBuilder.matches_regex)
        conn.create_function("LIST_HAS",3,QueryBuilder.list_has)

    def add_regex(col,regex):
        QueryBuilder.this_criteria.add('REGEX('+str(col)+',"'+regex.replace('"','""')+'"' + ")")

    def add_list(col,incl=[],excl=[]):
        if incl == []:
            incl_arg = ";"
        else:
            incl_arg = ";".join(incl)
        if excl == []:
            excl_arg = ";"
        else:
            excl_arg = ";".join(excl)
        QueryBuilder.this_criteria.add('LIST_HAS(' + str(col) + ',"' + incl_arg + '","' + excl_arg + '")')

    def add_equality_operation(col,val,eq):
        QueryBuilder.this_criteria.add(col + eq + str(val))

    def combine_this_criteria():
        QueryBuilder.this_criteria = " AND ".join(list(QueryBuilder.this_criteria))
        if len(QueryBuilder.criteria_groups) > 1:
            #QueryBuilder.criteria_groups.add("("+QueryBuilder.this_criteria+")")
            QueryBuilder.criteria_groups.append("("+QueryBuilder.this_criteria+")")
        else:
            #QueryBuilder.criteria_groups.add(QueryBuilder.this_criteria)
            QueryBuilder.criteria_groups.append(QueryBuilder.this_criteria)
        QueryBuilder.this_criteria = set()

    #returns True on success, False on failure
    def make_query():
        QueryBuilder.combine_this_criteria()
        if len(QueryBuilder.criteria_groups) > 1:
            """QueryBuilder.qry += "("
            QueryBuilder.qry += " AND ".join(list(QueryBuilder.criteria_groups))
            QueryBuilder.qry += ")"""
            if QueryBuilder.bool_operation == None:
                return False
            QueryBuilder.bool_operation = QueryBuilder.bool_operation.format(*QueryBuilder.criteria_groups)
            QueryBuilder.qry += QueryBuilder.bool_operation

        else:
            QueryBuilder.qry += list(QueryBuilder.criteria_groups)[0]
        #QueryBuilder.print_query()
        QueryBuilder.cursor_results = QueryBuilder.cursor.execute(QueryBuilder.qry)
        #QueryBuilder.criteria_groups = set()
        QueryBuilder.criteria_groups = []
        #print(QueryBuilder.qry)
        if QueryBuilder.debug_options["PRINT_QUERY"]:
            print("===QUERY===")
            QueryBuilder.print_query()
            print("===========")

    def print_query():
        print(QueryBuilder.qry)
    def print_results():
        if QueryBuilder.print_setting == "":
            for r in QueryBuilder.cursor_results:
                #print(r)
                print(str(r['NAME']) + "   " + str(r['MANA_COST']))
                print(r['TYPE'])
                print(r['CARD_TEXT'])
                print()
        if QueryBuilder.print_setting == 'count_bare':
            print(len(QueryBuilder.cursor.fetchall()))
        if QueryBuilder.print_setting == 'custom':
            #Code from: https://docs.python.org/3.5/library/stdtypes.html#str.format
            class Default(dict):
                def __missing__(self, key):
                    return key
            for r in QueryBuilder.cursor_results:
                print(QueryBuilder.custom_print_str.format_map(Default(r)))
        #QueryBuilder.cursor.fetchone()['COLOR_IDENTITY']
        #To get col names we can use:
        # names = [description[0] for description in cursor.description]
        #(Thanks,
        #http://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite)
        """ columns are in the following order:
        CMC, COLOR_IDENTITY, COLORS, LEGALITIES, LOYALTY, MANA_COST, NAME,
        POWER, PRINTINGS, RULINGS, SUBTYPES, SUPERTYPES, CARD_TEXT, TOUGHNESS,
        TYPE, TYPES """
