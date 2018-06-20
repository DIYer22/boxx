## 开发, 调试计算机视觉代码有哪些技巧？

抛砖引玉, 介绍一个Python 工具包 [**`boxx`**](https://github.com/DIYer22/boxx)


在调试视觉代码时, 基本就是和多维数组打交道, 多维数组有很多的属性，打印起来比较麻烦。 `boxx.loga` 可以一次性展现出一个数组的大多数属性.    
![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/gif/loga.gif)    

💡 **Note:** 
 * `loga` 是 "log array" 的缩写, 若 `array` 里面还含有 `nan` 或 `inf`, `loga` 也会一并提示出来。
 * `loga` 支持许多可以转为 `numpy` 的数据类型，包括 `torch.tensor`, `mxnet.ndarray`, `PIL.Image` 等。



做计算机视觉，可视化图像和 feature 非常重要。`boxx.show` 能方便地做可视化。   
![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/gif/show.gif)    
💡 **Note:** `show` 会在复杂的数据结构中 找出所有可能是图像的矩阵，并一一显示(`plt.imshow`)出来。 当然，`show` 也支持 `numpy`，`torch`，`mxnet`，`PIL.Image` .etc


在开发 CV 代码时，会遇到一些复杂的 dict，list（比如 batch、模型参数）。`boxx.tree` 可以直观地展示复杂结构。   
![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/gif/tree.gif)    

💡 **Note:** 在理解和适配别人的代码时，经常用到 `tree`。`tree` 还支持自动从 `torch.Dataloader/Dataset` 中 sample 一个 batch 来可视化 (P.S. `boxx.show` 也支持) 

---
以上三个工具是我在视觉领域经常用到的工具, 接下来介绍一些通用的 Python 开发调试工具，只要写 Python 代码，都可以用上。

打印变量是最简单、直接的debug方式, 那能不能更简单？   
![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/img/p.png)    

💡 **Note:** `boxx.p` 使用了 magic method, `p/x` 便会打印 x 并返回 x。这样便可以在任何地方打印，比如 例子中的 `p/randint(0, 3)` 就不需要新建变量便可直接打印


在函数内运行 `p()`，便会将函数或 module 内的所有变量名和值一同打印(相当于快捷打印 `locals()`)    
![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/img/p_call.png)    

💡 **Note:** 在函数内 `import boxx.p` 和 `p()` 有相同的效果


许多数情况下， 直接 `print` 无法获得调试的关键信息。 比如训练 loss 跑飞了, 导致 Bug 的可能是 `tensor` 的尺度/类型不对, 矩阵里有 nan , inf 等多种情况。我曾遇到过 [梯度含有nan](https://www.zhihu.com/question/67209417/answer/277425438) 的情况

这时 就必须对矩阵进行分析, 方式有：
 1. 在调试处加上 `print(x.mean(), np.hasinf(x),.np.hasnan(x))`
 2. 设置断点进行分析    
 
方法1 每改一次调试代码 都要运行整个代码, 不灵活，操作也繁琐。   
方法2 中进入和退出 Debug console 比较麻烦，Debug console 本身也不太好用（没有自动补全功能）    
`boxx.g` 提供了一种新的方式，通过 `g.name` 可以将变量传到当前的 Python 交互终端   
![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/gif/g.gif)    

变量传到 Python 终端后，就能对变量进行全面分析了，比如 使用 `loga`，`tree` 来分析

💡 **Note:**   
 * `gg` 的意思是 `to Global and log`， 和 `g` 的用法一样, 但 `gg` 会在传输的同时打印变量. 
 * 需要注意， 如果之前在终端中存在一样的变量名称，则变量的值会被新值覆盖.

在函数内运行 `g()`，便会将函数 (或 module) 内的所有变量一同传到当前的 Python 交互终端     
![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/gif/g_call.gif)    

这样 任何错误都可以在终端中复现和分析了。当然， 注意不要覆盖重要的全局变量。

💡 **Note:** 在函数内 `import boxx.g` 和 `g()` 有相同的效果


<!--刚才讲了对变量的两类操作 打印和传输到终端，`p/x` 和 `g.name=x` 是对单个变量操作，`p()` 和 `g()` 则是对整个函数或模块内的变量(`locals()`)进行操作。    -->
在实际开发调试中, 函数或 module 内可能含有非常多的变量 但我们只对几个变量感兴趣,  `with p`, `with g`, `with gg` 可以使操作只作用于几个感兴趣的变量，只需把变量放入 `with` 结构中即可 :     
![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/gif/w.gif)        
  💡 **Note:**  
  * `with p`, `with g`, `with gg` 只作用于在 `with` 结构中进行赋值操作的变量. 
  * 如果变量名在 `with` 前存在于 `locals()` 中, 同时 `id(变量)` 没有变化 , `with` 结构可能无法检测到该变量.

总结一下，`boxx` 的调试工具可以汇总为一个表

 **`boxx` 调试工具矩阵**     

| 变量个数 \ 操作 | print | transport | print & transport |
| :---- | :---- | :---- | :---- |
| 单变量 | `p/x` | `g.name/x` | `gg.name/x`|
| 多变量 | `with p:` | `with g:` | `with gg:` |
| `locals()`| `p()` | `g()` | `gg()` |
| `locals()`\_2 | `import boxx.p` | `import boxx.g` | `import boxx.gg` |    

  💡 **Note:**   
  * **transport** 操作是指 把函数内的变量传送到 Python interactive console 中
  * **`locals()`** 指 作用于函数或 module 内的所有变量
  * **`locals()`\_2**: 当 `boxx` 未导入时， `import boxx.{操作}` 能等价于 `from boxx import {操作};{操作}()`


在学习新框架或适配大佬代码时，经常会使用 `print(x)`, `dir(x)`, `help(x)`, `type(x)` 来了解某个变量的各方面的信息 (变量可能是 值/function/class/module 等)，于是我写了一个 `boox.what(x)` 来全面了解"what is `x`?"： 
  [![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/img/what.png) ](./img/what.png)    
  💡 **Note:** `what(x)` 通过打印 `x` 自己及`x` 的 **文档**, **父类继承关系**, **内部结构** 及 **所有属性** 来全面了解 `x`. 是 `help(x)` 的补充.
  
---

说了这么多调试 再说一下性能调优

测试代码性能时，计时很常用, 我写了一个方便的计时工具`boxx.timeit`  将想要计时的代码块放入 `with timeit():` 中就可以计时了:   
![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/img/timeit.png)    


此外 [`SnakeViz`](https://jiffyclub.github.io/snakeviz/) 是一个很棒的性能分析工具，`SnakeViz` 能够通过 `cProfile` 文件，来统计代码的函数调用情况，并可视化出代码的 [火焰图](http://www.ruanyifeng.com/blog/2017/09/flame-graph.html)。但是， 先生成 `cProfile` 文件，再运行 `SnakeViz` 的流程非常繁琐，我把这一套操作封装成了 `boxx.performance` 来简化流程：     
  [![](https://raw.githubusercontent.com/DIYer22/boxx/master/other/gif/performance.gif) ](./gif/performance.gif)    
  
  💡 **Note:** `performance` 也支持字符串形式的 Python 代码.


如今的数据集都数百上千 GB，在数据清洗和预处理时 要写多进程的 Python 代码 来榨干 CPU 的每一个线程获得加速。但我觉得 Python 多进程的几个范式都不够方便，我参照 `map` 的思想和用法把多进程操作封装成 `boxx.mapmp` 函数(意思是"Map for Mulit Processing"). `mapmp` 和 `map` 有一样的用法， 只需把 `map` 替换为 `mapmp` 即可获得多进程加速:    
  [![click to restart GIF and see more clearer GIF](./gif/mapmp.gif) ](./gif/mapmp.gif)    
  💡 **Note:** 
  * `mapmp` 的 **pool** 参数来控制进程数目，默认为 CPU 线程数目.
  * 在多进程程序中, 打印进度往往非常麻烦. `mapmp` 的 **printfreq** 参数能解决这个问题.
  * 如同 `map` 一样，`mapmp` 支持将多个参数输入函数，如`mapmp(add, list_1, list_2)`
  * 在 Python 中，多进程代码最好在 `__name__ == '__main__'` 环境中运行.
  * 如果加速 `numpy` 程序，请注意 [在 MKL 版本的 `numpy` 中，多进程会更慢](https://blog.skyaid-service.org/2017/08/15/numpy_performance/), 可以运行 `boxx.testNumpyMultiprocessing()` 来测试当前环境对多进程 `numpy` 的友好程度


当要下载 url 形式的数据集或网络爬取图片时，多线程编程对这类高IO操作会很有用。`boxx` 还有个多线程版本的 `map` -- `mapmt` (意思是 "Map for Mulit Threading")。`mapmt` 用法和 `mapmp` 一样, 但没有多进程的诸多限制。

---

 <!--dict 经常用来存储属性, 但是 字典调用属性麻烦 dic[`label`] 我继承 dict 写了一个dicto, 调用属性和 JavaScript 一样方便, 
我还在 boxx 中 内置了一个

tree show what npa tprgb 都是调试代码时 才用到的工具, 使用频率很高 人生苦短 为了少打括号 以上方法全都支持减号来调用 call 即 fun-x 来调用

说完调试 再说一下性能调优 -->



再分享一下我自己在写视觉代码的感受吧

由于我自己
 1. 写 CV 代码离不开强大的 [Qt console for IPython](https://ipython.org/ipython-doc/3/interactive/qtconsole.html)
 2. 受不了远程编辑对网络的依赖和延迟

所以 一直用 Anaconda 自带的 Spyder 作为 Python 开发的 IDE. Spyder 虽然不够强大，但自带的 Qt-IPython, 配合自己写的工具，调试起来还是比较方便, 顺手。所以, 我开发的工具都尽可能地直接, 简洁，上面介绍的大部分工具都支持 `func-x` 来代替 `func(x)` 以方便调试时调用。甚至，我还写了一些字符串处理工具，直接在IPython 内使用, 以弥补 Spyder 作为 IDE 的不足。 


此外，我的工作流一般是 先在本地开发调试, 用 `boxx.sysi` 检测运行环境来自动切换运行参数, 本地开发调试 OK 了, 用 `rsync` 命令 只传改过的 .py 文件到服务器 再来 train。虽然这样传代码比较麻烦, 但开发, 调试起来会方便很多。
  
之前在实验室一直是本地 GPU 环境调试 比较方便。实习后, 旷厂不提供本地 GPU。我主力是 PyTorch, 为了方便调试 我写了个 `boxx.ylth` 包，如果检测到没有 CUDA 环境，`boxx.ylth` 会强行使 `.cuda()` 和大部分 GPU 操作无效。只要在代码开头 `import boxx.ylth` 大多数只基于 GPU 的 torch 代码, 可以不经更改 直接在 CPU 上运行和调试。(这操作太暴力 请慎用)



---


GitHub 主页：https://github.com/DIYer22/boxx
 
安装：`pip install git+https://github.com/DIYer22/boxx` ([其他安装方法及说明](https://github.com/DIYer22/boxx/blob/master/README_zh_cn.md#%E4%BA%8C-%E5%AE%89%E8%A3%85))
 
教程：**`boxx`** 的教程是一个可执行的在线 Notebook。 也就是说，无需下载和运行任何代码，只需浏览器打开链接，就可以在线执行 Notebook 教程中的代码块。  
* [**=> 可直接执行的在线教程**](https://mybinder.org/v2/gh/DIYer22/boxx-ipynb/master?filepath=tutorial_for_boxx.ipynb)
 
最后 特别感谢徐晓栋、吴国栋、范浩强和熊鹏飞对 `boxx` 提出的建议。
