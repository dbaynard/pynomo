#    PyNomo - nomographs with Python
#    Copyright (C) 2007  Leif Roschier
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
from numpy import *
from pyx import *
from nomo_axis import *

class Nomograph_N_lin:
    """
    Writes N parallel line nomographs
    """
    def __init__(self,functions,N):
        self.functions=functions
        self.N=N
        try:
            {'4': self._make_4_,
             '5': self._make_5_}[`N`]()
        except KeyError:
            print "N=%i is not defined" % N
        self.x_multiplier=self.functions['nomo_width']/N
        self.y_multiplier=self.functions['nomo_height']/(self._max_y_()-self._min_y_())
        self.Ry_min=self._min_y_()*1.2
        self.Ry_max=self._max_y_()*1.2
        print self.x_multiplier
        print self.y_multiplier

    def give_u_x(self,n):
        # n:th function
        return lambda value:self.x_func[n](value)*self.x_multiplier

    def give_u_y(self,n):
        return lambda value:self.y_func[n](value)*self.y_multiplier

    def give_R_x(self,n):
        # n:th function
        return lambda value:self.xR_func[n](value)*self.x_multiplier

    def give_R_y(self):
        # n:th function
        return self._give_R_y_

    def _give_R_y_(self,value):
        if value <= 0.5:
            result=self.Ry_min
        else:
            result=self.Ry_max
        return result

    def _make_4_(self):
        """ makes nomogram with 4 variables
        f1+f2+f3+f4=0
        """
        self.x_func={} # x coordinate to map points into canvas
        self.y_func={} # y coordinate to map points into canvas
        self.xR_func={} # turning-point axis
        self.x_func[1]=lambda u1:0
        self.x_func[2]=lambda u2:1
        self.x_func[3]=lambda u3:3
        self.x_func[4]=lambda u4:4
        self.xR_func[1]=lambda uR1:2
        self.y_func[1]=lambda u1:self.functions['f1'](u1)
        self.y_func[2]=lambda u2:-0.5*self.functions['f2'](u2)
        self.y_func[3]=lambda u3:0.5*self.functions['f3'](u3)
        self.y_func[4]=lambda u4:-self.functions['f4'](u4)
        # let's find maximum y-value for scaling

    def _make_5_(self):
        """ makes nomogram with 5 variables
        f1+f2+f3+f4+f5=0
        """
        self.x_func={} # x coordinate to map points into canvas
        self.y_func={} # y coordinate to map points into canvas
        self.xR_func={} # turning-point axis
        self.x_func[1]=lambda x1:0
        self.x_func[2]=lambda x2:1
        self.x_func[3]=lambda x3:3
        self.x_func[4]=lambda x4:5
        self.x_func[4]=lambda x5:6
        self.xR_func[1]=lambda xR1:2
        self.xR_func[2]=lambda xR1:2
        self.y_func[1]=lambda u1:self.functions['f1'](u1)
        self.y_func[2]=lambda u2:-0.5*self.functions['f2'](u2)
        self.y_func[3]=lambda u3:0.5*self.functions['f3'](u3)
        self.y_func[4]=lambda u4:-0.5*self.functions['f4'](u4)
        self.y_func[5]=lambda u5:self.functions['f5'](u5)

    def  _max_y_(self):
            Ns=range(self.N)

            max1=max([self.y_func[n+1](self.functions['u_max'][n]) for n in Ns])
            max2=max([self.y_func[n+1](self.functions['u_min'][n]) for n in Ns])
            print max(max1,max2)
            return max(max1,max2)
    def  _min_y_(self):
            Ns=range(self.N)
            print Ns
            min1=min([self.y_func[n+1](self.functions['u_max'][n]) for n in Ns])
            min2=min([self.y_func[n+1](self.functions['u_min'][n]) for n in Ns])
            print min(min1,min2)
            print [self.y_func[n+1](self.functions['u_max'][n]) for n in Ns]
            return min(min1,min2)



if __name__=='__main__':
    functions={'u_min':array([1.0,1.0,2.0,2.0]),
               'u_max':array([10.0,10.0,20.0,20.0]),
               'f1':lambda u1:u1,
               'f2':lambda u2:u2,
               'f3':lambda u3:u3,
               'f4':lambda u4:-u4,
               'nomo_width':10.0,
               'nomo_height':10.0}
    nomo=Nomograph_N_lin(functions,4)
    c = canvas.canvas()
    ax1=Nomo_Axis(func_f=nomo.give_u_x(1),func_g=nomo.give_u_y(1),
                  start=functions['u_min'][0],stop=functions['u_max'][0],
                  turn=-1,title='f1',canvas=c,type='linear',
                  tick_levels=3,tick_text_levels=1)
    ax2=Nomo_Axis(func_f=nomo.give_u_x(2),func_g=nomo.give_u_y(2),
                  start=functions['u_min'][1],stop=functions['u_max'][1],
                  turn=1,title='f2',canvas=c,type='linear',
                  tick_levels=3,tick_text_levels=1)
    ax3=Nomo_Axis(func_f=nomo.give_u_x(3),func_g=nomo.give_u_y(3),
                  start=functions['u_min'][2],stop=functions['u_max'][2],
                  turn=-1,title='f3',canvas=c,type='linear',
                  tick_levels=3,tick_text_levels=1)
    ax4=Nomo_Axis(func_f=nomo.give_u_x(4),func_g=nomo.give_u_y(4),
                  start=functions['u_min'][3],stop=functions['u_max'][3],
                  turn=-1,title='f4',canvas=c,type='linear',
                  tick_levels=3,tick_text_levels=1)
    R=Nomo_Axis(func_f=nomo.give_R_x(1),func_g=lambda a:a,
                  start=-5,stop=10,
                  turn=-1,title='R',canvas=c,type='linear',
                  tick_levels=0,tick_text_levels=0)
    #c.stroke(path.line(nomo.give_R_x(1), nomo.Ry_min, nomo.give_R_x(1), nomo.Ry_max))
    c.writePDFfile("nomolin")
