import sys,MySQLdb,time,string,re,os

fields = ["bug_id","assigned_to","bug_file_loc","bug_severity","bug_status","creation_ts","delta_ts","short_desc","op_sys","priority","rep_platform",
"reporter","version","resolution","target_milestone","qa_contact","status_whiteboard","votes","lastdiffed","everconfirmed","reporter_accessible",
"cclist_accessible","alias","estimated_time","remaining_time","product_id","component_id","deadline","cf_blocking_fennec","cf_blocking_191","cf_status_191",
"cf_status_192","cf_blocking_20","cf_blocking_thunderbird30","cf_status_thunderbird30","cf_blocking_192","cf_blocking_thunderbird31","cf_status_thunderbird31",
"cf_status_20","cf_status_seamonkey21","cf_blocking_seamonkey21","cf_blocking_thunderbird32","cf_status_thunderbird32","cf_blocking_thunderbird33","cf_status_thunderbird33",
"cf_blocking_fx", "cf_tracking_firefox5", "cf_status_firefox5" ,"cf_tracking_firefox6","cf_colo_site","cf_tracking_firefox7","cf_status_firefox6","cf_status_firefox7",
"cf_crash_signature","cf_tracking_thunderbird6","cf_tracking_thunderbird7","cf_status_thunderbird6","cf_status_thunderbird7","cf_tracking_seamonkey22",
"cf_tracking_seamonkey23","cf_tracking_seamonkey24","cf_tracking_firefox8","cf_status_firefox8","cf_tracking_seamonkey25","cf_status_seamonkey22",
"cf_status_seamonkey23","cf_status_seamonkey24","cf_status_seamonkey25","cf_tracking_thunderbird8","cf_status_thunderbird8","cf_tracking_firefox9",
"cf_status_firefox9","cf_tracking_seamonkey26","cf_status_seamonkey26","cf_tracking_thunderbird9","cf_status_thunderbird9","cf_office","cf_due_date",
"cf_tracking_firefox10","cf_status_firefox10","cf_tracking_thunderbird10","cf_status_thunderbird10","cf_tracking_seamonkey27","cf_status_seamonkey27",
"cf_tracking_firefox11","cf_status_firefox11","cf_tracking_thunderbird11","cf_status_thunderbird11","cf_tracking_seamonkey28","cf_status_seamonkey28",
"cf_tracking_firefox12","cf_status_firefox12","cf_tracking_thunderbird12","cf_status_thunderbird12","cf_tracking_seamonkey29","cf_status_seamonkey29",
"cf_tracking_esr10","cf_status_esr10","cf_tracking_firefox13","cf_status_firefox13","cf_tracking_thunderbird13","cf_status_thunderbird13","cf_tracking_seamonkey210",
"cf_status_seamonkey210","cf_tracking_thunderbird_esr10","cf_status_thunderbird_esr10","cf_blocking_fennec10","cf_tracking_firefox14","cf_status_firefox14",
"cf_tracking_thunderbird14","cf_status_thunderbird14","cf_tracking_seamonkey211","cf_status_seamonkey211","cf_last_resolved","cf_blocking_kilimanjaro",
"cf_tracking_firefox15","cf_status_firefox15","cf_tracking_thunderbird15","cf_status_thunderbird15","cf_tracking_seamonkey212","cf_status_seamonkey212",
"cf_blocking_basecamp","cf_tracking_firefox16","cf_status_firefox16","cf_tracking_thunderbird16","cf_status_thunderbird16","cf_tracking_seamonkey213",
"cf_status_seamonkey213","cf_tracking_firefox17","cf_status_firefox17","cf_tracking_thunderbird17","cf_status_thunderbird17","cf_tracking_seamonkey214",
"cf_status_seamonkey214","cf_tracking_firefox18","cf_status_firefox18","cf_tracking_thunderbird18","cf_status_thunderbird18","cf_tracking_seamonkey215",
"cf_status_seamonkey215","cf_tracking_firefox19","cf_status_firefox19","cf_tracking_thunderbird19","cf_status_thunderbird19","cf_tracking_firefox_esr17",
"cf_status_firefox_esr17","cf_tracking_seamonkey216","cf_status_seamonkey216","cf_shadow_bug","cf_tracking_firefox20","cf_status_firefox20",
"cf_tracking_thunderbird20","cf_status_thunderbird20","cf_tracking_thunderbird_esr17","cf_status_thunderbird_esr17","cf_tracking_seamonkey217",
"cf_status_seamonkey217","cf_status_b2g18","cf_tracking_b2g18","cf_blocking_b2g"]

