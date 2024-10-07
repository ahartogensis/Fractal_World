import maya.cmds as cmds
import random
import math

'''
Creates a fractal mountain using subdivision and vertex displacement
'''

def create_fractal_mountain(size=20, subdivisions=10, randomness=5, x=0, y=0, z=0):
    #Create initial plane
    plane = cmds.polyPlane(width=size, height=size, sx=1, sy=1, name="mountain")[0]
    if not (x == 0 and y == 0 and z == 0):
        cmds.move(x, y, z, plane, absolute=True)
    #Calculate the number of iterations to get the correct number of subdivisions 
    #given by chatgpt to because of the grid style of the plane
    iterations = int(math.log2(subdivisions)) + 1
   
    #saves all the corners 
    original_vertices = [f'{plane}.vtx[0]', f'{plane}.vtx[1]', f'{plane}.vtx[2]', f'{plane}.vtx[3]'] 
    
    #Use initial Y position for corners/ same for all corners 
    init_y = cmds.pointPosition(original_vertices[0], world=True)[1] 
    
    for i in range(iterations):
        #Subdivide the mesh
        #command given by chatgpt
        cmds.polySubdivideFacet(plane, dv=1, ch=True)
        
        #Get all vertices
        vertices = cmds.ls(f"{plane}.vtx[*]", flatten=True)
        
        
        #Randomize the position of vertices and creates cross edges 
        for v in vertices:
            current_pos = cmds.pointPosition(v, world=True)

            #Apply raondom displacement 
            if v not in original_vertices:
                x_pos = current_pos[0]
                new_y = current_pos[1] + random.uniform(init_y, randomness)
                z_pos = current_pos[2]
                cmds.move(x_pos, new_y, z_pos, v, absolute=True)

                
        randomness *= 0.5
    
    #Smooth the final result
    cmds.polySmooth(plane, divisions=1)
    

    return plane