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
                 text_color=color.rgb.black, axis_color=color.rgb.black,
                 manual_axis_data={},axis_appear={},side='left'):
        self.func_f=func_f
        self.func_g=func_g
        self.start=start
        self.stop=stop
        self.side=side
        self.turn=turn # to be removed, use side
        self.title=title
        self.canvas=canvas
        self.title_x_shift=title_x_shift
        self.title_y_shift=title_y_shift
        self.text_style=text_style
        self.tick_levels=tick_levels
        self.tick_text_levels=tick_text_levels
        axis_appear_default_values={
                             'text_distance_0':1.0,
                             'text_distance_1':1.0/4,
                             'text_distance_2':1.0/4,
                             'grid_length_0':3.0/4,
                             'grid_length_1':0.9/4,
                             'grid_length_2':0.5/4,
                             'grid_length_3':0.3/4}
        self.axis_appear=axis_appear_default_values
        self.axis_appear.update(axis_appear)

        if type=='log':
            self._make_log_axis_(start=start,stop=stop,f=func_f,g=func_g,turn=turn)
            self.draw_axis(canvas)
        if type=='linear':
            self._make_linear_axis_(start=start,stop=stop,f=func_f,g=func_g,turn=turn)
            self.draw_axis(canvas)
        if type=='manual point':
            self._make_manual_axis_circle_(manual_axis_data)
            self.draw_axis(canvas)
        if type=='manual line':
            self._make_manual_axis_line_(manual_axis_data)
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
        du=math.fabs(start-stop)*1e-6
        dy=(g(start+du)-g(start))
        self._determine_turn_()
        turn=self.turn
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
                text_distance=self.axis_appear['text_distance_0']
                grid_length=self.axis_appear['grid_length_0']
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
                text_distance=self.axis_appear['text_distance_1']
                grid_length=self.axis_appear['grid_length_1']
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
                text_distance=self.axis_appear['text_distance_2']
                grid_length=self.axis_appear['grid_length_2']
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
                grid_length=self.axis_appear['grid_length_3']
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
        self._determine_turn_()
        turn=self.turn
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
            for number in scipy.concatenate((scipy.arange(1,2,0.2),scipy.arange(2,3,0.5),scipy.arange(3,10,1))):
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
                    line.append(path.lineto(f(u), g(u)))
                    if (number==1):
                        text_distance=self.axis_appear['text_distance_0']
                        grid_length=self.axis_appear['grid_length_0']
                        if dy<=0:
                            text_attr=[text.valign.middle,text.halign.right,text.size.small,trafo.rotate(angle)]
                        else:
                            text_attr=[text.valign.middle,text.halign.left,text.size.small,trafo.rotate(angle)]
                        if self.tick_text_levels>0:
                            texts.append((self._put_text_(u),f(u)+text_distance*dy_unit,g(u)-text_distance*dx_unit,text_attr))
                        #line.append(path.lineto(f(u), g(u)))
                        if self.tick_levels>0:
                            line.append(path.lineto(f(u)+grid_length*dy_unit, g(u)-grid_length*dx_unit))
                        line.append(path.moveto(f(u), g(u)))
                    else:
                        if number in [2,3,4,5,6,7,8,9]:
                            text_distance=self.axis_appear['text_distance_1']
                            grid_length=self.axis_appear['grid_length_1']
                        else:
                            text_distance=self.axis_appear['text_distance_2']
                            grid_length=self.axis_appear['grid_length_2']
                        if dy<=0:
                            text_attr=[text.valign.middle,text.halign.right,text.size.tiny,trafo.rotate(angle)]
                        else:
                            text_attr=[text.valign.middle,text.halign.left,text.size.tiny,trafo.rotate(angle)]
                        if self.tick_text_levels>1:
                            texts.append((self._put_text_(u),f(u)+text_distance*dy_unit,g(u)-text_distance*dx_unit,text_attr))
                        #thin_line.append(path.lineto(f(u), g(u)))
                        if self.tick_levels>1:
                            if number in [2,3,4,5,6,7,8,9]:
                                line.append(path.moveto(f(u), g(u)))
                                line.append(path.lineto(f(u)+grid_length*dy_unit, g(u)-grid_length*dx_unit))
                            else:
                                thin_line.append(path.moveto(f(u), g(u)))
                                thin_line.append(path.lineto(f(u)+grid_length*dy_unit, g(u)-grid_length*dx_unit))
                            line.append(path.lineto(f(u), g(u)))
        self.line=line
        self.thin_line=thin_line
        self.texts=texts

    def _make_manual_axis_circle_(self,manual_axis_data):
        """
        draws axis with only circles and texts
        """
        f=self.func_f
        g=self.func_g
        self._determine_turn_()
        turn=self.turn
        texts=list([])
        line = path.path(path.moveto(f(self.start), g(self.start)))
        thin_line=path.path(path.moveto(f(self.start), g(self.start)))
        for number, label_string in manual_axis_data.iteritems():
            text_distance=1.0/4*turn
            if self.side=='left':
                text_attr=[text.valign.middle,text.halign.right,text.size.small]
            else:
                text_attr=[text.valign.middle,text.halign.left,text.size.small]
            texts.append((label_string,f(number)+text_distance,
                          g(number),text_attr))
            self.canvas.fill(path.circle(f(number), g(number), 0.02))
        self.line=line
        self.thin_line=thin_line
        self.texts=texts

    def _make_manual_axis_line_(self,manual_axis_data):
        """
        draws axis with texts, line and ticks where texts are
        """
        # for numerical derivative to find angle
        f=self.func_f
        g=self.func_g
        self._determine_turn_()
        turn=self.turn
        du=math.fabs(self.start-self.stop)*1e-6
        texts=list([])
        if (self.start<self.stop):
            min=self.start
            max=self.stop
            turn=turn*-1.0
        else:
            min=self.stop
            max=self.start
        # lets make the line
        line_length_straigth=math.sqrt((f(max)-f(min))**2+(g(max)-g(min))**2)
        sections=300.0 # about number of sections
        section_length=line_length_straigth/sections
        line = path.path(path.moveto(f(self.start), g(self.start)))
        thin_line=path.path(path.moveto(f(self.start), g(self.start)))
        u=min
        while u<max:
            dx=(f(u+du)-f(u))*turn
            dy=(g(u+du)-g(u))*turn
            dl=math.sqrt(dx**2+dy**2)
            delta_u=du*section_length/dl
            u+=delta_u
            line.append(path.lineto(f(u), g(u)))
        # make lines and texts
        for number, label_string in manual_axis_data.iteritems():
            dx=(f(number+du)-f(number))*turn
            dy=(g(number+du)-g(number))*turn
            dx_unit=dx/math.sqrt(dx**2+dy**2)
            dy_unit=dy/math.sqrt(dx**2+dy**2)
            if dy_unit!=0:
                angle=-math.atan(dx_unit/dy_unit)*180/math.pi
            else:
                angle=0
            text_distance=self.axis_appear['text_distance_1']
            grid_length=self.axis_appear['grid_length_1']
            if dy<=0:
                text_attr=[text.valign.middle,text.halign.left,text.size.small,trafo.rotate(angle)]
            else:
                text_attr=[text.valign.middle,text.halign.right,text.size.small,trafo.rotate(angle)]
            texts.append((label_string,f(number)-text_distance*dy_unit,g(number)+text_distance*dx_unit,text_attr))
            line.append(path.moveto(f(number), g(number)))
            line.append(path.lineto(f(number)-grid_length*dy_unit, g(number)+grid_length*dx_unit))
            #self.canvas.fill(path.circle(f(number), g(number), 0.02))
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

    def _determine_turn_(self):
        """
         determines if we are going upwards or downwards at start
        """
        g=self.func_g
        f=self.func_f
        start=self.start
        stop=self.stop
        du=math.fabs(start-stop)*1e-6
        dy=(g(start+du)-g(start))
        if dy<=0 and self.side=='left':
            self.turn=1.0
        if dy>0 and self.side=='left':
            self.turn=-1.0
        if dy<=0 and self.side=='right':
            self.turn=-1.0
        if dy>0 and self.side=='right':
            self.turn=1.0
