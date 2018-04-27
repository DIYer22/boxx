# -*- coding: utf-8 -*-

import os,glob
from ..ylsys import tmpYl

def showImgsInBrowser(paths):
    '''图片展示分析工具  使用浏览器同步显示图片的image,gt,resoult 等
    支持放大缩小与拖拽
    
    Parameters
    ----------
    paths : list of path
        图片地址组成的数组
    '''
    paths = list(map(os.path.abspath,paths))
    html = getShowsHtml()
    s = 'srcs = [%s]'%(",".join(['"%s"'%p for p in paths]))
    html = html.replace('//replaceTagForPython',s.replace('\\',r'\\'))
    htmlp = os.path.join(tmpYl, 'shows-%s.html') %len(glob.glob(os.path.join(tmpYl, 'shows-*.html')))
    with open(htmlp,'w') as f:
        f.write(html)
    import webbrowser 
    webbrowser.open_new_tab(htmlp)

def getShowsHtml():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>quickSeg image</title>
      <script src="http://apps.bdimg.com/libs/jquery/2.0.0/jquery.min.js"></script>

      <script src="https://cdn.bootcss.com/dat-gui/0.6.5/dat.gui.js"></script>
      <!-- <script src="./leiYangFuns.js"></script> -->
      <style>
      </style>
      <script>
      log = console.log
      int = parseInt
      float = parseFloat
      pow = Math.pow
      max=(x)=>{
        var m=x[0]
        for (var i = 0; i < x.length; i++) {
            m=x[i]>m?x[i]:m
        };
        return m
      }
      min=(l)=>-max(l.map((x)=>-x))
      len= (x)=>x.length
      </script>
    </head>
    <body style="margin:0;padding:0">
    	<canvas id="canvas" width="" height="" style="top:0px;left:0px">
    	</canvas>
    </body>
    <script>
    canvas = document.getElementById('canvas')
    var ctx = canvas.getContext('2d');

    window.addEventListener("resize", resizeCanvas, false);

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        var n = len(srcs)
        bys = int(n/bxs)+Boolean(n%bxs)
        if(bys<=bxs){
          canvas.height = window.innerHeight;
        }else(
          canvas.height = window.innerWidth*bys/bxs
        )
        var w=canvas.width
        var h=canvas.height

        sw = w/bxs
        sh = h/bys
        flash();
    }
    busy = 0
    roundTag = 0
    flashInner = ()=>{
      roundTag += 1
      if (busy){
        return
      }
      var tag = roundTag
      busy = 1
      var bx=0
      var by=0
      for (var src of srcs) {
        if (roundTag!=tag){
          busy=0;
          flash()
          return
        }
        drawImage(src,bx,by)
        bx += 1
        if(bx==bxs){
          by+=1
          bx=0
        }
      }
      busy=0;
      if (roundTag!=tag){
        flash()
      }
    }
    flash = ()=>{setTimeout(flashInner,0)}

    drawImage = (src,bx,by)=>{
      var img = new Image();
      img.onload = function(){
        imgh = img.height
        imgw = img.width
        if(scale == -1){
          sca = min([sw/imgw,sh/imgh])
          scale = Math.log2(sca)
        }
        sca = pow(2,scale)
        var left = max([0,imgw*fx-sw/sca/2])
        var right = min([imgw,imgw*fx+sw/sca/2])
        var up = max([0,imgh*fy-sh/sca/2])
        var down = min([imgh,imgh*fy+sh/sca/2])
        var leftt = max([0,sw/2-imgw*fx*sca])
        var rightt = min([sw,sw/2+imgw*(1-fx)*sca])
        var upp = max([0,sh/2-imgh*fy*sca])
        var downn = min([sh,sh/2+imgh*(1-fy)*sca])
        ctx.clearRect(bx*sw,by*sh,sw,sh);
        ctx.drawImage(img,left,up,right-left,down-up,   bx*sw+leftt,by*sh+upp,rightt-leftt,downn-upp);
          // ctx.drawImage(img,0,0,6000,6000,   0,0,1000,1000);
      }
      img.src = src;
    }

    var view = {
        scroll:(e)=>{
            e.preventDefault()
            var x=e.offsetX
            var y=e.offsetY
            var change = int(e.deltaY)
            var zoomSpeed = 0.2
            if (change<0){
                scale += (zoomSpeed)
            }
            if (change>=0){
                scale -= (zoomSpeed)
            }
            flash()
        },
        onMove:(e)=>{
            e.preventDefault()
            var x = e.clientX-xBegin
            var y = e.clientY-yBegin
            fx = fxBegin - x/sca/imgw
            fx = min([1,max([0,fx])])
            fy = fyBegin - y/sca/imgh
            fy = min([1,max([0,fy])])
            flash()
        },

        onDown:(e)=>{
            e.preventDefault()
            var x = e.clientX
            var y = e.clientY
            xBegin = x
            yBegin = y
            fxBegin = fx
            fyBegin = fy
            canvas.onmousemove = view.onMove
        },
        onUp:()=>{
            canvas.onmousemove = null
        },
        mouseBegin:()=>{
            window.onmousewheel=view.scroll
            window.onmousedown = view.onDown
            window.onmouseup = view.onUp
            onmouseup()
        }
    }
    scale = -1
    fx = .5
    fy = .5

    var srcs = []
    //replaceTagForPython
    bxs = 2

    resizeCanvas()
    view.mouseBegin()
    var gui = new dat.GUI();
    var con = gui.add(window, 'scale',-10,5).listen();
    con.onChange( (v)=>{
        flash()
    })

    // var con2 = gui.add(window, 'fx',0.,1.0).listen();
    // var con3 = gui.add(window, 'fy',0.,1.0).listen();
    // con2.onFinishChange = con3.onFinishChange = con.onFinishChange

    var con4 = gui.add(window, 'bxs',1,5).step(1).listen();
    con4.onChange ( function(v){
      bxs = int(v)
      resizeCanvas()
    })
    </script>
    </html>

    '''
if __name__ == '__main__':
    pass
