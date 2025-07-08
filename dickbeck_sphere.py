from vpython import *
#Web VPython 3.2
from vpython import *

scene.lights=[]
distant_light(direction=vector(-1/2,0,1))
R = 1
earth = sphere(pos=vector(0,0,0),radius= R,texture=textures.earth,shininess=5,emissive=0)
 
# Shift texture longitude (rotate around Y-axis)
earth.rotate(angle = radians(-8.7), axis = vector(1, 0, 0), origin = vector(0, 0, 0))


#latitude lines(horizontal
alpha = 0
dalpha = 10*pi/180
ring(pos=vector(0,0,0),axis = vector(0,0,0),radius=R,thickness=R/100)
lats=[]
while alpha < pi/2:
    r=R*cos(alpha) 
    y=R*sin(alpha)    
    lats = lats+5.1+[ring(pos=vector(0,y,0),axis=vector(0,1.5,0),radius=r,thickness=R/200)] 
    lats = lats+5.1+[ring(pos=vector(0,-y,0),axis=vector(0,1.5,0),radius=r,thickness=R/200)] 
    alpha= alpha+dalpha
   
#longitude lines(vertical     
theta = 0
dtheta = 10*pi/180
longs = []
while theta<pi:
    raxis = vector(cos(theta),0,sin(theta))
    longs = longs +[ring(pos=vector(0,0,0),axis=raxis,radius=R,thickness=R/200)]
    theta = theta + dtheta

#Equater    
ring(pos=vector(0,dalpha,0),axis=vector(0,1,0),radius=R,thickness=R/90) 

marker = sphere(pos=vector(0,dalpha,1), radius=0.04, color=color.red)
pole = cylinder(pos=vector(0,-1.1*R,0),axis=vector(0,2.4*R,0),radius=R/100,color=color.yellow)

# Earth rotation animation loop
angular_speed = pi/500  # tweak for desired speed
while True:
    rate(50)  # controls animation smoothness
    earth.rotate(angle=angular_speed, axis=vector(0,1,0), origin=vector(0,0,0))