#
#    This file is part of PyNomo -
#    a program to create nomographs with Python (http://pynomo.sourceforge.net/)
#
#    Copyright (C) 2007-2008  Leif Roschier  <lefakkomies@users.sourceforge.net>
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
import random

class Nomo_Axis:
    """
    Main class to draw axis.
    """
    def __init__(self,func_f,func_g,start,stop,turn,title,canvas,type='linear',
                 text_style='normal',title_x_shift=0,title_y_shift=0.25,
                 tick_levels=4,tick_text_levels=3,
                 text_color=color.rgb.black, axis_color=color.rgb.black,
                 manual_axis_data={},axis_appear={},side='left',
                 base_start=None, base_stop=None):
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
                             'text_distance_3':1.0/4,
                             'text_distance_4':1.0/4,
                             'grid_length_0':3.0/4,
                             'grid_length_1':0.9/4,
                             'grid_length_2':0.5/4,
                             'grid_length_3':0.3/4,
                             'grid_length_4':0.3/4,
                             'text_size_0': text.size.small,
                             'text_size_1': text.size.scriptsize,
                             'text_size_2': text.size.tiny,
                             'text_size_3': text.size.tiny,
                             'text_size_4': text.size.tiny,
                             'text_size_log_0': text.size.small,
                             'text_size_log_1': text.size.tiny,
                             'text_size_log_2': text.size.tiny,
                             'text_size_manual': text.size.small,
                             'title_distance_center':0.5,
                             'title_opposite_tick':True,
                             'title_draw_center':False,
                             'text_format':"$%3.2f$"}
        self.axis_appear=axis_appear_default_values
        self.axis_appear.update(axis_appear)

        if type=='log':
            self._make_log_axis_(start=start,stop=stop,f=func_f,g=func_g,turn=turn)
        if type=='linear':
            self._make_linear_axis_(start=start,stop=stop,f=func_f,g=func_g,turn=turn,
                                    base_start=base_start,base_stop=base_stop)
        if type=='manual point':
            self._make_manual_axis_circle_(manual_axis_data)
        if type=='manual line':
            self._make_manual_axis_line_(manual_axis_data)

        self.draw_axis(canvas)
        if self.axis_appear['title_draw_center']:
            self._draw_title_center_(canvas)
        else:
            self._draw_title_top_(canvas)

    def _test_tick_(self,u,tick,scale_max):
        """ tests if it is time to put a tick
        u=value
        tick=step to put ticks
        scale_max=scale from min to max
        for example:
        u=0.2, tick=0.1 gives True
        u=0.25, tick=0.1 gives False """
        closest_number=_find_closest_tick_number_(u,tick)
        result=False
        if math.fabs(u-closest_number)< (scale_max*1e-6):
            result=True
        return result
        #return math.fabs(math.modf(u/tick)[0]) < (scale_max*1e-5) or math.fabs((math.modf(u/tick)[0]-1)) < (scale_max*1e-8)