fieldslen = len(fields)

qfields = []
for n in fields:
    qfields.append("bugs."+n)
qfields[5] = "UNIX_TIMESTAMP(bugs.creation_ts)"
qfields[6] = "UNIX_TIMESTAMP(bugs.delta_ts)"
qfields[18] = "UNIX_TIMESTAMP(bugs.lastdiffed)"
idx = qfields.index("bugs.cf_last_resolved")
qfields[idx] = "UNIX_TIMESTAMP(bugs.cf_last_resolved)"
ids = qfields.index("bugs.product_id")
qfields[idx] = "products.name"
ids = qfields.index("bugs.component_id")
qfields[idx] = "components.name"


fields_out = []
for n in fields:
    fields_out.append(n)
ids = fields_out.index("product_id")
fields_out[idx] = "product"
ids = fields_out.index("component_id")
fields_out[idx] = "component"

querystr = ",".join(qfields)

issues2013 = dict()

def getname(uid):
    rs = ()
    try:
        conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="mozilla",port=3306)
        cur = conn.cursor()
        cur.execute("select login_name,realname from profiles where userid="+uid+";")
        rs = cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error"
        sys.exit()
    login_name = rs[0][0]
    login_name = login_name.replace(";","SEMICOLON")
    login_name = login_name.replace("=","EQUAL")        
    realname = rs[0][1]
    realname = realname.replace(";","SEMICOLON")
    realname = realname.replace("=","EQUAL")
    return [login_name,realname]

rs = ()

try:
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="mozilla",port=3306)
    cur = conn.cursor()
    cur.execute("select "+querystr+" from bugs,components,products where bugs.product_id=products.id and component_id=components.id;")
    rs = cur.fetchall()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error"
    sys.exit()

print("s1")

for n in rs:
    bid = str(n[0])
    issues2013[bid] = [1,1]
    for i in range(1,fieldslen):
        if str(n[i])=="None" or str(n[i])=="" or str(n[i])=="---":
            continue
        if fields[i]=="reporter":
            names = getname(str(n[i]))
            issues2013[bid].append("reporter="+names[0])
            issues2013[bid].append("reporter_name="+names[1])
        elif fields[i]=="assigned_to":
            names = getname(str(n[i]))
            issues2013[bid].append("assigned_to="+names[0])
            issues2013[bid].append("assigned_to_name="+names[1])
        elif fields[i]=="qa_contact":
            names = getname(str(n[i]))
            issues2013[bid].append("qa_contact="+names[0])
            issues2013[bid].append("qa_contact_name="+names[1])
        else:
            fv = str(n[i]).replace("\n\r","NEWLINE")
            fv = str(n[i]).replace("\n\r","NEWLINE")
            fv = fv.replace("\r\n","NEWLINE")
            fv = fv.replace("\n","NEWLINE")
            fv = fv.replace("\r","NEWLINE")
            fv = fv.replace(";","SEMICOLON")
            fv = fv.replace("=","EQUAL")
            issues2013[bid].append(fields_out[i]+"="+fv)

print("s2")

try:
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="mozilla",port=3306)
    cur = conn.cursor()
    cur.execute("select cc.bug_id,profiles.login_name from cc,profiles where profiles.userid=cc.who;")
    rs = cur.fetchall()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error"
    sys.exit()

