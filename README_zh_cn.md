**Language :** [![English](https://jaywcjlove.github.io/sb/lang/english.svg)](https://github.com/DIYer22/boxx) [![Chinese](https://jaywcjlove.github.io/sb/lang/chinese.svg)](./README_zh_cn.md)
  
<br>
<h1 align="center">Box-X</h1>


<div align="center">
  <strong>Hack Python and Vision</strong>
</div>

<div align="center">
  <strong><code>Box-X</code></strong> 是一个旨在提高 Python 代码开发和调试效率的工具库，尤其是在  <strong>科学计算</strong> 和 <strong>计算机视觉</strong> 领域.
</div>

<br/>

<div align="center">
  <!-- Build Status -->
  <a href="https://travis-ci.org/DIYer22/boxx">
    <img src="https://img.shields.io/badge/build-passing-brightgreen.svg" alt="build">
  </a>
  
  <!-- pyversions -->
  <a href="https://pypi.python.org/pypi/boxx">
    <img src="https://img.shields.io/pypi/pyversions/boxx.svg" alt="pyversions">
  </a>
  <!-- platform -->
  <a href="">
    <img src="https://img.shields.io/badge/platform-linux%20%7C%20osx%20%7C%20win-blue.svg" alt="platform">
  </a>
  <!-- License -->
  <!--<a href="https://www.github.com/DIYer22/boxx">
    <img src="https://img.shields.io/pypi/l/boxx.svg" alt="LICENSE">
  </a>-->
  <!-- Version -->
  <a href="https://pypi.python.org/pypi/boxx">
    <img src="https://img.shields.io/pypi/v/boxx.svg" alt="PyPI">
  </a>
  <!-- Binder -->
  <a href="https://mybinder.org/v2/gh/DIYer22/boxx-ipynb/master?filepath=tutorial_for_boxx.ipynb">
    <img src="https://mybinder.org/badge.svg" alt="Binder">
  </a>
</div>


<div align="center">

 ### [简介](#一-简介) | [安装](#二-安装) | [示例](#三-示例) | [教程](#四-教程) | [致谢](#五-致谢)
</div>


<div align="center">
  <sub>Code with <span style="color:red">❤︎</span> by
  <a href="https://github.com/DIYer22">DIYer22</a> and
  <a href="https://github.com/DIYer22/boxx/graphs/contributors">
    contributors
  </a>
  </sub>
</div>

<br/>


---
## 一. 简介

**`Box-X`** 的目标是提高 Python 代码的开发和调试效率.    

特别是在 **科学计算** 和 **计算机视觉** 领域有着良好的支持. 

因此，工具库的所有功能 会根据该功能是否通用 而被分为了两个部分:    
 * **通用功能**: 这些功能（工具）可以在任何 Python 开发中发挥作用

 * **科学计算和计算机视觉功能**: 这些功能（工具）主要用于科学计算和计算机视觉领域

 
**`boxx`** 兼容 **`Python 2/3`** 及 **`Linux | macOS | Windows`** 操作系统, 支持 纯 Python、IPython、Spyder、Jupyer Notebook 等 Python 运行环境

P.S. 如果对计算机视觉感兴趣，这里有一个详尽的关于 **`boxx`** 的介绍：

 > [开发, 调试计算机视觉代码有哪些技巧？ ![](http://wangchujiang.com/sb/ico/zhihu.svg)](https://www.zhihu.com/question/280472255/answer/422068650)

## 二. 安装

```
pip install boxx
```

## 三. 示例

示例也被分为了两个部分

左侧为 **通用功能**，右侧为 **科学计算和计算机视觉功能**。

💡 **Note:** 
 * *点击图片可以查看大图，如果是 GIF，GIF还会从头开始播放*
 * *下面的内容是为桌面浏览器排版的内容，如通过手机浏览器查看，推荐访问[**=> 静态的 Tutorial**](https://nbviewer.jupyter.org/github/DIYer22/boxx-ipynb/blob/master/tutorial_for_boxx.ipynb)*

<table  style="">
  <tr>
    <td valign="top" width="50%">
    
  ### 通用功能
  <hr></hr>
        
  #### ▶  `p/x` 是更方便 `print(x)` 的方式   
  `p/x` 在执行 `print(x)` 后会返回 `x`
  [![click to restart GIF and see more clearer GIF](./other/img/p.png)](./other/img/p.png)     
  💡 **Note:** `p/x` 能够方便的打印表达式中的值.
        <hr></hr>
        <br><br>
        <br><br>
        
  #### ▶  `g.name = x` 和 `g.name/x` 可以把函数内的变量传送到 Python interactive console 中
  [![click to restart GIF and see more clearer GIF](./other/gif/g.gif) ](./other/gif/g.gif)    
  💡 **Note:** 
 * `gg` 的意思是 `to Global and log`， 和 `g` 的用法一样, 但 `gg` 会在传输的同时打印变量. 
  * 需要注意， 如果之前在终端中存在一样的变量名称，则变量的值会被新值覆盖.
        <hr></hr>
        <br><br>
        <br><br>
        
  #### ▶ `g()` 一次性传输函数内的所有变量到 Python interactive console 中
  [![click to restart GIF and see more clearer GIF](./other/gif/g_call.gif) ](./other/gif/g_call.gif)    
  💡 **Note:** `g()` 在 Debug 时非常有用. `import boxx.g` 是 `g()` 的便携版本，避免了 `from boxx import g;g()`(`import boxx.gg` 同理)
        <hr></hr>
        <br><br>
        <br><br>
        
  #### ▶ `with p`, `with g`, `with gg` 分别是 `p`, `g`, `gg` 的多变量版本，只需把变量放入 `with` 结构中即可
  使得对应操作只作用于感兴趣的几个变量
  [![click to restart GIF and see more clearer GIF](./other/gif/w.gif) ](./other/gif/w.gif)    
  💡 **Note:** 
  * `with p`, `with g`, `with gg` 只作用于在 `with` 结构中进行赋值操作的变量. 
  * 如果变量名在 `with` 前存在于 `locals()` 中, 同时 `id(变量)` 没有变化 , `with` 结构可能无法检测到该变量. 
        <hr></hr>
        
    </td>
    <td valign="top">
    
  ### 科学计算和计算机视觉功能

  本部分通过用例来介绍几个在 **科学计算** 和 **计算机视觉** 领域内的一些实用工具 . 几乎所有的工具(函数) 都支持 `numpy`, `torch.tensor`, `mxnet.ndarray`, `PIL.Image` 等类似多维数组的数据类型    
  
  💡 **Note:** 若通过 `ssh` 在远程服务器上执行代码， 建议在 `ssh` 加上 `-X` 参数，使可视化的 `plt` 图表能传输到本地显示，即 `ssh -X user@host`。
        <hr></hr>

  #### ▶ 用 `loga` 来可视化多维数组   
  `loga` 是 "log array" 的缩写, `loga` 能展示多维数组的许多属性.
  [![click to restart GIF and see more clearer GIF](./other/gif/loga.gif)](./other/gif/loga.gif)     
  💡 **Note:** `loga` 支持 `numpy`, `torch.tensor`, `mxnet.ndarray`, `PIL.Image` .etc 
        <hr></hr>
        <br><br>
        <br><br>

  #### ▶ 用 `show` 来方便地可视化图像，哪怕图像隐藏于复杂的结构中
  `show` 能够从复杂结构中找出所有类型的图像 并可视化他们。它甚至支持从 torch 的 Dataloader 中展示一个 batch 的图像
  [![click to restart GIF and see more clearer GIF](./other/gif/show.gif)](./other/gif/show.gif)    
  💡 **Note:** 如果有函数作为 `show` 的参数(比如 `torgb`)，则会对所有 `numpy` 执行此函数后再可视化。
        <hr></hr>
        <br><br>
        <br><br>

  #### ▶ 使用 `tree` 来可视化复杂结构
  如同 shell 中的 `tree` 命令， `boxx.tree` 可以直观地展示复杂结构.
  [![click to restart GIF and see more clearer GIF](./other/gif/tree.gif)](./other/gif/tree.gif)    
  💡 **Note:** `tree` 支持的数据有 `list`, `tuple`, `dict`, `numpy`, `torch.tensor/Dataset/DataLoader`, `mxnet.ndarray`, `PIL.Image`.etc
        <hr></hr>
    </td>
  </tr>
</table> 


<table  style="">
  <tr>
    <td valign="top" width="50%">
    
  #### ▶ `boxx` 调试工具矩阵
| 变量个数 \ 操作 | print | transport | print & transport |
| :---- | :---- | :---- | :---- |
| 单变量 | `p/x` | `g.name/x` | `gg.name/x`|
| 多变量 | `with p:` | `with g:` | `with gg:` |
| `locals()`| `p()` | `g()` | `gg()` |
| `locals()`\_2 | `import boxx.p` | `import boxx.g` | `import boxx.gg` |    

  💡 **Note:**   
  * **transport** 操作是指 把函数内的变量传送到 Python interactive console 中
  * **`locals()`** 指作 用于函数或 module 内的所有变量
  * **`locals()`\_2**: 当 `boxx` 未导入时， `import boxx.{操作}` 能等价于 `from boxx import {操作};{操作}()`
        <br><br>
        <hr></hr>
        
  ####  ▶ 使用 `what` 来了解任何对象
  [![click to restart GIF and see more clearer GIF](./other/img/what.png) ](./other/img/what.png)    
  💡 **Note:** `what(x)` 通过打印 `x` 自己及`x` 的 **文档**, **父类继承关系**, **内部结构** 及 **所有属性** 来全面了解 `x`. 是 `help(x)` 的补充.
        <br><br>
        <hr></hr>
        
  #### ▶ `timeit` 是一个方便的计时工具
  [![click to restart GIF and see more clearer GIF](./other/img/timeit.png) ](./other/img/timeit.png)    
  💡 **Note:** `timeit` 会对在 `with` 结构下的代码块进行计时，并用蓝色来打印出运行的时间.
        <br><br>
        <hr></hr>
        
  #### ▶ `mapmp` 是多进程版本的 `map`
  `mapmp` 是 "MAP for Multi Process"的缩写, 和 `map` 有着一样的用法，但会用多进程加速.    
  [![click to restart GIF and see more clearer GIF](./other/gif/mapmp.gif) ](./other/gif/mapmp.gif)    
  💡 **Note:** 
  * `mapmp` 的 **pool** 参数来控制进程数目，默认为 CPU 线程数目.
  * 在多进程程序中, 打印进度往往非常麻烦. `mapmp` 的 **printfreq** 参数能解决这个问题.
  * 如同 `map` 一样，`mapmp` 支持将多个参数输入函数，如`mapmp(add, list_1, list_2)`
  * 在 Python 中，多进程代码最好在 `__name__ == '__main__'` 环境中运行.
  * 如果加速 `numpy` 程序，请注意 [在 MKL 版本的 `numpy` 中，多进程会更慢](https://blog.skyaid-service.org/2017/08/15/numpy_performance/), 可以运行 `boxx.testNumpyMultiprocessing()` 来测试当前环境对多进程 `numpy` 的友好程度
        <br><br>
        <hr></hr>
        
  #### ▶ 用 `heatmap` 来展示代码的运行时间热力图
  [![click to restart GIF and see more clearer GIF](./other/img/heatmap.png) ](./other/img/heatmap.png)    
  💡 **Note:** `heatmap` 也支持字符串形式的 Python 代码.
        <br><br>
        <hr></hr>
        
  #### ▶ `performance` 可以统计函数调用并通过[火焰图](http://www.ruanyifeng.com/blog/2017/09/flame-graph.html)可视化代码性能
  [![click to restart GIF and see more clearer GIF](./other/gif/performance.gif) ](./other/gif/performance.gif)    
  💡 **Note:** `performance` 也支持字符串形式的 Python 代码.
    </td>
  </tr>
</table>

---

## 四. 教程

**`boxx`** 的教程是一个 Jupyter Notebook 文件，可以边看边运行.

有三种方式来查看/运行此教程

#### 方式一：可执行的在线 Notebook: 
Notebook 文件被运行在 [Binder](https://mybinder.org) 上。[Binder](https://mybinder.org) 提供了可执行、可交互的在线 Notebook 环境.    
也就是说，无需下载和运行任何代码，只需浏览器打开链接，就可以在线执行 Notebook 教程中的代码块。  
* [**=> 可直接执行的在线教程**](https://mybinder.org/v2/gh/DIYer22/boxx-ipynb/master?filepath=tutorial_for_boxx.ipynb)

#### 方式二：下载并在本地打开教程:

```bash
git clone https://github.com/DIYer22/boxx
cd boxx/
python setup.py install
jupyter notebook
```
在 Jupyter Notebook 中打开 `./tutorial_for_boxx.ipynb` 即可.

#### 方式三：静态的 Notebook:
 只能看 不能交互的 Notebook.
* [**=> 静态的 Tutorial**](https://nbviewer.jupyter.org/github/DIYer22/boxx-ipynb/blob/master/tutorial_for_boxx.ipynb)


## 五. 致谢
 * 特别感谢徐晓栋、吴国栋、范浩强和熊鹏飞对 `boxx` 提出的建议
 * I develop **`boxx`** in [Spyder IDE](https://github.com/spyder-ide/spyder), [Spyder](https://github.com/spyder-ide/spyder) is a awesome Scientific Python Development Environment with Powerful [**Qt-IPython**](https://github.com/jupyter/qtconsole)
 * `performance` is supported by [SnakeViz](https://jiffyclub.github.io/snakeviz/)
 * `heatmap` is supported by [csurfer/pyheat](https://github.com/csurfer/pyheat)