#    def _find_closest_tick_number_(self,number,tick_divisor):
#        """
#        finds closest number with integer number of divisors from zero
#        """
#        n=number//tick_divisor
#        tick_number=n*tick_divisor
#        error=math.fabs(tick_number-number)
#        if math.fabs(((n+1)*tick_divisor)-number)< error:
#            tick_number=(n+1)*tick_divisor
#            error=math.fabs(tick_number-number)
#        if math.fabs(((n-1)*tick_divisor)-number)< error:
#            tick_number=(n-1)*tick_divisor
#            error=math.fabs(tick_number-number)
#        return tick_number


    def _make_linear_axis_old_(self,start,stop,f,g,turn=1):
        """
        OBSOLETE, use _make_linear_axis_
        Makes a linear scale according to functions f(u) and g(u)
        with values u in range [start, stop].
        """
        line = path.path(path.moveto(f(start), g(start)))
        thin_line=path.path(path.moveto(f(start), g(start)))
        # for numerical derivative to find angle
        du=math.fabs(start-stop)*1e-6
        dy=(g(start+du)-g(start))
        #self._determine_turn_()
        turn=_determine_turn_(f=self.func_f,g=self.func_g,start=self.start,
                              stop=self.stop,side=self.side)
        #turn=self.turn
        # which number to divide. how many decades there are
        ##scale_max=10.0**math.ceil(math.log10(math.fabs(start-stop)))
        scale_max=10.0**round(math.log10(math.fabs(start-stop)))
        tick_min=scale_max/(500.0)
        tick_max=scale_max/10.0
        tick_1=scale_max/20.0
        tick_2=scale_max/100.0
        start_new=_find_closest_tick_number_(start,tick_min)
        stop_new=_find_closest_tick_number_(stop,tick_min)
        #print "tick_min %f"%tick_min
        #print "start_new %f"%start_new
        #print "stop_new %f"%stop_new
        texts=list([])
        steps=round(math.fabs(start_new-stop_new)/tick_min)+1
        for u in scipy.linspace(start_new,stop_new,steps):
            #print u
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

    def _make_linear_axis_(self,start,stop,f,g,turn=1,base_start=None,base_stop=None):
        """
        Makes a linear scale according to functions f(u) and g(u)
        with values u in range [start, stop].
        """
        # line lists
        line = path.path(path.moveto(f(start), g(start)))
        thin_line=path.path(path.moveto(f(start), g(start)))
        # text list
        texts=[]
        # let's find tick positions
        tick_0_list,tick_1_list,tick_2_list,tick_3_list,tick_4_list,start_ax,stop_ax=\
        find_linear_ticks(start,stop,base_start,base_stop)
        # let's find tick angles
        dx_units_0,dy_units_0,angles_0=find_tick_directions(tick_0_list,f,g,self.side,start,stop)
        dx_units_1,dy_units_1,angles_1=find_tick_directions(tick_1_list,f,g,self.side,start,stop)
        dx_units_2,dy_units_2,angles_2=find_tick_directions(tick_2_list,f,g,self.side,start,stop)
        dx_units_3,dy_units_3,angles_3=find_tick_directions(tick_3_list,f,g,self.side,start,stop)
        dx_units_4,dy_units_4,angles_4=find_tick_directions(tick_4_list,f,g,self.side,start,stop)

        # tick level 0
        if self.tick_levels>0:
            self._make_tick_lines_(tick_0_list,line,f,g,dx_units_0,dy_units_0,
                              self.axis_appear['grid_length_0'])
        # text level 0
        if self.tick_text_levels>0:
            self._make_texts_(tick_0_list,texts,f,g,dx_units_0,dy_units_0,angles_0,
                     self.axis_appear['text_distance_0'],
                     self.axis_appear['text_size_0'])
        # tick level 1
        if self.tick_levels>1:
            self._make_tick_lines_(tick_1_list,line,f,g,dx_units_1,dy_units_1,
                              self.axis_appear['grid_length_1'])
        # text level 1
        if self.tick_text_levels>1:
            self._make_texts_(tick_1_list,texts,f,g,dx_units_1,dy_units_1,angles_1,
                     self.axis_appear['text_distance_1'],
                     self.axis_appear['text_size_1'])
        # tick level 2
        if self.tick_levels>2:
            self._make_tick_lines_(tick_2_list,line,f,g,dx_units_2,dy_units_2,
                              self.axis_appear['grid_length_2'])
        # text level 2
        if self.tick_text_levels>2:
            self._make_texts_(tick_2_list,texts,f,g,dx_units_2,dy_units_2,angles_2,
                     self.axis_appear['text_distance_2'],
                     self.axis_appear['text_size_2'])
        # tick level 3
        if self.tick_levels>3:
            self._make_tick_lines_(tick_3_list,thin_line,f,g,dx_units_3,dy_units_3,
                              self.axis_appear['grid_length_3'])
        # text level 3
        if self.tick_text_levels>3:
            self._make_texts_(tick_3_list,texts,f,g,dx_units_3,dy_units_3,angles_3,
                     self.axis_appear['text_distance_3'],
                     self.axis_appear['text_size_3'])
        # tick level 4
        if self.tick_levels>4:
            self._make_tick_lines_(tick_4_list,thin_line,f,g,dx_units_4,dy_units_4,
                              self.axis_appear['grid_length_4'])
        # text level 4
        if self.tick_text_levels>4:
            self._make_texts_(tick_4_list,texts,f,g,dx_units_4,dy_units_4,angles_4,
                     self.axis_appear['text_distance_4'],
                     self.axis_appear['text_size_4'])
        # make main line
        self._make_main_line_(start,stop,line,f,g)

        self.line=line
        self.thin_line=thin_line
        self.texts=texts

    def _make_log_axis_(self,start,stop,f,g,turn=1):
        """
        Makes a log scale
        """
        # line lists
        line = path.path(path.moveto(f(start), g(start)))
        thin_line=path.path(path.moveto(f(start), g(start)))
        # text list
        texts=[]
        # let's find tick positions
        tick_0_list,tick_1_list,tick_2_list,start_ax,stop_ax=\
        find_log_ticks(start,stop)
        # let's find tick angles
        dx_units_0,dy_units_0,angles_0=find_tick_directions(tick_0_list,f,g,self.side,start,stop)
        dx_units_1,dy_units_1,angles_1=find_tick_directions(tick_1_list,f,g,self.side,start,stop)
        dx_units_2,dy_units_2,angles_2=find_tick_directions(tick_2_list,f,g,self.side,start,stop)

        # tick level 0
        if self.tick_levels>0:
            self._make_tick_lines_(tick_0_list,line,f,g,dx_units_0,dy_units_0,
                              self.axis_appear['grid_length_0'])
        # text level 0
        if self.tick_text_levels>0:
            self._make_texts_(tick_0_list,texts,f,g,dx_units_0,dy_units_0,angles_0,
                     self.axis_appear['text_distance_0'],
                     self.axis_appear['text_size_log_0'])
        # tick level 1
        if self.tick_levels>1:
            self._make_tick_lines_(tick_1_list,line,f,g,dx_units_1,dy_units_1,
                              self.axis_appear['grid_length_1'])
        # text level 1
        if self.tick_text_levels>1:
            self._make_texts_(tick_1_list,texts,f,g,dx_units_1,dy_units_1,angles_1,
                     self.axis_appear['text_distance_1'],
                     self.axis_appear['text_size_log_1']) # smaller with log axis
        # tick level 2
        if self.tick_levels>2:
            self._make_tick_lines_(tick_2_list,line,f,g,dx_units_2,dy_units_2,
                              self.axis_appear['grid_length_2'])
        # text level 2
        if self.tick_text_levels>2:
            self._make_texts_(tick_2_list,texts,f,g,dx_units_2,dy_units_2,angles_2,
                     self.axis_appear['text_distance_2'],
                     self.axis_appear['text_size_log_2'])

        # make main line
        self._make_main_line_(start,stop,line,f,g)

        self.line=line
        self.thin_line=thin_line
        self.texts=texts

    def _make_texts_(self,tick_list,text_list,f,g,dx_units,dy_units,angles,
                     text_distance,text_size):
        """
        makes list of text definitions
        """
        for idx,u in enumerate(tick_list):
            if dy_units[idx]<0:
                text_attr=[text.valign.middle,text.halign.right,text_size,trafo.rotate(angles[idx])]
            else:
                text_attr=[text.valign.middle,text.halign.left,text_size,trafo.rotate(angles[idx])]
            text_list.append((self._put_text_(u),f(u)+text_distance*dy_units[idx],
                              g(u)-text_distance*dx_units[idx],text_attr))

    def _make_tick_lines_(self,tick_list,tick_lines,f,g,dx_units,dy_units,
                          tick_length):
        """
        appends to list tick_list lines to be tick markers
        """
        for idx,u in enumerate(tick_list):
            tick_lines.append(path.moveto(f(u), g(u)))
            tick_lines.append(path.lineto(f(u)+tick_length*dy_units[idx],
                                          g(u)-tick_length*dx_units[idx]))

    def _make_main_line_(self,start,stop,main_line,f,g):
        """
        draws the major skeleton of axis
        """
        if start>stop:
            start,stop=stop,start
        du=math.fabs(stop-start)*1e-12
        # approximate line length is found
        line_length_straigth=math.sqrt((f(start)-f(stop))**2+(g(start)-g(stop))**2)
        random.seed(0.0) # so that mistakes always the same
        for dummy in range(100): # for case if start = stop
            first=random.uniform(start,stop)
            second=random.uniform(start,stop)
            temp=math.sqrt((f(first)-f(second))**2+(g(first)-g(second))**2)
            if temp>line_length_straigth:
                line_length_straigth=temp
                #print "length: %f"%line_length_straigth
        sections=350.0 # about number of sections
        section_length=line_length_straigth/sections
        u=start
        laskuri=1
        main_line.append(path.moveto(f(start), g(start)))
        while True:
            if u<stop:
                main_line.append(path.lineto(f(u), g(u)))
                dx=(f(u+du)-f(u))
                dy=(g(u+du)-g(u))
                dl=math.sqrt(dx**2+dy**2)
                if dl>0:
                    delta_u=du*section_length/dl
                else:
                    delta_u=du
                # in order to avoid too slow derivatives
                if math.fabs(stop-start)<(delta_u*100.0):
                    delta_u=math.fabs(stop-start)/500.0
                u+=delta_u

            else:
                main_line.append(path.lineto(f(stop), g(stop)))
                break

    def _find_center_value_(self,start,stop,f,g):
        """
        finds value of approximate centerpoint of line
        """
        if start>stop:
            start,stop=stop,start
        du=math.fabs(stop-start)*1e-12
        # approximate line length is found
        line_length_straigth=math.sqrt((f(start)-f(stop))**2+(g(start)-g(stop))**2)
        random.seed(0.0) # so that mistakes always the same
        for dummy in range(100): # for case if start = stop
            first=random.uniform(start,stop)
            second=random.uniform(start,stop)
            temp=math.sqrt((f(first)-f(second))**2+(g(first)-g(second))**2)
            if temp>line_length_straigth:
                line_length_straigth=temp
                #print "length: %f"%line_length_straigth
        sections=350.0 # about number of sections
        section_length=line_length_straigth/sections
        # let's start length
        u=start
        length=0.0
        counter=0
        while True:
            if u<stop:
                dx=(f(u+du)-f(u))
                dy=(g(u+du)-g(u))
                dl=math.sqrt(dx**2+dy**2)
                if dl>0:
                    delta_u=du*section_length/dl
                else:
                    delta_u=du
                length+=section_length
                u+=delta_u
            else:
                break
            #counter+=1
            #print counter
        #print "length %g" % length
        # let's find middlepoint
        u=start
        length_0=0.0
        counter=0
        while True:
            if length_0<(length/2.0):
                dx=(f(u+du)-f(u))
                dy=(g(u+du)-g(u))
                dl=math.sqrt(dx**2+dy**2)
                if dl>0:
                    delta_u=du*section_length/dl
                else:
                    delta_u=du
                length_0+=section_length
                u+=delta_u
            else:
                break
            counter+=1
            #print counter
            #print length_0
        return u


    def _make_log_axis_old(self,start,stop,f,g,turn=1):
        """
        OBSOLETE
        draw logarithmic axis
        """
        # for numerical derivative to find angle
        du=math.fabs(start-stop)*1e-6
        #self._determine_turn_()
        turn=_determine_turn_(f=self.func_f,g=self.func_g,start=self.start,
                              stop=self.stop,side=self.side)
        #turn=self.turn
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
                if (u-min)>0: # to avoid too big du values
                    du=(u-min)*1e-6
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
        #self._determine_turn_()
        turn=_determine_turn_(f=self.func_f,g=self.func_g,start=self.start,
                              stop=self.stop,side=self.side)
        #turn=self.turn
        texts=list([])
        line = path.path(path.moveto(f(self.start), g(self.start)))
        thin_line=path.path(path.moveto(f(self.start), g(self.start)))
        for number, label_string in manual_axis_data.iteritems():
            text_distance=1.0/4
            text_size=self.axis_appear['text_size_manual']
            if self.side=='left':
                text_attr=[text.valign.middle,text.halign.right,text_size]
                texts.append((label_string,f(number)-text_distance,
                          g(number),text_attr))
            else:
                text_attr=[text.valign.middle,text.halign.left,text_size]
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
        #self._determine_turn_()
        turn=_determine_turn_(f=self.func_f,g=self.func_g,start=self.start,
                              stop=self.stop,side=self.side)
        #turn=self.turn
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
            text_size=self.axis_appear['text_size_manual']
            if dy<=0:
                text_attr=[text.valign.middle,text.halign.left,text_size,trafo.rotate(angle)]
            else:
                text_attr=[text.valign.middle,text.halign.right,text_size,trafo.rotate(angle)]
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

    def _draw_title_top_(self,c):
        """
         make title to top
        """
        best_u=self.start
        y_max=self.func_g(best_u)
        if self.func_g(self.stop)>y_max:
            y_max=self.func_g(self.stop)
            best_u=self.stop
        for dummy in range(500):
            number=random.uniform(min(self.start,self.stop),max(self.start,self.stop))
            y_value=self.func_g(number)
            if y_value>y_max:
                y_max=y_value
                best_u=number
        c.text(self.func_f(best_u)+self.title_x_shift,
                self.func_g(best_u)+self.title_y_shift,
                self.title,[text.halign.center])

