def elist():
    file=open("emojilist.csv", mode="r", encoding='utf-8').read().split("\n")
    ls=[]
    for c,x in enumerate(file):
        if c==0:
            continue
        else:
            ls.append(x.split(","))
    del ls[-1]
    return ls
