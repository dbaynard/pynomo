#
#    This file is part of PyNomo -
#    a program to create nomographs with Python (http://pynomo.sourceforge.net/)
#
#    Copyright (C) 2007  Leif Roschier  <lefakkomies@users.sourceforge.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyx import *
import math
import scipy

class Nomo_Axis:
    """
    Main class to draw axis.
    """
    def __init__(self,func_f,func_g,start,stop,turn,title,canvas,type='linear',
                 text_style='normal',title_x_shift=0,title_y_shift=0.25,
                 tick_levels=10,tick_text_levels=10,
                 text_color=color.rgb.black, axis_color=color.rgb.black):
        self.func_f=func_f
        self.func_g=func_g
        self.start=start
        self.stop=stop
        self.turn=turn
        self.title=title
        self.canvas=canvas
        self.title_x_shift=title_x_shift
        self.title_y_shift=title_y_shift
        self.text_style=text_style
        self.tick_levels=tick_levels
        self.tick_text_levels=tick_text_levels
        if type=='log':
            self._make_log_axis_(start=start,stop=stop,f=func_f,g=func_g,turn=turn)
        else:
            self._make_linear_axis_(start=start,stop=stop,f=func_f,g=func_g,turn=turn)
        self.draw_axis(canvas)

    def _test_tick_(self,u,tick,scale_max):
        """ tests if it is time to put a tick
        u=value
        tick=step to put ticks
        scale_max=scale from min to max
        for example:
        u=0.2, tick=0.1 gives True
        u=0.25, tick=0.1 gives False """
        return math.fabs(math.modf(u/tick)[0]) < (scale_max*1e-8) or math.fabs((math.modf(u/tick)[0]-1)) < (scale_max*1e-8)


    def _make_linear_axis_(self,start,stop,f,g,turn=1):
        """ Makes a linear scale according to functions f(u) and g(u)
        with values u in range [start, stop]. turn=-1 makes ticks to change side
        """
        line = path.path(path.moveto(f(start), g(start)))
        thin_line=path.path(path.moveto(f(start), g(start)))
        # for numerical derivative to find angle
        du=math.fabs(start-stop)*1e-4
        # which number to divide. how many decades there are
        scale_max=10.0**math.ceil(math.log10(math.fabs(start-stop)))
        tick_min=scale_max/500.0
        tick_max=scale_max/10.0
        tick_1=scale_max/20.0
        tick_2=scale_max/100.0
        texts=list([])
        steps=math.fabs(start-stop)/tick_min+1
        for u in scipy.linspace(start,stop,steps):
            dx=(f(u+du)-f(u))*turn
            dy=(g(u+du)-g(u))*turn
            dx_unit=dx/math.sqrt(dx**2+dy**2)
            dy_unit=dy/math.sqrt(dx**2+dy**2)
            if dy_unit!=0:
                angle=-math.atan(dx_unit/dy_unit)*180/math.pi
            else:
                angle=0
            # floating arithmetic makes life difficult, that's why _test_tick_ function
            if self._test_tick_(u,tick_max,scale_max):
                text_distance=1.0
                grid_length=3.0/4
                if dy<=0:
                    text_attr=[text.valign.middle,text.halign.right,text.size.small,trafo.rotate(angle)]
                else:
                    text_attr=[text.valign.middle,text.halign.left,text.size.small,trafo.rotate(angle)]
                #texts.append((`u`,f(u)+text_distance*dy_unit,g(u)-text_distance*dx_unit,text_attr))
                if self.tick_text_levels>0:
                    texts.append((self._put_text_(u),f(u)+text_distance*dy_unit,g(u)-text_distance*dx_unit,text_attr))
                line.append(path.lineto(f(u), g(u)))
                if self.tick_levels>0:
                    line.append(path.lineto(f(u)+grid_length*dy_unit, g(u)-grid_length*dx_unit))
                line.append(path.moveto(f(u), g(u)))
            elif self._test_tick_(u,tick_1,scale_max):
                grid_length=1.0/4
                text_distance=1.5/4
                if dy<=0:
                    text_attr=[text.valign.middle,text.halign.right,text.size.scriptsize,trafo.rotate(angle)]
                else:
                    text_attr=[text.valign.middle,text.halign.left,text.size.scriptsize,trafo.rotate(angle)]
                if self.tick_text_levels>1:
                    texts.append((self._put_text_(u),f(u)+text_distance*dy_unit,g(u)-text_distance*dx_unit,text_attr))
                line.append(path.lineto(f(u), g(u)))
                if self.tick_levels>1:
                    line.append(path.lineto(f(u)+grid_length*dy_unit, g(u)-grid_length*dx_unit))
                line.append(path.moveto(f(u), g(u)))
            elif self._test_tick_(u,tick_2,scale_max):
                grid_length=0.5/4
                text_distance=1.0/4
                if dy<=0:
                    text_attr=[text.valign.middle,text.halign.right,text.size.tiny,trafo.rotate(angle)]
                else:
                    text_attr=[text.valign.middle,text.halign.left,text.size.tiny,trafo.rotate(angle)]
                if self.tick_text_levels>2:
                    texts.append((self._put_text_(u),f(u)+text_distance*dy_unit,g(u)-text_distance*dx_unit,text_attr))
                line.append(path.lineto(f(u), g(u)))
                if self.tick_levels>2:
                    line.append(path.lineto(f(u)+grid_length*dy_unit, g(u)-grid_length*dx_unit))
                line.append(path.moveto(f(u), g(u)))
            else:
                grid_length=0.3/4
                thin_line.append(path.moveto(f(u), g(u)))
                if self.tick_levels>3:
                    thin_line.append(path.lineto(f(u)+grid_length*dy_unit, g(u)-grid_length*dx_unit))
                thin_line.append(path.moveto(f(u), g(u)))
                line.append(path.lineto(f(u), g(u)))
        self.line=line
        self.thin_line=thin_line
        self.texts=texts
    def _make_log_axis_(self,start,stop,f,g,turn=1):
        """ draw logarithmic axis
        """
        # for numerical derivative to find angle
        du=math.fabs(start-stop)*1e-6
        texts=list([])
        if (start<stop):
            min=start
            max=stop
        else:
            min=stop
            max=start
        line = path.path(path.moveto(f(min), g(min)))
        thin_line=path.path(path.moveto(f(min), g(min)))
        max_decade=math.ceil(math.log10(max))
        min_decade=math.floor(math.log10(min))
        for decade in scipy.arange(min_decade,max_decade+1,1):
            for number in scipy.concatenate((scipy.arange(1,2,0.2),scipy.arange(2,10,1))):
                u=number*10.0**decade
                dx=(f(u+du)-f(u))*turn
                dy=(g(u+du)-g(u))*turn
                dx_unit=dx/math.sqrt(dx**2+dy**2)
                dy_unit=dy/math.sqrt(dx**2+dy**2)
                if dy_unit!=0:
                    angle=-math.atan(dx_unit/dy_unit)*180/math.pi
                else:
                    angle=0
                if u>=min and u<=max:
                    if (number==1):
                        grid_length=3.0/4
                        text_distance=1.0
                        if dy<=0:
                            text_attr=[text.valign.middle,text.halign.right,text.size.small,trafo.rotate(angle)]
                        else:
                            text_attr=[text.valign.middle,text.halign.left,text.size.small,trafo.rotate(angle)]
                        if self.tick_text_levels>0:
                            texts.append((self._put_text_(u),f(u)+text_distance*dy_unit,g(u)-text_distance*dx_unit,text_attr))
                        line.append(path.lineto(f(u), g(u)))
                        if self.tick_levels>0:
                            line.append(path.lineto(f(u)+grid_length*dy_unit, g(u)-grid_length*dx_unit))
                        line.append(path.moveto(f(u), g(u)))
                    else:
                        grid_length=0.3/4
                        text_distance=1.0/4
                        if dy<=0:
                            text_attr=[text.valign.middle,text.halign.right,text.size.tiny,trafo.rotate(angle)]
                        else:
                            text_attr=[text.valign.middle,text.halign.left,text.size.tiny,trafo.rotate(angle)]
                        if self.tick_text_levels>1:
                            texts.append((self._put_text_(u),f(u)+text_distance*dy_unit,g(u)-text_distance*dx_unit,text_attr))
                        thin_line.append(path.lineto(f(u), g(u)))
                        if self.tick_levels>1:
                            thin_line.append(path.lineto(f(u)+grid_length*dy_unit, g(u)-grid_length*dx_unit))
                        thin_line.append(path.moveto(f(u), g(u)))
                        line.append(path.lineto(f(u), g(u)))
        self.line=line
        self.thin_line=thin_line
        self.texts=texts

    def draw_axis(self,c):
        c.stroke(self.line, [style.linewidth.normal])
        c.stroke(self.thin_line, [style.linewidth.thin])
        for ttext,x,y,attr in self.texts:
            c.text(x,y,ttext,attr)
        # make title
        # find out if start or stop has higher y-value
        if self.func_g(self.stop)>self.func_g(self.start):
            c.text(self.func_f(self.stop)+self.title_x_shift,
                    self.func_g(self.stop)+self.title_y_shift,
                    self.title,[text.halign.center])
        else:
            c.text(self.func_f(self.start)+self.title_x_shift,
                    self.func_g(self.start)+self.title_y_shift, self.title,
                    [text.halign.center])

    def _put_text_(self,u):
        if self.text_style=='oldstyle':
            return r"$\oldstylenums{%3.2f}$ " %u
        else:
            return r"$%3.2f$ " %u

