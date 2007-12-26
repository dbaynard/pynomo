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
                             'u_stop':1.0,
                             'v_start':0.0,
                             'v_stop':1.0,
                             'u_values':[0.0,0.5,1.0],
                             'v_values':[0.0,0.5,1.0]}
        self.grid_data=data_default_values
        self.grid_data.update(data)
        self._draw_line_u_()
        self._draw_line_v_()

    def _draw_line_u_(self):
        """
        draws a single line from start to stop for variable u
        """
        start=self.grid_data['u_start']
        stop=self.grid_data['u_stop']
        for v in self.grid_data['v_values']:
            print v
            f_here,g_here=self._make_u_funcs_(v)
            self._draw_line_(f_here,g_here,start,stop)

    def _draw_line_v_(self):
        """
        draws a single line from start to stop for variable v
        """
        start=self.grid_data['v_start']
        stop=self.grid_data['v_stop']
        for u in self.grid_data['u_values']:
            print u
            f_here,g_here=self._make_v_funcs_(u)
            self._draw_line_(f_here,g_here,start,stop)

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

    def _draw_line_(self,f,g,start,stop):
        du=fabs(start-stop)*1e-6
        line_length_straigth=sqrt((f(start)-f(stop))**2+(g(start)-g(stop))**2)
        sections=300.0 # about number of sections
        section_length=line_length_straigth/sections
        line = path.path(path.moveto(f(start), g(start)))
        u=start
        while u<stop:
            dx=(f(u+du)-f(u))
            dy=(g(u+du)-g(u))
            dl=sqrt(dx**2+dy**2)
            delta_u=du*section_length/dl
            u+=delta_u
            line.append(path.lineto(f(u), g(u)))
        self.canvas.stroke(line, [style.linewidth.normal])

if __name__=='__main__':
    def f(a,b):
        return sin(a)+cos(b)
    def g(a,b):
        return 2*cos(a)-sin(b)

    c = canvas.canvas()
    gridi=Nomo_Grid(f,g,c)
    c.writePDFfile("test_nomo_grid")