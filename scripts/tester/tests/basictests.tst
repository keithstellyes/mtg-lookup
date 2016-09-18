TST=STD
1#-print count_bare "Deathcult Rogue"
1#"Deathcult Rogue" -print count_bare
16#-print count_bare cephalid
14#-print count_bare "^cephalid"
1#-print count_bare "cephalid a"
2#-print count_bare "(cephalid a)|(cephalid b)"
4#"cephalid s" -print count_bare
16#-print count_bare "(?=cephalid)"
4#-print count_bare "(?=.*cephalid)(?=.*er$)"
5#-print count_bare cephalid -text draw
0#-print count_bare -text "wow that's a real nice boat you dun got there!!!!"
16#-print count_bare jace
16#-print count_bare jace -colorid u
16#-print count_bare jace -colorid -x b
0#-print count_bare jace -colorid -x u
5#-print count_bare goblin -colorid w
3#-print count_bare goblin -colorid w -text strike
0#-print count_bare goblin -colorid w -text strike -colorid -x r
31#-print count_bare -type Scarecrow
30#-print count_bare -type Scarecrow -type Artifact
1#-print count_bare -type scarecrow -type LEGenDarY
1#-type SCAREcrow -print count_bare -type leGENDARY -text perm
340#-bool "0|1" -type scarecrow , -type goblin
