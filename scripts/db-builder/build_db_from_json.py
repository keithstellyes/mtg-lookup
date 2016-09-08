"""
build-db-from-json.py
"""
print("...Importing libs...")

import json,os,sqlite3

print("...Calculating absolute path of data directory...")
data_dir = str(os.getcwd()).split("/")
data_dir = data_dir[0:len(data_dir)-2]
data_dir.append("data")
data_dir = "/".join(data_dir)+"/"
print("Data directory:")
print(data_dir)

print("...Building sqlite DB from JSON's...")

data = json.load(open(data_dir + 'AllCards-x.json','r'))

print("AllCards-x.json loaded succesfully.")

card_count = len(data.keys())

print("# of cards:",card_count)

print("...Scanning for unique keys...")

unique_keys = set()

for k in data.keys():
    for kk in data[k].keys():
        unique_keys.add(kk)
print("# of unique card keys:",len(unique_keys))
unique_keys_list = sorted(set(unique_keys))
print("===KEYS===")
print(";".join(unique_keys_list))
print("==========")

print("...Getting detailed information per key...")
for uk in unique_keys_list:
    cards_with = card_count
    occuring_types = set()
    occuring_values = set()

    for k in data.keys():
        try:
            occuring_types.add(str(type(data[k][uk])))
            occuring_values.add(str(data[k][uk]))
        except KeyError:
            cards_with -= 1
    print("=KEY DETAILS=")
    print("JSON key name:",uk)
    print("# of cards with key:",cards_with)
    print("# of unique types:",len(occuring_types))
    print("# of unique values:",len(occuring_values))
    print("Occuring types:",";".join(sorted(list(occuring_types))))
    print("=============")

"""
===KEYS===
cmc;colorIdentity;colors;hand;imageName;layout;legalities;life;loyalty;
manaCost;name;names;power;printings;rulings;source;starter;subtypes;supertypes;
text;toughness;type;types
==========
"""

print("...Starting DB building...")
db_file = data_dir + "data.db"
print("...Saving as"+db_file+"...")
conn = sqlite3.connect(db_file)
print("File opened succesfully")
c = conn.cursor()
print("DB Cursor created")
qry = "CREATE TABLE CARDS (CMC INTEGER,COLOR_IDENTITY TEXT,COLORS TEXT,"
qry += "LEGALITIES TEXT,LOYALTY INTEGER,MANA_COST TEXT,NAME TEXT,"
qry += "POWER INTEGER, PRINTINGS TEXT, RULINGS TEXT, SUBTYPES TEXT,"
qry += "SUPERTYPES TEXT, CARD_TEXT TEXT, TOUGHNESS INTEGER, TYPE TEXT,"
qry += "TYPES TEXT)"
print("...Executing query:...")
print(qry)
print("......................")
c.execute(qry)

#TODO Try nulls for power and such (as in, queries like ,,)
#TODO Empty strings instead for text-less ones? Or even just like above
#TODO More tables for printings/legalities/etc.
for k in data.keys():
    qry = "INSERT INTO CARDS (NAME,CMC,COLOR_IDENTITY,COLORS,LEGALITIES,"
    qry += "LOYALTY,MANA_COST,POWER,PRINTINGS,RULINGS,SUBTYPES,"
    qry += "SUPERTYPES,CARD_TEXT,TOUGHNESS,TYPE,TYPES) VALUES("
    try:
        qry += '"'+str(data[k]['name']).replace('"','""')+'"'
    except:
        qry += "'NULL'"
    qry += ","

    try:
        qry += str(data[k]['cmc'])
    except KeyError:
        qry += "0"
    qry += ","

    try:
        qry += "'"+";".join(data[k]['colorIdentity'])+"'"
    except KeyError:
        qry += "NULL"
    qry += ","

    try:
        qry += "'"+";".join(data[k]['colors'])+"'"
    except KeyError:
        qry += "'NULL'"
    qry += ","

    """
    try:
        #qry += ";".join(data[k]['legalities'])
        qry += str(data[k]['legalities'])
    except KeyError:
        qry += "NULL"
    qry += ","
    """
    qry += "'',"

    try:
        qry += str(data[k]['loyalty'])
    except KeyError:
        qry += "-1"
    qry += ","

    try:
        qry += "'"+data[k]['manaCost']+"'"
    except KeyError:
        qry += "'NULL'"
    qry += ","

    try: #-42 if no power, -43 is not int-able
        qry += str(int(data[k]['power']))
    except KeyError:
        qry += "-42"
    except ValueError:
        qry += "-43"
    qry += ","

    try:
        qry += "'"+";".join(data[k]['printings'])+"'"
    except KeyError:
        qry += "'NULL'"
    qry += ","

    """
    try:
        qry += str(data[k]['rulings'])
    except KeyError:
        qry += "NULL"
    qry += ","
    """
    qry += "'',"

    try:
        qry += "'"+";".join(data[k]['subtypes'])+"'"
    except KeyError:
        qry += "'NULL'"
    qry += ","

    try:
        qry += "'"+";".join(data[k]['supertypes'])+"'"
    except KeyError:
        qry += "'NULL'"
    qry += ","

    try:
        qry += '"'+data[k]['text'].replace('"','""')+'"'
    except KeyError:
        qry += "'NULL'"
    qry += ","

    try: #-42 if no toughness, -43 is not int-able
        qry += str(int(data[k]['toughness']))
    except KeyError:
        qry += "-42"
    except ValueError:
        qry += "-43"
    qry += ","

    try:
        qry += '"'+data[k]['type']+'"'
    except KeyError:
        qry += "'NULL'"
    qry += ","

    try:
        qry += '"'+";".join(data[k]['types'])+'"'
    except KeyError:
        qry += "'NULL'"

    try:
        c.execute(qry+")")
        #print(".",end="")
    except Exception as e:
        print(e)
        print("====")
        print(qry+")")
        print("====")
print("Table built!")
print("...Committing and 'closing connection'")

conn.commit()
conn.close()

print("All done, let's hope everything worked :)")