## Testing
if __name__=='__main__':
    def f1(L):
        return 2*(L*L-8*L-5)/(3*L*L+2*L+7)
    def g1(L):
        return 10*(8*L*L+12*L-8)/(3*L*L+2*L+7)
    def f1a(L):
        return 5
    def g1a(L):
        return 3*math.log10(L)
    def f1b(L):
        return 1.5
    def g1b(L):
        return L*1.3
    def f1c(L):
        return 10+L/10.0
    def g1c(L):
        return L

    def f1d(angle):
        return math.sin(angle/180*math.pi)*3+17
    def g1d(angle):
        return math.cos(angle/180*math.pi)*5+5

    manual_axis_data={1.0:'first',
                     2.0:'second',
                     3.0:'third',
                     3.1415:r'$\pi$',
                     4.0:'fourth',
                     5.0:'fifth',
                     6.0:'sixth',
                     7.0:'seventh',
                     8.0:'eigth',
                     9.0:'nineth',
                     10.0:'tenth'}


    c = canvas.canvas()
    #gg3=Nomo_Axis(func_f=f3,func_g=g3,start=1.0,stop=0.5,turn=-1,title='func 1',canvas=c,type='linear')
    gr1=Nomo_Axis(func_f=f1,func_g=g1,start=0.5,stop=1.0,turn=-1,title='func 1',
                  canvas=c,type='linear',side='left')
    gr11=Nomo_Axis(func_f=f1,func_g=g1,start=0.5,stop=1.0,turn=-1,title='func 1',
                  canvas=c,type='linear',side='right')
    gr2=Nomo_Axis(func_f=f1a,func_g=g1a,start=1.0,stop=1e4,turn=-1,title='func 2',
                  canvas=c,type='log',side='left')
    gr22=Nomo_Axis(func_f=f1a,func_g=g1a,start=1.0,stop=1e4,turn=-1,title='func 2',
                  canvas=c,type='log',side='right')
    gr3=Nomo_Axis(func_f=f1b,func_g=g1b,start=1.0,stop=10,turn=-1,title='func 3',
                  canvas=c,type='manual point',
                  manual_axis_data=manual_axis_data,side='left')
    gr33=Nomo_Axis(func_f=f1b,func_g=g1b,start=1.0,stop=10,turn=-1,title='func 3',
                  canvas=c,type='manual point',
                  manual_axis_data=manual_axis_data,side='right')

    gr4=Nomo_Axis(func_f=f1c,func_g=g1c,start=1.0,stop=10,turn=-1,title='func 4',
                  canvas=c,type='manual line',
                  manual_axis_data=manual_axis_data,side='right')
    gr44=Nomo_Axis(func_f=f1c,func_g=g1c,start=1.0,stop=10,turn=-1,title='func 4',
                  canvas=c,type='manual line',
                  manual_axis_data=manual_axis_data,side='left')

    # for some reason, this does not work when stop is 359 ??
    gr5=Nomo_Axis(func_f=f1d,func_g=g1d,start=0.0,stop=300.0,turn=-1,title='func 1',
                  canvas=c,type='linear',side='right')
    #gg4=Nomo_Axis(func_f=f4,func_g=g4,start=0.5,stop=1.0,turn=-1,title='func 3',canvas=c,type='linear')
    c.writePDFfile("test_nomo_axis")
