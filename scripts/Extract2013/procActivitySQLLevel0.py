import sys,MySQLdb,time,string,re,os

rs = ()

try:
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="mozilla",port=3306)
    cur = conn.cursor()
    cur.execute("select bugs_activity.bug_id,profiles.login_name,bugs_activity.bug_when,fielddefs.description,bugs_activity.removed,bugs_activity.added from bugs_activity,fielddefs,profiles where profiles.userid=bugs_activity.who and bugs_activity.fieldid=fielddefs.id;")
    rs = cur.fetchall()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error"
    sys.exit()

bug_act = {}

for n in rs:
    bid = str(n[0])
    if not bug_act.has_key(bid):
        bug_act[bid] = []
    idx = str(len(bug_act[bid])/5)
    nn = []
    for m in n:
        fv = str(m).replace("\n\r","NEWLINE")
        fv = fv.replace("\r\n","NEWLINE")
        fv = fv.replace("\n","NEWLINE")
        fv = fv.replace("\r","NEWLINE")
        fv = fv.replace(";","SEMICOLON")
        fv = fv.replace("=","EQUAL")
        nn.append(fv)
    bug_act[bid].append(idx+":0="+nn[1])
    bug_act[bid].append(idx+":1="+nn[2])
    bug_act[bid].append(idx+":2="+nn[3])
    bug_act[bid].append(idx+":3="+nn[4])
    bug_act[bid].append(idx+":4="+nn[5])

outputfile = sys.argv[1]

f_out = open(outputfile,"w")

count = 0
for k,v in bug_act.iteritems():
    f_out.write(str(count)+";"+k+";"+";".join(v)+"\n")
    count += 1

f_out.close()
