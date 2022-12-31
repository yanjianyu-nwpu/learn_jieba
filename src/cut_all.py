import jieba


seg_list = jieba.cut("我来到北京清华大学jjkewe", cut_all=True,HMM=False,use_paddle=False)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式
