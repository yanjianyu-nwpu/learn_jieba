# Install

## 0 jiba	

用的是windows系统，python 3.10 ；下载github zip仓库。安装命令：

```python
python step_up.py install 
```

## 1 paddlepaddle-tiny

​	参考https://blog.csdn.net/lyz19961221/article/details/127650788

​	上pypi https://pypi.org/project/paddlepaddle-tiny/#files 下载whl文件

```
pip debug --verbose
```

​	看有平台支持哪些版本，最后看到 需要abi3的接口，把cp73-cp37m.whl文件改成 cp37-abi3 

​	然后安装

```
pip install .\paddlepaddle_tiny-1.6.1-cp37-abi3-win_amd64.whl  -i https://pypi.tuna.tsinghua.edu.cn/simple
```

需要安装 paddlepaddle 和 protobuf

```
pip install paddlepaddle==2.3.2 -i https://mirror.baidu.com/pypi/simple
```

```
pip install protobuf==3.20.0 -i https://mirror.baidu.com/pypi/simple
```

启动的时候需要使用 

```
import jieba
import paddle
paddle.enable_static()
jieba.enable_paddle()
```