#        # find out if start or stop has higher y-value
#        if self.func_g(self.stop)>self.func_g(self.start):
#            c.text(self.func_f(self.stop)+self.title_x_shift,
#                    self.func_g(self.stop)+self.title_y_shift,
#                    self.title,[text.halign.center])
#        else:
#            c.text(self.func_f(self.start)+self.title_x_shift,
#                    self.func_g(self.start)+self.title_y_shift, self.title,
#                    [text.halign.center])

    def _draw_title_center_(self,c):
        """
        draws axis title to the axis center
        """
        f=self.func_f
        g=self.func_g
        u_mid=self._find_center_value_(self.start,self.stop,f,g)
        #u_mid=(self.start+self.stop)/2.0
        #x_start=f(self.start)
        #x_stop=f(self.stop)
        #y_start=g(self.start)
        #y_stop=g(self.stop)
        #center_x=(x_start+x_stop)/2.0
        #center_y=(y_start+y_stop)/2.0
        center_x=f(u_mid)
        center_y=g(u_mid)

        du=math.fabs(self.start-self.stop)*1e-6
        turn=self.turn
        if not self.axis_appear['title_opposite_tick']:
            turn=turn*(-1)
        dx=(f(u_mid+du)-f(u_mid))*turn
        dy=(g(u_mid+du)-g(u_mid))*turn
        dx_unit=dx/math.sqrt(dx**2+dy**2)
        dy_unit=dy/math.sqrt(dx**2+dy**2)
        if dy_unit!=0:
            angle=-math.atan(dx_unit/dy_unit)*180/math.pi+90.0
        else:
            angle=0-90.0
        angle = (angle+90)%180-90
        text_distance=self.axis_appear['title_distance_center']
        c.text(center_x-text_distance*dy_unit,
               center_y+text_distance*dx_unit,
               self.title,[text.halign.center,trafo.rotate(angle)])
        #text_attr=[text.valign.middle,text.halign.left,text.size.small,trafo.rotate(angle)]
        #texts.append((label_string,f(number)-text_distance*dy_unit,g(number)+text_distance*dx_unit,text_attr))

    def _put_text_(self,u):
        if self.text_style=='oldstyle':
            return r"$\oldstylenums{%3.2f}$ " %u
        else:
            #return r"$%3.2f$ " %u
            return self.axis_appear['text_format'] % u

