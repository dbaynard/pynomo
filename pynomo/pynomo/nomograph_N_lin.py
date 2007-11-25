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
        # initial transformation = no transformation
        self.alpha1=1.0
        self.beta1=0.0
        self.gamma1=0.0
        self.alpha2=0.0
        self.beta2=1.0
        self.gamma2=0.0
        self.alpha3=0.0
        self.beta3=0.0
        self.gamma3=0.0
        try:
            {'4': self._make_4_,
             '5': self._make_5_}[`N`]()
        except KeyError:
            print "N=%i is not defined" % N
        self.R_padding=1.3
        self.x_multiplier=self.functions['nomo_width']/N
        self.y_multiplier=self.functions['nomo_height']/(self._max_y_()-self._min_y_())/self.R_padding
        self._make_transformation_matrix_()
        self.Ry_min=self._min_y_()*self.R_padding*self.y_multiplier
        self.Ry_max=self._max_y_()*self.R_padding*self.y_multiplier


    def give_u_x(self,n):
        # n:th function
        #return lambda value:self.x_func[n](value)*self.x_multiplier
        return lambda value:((self.alpha1*self.x_func[n](value)+self.beta1*self.y_func[n](value)+self.gamma1)\
        /(self.alpha3*self.x_func[n](value)+self.beta3*self.y_func[n](value)+self.gamma3))[0]

    def give_u_y(self,n):
        #return lambda value:self.y_func[n](value)*self.y_multiplier
        return lambda value:((self.alpha2*self.x_func[n](value)+self.beta2*self.y_func[n](value)+self.gamma2)\
        /(self.alpha3*self.x_func[n](value)+self.beta3*self.y_func[n](value)+self.gamma3))[0]

    def give_R_x(self,n):
        # n:th function
        #return lambda value:self.xR_func[n](value)*self.x_multiplier
        return lambda value:((self.alpha1*self.xR_func[n](value)+self.beta1*self.yR_func[n](value)+self.gamma1)\
        /(self.alpha3*self.xR_func[n](value)+self.beta3*self.yR_func[n](value)+self.gamma3))[0]

    def give_R_y(self):
        # n:th function
        #return self._give_R_y_
        return lambda value:((self.alpha2*self.xR_func[n](value)+self.beta2*self.yR_func[n](value)+self.gamma2)\
        /(self.alpha3*self.xR_func[n](value)+self.beta3*self.yR_func[n](value)+self.gamma3))[0]


    def _make_4_(self):
        """ makes nomogram with 4 variables
        f1+f2+f3+f4=0
        """
        self.x_func={} # x coordinate to map points into canvas
        self.y_func={} # y coordinate to map points into canvas
        self.xR_func={} # turning-point axis
        self.yR_func={}
        self.x_func[1]=lambda u1:0
        self.x_func[2]=lambda u2:1
        self.x_func[3]=lambda u3:3
        self.x_func[4]=lambda u4:4
        self.xR_func[1]=lambda uR1:2
        self.y_func[1]=lambda u1:self.functions['f1'](u1)
        self.y_func[2]=lambda u2:-0.5*self.functions['f2'](u2)
        self.y_func[3]=lambda u3:0.5*self.functions['f3'](u3)
        self.y_func[4]=lambda u4:-self.functions['f4'](u4)
        self.yR_func[1]=lambda uR1:uR1
        # let's find maximum y-value for scaling

    def _make_5_(self):
        """ makes nomogram with 5 variables
        f1+f2+f3+f4+f5=0
        """
        self.x_func={} # x coordinate to map points into canvas
        self.y_func={} # y coordinate to map points into canvas
        self.xR_func={} # turning-point axis
        self.yR_func={}
        self.x_func[1]=lambda x1:0
        self.x_func[2]=lambda x2:1
        self.x_func[3]=lambda x3:3
        self.x_func[4]=lambda x4:5
        self.x_func[5]=lambda x5:6
        self.xR_func[1]=lambda xR1:2
        self.xR_func[2]=lambda xR2:4
        self.y_func[1]=lambda u1:self.functions['f1'](u1)
        self.y_func[2]=lambda u2:-0.5*self.functions['f2'](u2)
        self.y_func[3]=lambda u3:0.5*self.functions['f3'](u3)
        self.y_func[4]=lambda u4:-0.5*self.functions['f4'](u4)
        self.y_func[5]=lambda u5:self.functions['f5'](u5)
        self.yR_func[1]=lambda yR1:yR1
        self.yR_func[2]=lambda yR2:yR2

    def  _max_y_(self):
            Ns=range(self.N)

            max1=max([self.y_func[n+1](self.functions['u_max'][n]) for n in Ns])
            max2=max([self.y_func[n+1](self.functions['u_min'][n]) for n in Ns])
            return max(max1,max2)
    def  _min_y_(self):
            Ns=range(self.N)
            min1=min([self.y_func[n+1](self.functions['u_max'][n]) for n in Ns])
            min2=min([self.y_func[n+1](self.functions['u_min'][n]) for n in Ns])
            return min(min1,min2)

    def _make_row_(self,coordinate='x',x=1.0,y=1.0,coord_value=1.0):
        """ Makes transformation matrix. See eq.37,a
        in Allcock. We take \alpha_1=1. h=1.
        """
        # to make expressions shorter
        cv=coord_value
        if  coordinate=='x':
            row=array([y,1,0,0,0,-cv*x,-cv*y,-cv*1])
            value=array([x])
        if  coordinate=='y':
            row=array([0,0,x,y,1,-cv*x,-cv*y,-cv*1])
            value=array([0])
        return row,value
    def test(self):
        return lambda x:x

    def _make_transformation_matrix_(self):
        """ Makes transformation from polygon (non-intersecting) to rectangle
            (x1,y1)     (x3,y3)          (x1t,y1t)      (x3t,y3t)       (0,height)    (width,height)
               |  polygon  |      ---->      |   rectangle  |       =
            (x2,y2)     (x4,y4)          (x2t,y2t)      (x4t,y4t)       (0,0)         (width,0)
        """
        x1=self.x_func[1](self.functions['u_min'][0])
        x2=self.x_func[1](self.functions['u_max'][0])
        x3=self.x_func[self.N](self.functions['u_min'][self.N-1])
        x4=self.x_func[self.N](self.functions['u_max'][self.N-1])
        y1=min(self.y_func[1](self.functions['u_min'][0]),self.y_func[1](self.functions['u_max'][0]))
        y2=max(self.y_func[1](self.functions['u_min'][0]),self.y_func[1](self.functions['u_max'][0]))
        y3=min(self.y_func[self.N](self.functions['u_min'][self.N-1]),\
               self.y_func[self.N](self.functions['u_max'][self.N-1]))
        y4=max(self.y_func[self.N](self.functions['u_min'][self.N-1]),\
               self.y_func[self.N](self.functions['u_max'][self.N-1]))

        width=self.functions['nomo_width']
        height=self.functions['nomo_height']#/self.R_padding
        row1,const1=self._make_row_(coordinate='x',coord_value=0,x=x2,y=y2)
        row2,const2=self._make_row_(coordinate='y',coord_value=0,x=x2,y=y2)
        row3,const3=self._make_row_(coordinate='x',coord_value=0,x=x1,y=y1)
        row4,const4=self._make_row_(coordinate='y',coord_value=height,x=x1,y=y1)
        row5,const5=self._make_row_(coordinate='x',coord_value=width,x=x4,y=y4)
        row6,const6=self._make_row_(coordinate='y',coord_value=0,x=x4,y=y4)
        row7,const7=self._make_row_(coordinate='x',coord_value=width,x=x3,y=y3)
        row8,const8=self._make_row_(coordinate='y',coord_value=height,x=x3,y=y3)


        matrix=array([row1,row2,row3,row4,row5,row6,row7,row8])
        b=array([const1,const2,const3,const4,const5,const6,const7,const8])
        coeff_vector=linalg.solve(matrix,b)
        self.alpha1=-1
        self.beta1=coeff_vector[0]
        self.gamma1=coeff_vector[1]
        self.alpha2=coeff_vector[2]
        self.beta2=coeff_vector[3]
        self.gamma2=coeff_vector[4]
        self.alpha3=coeff_vector[5]
        self.beta3=coeff_vector[6]
        self.gamma3=coeff_vector[7]
        #print coeff_vector
        return coeff_vector
    def _find_polygon_(self):
        """
        finds limiting polygon for transformation
        """
        # let's find max and min y values
        list1=[self.y_func[n+1](self.functions['u_min'][n]) for n in range(self.N)]
        list2=[self.y_func[n+1](self.functions['u_max'][n]) for n in range(self.N)]
        print list1
        print list2
        min_val,min_idx = list1[0],0
        max_val,max_idx = list1[0],0
        for idx,value in enumerate(list1[1:]):
            if value < min_val:
                min_val,min_idx = value,idx+1
            if value > max_val:
                max_val,max_idx = value,idx+1
        for idx,value in enumerate(list2[0:]):
            if value < min_val:
                min_val,min_idx = value,idx+1
            if value > max_val:
                max_val,max_idx = value,idx+1
        # let's find min slopes
        list1_slope_upper=[self.y_func[n+1](self.functions['u_min'][n]) for n in range(self.N) if n!=(max_idx-1)]
        list2_slope_upper=[self.y_func[n+1](self.functions['u_max'][n]) for n in range(self.N) if n!=(max_idx-1)]
        list1_slope_lower=[self.y_func[n+1](self.functions['u_min'][n]) for n in range(self.N) if n!=(min_idx-1)]
        list2_slope_lower=[self.y_func[n+1](self.functions['u_max'][n]) for n in range(self.N) if n!=(min_idx-1)]
        # to be continued
        return max_val,min_val,max_idx,min_idx

