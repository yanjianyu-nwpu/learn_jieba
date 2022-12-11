import re

re_skip_default = re.compile("(\r\n|\s)", re.U)

t = u"特斯拉\r\n分为\sfew "
print(t)

t = ["1","2","2"]

def gg():
    print("EFE")
    for x in t:
        print(x)
        yield x
print("uiofew")
gg()
print("mnjwf")