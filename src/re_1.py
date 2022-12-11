import re

re_skip_default = re.compile("(\r\n|\s)", re.U)

t = u"特斯拉\r\n分为\sfew "
print(t)
