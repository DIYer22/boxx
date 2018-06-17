

<h1 align="center">Box-X</h1>

<div align="center">
  <strong>:high_brightness:Hack Python and Vision:crescent_moon:</strong>
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
  <a href="https://www.github.com/DIYer22/boxx">
    <img src="https://img.shields.io/pypi/l/boxx.svg" alt="LICENSE">
  </a>
  <!-- Version -->
  <a href="https://pypi.python.org/pypi/boxx">
    <img src="https://img.shields.io/pypi/v/boxx.svg" alt="PyPI">
  </a>
  <!-- Binder -->
  <a href="https://mybinder.org/v2/gh/DIYer22/boxx/master?filepath=tutorial_for_boxx.ipynb">
    <img src="https://mybinder.org/badge.svg" alt="Binder">
  </a>
  <!--  -->
  <a href="">
    <img src="" alt="">
  </a>

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

尤其对 **科学计算** 和 **计算机视觉** 领域有良好的支持. 

因此，工具库的所用功能 会根据该功能是否为通用功能 而被分为了两个部分:    
 * **通用功能**: 这些功能（工具）可以在任何 Python 开发中发挥作用

 * **科学计算和计算机视觉功能**: 这些功能（工具）主要用于科学计算和计算机视觉领域
 
可以去 [=> 例子](#四-例子) 处瞥一眼效果.

P.S. **`boxx`** 同时支持 **`Python 2/3`** 及 **`Linux | macOS | Windows`** 操作系统.

## 二. 安装


#### 源码安装
```bash
git clone https://github.com/DIYer22/boxx
cd boxx/
python setup.py install
```
💡 **Note:** 由于国内的 `pip` 镜像平均有好几天的延迟，强烈推荐从 GitHub 安装.

#### Linux or macOS
```
pip install git+https://github.com/DIYer22/boxx
```

#### Windows
```
pip install boxx -U
```
💡 **Note:** 确保 `pip` 镜像的 `boxx` 版本大于 `0.9`，否则请源码安装。
## 三. 教程

**`boxx`** 的教程是一个 Jupyter Notebook 文件，可以边看边运行，Notebook 文件在 [`./tutorial_for_boxx.ipynb`](./tutorial_for_boxx.ipynb)

有三种方式来查看/运行此教程
#### 方式一：可直接执行的在线 Notebook: 
Notebook 文件被运行在 [Binder](https://mybinder.org) 上。[Binder](https://mybinder.org) 提供了可执行、可交互的在线 Notebook 环境.    
也就是说，无需下载和运行任何代码，只需浏览器打开链接，就可以执行任何 Notebook 中的代码块。  
* [**=> 可直接执行的在线教程**](https://mybinder.org/v2/gh/DIYer22/boxx/master?filepath=tutorial_for_boxx.ipynb)

#### 方式二：下载并在本地打开教程:

```bash
git clone https://github.com/DIYer22/boxx
cd boxx/
python setup.py install
jupyter notebook
```
在 Notebook 中打开 `./tutorial_for_boxx.ipynb` 即可.

#### 方式三：静态的 Notebook:
 只能看 不能交互的 Notebook.
* [**=> 静态的 Tutorial**](https://nbviewer.jupyter.org/github/DIYer22/boxx/blob/master/tutorial_for_boxx.ipynb)


## 四. 例子

Examples are divided into 2 parts too.   

**General Python Tool** on left, **Scientific Computing and Computer Vision Tool** on right.

💡 **Note:** *Click the GIF or image will restart GIF and see more clearer GIF or image*

<table  style="">
  <tr>
    <td valign="top" width="50%">
    
  ### General Python Tool 
  <hr></hr>
        
  #### ▶  `p/x` is better way to `print(x)`    
  `p/x` will `print(x)` and return `x`
  [![click to restart GIF and see more clearer GIF](./other/img/p.png)](./other/img/p.png)     
  💡 **Note:** `p/x` is easy to print value in expression.
        <hr></hr>
        <br><br>
        <br><br>
        
  #### ▶ Use `g.name = x` or `g.name/x` to transport var to Python interactive console
  [![click to restart GIF and see more clearer GIF](./other/gif/g.gif) ](./other/gif/g.gif)    
  💡 **Note:** `gg` is same usage as `g`, but `gg` will pretty print all vars in `locals()`. 
        <hr></hr>
        <br><br>
        <br><br>
        
  #### ▶ `g()` to transport all vars that in the function to Python interactive console
  [![click to restart GIF and see more clearer GIF](./other/gif/g_call.gif) ](./other/gif/g_call.gif)    
  💡 **Note:** `g()` is a useful tool for debug. `import boxx.g` is convenient way to use `g()` instead of `from boxx import g;g()`(`import boxx.gg` is avaliable too)
        <hr></hr>
        <br><br>
        <br><br>
        
  #### ▶ `boxx` debug tool matrix
| How many vars \ Operation | print | transport | print & transport |
| :---- | :---- | :---- | :---- |
| 1 variable | `p/x` | `g.name/x` | `gg.name/x`|
|Multi variables | `with wp:` | `with wg:` | `with wgg:` |
|All `locals()`| `p()` | `g()` | `gg()` |
|All `locals()`\_2 | `import boxx.p` | `import boxx.g` | `import boxx.gg` |    

  💡 **Note:**   
  * **transport** mean "transport variable to Python interactive console"
  * **All `locals()`** mean all variables in the function or module
  * **All `locals()`\_2** is a convenient way to execution operation when `boxx` are not imported
        <hr></hr>
        <br><br>
        <br><br>
    </td>
    <td valign="top">
    
  ### Scientific Computing and Computer Vision

  Useful tools in **Scientific Computing** and **Computer Vision** field. All tools support array-like types, include `numpy`, `torch.tensor`, `mxnet.ndarray`, `PIL.Image` .etc 
        <hr></hr>
        <br><br>
        <br><br>

  #### ▶ `loga` to visualization matrix and tensor   
  `loga` is short of "log array", `loga` will show many attributes of array-like object.
  [![click to restart GIF and see more clearer GIF](./other/gif/loga.gif)](./other/gif/loga.gif)    
        <hr></hr>
        <br><br>
        <br><br>

  #### ▶ `show` every image in complex struct
  `show` could find every image in complex struct and imshow they.
  [![click to restart GIF and see more clearer GIF](./other/gif/show.gif)](./other/gif/show.gif)    
  💡 **Note:** if args inculde function. those functions will process all numpys befor imshow.
        <hr></hr>
        <br><br>
        <br><br>

  #### ▶ `tree` for visualization complex struct
  like `tree` command in shell that could visualization any struct in tree struct view.
  [![click to restart GIF and see more clearer GIF](./other/gif/tree.gif)](./other/gif/tree.gif)    
  💡 **Note:** `tree` support types include `list`, `tuple`, `dict`, `numpy`, `torch.tensor/Dataset/DataLoader`, `mxnet.ndarray`, `PIL.Image`.etc
        <hr></hr>
        <br><br>
        <br><br>
    </td>
  </tr>
</table> 



---

## 5. Acknowledgments
 * `boox.x_` is supported by [Fn.py: enjoy FP in Python](https://github.com/kachayev/fn.py)
 * `performance` is supported by [SnakeViz](https://jiffyclub.github.io/snakeviz/)
 * `heatmap` is supported by [csurfer/pyheat](https://github.com/csurfer/pyheat)
 * I develop **`boxx`** in [Spyder IDE](https://github.com/spyder-ide/spyder), [Spyder](https://github.com/spyder-ide/spyder) is a awesome Scientific Python Development Environment with Powerful [**Qt-IPython**](https://github.com/jupyter/qtconsole)