if __name__=='__main__':
    functions={'u_min':array([0.0,0.0,0.0,0.0]),
               'u_max':array([10.0,10.0,10.0,10.0]),
               'f1':lambda u1:u1,
               'f2':lambda u2:u2,
               'f3':lambda u3:u3,
               'f4':lambda u4:-u4,
               'nomo_width':14.0,
               'nomo_height':14.0}
    nomo=Nomograph_N_lin(functions,4)
    print nomo.give_u_x(1)(functions['u_min'][0])
    print nomo.give_u_y(1)(functions['u_min'][0])
    print nomo.give_u_x(1)(functions['u_max'][0])
    print nomo.give_u_y(1)(functions['u_max'][0])
    print nomo.give_u_x(4)(functions['u_min'][3])
    print nomo.give_u_y(4)(functions['u_min'][3])
    print nomo.give_u_x(4)(functions['u_max'][3])
    print nomo.give_u_y(4)(functions['u_max'][3])
    print nomo._find_polygon_()
    c = canvas.canvas()
    ax1=Nomo_Axis(func_f=nomo.give_u_x(1),func_g=nomo.give_u_y(1),
                  start=functions['u_min'][0],stop=functions['u_max'][0],
                  turn=1,title='f1',canvas=c,type='linear',
                  tick_levels=2,tick_text_levels=1)
    ax2=Nomo_Axis(func_f=nomo.give_u_x(2),func_g=nomo.give_u_y(2),
                  start=functions['u_min'][1],stop=functions['u_max'][1],
                  turn=-1,title='f2',canvas=c,type='linear',
                  tick_levels=2,tick_text_levels=1)
    ax3=Nomo_Axis(func_f=nomo.give_u_x(3),func_g=nomo.give_u_y(3),
                  start=functions['u_min'][2],stop=functions['u_max'][2],
                  turn=-1,title='f3',canvas=c,type='linear',
                  tick_levels=2,tick_text_levels=1)
    ax4=Nomo_Axis(func_f=nomo.give_u_x(4),func_g=nomo.give_u_y(4),
                  start=functions['u_min'][3],stop=functions['u_max'][3],
                  turn=-1,title='f4',canvas=c,type='linear',
                  tick_levels=4,tick_text_levels=2)
    R=Nomo_Axis(func_f=nomo.give_R_x(1),func_g=lambda a:a,
                  start=nomo.Ry_min,stop=nomo.Ry_max,
                  turn=-1,title='R',canvas=c,type='linear',
                  tick_levels=0,tick_text_levels=0)
    #c.stroke(path.line(nomo.give_R_x(1), nomo.Ry_min, nomo.give_R_x(1), nomo.Ry_max))
    c.writePDFfile("nomolin")

    # example 2
    # f1+f2+f3+f4=f5
    functions={'u_min':array([0.0,0.0,0.0,0.0,0.0]),
               'u_max':array([10.0,10.0,10.0,10.0,10.0]),
               'f1':lambda u1:u1,
               'f2':lambda u2:u2,
               'f3':lambda u3:u3,
               'f4':lambda u4:u4,
               'f5':lambda u5:-u5,
               'nomo_width':12.0,
               'nomo_height':18.0}
    nomo=Nomograph_N_lin(functions,5)
    print nomo.give_u_x(1)(functions['u_min'][0])
    print nomo.give_u_y(1)(functions['u_min'][0])
    print nomo.give_u_x(1)(functions['u_max'][0])
    print nomo.give_u_y(1)(functions['u_max'][0])
    print nomo.give_u_x(5)(functions['u_min'][4])
    print nomo.give_u_y(5)(functions['u_min'][4])
    print nomo.give_u_x(5)(functions['u_max'][4])
    print nomo.give_u_y(5)(functions['u_max'][4])
    c = canvas.canvas()
    ax1=Nomo_Axis(func_f=nomo.give_u_x(1),func_g=nomo.give_u_y(1),
                  start=functions['u_min'][0],stop=functions['u_max'][0],
                  turn=1,title='f1',canvas=c,type='linear',
                  tick_levels=2,tick_text_levels=1)
    ax2=Nomo_Axis(func_f=nomo.give_u_x(2),func_g=nomo.give_u_y(2),
                  start=functions['u_min'][1],stop=functions['u_max'][1],
                  turn=-1,title='f2',canvas=c,type='linear',
                  tick_levels=2,tick_text_levels=1)
    ax3=Nomo_Axis(func_f=nomo.give_u_x(3),func_g=nomo.give_u_y(3),
                  start=functions['u_min'][2],stop=functions['u_max'][2],
                  turn=-1,title='f3',canvas=c,type='linear',
                  tick_levels=2,tick_text_levels=1)
    ax4=Nomo_Axis(func_f=nomo.give_u_x(4),func_g=nomo.give_u_y(4),
                  start=functions['u_min'][3],stop=functions['u_max'][3],
                  turn=1,title='f4',canvas=c,type='linear',
                  tick_levels=2,tick_text_levels=1)
    ax5=Nomo_Axis(func_f=nomo.give_u_x(5),func_g=nomo.give_u_y(5),
                  start=functions['u_min'][4],stop=functions['u_max'][4],
                  turn=1,title='f5',canvas=c,type='linear',
                  tick_levels=4,tick_text_levels=2)

    R1=Nomo_Axis(func_f=nomo.give_R_x(1),func_g=lambda a:a,
                  start=nomo.Ry_min,stop=nomo.Ry_max,
                  turn=-1,title='R1',canvas=c,type='linear',
                  tick_levels=0,tick_text_levels=0)
    R2=Nomo_Axis(func_f=nomo.give_R_x(2),func_g=lambda a:a,
                  start=nomo.Ry_min,stop=nomo.Ry_max,
                  turn=-1,title='R2',canvas=c,type='linear',
                  tick_levels=0,tick_text_levels=0)
    #c.stroke(path.line(nomo.give_R_x(1), nomo.Ry_min, nomo.give_R_x(1), nomo.Ry_max))
    c.writePDFfile("nomolin2")
