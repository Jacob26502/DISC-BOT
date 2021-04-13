import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "emojilist.csv"
abs_file_path = os.path.join(script_dir, rel_path)
def elist():
    file=open(abs_file_path, mode="r", encoding='utf-8').read().split("\n")
    ls=[]
    for c,x in enumerate(file):
        if c==0:
            continue
        else:
            ls.append(x.split(","))
    del ls[-1]
    return ls
