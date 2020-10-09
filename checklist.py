
file=open("emojilist.csv", mode="r").read().split("\n")
ls=[]
for x in file:
    ls.append(x.split(","))
