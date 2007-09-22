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
          - f1(u)=f2(v)+f3(w)
          - f1(u)=f2(v)*f3(w)
        General
        -------
          - An equation in determinant form::
              -------------------------
              | f1(u) | g1(v) | h1(w) |
              -------------------------
              | f2(u) | g2(v) | h2(w) | = 0
              -------------------------
              | f3(u) | g3(v) | h3(w) |
              -------------------------
    Axis
    ====
      Axes may be chosen to be linear or logarithmic

    """
    def __init__(self,nomo_type,nomo_height=20.0,nomo_width=10.0):
        """
        @param nomo_type: This values describes the type of nomogram.
            allowed values are:
                - 'f1(u)=f2(v)+f3(w)'
                - 'f1(u)=f2(v)*f3(w)'
                - 'general3', a general determinant::
                        -------------------------
                        | f1(u) | g1(v) | h1(w) |
                        -------------------------
                        | f2(u) | g2(v) | h2(w) |
                        -------------------------
                        | f3(u) | g3(v) | h3(w) |
                        -------------------------

        @type nomo_type: string
        """
        pass