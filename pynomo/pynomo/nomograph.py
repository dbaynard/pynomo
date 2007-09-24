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
          - F1(u)=F2(v)+F3(w)
          - F1(u)=F2(v)*F3(w)
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
    def __init__(self,nomo_type,functions,nomo_height=20.0,nomo_width=10.0
                 ):
        """
        @param nomo_type: This values describes the type of nomogram.
            allowed values are:
                - 'F1(u)=F2(v)+F3(w)'
                - 'F1(u)=F2(v)*F3(w)'
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
                {'F1':lambda z:z,
                 'F2':lambda x:x*x,
                 'F3':lambda y:2*y}

        """
        self.functions=functions
        try:
            {'F1(u)=F2(v)+F3(w)': self.init_sum_three,
             'F1(u)=F2(v)*F3(w)': self.init_product_three,
             'general3': self.init_general}[nomo_type]()
        except KeyError:
            print "nomo_type not valid"

    def init_sum_three(self):
        """
        Make initializations for nomogram f1(u)=f2(v)+f3(w)
        """
        self.f1 = lambda u: 0.0
        self.g1 = lambda u: self.functions['F1']
        self.h1 = lambda u: 1.0
        self.f2 = lambda u: 1.0
        self.g2 = lambda u: 0.5*self.functions['F3']
        self.h2 = lambda u: 1.0
        self.f3 = lambda u: 0.5
        self.g3 = lambda u: self.functions['F2']
        self.h3 = lambda u: 1.0