

<h1 align="center">Box-X</h1>

<div align="center">
  <strong>:high_brightness:Hack Python and Vision:crescent_moon:</strong>
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

## Examples

All Tools are divided into 2 parts by wether the tool is general:    
 * Left Part: [**General Python Tool**](#1.-General-Python-Tool). The tools could be used anywhere in Python

 * Right Part: [**Scientific Computing and Computer Vision Tool**](#2.-Scientific-Computing-and-Computer-Vision-Tool). Those tools are useful in Scientific Computing and Computer Vision field

*P.S. click the GIF picture to see more clearer GIF*

<table  style="">
  <tr>
    <td valign="top" width="50%">
    
  ### General Python Tool 
  <hr></hr>
        
  #### ▶ Use `p/x` instead of `print(x)`   
  `p/x` will `print(x)` and return `x`
  [![](./other/gif/p.gif)](./other/gif/p.gif)
  💡 **Note:** `p/x` is easy to print value in expression.
        <hr></hr>
        <br><br>
        <br><br>
        
  #### ▶ Use `g.name = x` or `g.name/x` to transport var to Python interactive console
  [![](./other/gif/g.gif) ](./other/gif/g.gif)   
  💡 **Note:** `gg` is same usage as `g`, but `gg` will pretty print all vars in `locals()`. 
        <hr></hr>
        <br><br>
        <br><br>
        
  #### ▶ `g()` to transport all vars that in the function to Python interactive console
  [![](./other/gif/g_call.gif) ](./other/gif/g_call.gif)
  💡 **Note:** `g()` is a useful tool for debug. `import boxx.g` is convenient way to use `g()` instead of `from boxx import g;g()`(`import boxx.gg` is avaliable too)
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
  `loga` will show many attributes of array-like object.
  [![](./other/gif/loga.gif)](./other/gif/loga.gif)
        <hr></hr>
        <br><br>
        <br><br>

  #### ▶ `show` every image in complex struct
  `show` could find every image in complex struct and imshow they.
  [![](./other/gif/show.gif)](./other/gif/show.gif)
  💡 **Note:** if args inculde funcation. those funcations will process all numpys befor imshow.
        <hr></hr>
        <br><br>
        <br><br>

  #### ▶ `tree` for visualization complex struct
  like `tree` command in shell that could visualization any struct in tree struct view.
  [![](./other/gif/tree.gif)](./other/gif/tree.gif)
  💡 **Note:** `tree` support types include `list`, `tuple`, `dict`, `numpy`, `torch.tensor/Dataset/DataLoader`， `mxnet.ndarray`, `PIL.Image`.etc
        <hr></hr>
        <br><br>
        <br><br>
    </td>
  </tr>
</table> 



---

## Box-X Tutorial

[**Tutorial for computer device**](https://mybinder.org/v2/gh/DIYer22/boxx/master?filepath=tutorial_for_boxx.ipynb): We use [Binder](https://mybinder.org) to run this Tutorial in an executable environment. That's mean you can **run tutorial cells rightnow** in your browser without download repository.


[**Tutorial for mobile device**](https://nbviewer.jupyter.org/github/DIYer22/boxx/blob/master/tutorial_for_boxx.ipynb): Just view the Tutorial.

## Acknowledgments
 * `boox.x_` is supported by [Fn.py: enjoy FP in Python](https://github.com/kachayev/fn.py)
 * `performance` is supported by [SnakeViz](https://jiffyclub.github.io/snakeviz/)
 * `heatmap` is supported by [csurfer/pyheat](https://github.com/csurfer/pyheat)
 * I develop **`boxx`** in [Spyder IDE](https://github.com/spyder-ide/spyder), [Spyder](https://github.com/spyder-ide/spyder) is a awesome Scientific Python Development Environment with Powerful [**Qt-IPython**](https://github.com/jupyter/qtconsole)



