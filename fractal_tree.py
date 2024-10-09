import maya.cmds as cmds
import random
import math

'''
File creates Fractal trees'''



def create_tree(pos, az_angle, pol_angle, length, depth, group):
    #creates a fractal tree
    if depth == 0:
        #base
        return None
        
    #Find end points of each branch --> change from polar to spherical
    end_x = pos[0] + length * math.sin(math.radians(pol_angle)) * math.cos(math.radians(az_angle))
    end_y = pos[1] + length * math.sin(math.radians(pol_angle)) * math.sin(math.radians(az_angle))
    end_z = pos[2] + length * math.cos(math.radians(pol_angle))
    end = (end_x, end_y, end_z)
    
    branch_path = cmds.curve(p=[pos, end], d=1)
    
    #Add a cylindar or what I called bark to the curve
    branch_profile = cmds.circle(radius=0.05, name='branch_profile', sections=8)[0]    
    
    branch = cmds.extrude(branch_profile, branch_path,
        et=2,
        ucp=True,
        fpt=True,
        upn=True,
        rotation=0,
        scale=1,
        name="branch")[0]

    if pol_angle > 90:
        #reverse the surface if the reverse is true
        cmds.reverseSurface(branch, direction=2, constructionHistory=True, replaceOriginal=True)

    #Clean up the profile and curve by deleting them after extrusion
    cmds.delete(branch_profile, branch_path)
    
    
    #Add branch to group
    cmds.parent(branch, group)

    #Recursive creation of child branches
    #horizontal rotation
    left_az_angle = az_angle - random.uniform(0, 45)
    right_az_angle = az_angle + random.uniform(0, 45)
    
    #vertical rotation
    left_pol_angle = pol_angle - random.uniform(0, 45)
    right_pol_angle = pol_angle + random.uniform(0, 45)
    
    #if the branch is on the left, it will need to have the surface reversed 
    create_tree(end, left_az_angle, left_pol_angle, length * 0.8, depth - 1, group)
    create_tree(end, right_az_angle, right_pol_angle, length * 0.8, depth - 1, group)

def generate_fractal_tree(pos, trunk_length=10, max_depth=4):
    # Create the tree
    t_group = cmds.group(empty=True, name='fractal_tree')
    trunk = create_tree(pos, 90, 90, trunk_length, max_depth,t_group)
    return t_group
