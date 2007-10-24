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
from math import *
"""
Example nomograph of equation T=((1+p/100)^N-1)*100
N = years
p = interest rate as percentage
N = total interest after N years
equation in suitable form is
log(T/100+1)=N*log(1+p/100)
"""
nomo_type='F2(v)=F3(w)/F1(u)'
functions1={ 'filename':'nomogram_interest.pdf',
        'F2':lambda T:log(T/100.0+1.0),
        'v_start':20.0,
        'v_stop':900.0,
        'v_title':r'Total interest \%',
        'v_scale_type':'log',
        'F1':lambda N:1/N,
        'u_start':3.0,
        'u_stop':20.0,
        'u_title':'Years',
        'u_scale_type':'linear',
        'F3':lambda p:log(1.0+p/100.0),
        'w_start':0.2,
        'w_stop':20.0,
        'w_title':r'p \%',
        'w_title_x_shift':-1.0,
        'w_title_y_shift':0.25,
        'w_scale_type':'linear',}
nomograph.Nomograph(nomo_type=nomo_type,functions=functions1)