## Testing
if __name__=='__main__':
    skaalaus_x=2*4*1.3
    skaalaus_y=2*12*1.3
    def f1(L):
        return skaalaus_x*(L*L-8*L-5)/(3*L*L+2*L+7)
    def g1(L):
        return skaalaus_y*(8*L*L+12*L-8)/(3*L*L+2*L+7)
    def f3(p):
        return skaalaus_x*((4*p*p+10*p+1)/(8*p*p+4*p+3))

    def g3(p):
        return skaalaus_y*((-12*p*p+4*p+8)/(8*p*p+4*p+3))
    def f4(p):
        return skaalaus_x*((4*p*p+10*p+1)/(8*p*p+4*p+3))+20

    def g4(p):
        return skaalaus_y*((-12*p*p+4*p+8)/(8*p*p+4*p+3))
    c = canvas.canvas()
    gg3=Nomo_Axis(func_f=f3,func_g=g3,start=1.0,stop=0.5,turn=-1,title='func 1',canvas=c,type='linear')
    gg1=Nomo_Axis(func_f=f1,func_g=g1,start=0.5,stop=1.0,turn=-1,title='func 3',canvas=c,type='linear')
    gg4=Nomo_Axis(func_f=f4,func_g=g4,start=0.5,stop=1.0,turn=-1,title='func 3',canvas=c,type='linear')
    c.writePDFfile("minimal6")
    print f1(1)
    print g1(1)