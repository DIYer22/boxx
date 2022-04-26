**Language :** [![English](https://jaywcjlove.github.io/sb/lang/english.svg)](https://github.com/DIYer22/boxx) [![Chinese](https://jaywcjlove.github.io/sb/lang/chinese.svg)](./README_zh_cn.md)
  
<br>
<h1 align="center">Box-X</h1>


<div align="center">
  <strong>Hack Python and Vision</strong>
</div>

<div align="center">
  A Tool-box for Efficient Build and Debug in Python. Especially for <strong>Scientific Computing</strong> and <strong>Computer Vision</strong>.
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

 ### [Introduce](#1-introduce) | [Install](#2-install) | [Tutorial](#3-tutorial) | [Examples](#4-examples) | [Acknowledgments](#5-acknowledgments)
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
## 1. Introduce

**`Box-X`** is a Tool-box for Efficient Build and Debug in Python.   

Especially for **Scientific Computing** and **Computer Vision**. 

So, all Tools are divided into 2 parts by wether the tool is general used:    
 * **General Python Tool**: Tools could be used anywhere in Python

 * **Scientific Computing and Computer Vision Tool**: Those tools are useful in Scientific Computing and Computer Vision field
 

P.S. **`boxx`** supports both **`Python 2/3`** on **`Linux | macOS | Windows`** with **`CPython | IPython | Spyder | Notebook`** environment.





## 2. Install

```
pip install boxx
```
<!--
#### Via pip
#### From source
```bash
git clone https://github.com/DIYer22/boxx
cd boxx/
python setup.py install
```
#### If no git
```
pip install boxx -U
```

💡 **Note:** 
 * Recommended to install via git or source because PyPI mirrors may has a big delay.
 * Please ensure `boxx`'s version > `0.9.1`. Otherwise, please install from source.

-->

## 3. Tutorial

**`Box-X`**'s Tutorial is a Jupyter Notebook file 

There are 3 methods to run or view this Notebook file

#### Method 1: Executable Interactive Online Notebook
We use [Binder](https://mybinder.org) to run Tutorial Notebook in  an executable interactive online jupyer environment.    
That's mean you can **run code in notebook rightnow** in your browser without download or install anything.    
* [**=> Executable Interactive Online Tutorial**](https://mybinder.org/v2/gh/DIYer22/boxx-ipynb/master?filepath=tutorial_for_boxx.ipynb)

#### Method 2: Download and Run at Local

```bash
git clone https://github.com/DIYer22/boxx
cd boxx/
python setup.py install
jupyter notebook
```
Then open `./tutorial_for_boxx.ipynb` in notebook.

#### Method 3: Static Noetbook
 Just view the Tutorial Notebook.
* [**=> Static Tutorial**](https://nbviewer.jupyter.org/github/DIYer22/boxx-ipynb/blob/master/tutorial_for_boxx.ipynb)


## 4. Examples

Examples are divided into 2 parts too.   

**General Python Tool** on left, **Scientific Computing and Computer Vision Tool** on right.

💡 **Note:** 
 * *Click the image will see more clearer image, and if image is GIF, GIF will be replayed*
 * *The following content is layout of desktop browser, if you are viewing through a mobile browser, it is recommended to visit [**=> Static Tutorial**](https://nbviewer.jupyter.org/github/DIYer22/boxx-ipynb/blob/master/tutorial_for_boxx.ipynb)*

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
        
  #### ▶ Use `g.name = x` or `g.name/x` to transport variable to Python interactive console
  [![click to restart GIF and see more clearer GIF](./other/gif/g.gif) ](./other/gif/g.gif)    
  💡 **Note:** 
  * `gg` is the meaning of "to Global and log", has same usage as `g`, but `gg` will print the transported variable. 
  *  if variable name exists in console before, the variable's value will be covered by new value.
        <hr></hr>
        <br><br>
        <br><br>
        
  #### ▶ `g()` to transport all vars that in the function to Python interactive console
  [![click to restart GIF and see more clearer GIF](./other/gif/g_call.gif) ](./other/gif/g_call.gif)    
  💡 **Note:** `g()` is a useful tool for debug. `import boxx.g` is convenient way to use `g()` instead of `from boxx import g;g()`(`import boxx.gg` is avaliable too)
        <hr></hr>
        <br><br>
        <br><br>
        
  #### ▶ `with p`, `with g`, `with gg` are mulit variables version of `p`, `g`, `gg` that work under "with statement"
  Only act on interested variables which is under "with statement"
  [![click to restart GIF and see more clearer GIF](./other/gif/w.gif) ](./other/gif/w.gif)    
  💡 **Note:** 
  * `with p`, `with g`, `with gg` only act on assignment variables under "with statement". 
  * If variable's name exists in `locals()` before and `id(variable)` not change ,variable may not be detected 
        <hr></hr>
        
    </td>
    <td valign="top">
    
  ### Scientific Computing and Computer Vision

  Useful tools in **Scientific Computing** and **Computer Vision** field. All tools support array-like types, include `numpy`, `torch.tensor`, `mxnet.ndarray`, `PIL.Image` .etc     
  
  💡 **Note:** If you are using `ssh` to execute code on a remote server, it is recommended that `ssh` plus `-X` make visualized `plt` charts can be transferred to the local and display, like `ssh -x user@host`.
        <hr></hr>

  #### ▶ `loga` to visualization matrix and tensor   
  `loga` is short of "log array", `loga` will show many attributes of array-like object.
  [![click to restart GIF and see more clearer GIF](./other/gif/loga.gif)](./other/gif/loga.gif)     
  💡 **Note:** `loga` analysis array-like object by it's shape, max, min, mean, and distribute. Support `numpy`, `torch.tensor`, `mxnet.ndarray`, `PIL.Image` .etc 
        <hr></hr>
        <br><br>
        <br><br>

  #### ▶ `show` is easy to do `imshow`, even images are in complex struct
  `show` could find every image in complex struct and imshow they.
  [![click to restart GIF and see more clearer GIF](./other/gif/show.gif)](./other/gif/show.gif)    
  💡 **Note:** if args inculde function(like `torgb`). those functions will process all numpys befor imshow.
        <hr></hr>
        <br><br>
        <br><br>

  #### ▶ `tree` for visualization complex struct
  like `tree` command in shell, `boxx.tree` could visualization any struct in tree struct view.
  [![click to restart GIF and see more clearer GIF](./other/gif/tree.gif)](./other/gif/tree.gif)    
  💡 **Note:** `tree` support types include `list`, `tuple`, `dict`, `numpy`, `torch.tensor/Dataset/DataLoader`, `mxnet.ndarray`, `PIL.Image`.etc
        <hr></hr>
    </td>
  </tr>
</table> 


<table  style="">
  <tr>
    <td valign="top" width="50%">
    
  #### ▶ `boxx` debug tool matrix
| How many vars \ Operation | print | transport | print & transport |
| :---- | :---- | :---- | :---- |
| Single variable | `p/x` | `g.name/x` | `gg.name/x`|
|Multi variables | `with p:` | `with g:` | `with gg:` |
|All `locals()`| `p()` | `g()` | `gg()` |
|All `locals()`\_2 | `import boxx.p` | `import boxx.g` | `import boxx.gg` |    

  💡 **Note:**   
  * **transport** mean "transport variable to Python interactive console"
  * **All `locals()`** mean operation will act on all variables in the function or module
  * **All `locals()`\_2 :** when `boxx` are not imported, `import boxx.{operation}` is a convenient way to execution operation 
        <br><br>
        <hr></hr>
        
  ####  ▶ `what` to know "What's this?"
  [![click to restart GIF and see more clearer GIF](./other/img/what.png) ](./other/img/what.png)    
  💡 **Note:** `what(x)` will show "what is `x`?" by pretty print it's **Self**, **Document**, **Father Classes**, **Inner Struct** and **Attributes**. It is a supplement of `help(x)`.
        <br><br>
        <hr></hr>
        
  #### ▶ `timeit` is convenient timing tool 
  [![click to restart GIF and see more clearer GIF](./other/img/timeit.png) ](./other/img/timeit.png)    
  💡 **Note:** `timeit` will timing code block under "with statement" and print spend time in blue color.
        <br><br>
        <hr></hr>
        
  #### ▶ `mapmp` is Multi Process version of `map`
  `mapmp` is the meaning of "MAP for Multi Process", has the same usage as `map` but faster.    
  [![click to restart GIF and see more clearer GIF](./other/gif/mapmp.gif) ](./other/gif/mapmp.gif)    
  💡 **Note:** 
  * **pool** parameter in `mapmp` mean the number of Process, the default is the number of CPUs in the system.
  * In multi process programs, display processing progress is troublesome. **printfreq** parameter in `mapmp` can handle this problem.
  * Like `map`, `mapmp` support muliti args to as input to function, like `mapmp(add, list_1, list_2)`.
  *  * It's better to run multi process under `__name__ == '__main__'` environment.
  * If you speed up the `numpy` program, note that in the MKL version of `numpy`, multiple processes will be slower. You can run `boxx.testNumpyMultiprocessing()` to test how friendly the current environment is to a multi-process `numpy`. 
        <br><br>
        <hr></hr>
        
  #### ▶ `heatmap` to show the time heat map of your code
  [![click to restart GIF and see more clearer GIF](./other/img/heatmap.png) ](./other/img/heatmap.png)    
  💡 **Note:** `heatmap` also support python code string.
        <br><br>
        <hr></hr>
        
  #### ▶ `performance` could statistic function calls and visualize code performance   
  [![click to restart GIF and see more clearer GIF](./other/gif/performance.gif) ](./other/gif/performance.gif)    
  💡 **Note:** `performance` also support python code string.
    </td>
  </tr>
</table>











---

















## 5. Acknowledgments
 * Thanks to Xiaodong Xu, Guodong Wu, Haoqiang Fan, Pengfei Xiong for their suggestions
 * I develop **`boxx`** in [Spyder IDE](https://github.com/spyder-ide/spyder), [Spyder](https://github.com/spyder-ide/spyder) is a awesome Scientific Python Development Environment with Powerful [**Qt-IPython**](https://github.com/jupyter/qtconsole)
 * `performance` is supported by [SnakeViz](https://jiffyclub.github.io/snakeviz/)
 * `heatmap` is supported by [csurfer/pyheat](https://github.com/csurfer/pyheat)



