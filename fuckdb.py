from tinydb import TinyDB, Query, where
import json
db = TinyDB('db.json')
check = []
list=[]
count=0
for x in db.all():
    print(x['id'])
    if x['id'] not in check:
        check.append(x['id'])
        list.append(x)
        print(x.doc_id)
    else:
        db.remove(doc_ids=[x.doc_id])
        count+=1

print(list)
print(count)
