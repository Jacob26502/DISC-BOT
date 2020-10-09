def elist():
    file=open("emojilist.csv", mode="r").read().split("\n")
    ls=[]
    for c,x in enumerate(file):
        if c==0:
            continue
        else:
            ls.append(x.split(","))
    return ls
