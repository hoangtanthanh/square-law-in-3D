'''
  Graphical intuition to MOSFET square-law
  Author: Thanh(Tony) Hoang 
  Date: 10th June 2016
'''
#global variable
Vth = 0.8 # V threshold
Id_Vds = 1  # plot Id vs Vds graph: set Id_Vds=1 else set = 0
Id_Vgs = 0  # plot Id vs Vgs graph: set Id_Vgs=1 else set = 0

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib import cm
import matplotlib.pyplot as plt

#src: https://codeyarns.com/2014/11/13/how-to-get-orthographic-projection-in-3d-plot-of-matplotlib/
def orthogonal_proj(zfront, zback):
    a = (zfront+zback)/(zfront-zback)
    b = -2*(zfront*zback)/(zfront-zback)
    # -0.0001 added for numerical stability as suggested in:
    # http://stackoverflow.com/questions/23840756
    return np.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,a,b],
                        [0,0,-0.0001,zback]])
# Later in your plotting code ...
proj3d.persp_transformation = orthogonal_proj

# cmos square_law function without Kpn*W/L
def square_law(Vds, Vgs):
  #sub threshold region
  if (Vgs<=Vth):
    return 0
  #triode-operating region
  elif (Vds<=Vgs-Vth):
    return (Vgs-Vth)*Vds-(Vds**2)/2
  #saturation-operating region
  else:
    return 0.5*(Vgs-Vth)**2
    
#main function
if __name__=="__main__":
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  x = y = np.arange(0, 20.0, 0.1)
  X, Y = np.meshgrid(x, y)
  zs = np.array([square_law(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
  Z = zs.reshape(X.shape)

  ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.5) #plot the graph
  
  #projection contours
  cset = ax.contour(X, Y, Z, zdir='x', offset=20, cmap=cm.coolwarm)
  cset = ax.contour(X, Y, Z, zdir='y', offset=0, cmap=cm.coolwarm)

  ax.set_xlabel('Vds Label')
  ax.set_ylabel('Vgs Label')
  ax.set_zlabel('Id Label')

  #Id vs Vgs or Id vs Vds
  if(Id_Vds):
    ax.view_init(elev=0.,azim=-90.)
  if(Id_Vgs):
    ax.view_init(elev=0.,azim=0.)
  
  plt.show()
