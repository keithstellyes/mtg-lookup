"""
This is the tester script. It processes every .tst file
"""
import datetime,os,sys,timeit

def evaluate_tstfile(fullpath,script_path):
    def val_printer(val_name,val):
        print(val_name+":")
        print(val)
        print("------------------------")
    def std_test(lines):
        fail_ctr = 0
        for line in lines:
            expected = line[:line.index("#")] + '\n'
            call = line[line.index("#")+1:].rstrip()
            result = os.popen("python3 " + script_path + ' ' + call).read()
            if expected != result:
                fail_ctr+=1
                print("========================")
                print("==========FAIL==========")
                print("========================")
                val_printer("Test file",fullpath)
                val_printer("Line",line.rstrip())
                val_printer("Call",call)
                val_printer("Expected result",expected)
                val_printer("Actual result",result)
                print("========================")
                print("========================")
                print("========================")
        print("________________________")
        print("Failed tests:"+str(fail_ctr))
        print("________________________")
        if not fail_ctr:
            print("NO FAILURES")
            print("________________________")
    lines = open(fullpath).readlines()
    i = 0

    while not(lines[i].startswith("TST=")):
        i+=1
    if lines[i] == "TST=STD\n":
        i+=1
        print("Evaluating..."+tstfile)
        print("...STANDARD TEST...")
        std_test(lines[i:])
THIS_PATH = os.path.realpath(__file__)
TEST_FILE_DIR = os.path.dirname(THIS_PATH) + "/tests/"
arr = THIS_PATH.split('/')
SCRIPT_PATH = '/'.join(arr[0:len(arr)-3]) + '/mtg_lookup.py'

#Does not include the .../tests/ part of the file name
#we can add it later, though
files = os.listdir(TEST_FILE_DIR)

#The Pythonic way of doing it
#Basically, this makes a new list from files, where
#each element in the new list meets the condition f.endswith(".tst")
tstfiles = [f for f in files if f.endswith(".tst")]

for i in range(len(tstfiles)):
    tstfiles[i] = TEST_FILE_DIR+tstfiles[i]

print("Test file dir:"+TEST_FILE_DIR)
print("Number of test files detected: "+str(len(tstfiles)))
print("Test files:\n"+"\n".join(tstfiles),end="\n\n")

for tstfile in tstfiles:
    print("Opening..." + tstfile)

    time_elapsed = timeit.timeit(lambda:evaluate_tstfile(tstfile,SCRIPT_PATH),number = 1)
    print("Time elapsed for {0}:\n{1}".format(tstfile,str(time_elapsed)))
    #print("Time elapsed for {0}:\n{1}".format(tstfile,str(datetime.datetime.now()-begin)))
