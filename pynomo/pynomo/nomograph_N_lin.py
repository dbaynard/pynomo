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
        self.y_multiplier=self.functions['nomo_height']/self._max_y_()

    def give_u_x(self,n,value):
        # n:th function
        return self.x_func[n](value)*self.x_multiplier

    def give_u_y(self,n,value):
        return self.y_func[n](value)*self.y_multiplier

    def give_R_x(self,n):
        # n:th function
        return self.xR_func[n](value)*self.x_multiplier

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
            """
            print array([[self.functions['u_min'][idx],self.functions['u_max'][idx]]
                            for idx in Ns])

            print        [(n+1,x)
                            for n in Ns
                            for x in array([[self.functions['u_min'][idx]]
                            for idx in Ns])]
                            """

            max1=max(max([self.y_func[n+1](x)
                            for n in Ns
                            for x in array([[self.functions['u_min'][idx]]
                            for idx in Ns])]))
            max2=max(max([self.y_func[n+1](x)
                            for n in Ns
                            for x in array([[self.functions['u_max'][idx]]
                            for idx in Ns])]))
            return max(max1,max2)



if __name__=='__main__':
    functions={'u_min':array([1.0,1.0,2.0,2.0]),
               'u_max':array([10.0,10.0,20.0,20.0]),
               'f1':lambda u1:u1**2,
               'f2':lambda u2:u2**2,
               'f3':lambda u3:u3**2,
               'f4':lambda u4:u4**2,
               'nomo_width':10.0,
               'nomo_height':10.0}
    nomo=Nomograph_N_lin(functions,4)
