# 4 cut_all

## 0  __get_DAG

```python
def get_DAG(self, sentence):
        self.check_initialized()
        DAG = {}
        N = len(sentence)
        for k in xrange(N):
            tmplist = []
            i = k
            frag = sentence[k]
            while i < N and frag in self.FREQ:
                if self.FREQ[frag]:
                    tmplist.append(i)
                i += 1
                frag = sentence[k:i + 1]
            if not tmplist:
                tmplist.append(k)
            DAG[k] = tmplist
        return DAG
```

这里输入是sentence

这里frag 就是一个一个的字，比如 “特斯拉” 结果就是  特 斯 拉

self.FREQ是词典

如果在词典里面在里面  



这里的流程如下：

​	双重循环，外循环 算是起点，然后看后续的序列能否匹配到词；如果匹配 放到tmplist，最后dag【k】 设置为所有的可能 





## 1 initialize 

### 1.1 参数

```python
def initialize(self, dictionary=None):
```

​	这里得到词典位置

​	这个函数主要就是 获取 词典  默认磁电式 dict.txt 文件

​	字典文件 分为三列 词  词频   词性



