#LICENSE: See LICENSE.txt
import sqlite3
import sys

try:
    from query_builder import QueryBuilder as qb
except ImportError:
    from modules.query_builder import QueryBuilder as qb

def parse_args():
    #arg_name:db_col_name

    #usage: -power ">5"
    #usage: -toughness 5
    int_keys = {"power":"POWER","toughness":"TOUGHNESS"
                ,"p":"POWER","t":"TOUGHNESS","cmc":"CMC"}

    #usage: -name REGEXPATTERN
    re_keys = {"name":"NAME","text":"CARD_TEXT"}

    #usage:
    #-type -i type_a type_b -x type_c
    #include types a, types b, exclude type c
    list_keys = {"type":"ALL_TYPES","legal":"LEGALITIES"
                 ,"colorid":"COLOR_IDENTITY","printings":"PRINTINGS"}
    misc_keys = ["-print","-help",","]
    valid_print_options = ['count_bare']

    i = 1

    arr_len = len(sys.argv)

    while i < arr_len:
        if sys.argv[i][0] != "-":
            #SET THIS CRITERIA NAME
            qb.add_regex("NAME",sys.argv[i])
            i += 1
            continue
        if sys.argv[i][1:] in re_keys.keys():
            col = re_keys[sys.argv[i][1:]]
            i += 1
            qb.addregex(col,sys.argv[i])
            i += 1
            continue
        if sys.argv[i][1:] in int_keys.keys():
            col = int_keys[sys.argv[i][1:]]
            i += 1
            try:
                int(sys.argv[i])
                val = sys.argv[i]
                qb.add_equality_operation(col,val,"==")
                i += 1
                continue
            except ValueError:
                if sys.argv[i][1] != "=" or sys.argv[i][1] != ">" or sys.argv[i][1] != "<":
                    qb.add_equality_operation(col,str(int(sys.argv[i][1:])),sys.argv[i][0])
                    i += 1
                    continue
                qb.add_equality_operation(col,str(int(sys.argv[i][1:])),sys.argv[i][0:2])
                i += 1
                continue
        #TODO: look into the sqlite3's adapter features for Python <-> sqlite data
        if sys.argv[i][1:] in list_keys.keys():
            arg = list_keys[sys.argv[i][1:]]
            i += 1
            inclusions = []
            exclusions = []
            if sys.argv[i] != '-x':
                inclusions.append(sys.argv[i])
            else:
                i += 1
                exclusions.append(sys.argv[i])
            qb.add_list(arg,inclusions,exclusions)

            i += 1
            continue
        #IF WE HIT HERE, WE'VE HIT MISCELANNY OPTIONS
        if sys.argv[i] in misc_keys:
            #PROCESS...
            if sys.argv[i] == "-print":
                i += 1
                if sys.argv[i] not in valid_print_options:
                    print("BAD ARGUMENT FOR -print:")
                    print(sys.argv[i])
                    sys.exit(1)
                qb.print_settings = sys.argv[i]
            i += 1
            continue
        print("Argument not recognized:")
        print(sys.argv[i])
        sys.exit(1)
