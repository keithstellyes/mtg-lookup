try:
    from query_builder import QueryBuilder
except ImportError:
    from modules.query_builder import QueryBuilder

print("Testing QueryBuilder...")
print("    -def push_bool_operation()")
################################################################################
print("        Testing push_bool_operation's error-finding...")
tests = {"DROP TABLES":False, "a":False, "DROP CARDS":False, "SELECT":False,
        "1|6":False,"0|1":True,"(0|1)":True,"0":True,"{":False, "0&1":True,
        "0|1 DROP CARDS":False,"0&(1|2)":True}
num_tests = len(tests)
failures = []

for test in tests.keys():
    result = QueryBuilder.push_bool_operation(test) == tests[test]
    if not result:
        failures.append(test)


print(str(len(failures)) + '/' + str(len(tests)) + ' tests FAILED:')
for failure in failures:
    print('FAILURE: ', failure)
    print('EXPECTED:', tests[failure])
    print('ACTUAL:  ', not(tests[failure]))

################################################################################
#Resetting
QueryBuilder.bool_operation = None
print("        Testing push_bool_operation's converting correctly")
tests = {"0|1":"{0} OR {1}","0&1":"{0} AND {1}","0&(1|2)":"{0} AND ({1} OR {2})"}

failure_output = ""
test_len = len(tests)
failures = test_len

for test in tests.keys():
    QueryBuilder.push_bool_operation(test)
    if QueryBuilder.bool_operation == tests[test]:
        failures -= 1
    else:
        failure_output += 'FAILURE: ' + test + '\n'
        failure_output += 'EXPECTED:' + tests[test] + '\n'
        failure_output += 'ACTUAL:  ' + QueryBuilder.bool_operation + '\n'

print(str(failures) + '/' + str(test_len) + ' tests FAILED:')
print(failure_output, end='')
