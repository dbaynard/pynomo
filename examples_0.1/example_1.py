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
import sys
sys.path.insert(0, "..")
from pynomo import *
"""
    Retaining wall example nomograph from Allcock's book. Also found in O'Cagne:
    Traite de Nomographie (1899).
    Eq: (1+L)h^2-L*h*(1+p)-1/3*(1-L)*(1+2*p)=0
    in determinant form::
          -----------------------------------------
          | 2*(u*u-1) | 3*u*(u+1) | -u*(u-1.0)    |
          -----------------------------------------
          |      v    |     1     |    -v*v       | = 0
          -----------------------------------------
          | 2*(2*w+1) | 3*(w+1)   |-(w+1)*(2*w+1) |
          -----------------------------------------

"""
nomo_type='general3'
functions2={'filename':'nomogram1.pdf',
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
            'w_title':'L',
            'title_y': 2,
            'title_box_width': 10,
            'title_str':r'Solution to retaining wall equation:  $(1+L)h^2-Lh(1+p)-1/3(1-L)(1+2p)=0$'}
nomograph.Nomograph(nomo_type=nomo_type,functions=functions2)
