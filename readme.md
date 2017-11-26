# Python 库 `yllab`


[yllab](https://github.com/DIYer22/yllab)是我自己积累的Python代码库，里面有Debug，图像，机器学习等方面的实用工具

**Demo** : use `Jupyter notebook` run `./Tutorial_of_yllab.ipynb`

**安装所需依赖库** : `pip install -r requirements.txt`

**建议** : 将此文件夹路径`./` 和 `./yl/`加入`PYTHONPATH`系统变量，方便导入调用


### 文件结构
```
yl
├── tool   # 常用Python工具module
│   ├── __init__.py
│   ├── toolFuncation.py
│   ├── toolIo.py
│   ├── toolLog.py
│   ├── toolStructObj.py
│   ├── toolSystem.py
│   └── toolTools.py
├── undetermined.py
├── yldb
│   ├── dbPublicFuncation.py
│   ├── __init__.py
│   ├── yldf.py
│   ├── ylmysql.py
│   └── ylsqlite.py
├── ylimg  # 关于图片处理的module
│   ├── __init__.py
│   ├── showImgsInBrowser.py
│   ├── ylimgTool.py
│   └── ylimgVideoAndGif.py
├── yllab.py
├── ylml   # 关于机器学习的module
│   ├── __init__.py
│   ├── ylmlEvalu.py
│   ├── ylmlTest.py
│   └── ylmlTrain.py
├── ylnp.py # 关于numpy的module
└── ylweb.py

yl-test     # 测试代码
├── imgForTest
├── toolTest.py
├── yldbTest.py
├── ylimgTest.py
└── ylmlTest.py

```
* *Pull request is welcome*
