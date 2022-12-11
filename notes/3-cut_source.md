# cut

## 1 intro

​	主函数用于切分完整中文句子到分离的word

### 1.1 参数  

- sentence 要被切的句子
- cut_all 模式 如果是true那么是full pattern 全切模式，所有可能结果；false是精准模式，没有冗余的词
- hmm 是否使用hmm 隐马尔可夫链模型

## 2 代码解读

### 2.1 参数/模型/正则表达式准备

- 前置条件判断

  - is_paddle_installed 判断安装情况
  - 把单词编码 strdecode 函数，感觉把切词内容解码；在附件读源码

- 判断是否需要使用paddle 

- re_han

  - ```
    re_han_default = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._%\-]+)", re.U)
    ```

  - 这里re.U是 用unicode 模式去看的问题这里有解释：https://m.656463.com/wenda/pythonremkzdreUsgsmyd_76

  - 应该是所有非 空格和其他的符号没在里面的类似 ^!还有空格 ，会被区分开，可跑src/re_0.py 理解，写了相关例子

    - 会把连续不带特殊字符和空格的词分开，注意一点，特殊字符之间不会分开比如 " ^8*" 会被切分成 " ^" "8" "*"

- re_skip

  - ```
    re_skip_default = re.compile("(\r\n|\s)", re.U)
    ```

  - 这里应该就是匹配空行 \s是指一个空白字符

- 会根据选择函数

  - cut_all 切除全部模式
  - hmm __cut_DAG 函数
  - 默认是 __cut_DAG_NO_HMM

### 2.2 主流程

```python
 blocks = re_han.split(sentence)
 for blk in blocks:
 	if not blk:
        continue
    if re_han.match(blk):
        for word in cut_block(blk):
            yield word
	else:
		tmp = re_skip.split(blk)
		for x in tmp:
			if re_skip.match(x):
            	yield x
            elif not cut_all:
                for xx in x:
                	yield xx
            else:
                yield x
```



- 先使用re_han 将句子切分
- yield 的学习在附件

## 3 其它工具函数/python 基础

### 3.1 strecode

```
def strdecode(sentence):
    if not isinstance(sentence, text_type):
        try:
            sentence = sentence.decode('utf-8')
        except UnicodeDecodeError:
            sentence = sentence.decode('gbk', 'ignore')
    return sentence
```

​	这个isinstance函数是类型判断，是否 list dict之类

### 3.2 yield

​	yield关键词 类似于return，会返回值；

​	但是yield会保存栈上下文，下一次调用函数的时候，直接接着运行。例子 src/yield.py