#    def _determine_turn_(self):
#        """
#         determines if we are going upwards or downwards at start
#        """
#        g=self.func_g
#        f=self.func_f
#        start=self.start
#        stop=self.stop
#        du=(stop-start)*1e-6
#        dy=(g(start+du)-g(start))
#        if dy<=0 and self.side=='left':
#            self.turn=1.0
#        if dy>0 and self.side=='left':
#            self.turn=-1.0
#        if dy<=0 and self.side=='right':
#            self.turn=-1.0
#        if dy>0 and self.side=='right':
#            self.turn=1.0

def _determine_turn_(f,g,start,stop,side):
    """
     determines if we are going upwards or downwards at start
    _determine_turn_(f=self.func_f,g=self.func_g,start=self.start,
                     stop=self.stop,side=self.side)
    """
    du=(stop-start)*1e-6
    dy=(g(start+du)-g(start))
    if dy<=0 and side=='left':
        turn=1.0
    if dy>0 and side=='left':
        turn=-1.0
    if dy<=0 and side=='right':
        turn=-1.0
    if dy>0 and side=='right':
        turn=1.0
    return turn


def _find_closest_tick_number_(number,tick_divisor):
    """
    finds closest number with integer number of divisors from zero
    """
    n=number//tick_divisor
    tick_number=n*tick_divisor
    error=math.fabs(tick_number-number)
    if math.fabs(((n+1)*tick_divisor)-number)< error:
        tick_number=(n+1)*tick_divisor
        error=math.fabs(tick_number-number)
    if math.fabs(((n-1)*tick_divisor)-number)< error:
        tick_number=(n-1)*tick_divisor
        error=math.fabs(tick_number-number)
    return tick_number

