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



结果就是记录所有可能的结果

比如是 特斯拉model3

那么存的结果是 {0:[3,9],3:[9]} 因为 特斯拉是一个词，特斯拉model3是一个词;记录每个ind到后面可能的词



## 0.1 精准模式 cut_all

 函数第一步是获取dag结果

query是 "我来到北京清华大学"

  ```
{0: [0], 1: [1, 2], 2: [2], 3: [3, 4], 4: [4], 5: [5, 6, 8], 6: [6, 7], 7: [7, 8], 8: [8]}
  ```

  这里可以看到 主要词有以下几个 来 来到 北京 清华 清华大学  华大  大学 



最后的结果是

```
我/ 来到/ 北京/ 清华/ 清华大学/ 华大/ 大学

```

  这里的代码比较复杂

```python
for k, L in iteritems(dag):
            if eng_scan == 1 and not re_eng.match(sentence[k]):
                eng_scan = 0
                yield eng_buf
            if len(L) == 1 and k > old_j:
                word = sentence[k:L[0] + 1]
                if re_eng.match(word):
                    if eng_scan == 0:
                        eng_scan = 1
                        eng_buf = word
                    else:
                        eng_buf += word
                if eng_scan == 0:
                    yield word
                old_j = L[0]
            else:
                for j in L:
                    if j > k:
                        yield sentence[k:j + 1]
                        old_j = j
        if eng_scan == 1:
            yield eng_buf

```

​                                                         

​                                                     

这里的循环比较复杂

这里re_eng是英文的匹配方式                 

```
re_eng = re.compile('[a-zA-Z0-9]', re.U)
```

​                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

这里是匹配每个英文参数



第一个if 就是如果匹配上了，并且这个地方不是英文匹配成功



第二个 if 如果这个起点只有一个词，且比原来起点靠后，可以进入

​			如果是是英文，设置 eng_scan并加上 这个char

​			如果不是英文，那么返回了

else 其他情况，会全部匹配



综上所数 __cut_all_ 精准模式就是会匹配所有的词，可能会有冗余；但是英文就是连着就ok





## 1 initialize 

### 1.1 参数

```python
def initialize(self, dictionary=None):
```

​	这里得到词典位置

​	这个函数主要就是 获取 词典  默认磁电式 dict.txt 文件

​	字典文件 分为三列 词  词频   词性



