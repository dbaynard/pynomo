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
from nomo_axis import *
from nomograph3 import *
class Nomograph:
    """
    Main module for easy building of nomographs.

    Types of nomographs:
    ====================
        Simple
        ------
          - F2(v)=F1(u)+F3(w)
          - F2(v)=F1(u)*F3(w)
        General
        -------
          - An equation in determinant form::
              -------------------------
              | f1(u) | g1(u) | h1(u) |
              -------------------------
              | f2(v) | g2(v) | h2(v) | = 0
              -------------------------
              | f3(w) | g3(w) | h3(w) |
              -------------------------
    Axis
    ====
      Axes may be chosen to be linear or logarithmic

    """
    def __init__(self,nomo_type,functions,nomo_height=15.0,nomo_width=10.0
                 ):
        """
        @param nomo_type: This values describes the type of nomogram.
            allowed values are:
                - 'F2(v)=F1(u)+F3(w)'
                - 'F2(v)=F3(w)/F1(u)'
                - 'general3', a general eq in determinant form::
                        -------------------------
                        | f1(u) | g1(u) | h1(u) |
                        -------------------------
                        | f2(v) | g2(v) | h2(v) | = 0
                        -------------------------
                        | f3(w) | g3(w) | h3(w) |
                        -------------------------

        @type nomo_type: string
        @param functions: dictionary with corresponding functions.
            for examples if we plan to plot z=x*x+2*y, then we have::
                functions={ 'filename':'nomogram1.pdf',
                            'F1':lambda z:z,
                            'u_start':1.0,
                            'u_stop':5.0,
                            'u_title':'z',
                            'F2':lambda x:x*x,
                            'v_start':1.0,
                            'v_stop':3.0,
                            'v_title','x'
                            'F3':lambda y:2*y,
                            'w_start':0.0,
                            'w_stop':3.0
                            'w_title','y'}

        """
        self.functions=functions
        self.nomo_height=nomo_height
        self.nomo_width=nomo_width
        try:
            {'F2(v)=F1(u)+F3(w)': self.init_sum_three,
             'F2(v)=F3(w)/F1(u)': self.init_product_three,
             'general3': self.init_general}[nomo_type]()
        except KeyError:
            print "nomo_type not valid"
        # This structure sets the limits
        vk=[['u',functions['u_start'],'x',0.0],
            ['u',functions['u_start'],'y',0.0],
            ['u',functions['u_stop'],'x',0.0],
            ['u',functions['u_stop'],'y',nomo_height],
            ['w',functions['w_start'],'x',nomo_width],
            ['w',functions['w_start'],'y',0.0],
            ['w',functions['w_stop'],'x',nomo_width],
            ['w',functions['w_stop'],'y',nomo_height]]
        nomo=Nomograph3(f1=self.f1,f2=self.f2,f3=self.f3,
                        g1=self.g1,g2=self.g2,g3=self.g3,
                        h1=self.h1,h2=self.h2,h3=self.h3,
                        vk=vk)
        c = canvas.canvas()
        u_axis=Nomo_Axis(func_f=nomo.give_x1,func_g=nomo.give_y1,
                         start=self.functions['u_start'],stop=self.functions['u_stop'],
                         turn=-1,title=self.functions['u_title'],canvas=c)
        v_axis=Nomo_Axis(func_f=nomo.give_x2,func_g=nomo.give_y2,
                         start=self.functions['v_start'],stop=self.functions['v_stop'],
                         turn=1,title=self.functions['v_title'],canvas=c)
        w_axis=Nomo_Axis(func_f=nomo.give_x3,func_g=nomo.give_y3,
                         start=self.functions['w_start'],stop=self.functions['w_stop'],
                         turn=-1,title=self.functions['w_title'],canvas=c)
        c.writePDFfile(self.functions['filename'])

    def init_sum_three(self):
        """
        Make initializations for nomogram F2(v)=F1(u)+F3(w)
        """
        self.f1 = lambda u: 0.0
        self.g1 = lambda u: self.functions['F1'](u)
        self.h1 = lambda u: 1.0
        self.f2 = lambda v: 0.5
        self.g2 = lambda v: 0.5*self.functions['F2'](v)
        self.h2 = lambda v: 1.0
        self.f3 = lambda w: 1.0
        self.g3 = lambda w: self.functions['F3'](w)
        self.h3 = lambda w: 1.0

    def init_product_three(self):
        """
        Make initializations for nomogram F2(v)=F3(w)/F1(u)::
                        ------------------------------------
                        |      1         | -F1(u)  | 1     |
                        ------------------------------------
                        | F2(v)/(F2(v)+1)|   0     | 1     | = 0
                        ------------------------------------
                        |      0         |  F3(w)  | 1     |
                        ------------------------------------
        """
        # u and w scales have to go in opposite directions in this nomograph
        if ((self.functions['u_start']-self.functions['u_stop'])*
        (self.functions['w_start']-self.functions['w_stop'])>0.0):
            self.functions['w_start'],self.functions['w_stop']= \
            self.functions['w_stop'],self.functions['w_start']

        self.f1 = lambda u: 1.0
        self.g1 = lambda u: -self.functions['F1'](u)
        self.h1 = lambda u: 1.0
        self.f2 = lambda v: self.functions['F2'](v)/(self.functions['F2'](v)+1.0)
        self.g2 = lambda v: 0.0
        self.h2 = lambda v: 1.0
        self.f3 = lambda w: 0.0
        self.g3 = lambda w: self.functions['F3'](w)
        self.h3 = lambda w: 1.0

    def init_general(self):
        """
        Make initializations for nomogram in determinant form::
                        -------------------------
                        | f1(u) | g1(u) | h1(u) |
                        -------------------------
                        | f2(v) | g2(v) | h2(v) | = 0
                        -------------------------
                        | f3(w) | g3(w) | h3(w) |
                        -------------------------
        """
        self.f1 = lambda u: self.functions['f1'](u)
        self.g1 = lambda u: self.functions['g1'](u)
        self.h1 = lambda u: self.functions['h1'](u)
        self.f2 = lambda v: self.functions['f2'](v)
        self.g2 = lambda v: self.functions['g2'](v)
        self.h2 = lambda v: self.functions['h2'](v)
        self.f3 = lambda w: self.functions['f3'](w)
        self.g3 = lambda w: self.functions['g3'](w)
        self.h3 = lambda w: self.functions['h3'](w)