def find_linear_ticks(start,stop,base_start=None,base_stop=None):
    """
    finds tick values for linear axis
    """
    if start>stop:
        start,stop=stop,start
    if (base_start != None) and (base_stop != None):
        scale_max=10.0**math.ceil(math.log10(math.fabs(base_start-base_stop))-0.5)
    else:
        scale_max=10.0**math.ceil(math.log10(math.fabs(start-stop))-0.5)
    tick_0=scale_max/10.0
    tick_1=scale_max/20.0
    tick_2=scale_max/100.0
    tick_3=scale_max/500.0
    tick_4=scale_max/1000.0
    tick_0_list=[]
    tick_1_list=[]
    tick_2_list=[]
    tick_3_list=[]
    tick_4_list=[]
    start_major=_find_closest_tick_number_(start,tick_0)
    stop_major=_find_closest_tick_number_(stop,tick_0)
    #print "scale_max %f"%scale_max
    #print "start %f"%start
    #print "start_major %f"%start_major
    #print "stop_major %f"%stop_major
    start_ax=None
    stop_ax=None
    for step in range(0,9001):
        number=start_major+step*tick_4
        if number>=start and number<=(stop*(1+1e-12)): # stupid numerical correction
            if start_ax==None:
                start_ax=number
            stop_ax=number
            if step%100==0:
                tick_0_list.append(number)
            if step%50==0 and step%100!=0:
                tick_1_list.append(number)
            if step%10==0 and step%50!=0 and step%100!=0:
                tick_2_list.append(number)
            if step%5==0 and step%10!=0 and step%50!=0 and step%100!=0:
                tick_3_list.append(number)
            if step%1==0 and step%5!=0 and step%10!=0 and step%50!=0 and step%100!=0:
                tick_4_list.append(number)
    #print tick_0_list
    #print tick_1_list
    #print tick_2_list
    return tick_0_list,tick_1_list,tick_2_list,tick_3_list,tick_4_list,\
            start_ax,stop_ax

