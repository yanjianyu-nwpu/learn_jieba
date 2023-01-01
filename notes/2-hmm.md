# 4 HMM切分

## 1 INTRODUTION

​	本文主要是研究 

```python
_cut_DAG_NO_HMM	
```

```python
def __cut_DAG(self, sentence):
        DAG = self.get_DAG(sentence)
        print(DAG)
        route = {}
        self.calc(sentence, DAG, route)
        x = 0
        buf = ''
        N = len(sentence)
        while x < N:
            y = route[x][1] + 1
            l_word = sentence[x:y]
            if y - x == 1:
                buf += l_word
            else:
                if buf:
                    if len(buf) == 1:
                        yield buf
                        buf = ''
                    else:
                        if not self.FREQ.get(buf):
                            recognized = finalseg.cut(buf)
                            for t in recognized:
                                yield t
                        else:
                            for elem in buf:
                                yield elem
                        buf = ''
                yield l_word
            x = y

        if buf:
            if len(buf) == 1:
                yield buf
            elif not self.FREQ.get(buf):
                recognized = finalseg.cut(buf)
                for t in recognized:
                    yield t
            else:
                for elem in buf:
                    yield elem

```



该函数 结果是

```
{0: [0], 1: [1, 2], 2: [2], 3: [3, 4], 4: [4], 5: [5, 6, 8], 6: [6, 7], 7: [7, 8], 8: [8]}
```

## 1.1 Calc

这里的calc 函数

```python
def calc(self, sentence, DAG, route):
        N = len(sentence)
        route[N] = (0, 0)
        logtotal = log(self.total)
        for idx in xrange(N - 1, -1, -1):
            route[idx] = max((log(self.FREQ.get(sentence[idx:x + 1]) or 1) -
                              logtotal + route[x + 1][0], x) for [idx]) 
```

```
 我/ 来到/ 北京/ 清华大学/ jjkewe
```

这里self.total是一个固定值60101967

然后是字典的词总数 

然后是倒序的遍历 

 计算方式如下：

- 句子长度  为N

- 先赋值一个  route N:{0,0}

- 后续开始遍历 idx 倒遍历啊

  - 里面小循环 x 是从idx 开始的可能的词              ，比如 清华/清华大学这样

  - 首先计算log(self.FREQ.get(sentence[idx:x + 1]) or 1) 这里 获取这个词的 频率，如果没有就是1 ；

  - 然后计算 

    - ```python
      route[idx] = max((log(self.FREQ.get(sentence[idx:x + 1]) or 1) -
                                    logtotal + route[x + 1][0], x) for x in DAG[idx]
                    )
      ```

  - 这里的方法是 根据词频和后续接上的结果的最优解

- 例子解释

  - 这里       route 9：（0，0） 然后 “学的频率是” 17482 所以计算出的 8：的结果是 log（17482）- log（601011967） + 0 
  - 这里 idx对应一个元组，一个是分数，一个是结束词的位置

- 整个例子结果是

  - {9: (0, 0), 8: (-8.142626068614787, 8), 7: (-8.006816355818659, 8), 6: (-17.53722513662092, 6), 5: (-11.085007904198626, 8), 4: 
    (-20.20431518448597, 4), 3: (-18.548194315526874, 4), 2: (-24.22732015246924, 2), 1: (-27.379629658355885, 2), 0: (-32.587853155857076, 0)}

## 1.2 循环

循环里面，主要解决的哪些单个字的问题 比如 我分未 这种

例子

我分威聚合物覅我风氛围

dag结果

{0: [0], 1: [1], 2: [2], 3: [3, 4, 5], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8], 9: [9, 10], 10: [10]}

calc结果

{11: (0, 0), 10: (-9.615006607454605, 10), 9: (-11.37631185674156, 10), 8: (-19.964642455463924, 8), 7: (-25.172865952965118, 7), 6: (-43.08441908072034, 6), 5: (-51.93413184481782, 5), 4: (-60.691597542147655, 4), 3: (-55.43145180115286, 5), 2: (-65.78657695946782, 2), 1: (-73.24478852395345, 1), 0: (-78.45301202145464, 0)}



```python
def __cut_DAG(self, sentence):
        DAG = self.get_DAG(sentence)
        print(DAG)
        route = {}
        self.calc(sentence, DAG, route)
        x = 0
        buf = ''
        N = len(sentence)
        while x < N:
            y = route[x][1] + 1
            l_word = sentence[x:y]
            # 如果是一个字会记下来
            if y - x == 1:
                
                buf += l_word
            else:
                if buf:
                    # 如果是最后一个字直接返回
                    if len(buf) == 1:
                        yield buf
                        buf = ''
                    else:
                        if not self.FREQ.get(buf):
                            recognized = finalseg.cut(buf)
                            for t in recognized:
                                yield t
                        # 如果是词典里面的字直接返回
                        else:
                            for elem in buf:
                                yield elem
                        buf = ''
                yield l_word
            x = y

        if buf:
            if len(buf) == 1:
                yield buf
            elif not self.FREQ.get(buf):
                recognized = finalseg.cut(buf)
                for t in recognized:
                    yield t
            else:
                for elem in buf:
                    yield elem

```



这里就是 如果是词典里面的词 直接返回；一个一个的词会记下来走hmm 

也就是 这个finalseg。cut



# 2 HMM实现

## 2.1 finalset.cut

代码比较简单

```python
def cut(sentence):
    sentence = strdecode(sentence)
    blocks = re_han.split(sentence)
    for blk in blocks:
        if re_han.match(blk):
            for word in __cut(blk):
                if word not in Force_Split_Words:
                    yield word
                else:
                    for c in word:
                        yield c
        else:
            tmp = re_skip.split(blk)
            for x in tmp:
                if x:
                    yield x
```

这里比较简单就把句子编码，把汉字挑出来



## 2.2 finalset.__cut

这里