if __name__=='__main__':
    """
    Example nomograph z=x*x+2*y
    """
    nomo_type='F2(v)=F1(u)+F3(w)'
    functions={ 'filename':'nomogram1.pdf',
            'F2':lambda z:z,
            'v_start':1.0,
            'v_stop':15.0,
            'v_title':'z',
            'F1':lambda x:x*x,
            'u_start':1.0,
            'u_stop':3.0,
            'u_title':'x',
            'F3':lambda y:2*y,
            'w_start':0.0,
            'w_stop':3.0,
            'w_title':'y'}
    Nomograph(nomo_type=nomo_type,functions=functions)

    """
    Example nomograph z=y/x or y=x*z
    """
    nomo_type='F2(v)=F3(w)/F1(u)'
    functions1={ 'filename':'nomogram2.pdf',
            'F2':lambda z:z,
            'v_start':2.0,
            'v_stop':0.5,
            'v_title':'z',
            'F1':lambda x:x,
            'u_start':1.0,
            'u_stop':5.0,
            'u_title':'x',
            'F3':lambda y:y,
            'w_start':5.0,
            'w_stop':1.0,
            'w_title':'y'}
    Nomograph(nomo_type=nomo_type,functions=functions1)
    """
    Example nomograph from Allcock's book. Eq xx=xx in determinant form::
              -----------------------------------------
              | 2*(u*u-1) | 3*u*(u+1) | -u*(u-1.0)    |
              -----------------------------------------
              |      v    |     1     |    -v*v       | = 0
              -----------------------------------------
              | 2*(2*w+1) | 3*(w+1)   |-(w+1)*(2*w+1) |
              -----------------------------------------

    """
    nomo_type='general3'
    functions2={ 'filename':'nomogram3.pdf',
            'f1':lambda u:2*(u*u-1.0),
            'g1':lambda u:3*u*(u+1.0),
            'h1':lambda u:-u*(u-1.0),
            'f2':lambda v:v,
            'g2':lambda v:1.0,
            'h2':lambda v:-v*v,
            'f3':lambda w:2.0*(2.0*w+1.0),
            'g3':lambda w:3.0*(w+1.0),
            'h3':lambda w:-(w+1.0)*(2.0*w+1.0),
            'u_start':0.5,
            'u_stop':1.0,
            'u_title':'p',
            'v_start':1.0,
            'v_stop':0.75,
            'v_title':'h',
            'w_start':1.0,
            'w_stop':0.5,
            'w_title':'L'}
    Nomograph(nomo_type=nomo_type,functions=functions2)

