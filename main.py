'''
This code creates fractal world. In the folder, there is a code called frac_mountain and fractal_tree that creates a fractal mountain
and fractal trees. This is the main code file. 
I handed in an assignment last week that only included the fractal mountain, but this week I added more options to the
gui as well as fractal trees. 

----------------------------------------How to use------------------------------------------------
opens up a GUI 
decides: 
    x, y, and z of the mountain
    size of the mountain
    number of subdivisions of the mountain 
    randomness of the mountain
    number of trees on the mountain

buttons:
    generates the mountain
    expands either left or right of the mountain you select (after you extand, you must reselect the middle portion)
    (keep size consistant for this feature to work)
    Add trees of number of trees (must be clicked on the mountain you want to add trees to)
    Clear the scene
    Reset the parameters given 
    Close the GUi
'''
import maya.cmds as cmds
import random
import math

import fractal_tree
import importlib
importlib.reload(fractal_tree)

import frac_mountain
import importlib
importlib.reload(frac_mountain)


class Fractal_Mountain_Window(object):
    def __init__(self):
        '''
        creates a gui for building up the mountain
        ''' 
        try:
            cmds.deleteUI(self.window, window=True)
        except Exception as e:
            print(f"Creating UI")

        self.window = "fractalMountainWindow"
        self.title = "Fractal Mountain Generator"
        self.window_size = (300, 400)
        self.mountain = None
        self.mountain_right = None
        self.mountain_left = None
        self.trees = None
        self.x = 0
        self.y = 0
        self.z = 0
        self.define_window()
    
    def define_window(self, *args):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title=self.title, widthHeight=self.window_size)

        main_layout = cmds.columnLayout(adjustableColumn=True)

        # Add UI elements
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 100, 100), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
    
        # Create three float fields
        self.x_pos = cmds.floatFieldGrp(label="X: ", value1=0.0, columnWidth2=(30, 60))
        self.y_pos = cmds.floatFieldGrp(label="Y: ", value1=0.0, columnWidth2=(30, 60))
        self.z_pos = cmds.floatFieldGrp(label="Z: ", value1=0.0, columnWidth2=(30, 60))
        
        # Return to the main layout
        cmds.setParent(main_layout)
        
        self.input_size = cmds.intSliderGrp(label="Size", min=1, max=20, value=10)
        self.input_subdivisions = cmds.intSliderGrp(label="Subdivision", min=1, max=20, value=10)
        self.input_randomness = cmds.floatSliderGrp(label="Randomness", min=0, max=10, value=5)

        cmds.button(label="Generate Fractal Mountain", command=self.generate_mountain)
        
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150), columnAttach=[(1, 'both', 0), (2, 'both', 0)])

        cmds.button(label="Extand right", command=self.duplicate_mountain_right)
        cmds.button(label="Extand left", command=self.duplicate_mountain_left)
        
        cmds.setParent(main_layout)
        
        
        self.input_trees = cmds.intSliderGrp(label="trees", min=1, max=20, value=10)
        
        cmds.button(label="Add Trees", command=self.create_trees)
        
        cmds.button(label="Clear", command=self.delete_mountains)
        cmds.button(label="Reset", command=self.reset)
        cmds.button(label="Close", command=self.close_window)

        cmds.showWindow()
            
    
    def generate_mountain(self, *args):
        '''gets the user input and creates a fractal mountain'''        
        cmds.select(clear=True)
        self.size = cmds.intSliderGrp(self.input_size, query=True, value=True)
        self.subdivisions = cmds.intSliderGrp(self.input_subdivisions, query=True, value=True)
        self.randomness = cmds.floatSliderGrp(self.input_randomness, query=True, value=True)
        
        self.x = cmds.floatFieldGrp(self.x_pos, query=True, value=True)[0]
        self.y = cmds.floatFieldGrp(self.y_pos, query=True, value=True)[0]
        self.z = cmds.floatFieldGrp(self.z_pos, query=True, value=True)[0]
        
        self.mountain = frac_mountain.create_fractal_mountain(size=self.size, subdivisions=self.subdivisions, randomness=self.randomness,x=self.x,y=self.y,z=self.z)
        
        #set a hypershade to the mountain
        material_name = 'mountain_m'
        #creates new material if not already there
        if not cmds.objExists(material_name):
            material = cmds.shadingNode('lambert', asShader=True, name=material_name)
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=material_name + "SG")
            cmds.connectAttr(material_name + ".outColor", shading_group + ".surfaceShader", force=True)
        else:
            shading_group = material_name + "SG"
        cmds.setAttr(material_name + ".color", 0.133, 0.545, 0.133, type="double3")

        cmds.select(self.mountain)
        cmds.hyperShade(assign=shading_group)
    
    def duplicate_mountain_right(self, *args):
        mountain = cmds.ls(selection=True)
        if mountain:
            self.mountain_right = cmds.duplicate(mountain, name="mountain_right")[0]
            #Mirror the second mountain by scaling in the X axis
            cmds.scale(-1, 1, 1, self.mountain_right)
            #Move the second mountain to the opposite side
            cmds.move(cmds.getAttr(".translateX") + self.size, cmds.getAttr(".translateY"), cmds.getAttr(".translateZ") ,self.mountain_right)
        else:
            print("Need to create first Mountain")
            
    def duplicate_mountain_left(self, *args):
        mountain = cmds.ls(selection=True)
        if mountain:
            self.mountain_left = cmds.duplicate(mountain, name="mountain_left")[0]
            # Mirror the second mountain by scaling in the X axis
            cmds.scale(-1, 1, 1, self.mountain_left)
            # Move the second mountain to the opposite sid
            cmds.move(cmds.getAttr(".translateX") - self.size, cmds.getAttr(".translateY"), cmds.getAttr(".translateZ"), self.mountain_left)
        else:
            print("Need to create first Mountain")
    
    def create_trees(self, *args):
        mountain = cmds.ls(selection=True)[0]
        if mountain:
            vertices = cmds.ls(f"{mountain}.vtx[*]", flatten=True)
            self.trees = cmds.intSliderGrp(self.input_trees, query=True, value=True)
            
            for _ in range(self.trees):
                t = random.randint(0, len(vertices) - 1)
                v = vertices[t]
                pos = cmds.pointPosition(v, world=True)
                
                tree = fractal_tree.generate_fractal_tree(pos, trunk_length=0.5, max_depth=4)
                material_name = 'tree_m'
                if not cmds.objExists(material_name):
                    material = cmds.shadingNode('lambert', asShader=True, name=material_name)
                    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=material_name + "SG")
                    cmds.connectAttr(material_name + ".outColor", shading_group + ".surfaceShader", force=True)
                else:
                    shading_group = material_name + "SG"
                cmds.setAttr(material_name + ".color", 0.212, 0.149, 0.141, type="double3")
        
                cmds.select(tree)
                cmds.hyperShade(assign=shading_group)
        else:
            print("No mountain yet")  
            
            
    def reset(self, *args):
        self.define_window()
            
    def delete_mountains(self, *args):
        polygons = cmds.ls(type='mesh')
        
        #Get the transforms of those polygonal objects (parent nodes)
        polygon_transforms = cmds.listRelatives(polygons, parent=True)
        
        # Delete the parent transforms, which deletes the entire polygon object
        if polygon_transforms:
            print("Mountains are all deleted")
            cmds.delete(polygon_transforms)
        
        #deletes the trees
        trees = []
        
        all_transforms = cmds.ls(type='transform')
        for transform in all_transforms:
            child_shapes = cmds.listRelatives(transform, shapes=True)
            if not child_shapes:
                trees.append(transform)
        if trees:
            cmds.delete(trees)
            print("Trees are all deleted")
    
    def close_window(self, *args):
        try:
            cmds.deleteUI(self.window, window=True)
        except Exception as e:
            print(f"No previous UI to close: {e}")

#runs the command
Fractal_Mountain_Window()