def find_log_ticks(start,stop):
    """
    finds tick values for linear axis
    """
    if (start<stop):
        min,max=start,stop
    else:
        min,max=stop,start
    #lists for ticks
    tick_0_list=[]
    tick_1_list=[]
    tick_2_list=[]
    max_decade=math.ceil(math.log10(max))
    min_decade=math.floor(math.log10(min))
    start_ax=None
    stop_ax=None
    for decade in scipy.arange(min_decade,max_decade+1,1):
        #for number in scipy.concatenate((scipy.arange(1,2,0.2),scipy.arange(2,3,0.5),scipy.arange(3,10,1))):
        for number in [1,1.2,1.4,1.6,1.8,2.0,2.5,3,4,5,6,7,8,9]:
            u=number*10.0**decade
            if u>=min and u<=max:
                if start_ax==None:
                    start_ax=number
                stop_ax=number
                if number==1:
                    tick_0_list.append(u)
                if number in [2,3,4,5,6,7,8,9]:
                    tick_1_list.append(u)
                if number in [1.2,1.4,1.6,1.8,2.5]:
                    tick_2_list.append(u)
    #print tick_0_list
    #print tick_1_list
    #print tick_2_list
    return tick_0_list,tick_1_list,tick_2_list,start_ax,stop_ax


