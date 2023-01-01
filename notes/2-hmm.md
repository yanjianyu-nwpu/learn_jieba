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

这里就是核心hmm的实现，首先是用了viterbi算法

```python
def __cut(sentence):
    global emit_P
  	# 这里
    prob, pos_list = viterbi(sentence, 'BMES', start_P, trans_P, emit_P)
    begin, nexti = 0, 0
    # print pos_list, sentence
    for i, char in enumerate(sentence):
        pos = pos_list[i]
        if pos == 'B':
            begin = i
        elif pos == 'E':
            yield sentence[begin:i + 1]
            nexti = i + 1
        elif pos == 'S':
            yield char
            nexti = i + 1
    if nexti < len(sentence):
        yield sentence[nexti:]
```



这里先解释这几个字母的意思

- HMM的典型模型是一个五元组:
  - StatusSet: 状态值集合
    ObservedSet: 观察值集合
    TransProbMatrix: 转移概率矩阵
    EmitProbMatrix: 发射概率矩阵
    InitStatus: 初始状态分布

- 所以状态值的集合可以有四个 :
  - 为(B, M, E, S): {B:begin, M:middle, E:end, S:single}。分别代表每个状态代表的是该字在词语中的位置，B代表该字是词语中的起始字，M代表是词语中的中间字，E代表是词语中的结束字，S则代表是单字成词。



## 2.3 Viterbi

这里输入的发射矩阵和转移矩阵是训练出来的矩阵：以下是 start_P trans_P 

```
{'B': -0.26268660809250016, 'E': -3.14e+100, 'M': -3.14e+100, 'S': -1.4652633398537678}
{'B': {'E': -0.51082562376599, 'M': -0.916290731874155}, 'E': {'B': -0.5897149736854513, 'S': -0.8085250474669937}, 'M': {'E': -0.33344856811948514, 'M': -1.2603623820268226}, 'S': {'B': -0.7211965654669841, 'S': -0.6658631448798212}}
```

然后这里的emit_P也是输入的 对那些单字开始的一概率



源码

```python
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]  # tabular
    path = {}
    for y in states:  # init
        V[0][y] = start_p[y] + emit_p[y].get(obs[0], MIN_FLOAT)
        path[y] = [y]
    for t in xrange(1, len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            em_p = emit_p[y].get(obs[t], MIN_FLOAT)
            (prob, state) = max(
                [(V[t - 1][y0] + trans_p[y0].get(y, MIN_FLOAT) + em_p, y0) for y0 in PrevStatus[y]])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath
	# 这里的path是最后一个字符，如果是某个状态，之前字符的角色
    # 因为最后一个字符只能是 e或者 s ，所以会判断 ，选一个结果
    (prob, state) = max((V[len(obs) - 1][y], y) for y in 'ES')

    return (prob, path[state])
```

大概情况如下就是上

很有意思的是，这个状态转方程有个对应矩阵

```
PrevStatus = {
    'B': 'ES',
    'M': 'MB',
    'S': 'SE',
    'E': 'BM'
}
```

那么可以看出 t+1的 ’B‘ 由t的’E‘ 和 ’S‘ 决定，并且是取大值；



比方说上述的

我分威

```
[{'B': -5.825987215274368, 'M': -3.14e+100, 'E': -3.14e+100, 'S': -5.977093751850913}, {'B': -12.352122900609341, 'M': -12.980913212539502, 'E': -12.15332204142366, 'S': -13.404775375712308}, {'B': -20.640760367860103, 'M': -21.278112715046454, 'E': -21.058693479833885, 'S': -22.62057916170157}]
{'B': ['B', 'E', 'B'], 'M': ['S', 'B', 'M'], 'E': ['S', 'B', 'E'], 'S': ['B', 'E', 'S']}
-21.058693479833885 ['S', 'B', 'E']
```

上面的 是 V path 和返回的结果  status是E

这里的path是记录如果 t+1 字符是某个状态，最后一个字符只能 E或者S，然后算出是E和S中概率大的，然后从path中找到前t个 字符的角色

