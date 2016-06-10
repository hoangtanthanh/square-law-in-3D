'''
graphical intuition to MOSFET square-law
'''
#global variable
Vth = 2 # V threshold
Id_Vds = 1  # plot Id vs Vds graph: set Id_Vds=1 else set = 0
Id_Vgs = 0  # plot Id vs Vgs graph: set Id_Vgs=1 else set = 0

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Colormap

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
  #sub-threshold region
  if (Vgs<=Vth):
    return (0,'b')
  #triode-operating region
  elif (Vds<=Vgs-Vth):
    return ((Vgs-Vth)*Vds-(Vds**2)/2,'y')
  #saturation-operating region
  else:
    return (0.5*(Vgs-Vth)**2,'r')
    
#main function
if __name__=="__main__":
  fig = plt.figure() 
  ax = fig.gca(projection='3d')
  
  #legends
  saturation = mpatches.Patch(color='r', alpha=0.3, label='saturation region')
  triode     = mpatches.Patch(color='y', alpha=0.3, label='triode region')
  sub        = mpatches.Patch(color='b', alpha=0.3, label='subthreshold region')
  
  ax.legend(handles=[saturation,triode,sub])
  
  x = y = np.arange(0, 20, 0.5)
  X, Y = np.meshgrid(x, y)
  
  colors = np.empty(X.shape, dtype=str) 
  Z = np.empty(X.shape, dtype=float)
  for y in range(len(Y)):
    for x in range(len(X)):
      Z[x,y], colors[x, y] = square_law(y,x)

  #plot the graph
  ax.plot_surface(X, Y, Z, rstride=2, cstride=2, facecolors=colors, alpha=0.3,
                       linewidth=0, antialiased=False)
  
  #projection contours
  cset = ax.contour(X, Y, Z, zdir='x', offset=20, cmap=cm.coolwarm)
  cset = ax.contour(X, Y, Z, zdir='y', offset=0, cmap=cm.coolwarm)

  ax.set_xlabel('Vds')
  ax.set_ylabel('Vgs')
  ax.set_zlabel('Id')

  #Id vs Vgs or Id vs Vds
  if(Id_Vds):
    ax.view_init(elev=0.,azim=-90.)
  if(Id_Vgs):
    ax.view_init(elev=0.,azim=0.)

  plt.show()