def find_tick_directions(list,f,g,side,start,stop):
    """
    finds tick directions and angles
    """
    angles=[]
    # following two values make unit vector
    dx_units=[]
    dy_units=[]
    turn=_determine_turn_(f=f,g=g,start=start,stop=stop,side=side)
    for idx,u in enumerate(list):
        if u!=list[-1]:
            du=(list[idx+1]-list[idx])*1e-6
        else:
            if len(list)>1:
                du=(list[-1]-list[-2])*1e-6
            else: # only one element in list
                du=(stop-start)*1e-6
        #print u
        dx=(f(u+du)-f(u))*turn
        dy=(g(u+du)-g(u))*turn
        dx_unit=dx/math.sqrt(dx**2+dy**2)
        dy_unit=dy/math.sqrt(dx**2+dy**2)
        if dy_unit!=0:
            angle=-math.atan(dx_unit/dy_unit)*180/math.pi
        else:
            angle=0
        dx_units.append(dx_unit)
        dy_units.append(dy_unit)
        angles.append(angle)
    return dx_units,dy_units,angles

## Testing
if __name__=='__main__':
    #find_log_ticks(990.0,999.0)
    #find_log_ticks(-33,52)
    find_log_ticks(0.12,10.0)
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
    gr5=Nomo_Axis(func_f=f1d,func_g=g1d,start=0.0,stop=360.0,turn=-1,title='func 1',
                  canvas=c,type='linear',side='left')

    gr10=Nomo_Axis(func_f=lambda u:20.0,func_g=lambda x:(x+12.5)/2.0,start=-17.1757381043,stop=19.5610135785,turn=-1,title='test neg.',
                  canvas=c,type='linear',side='right')

    gr11=Nomo_Axis(func_f=lambda u:25.0,func_g=lambda x:(x+12.5)/5.0,start=-40.0,stop=120.0,turn=-1,title='test neg.',
                  canvas=c,type='linear',side='right')
    #gg4=Nomo_Axis(func_f=f4,func_g=g4,start=0.5,stop=1.0,turn=-1,title='func 3',canvas=c,type='linear')
    c.writePDFfile("test_nomo_axis")
