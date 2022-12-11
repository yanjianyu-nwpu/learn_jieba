import re
'''
    结论：
    会把连续不带特殊字符和空格的词分开

    注意一点，特殊字符之间不会分开比如 " ^8*" 会被切分成 " ^" "8" "*"
'''

re_han_default = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._%\-]+)", re.U)


t1 = "特斯拉9围 殴 + 二+房+*+^ %fhwXeo"
k = re_han_default.split(t1)
print(k)

t2 = "kung单车配合…… 精灵车架 +0909"
k = re_han_default.split(t2)
print(k)
