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
from math import *
import scipy

class Nomo_Grid:
    """
    class to make grids
    """
    def __init__(self,func_f,func_g,canvas,data={}):
        self.f=func_f
        self.g=func_g
        self.canvas=canvas
        data_default_values={'u_start':0.0,
                             'u_stop':80.0,
                             'v_start':0.0,
                             'v_stop':1.0*pi/2,
                             'u_values':[0.0,0.25*pi/2,0.5*pi/2,0.75*pi/2,1.0*pi/2],
                             'v_values':[0.0,0.25*pi/2,0.5*pi/2,0.75*pi/2,1.0*pi/2]}
        self.grid_data=data_default_values
        self.grid_data.update(data)
        print self.grid_data
        self._draw_line_u_()
        self._draw_line_v_()

    def _draw_line_u_(self):
        """
        draws a single line from start to stop for variable u
        """
        start=self.grid_data['u_start']
        stop=self.grid_data['u_stop']
        for v in self.grid_data['v_values']:
            f_here,g_here=self._make_u_funcs_(v)
            self._draw_line_(f_here,g_here,start,stop,`v`)

    def _draw_line_v_(self):
        """
        draws a single line from start to stop for variable v
        """
        start=self.grid_data['v_start']
        stop=self.grid_data['v_stop']
        for u in self.grid_data['u_values']:
            f_here,g_here=self._make_v_funcs_(u)
            self._draw_line_(f_here,g_here,start,stop,`u`)

    def _make_u_funcs_(self,v_value):
        """
        copied trick to solve function defitions inside loop
        (I could not figure out how to use lambda...)
        """
        def f(u): return self.f(u,v_value)
        def g(u): return self.g(u,v_value)
        return f,g

    def _make_v_funcs_(self,u_value):
        """
        copied trick to solve function defitions inside loop
        (I could not figure out how to use lambda...)
        """
        def f(v): return self.f(u_value,v)
        def g(v): return self.g(u_value,v)
        return f,g

    def _draw_line_(self,f,g,start,stop,title):
        du=fabs(start-stop)*1e-9
        line_length_straigth1=sqrt((f(start)-f(stop))**2+(g(start)-g(stop))**2)
        diff=stop-start
        line_length_straigth2=sqrt((f(start+diff/3.0)-f(stop-diff/3.0))**2+\
                                   (g(start+diff/3.0)-g(stop-diff/3.0))**2)
        line_length_straigth=max(line_length_straigth1,line_length_straigth2)
        sections=300.0 # about number of sections
        section_length=line_length_straigth/sections
        line = path.path(path.moveto(f(start), g(start)))
        u=start
        laskuri=1
        while u<stop:
            dx=(f(u+du)-f(u))
            dy=(g(u+du)-g(u))
            dl=sqrt(dx**2+dy**2)
            delta_u=du*section_length/dl
            u+=delta_u
            #print u,stop
            laskuri=laskuri+1
            line.append(path.lineto(f(u), g(u)))
        self.canvas.stroke(line, [style.linewidth.normal])
        # start number
        dx=(f(start+du)-f(u))
        dy=(g(start+du)-g(u))
        dx_unit=dx/sqrt(dx**2+dy**2)
        dy_unit=dy/sqrt(dx**2+dy**2)
        if dy_unit!=0:
            angle=-atan(dx_unit/dy_unit)*180/pi
        else:
            angle=0
        text_distance=0.5
        if dy<=0:
            text_attr=[text.valign.top,text.halign.center,text.size.small,trafo.rotate(angle+90)]
        else:
            text_attr=[text.valign.top,text.halign.center,text.size.small,trafo.rotate(angle-90)]
        self.canvas.text(f(start)-text_distance*dy_unit,
                         g(start)-text_distance*dx_unit,
                         title,text_attr)
        self.canvas.fill(path.circle(f(start), g(start), 0.02))
        print "line drawn"


if __name__=='__main__':
    # functions for solartime
    def gamma(day):
        return 2*pi/365.0*(day-1+0.5)
    def eq_time(day):
        gamma0=gamma(day)
        return 229.18*(0.000075+0.001868*cos(gamma0)-0.032077*sin(gamma0)\
                       -0.014615*cos(2*gamma0)-0.040849*sin(2*gamma0))
    def eq_declination(day):
        g0=gamma(day)
        return 0.006918-0.399912*cos(g0)+0.070257*sin(g0)-0.006758*cos(2*g0)\
                +0.000907*sin(2*g0)-0.002697*cos(3*g0)+0.00148*sin(3*g0)
    def tst(day,hour):
        return hour*60.0+eq_time(day)
    def ha(day,hour):
        return tst/4.0-180.0


    def f(lat,day):
        dec=eq_declination(day)
        return 45*(sin(lat*pi/180.0)*sin(dec))/(1.0+(sin(lat*pi/180.0)*sin(dec)))
    def g(lat,day):
        dec=eq_declination(day) # in radians
        return 45*(cos(lat*pi/180.0)*cos(dec))/(1.0+cos(lat*pi/180.0)*cos(dec))

    data={   'u_start':0.0, # latitude
             'u_stop':90.0,
             'v_start':0.0, # day
             'v_stop':360.0,
             'u_values':[0.0,10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0],
             #'v_values':[0.0,60.0,120.0,180.0,240.0,300.0,365.0]
             'v_values':range(0.0,375.0,10.0)}

    c = canvas.canvas()
    gridi=Nomo_Grid(f,g,c,data=data)
    c.writePDFfile("test_nomo_grid")