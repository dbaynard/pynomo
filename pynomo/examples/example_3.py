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
from pynomo import *
"""
Example nomograph z=x*x+2*y. It is of type F2(v)=F1(u)+F3(w)
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
nomograph.Nomograph(nomo_type=nomo_type,functions=functions)