print("s3")

bug_cc = {}

for n in rs:
    bid = str(n[0])
    if not bug_cc.has_key(bid):
        bug_cc[bid] = []
    fv = str(n[1]).replace("\n\r","NEWLINE")
    fv = fv.replace("\r\n","NEWLINE")
    fv = fv.replace("\n","NEWLINE")
    fv = fv.replace("\r","NEWLINE")
    fv = fv.replace(";","SEMICOLON")
    fv = fv.replace("=","EQUAL")
    bug_cc[bid].append(fv)

for k,v in bug_cc.iteritems():
    if not issues2013.has_key(k):
        issues2013[k] = [1,1]
    issues2013[k].append("cc="+":".join(v))    

print("s4")

rs = ()

try:
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="mozilla",port=3306)
    cur = conn.cursor()
    cur.execute("select attachments.bug_id,profiles.login_name,attachments.attach_id,attachments.creation_ts,attachments.description,attachments.mimetype from attachments,profiles where attachments.submitter_id=profiles.userid;")
    rs = cur.fetchall()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error"
    sys.exit()

print("s5")

for n in rs:
    bid = str(n[0])
    if not issues2013.has_key(bid):
        issues2013[bid] = [1,1]
    nn = []
    for m in n:
        fv = str(m).replace("\n\r","NEWLINE")
        fv = fv.replace("\r\n","NEWLINE")
        fv = fv.replace("\n","NEWLINE")
        fv = fv.replace("\r","NEWLINE")
        fv = fv.replace(";","SEMICOLON")
        fv = fv.replace("=","EQUAL")
        nn.append(fv)
    issues2013[bid].append("attach:"+str(issues2013[bid][0])+":attacher="+nn[1])
    issues2013[bid].append("attach:"+str(issues2013[bid][0])+":attachid="+nn[2])
    issues2013[bid].append("attach:"+str(issues2013[bid][0])+":date="+nn[3])
    issues2013[bid].append("attach:"+str(issues2013[bid][0])+":desc="+nn[4])
    issues2013[bid].append("attach:"+str(issues2013[bid][0])+":type="+nn[5])
    issues2013[bid][0] += 1

print("s6")

rs = ()

try:
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="mozilla",port=3306)
    cur = conn.cursor()
    cur.execute("select longdescs.bug_id,longdescs.bug_when,longdescs.comment_id,longdescs.thetext,profiles.login_name,profiles.realname from longdescs,profiles where longdescs.who=profiles.userid;")
    rs = cur.fetchall()
    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print "Mysql Error"
    sys.exit()

print("s7")

for n in rs:
    bid = str(n[0])
    if not issues2013.has_key(bid):
        issues2013[bid] = [1,1]
    nn = []
    for m in n:
        fv = str(m).replace("\n\r","NEWLINE")
        fv = fv.replace("\r\n","NEWLINE")
        fv = fv.replace("\n","NEWLINE")
        fv = fv.replace("\r","NEWLINE")
        fv = fv.replace(";","SEMICOLON")
        fv = fv.replace("=","EQUAL")
        nn.append(fv)
    issues2013[bid].append("long:"+str(issues2013[bid][1])+":bug_when="+nn[1])
    issues2013[bid].append("long:"+str(issues2013[bid][1])+":commentid="+nn[2])
    issues2013[bid].append("long:"+str(issues2013[bid][1])+":text="+nn[3])
    issues2013[bid].append("long:"+str(issues2013[bid][1])+":who="+nn[4])
    issues2013[bid].append("long:"+str(issues2013[bid][1])+":who_name="+nn[5])
    issues2013[bid][1] += 1

print("s8")

outputfile = sys.argv[1]

f_out = open(outputfile,"w")

count = 0
for k,v in issues2013.iteritems():
    f_out.write(str(count)+";Bug#="+k+";"+";".join(v[2:])+"\n")
    count += 1

f_out.close()
