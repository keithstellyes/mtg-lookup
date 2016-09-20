try:
    from query_builder import QueryBuilder
except ImportError:
    from modules.query_builder import QueryBuilder

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
        try:
            print(len(QueryBuilder.cursor_results))
        except TypeError:
            print(len([r for r in QueryBuilder.cursor_results]))
    if QueryBuilder.print_setting == 'custom':
            #Code from: https://docs.python.org/3.5/library/stdtypes.html#str.format
        class Default(dict):
            def __missing__(self, key):
                return key
        for r in QueryBuilder.cursor_results:
            print(QueryBuilder.custom_print_str.format_map(Default(r)))
    if QueryBuilder.debug_options["PRINT_QUERY"]:
        print("===QUERY===")
        QueryBuilder.print_query()
        print("===========")
