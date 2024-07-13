import bpy
import numpy as np
from PIL import Image
from mathutils import Vector
import random
import math
import tensorflow as tf

image_path = "D:/Blender/Blender_NeuralNet/TestImages/3.jpeg"
path_to_model = "D:/Blender/Blender_NeuralNet/mnist_model.h5"

# Load the model using TensorFlow
model = tf.keras.models.load_model(path_to_model)

def delete_materials_and_cubes():
    # Delete all existing materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

    # Delete existing mesh objects in Blender scene
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

def make_image_array(image_path):
    # Load and preprocess image using PIL
    # Open the image file
    with Image.open(image_path) as img:
        # Convert the image to grayscale
        grayscale_img = img.convert("L")
        # Convert to numpy array and normalize
        image_array = np.array(grayscale_img) / 255.0
    return image_array


#----CREATE INPUT FEATURE ARRAY
# Create 28x28 cubes with spacing
def create_input_feature_array(image_array):
    spacing = 0.4  # Define the spacing between cubes
    n = (28, 28)
    size = 1
    cube_index = 1  # Start from 1 for naming
    for i in range(28):
        for j in range(28):
            x = j * (spacing + size) - (n[1] - 1) * (spacing + size) / 2
            y = 0
            z =  (n[0] - 1) * (spacing + size) / 2 - i * (spacing + size)
            bpy.ops.mesh.primitive_cube_add(
                size=1, 
                enter_editmode=False, 
                align='WORLD', 
                location = (x, y, z)
                #location=(i + i*spacing, 0, j + j*spacing)
            )
            cube = bpy.context.object
            # Name the cube
            cube.name = f"InputCube.{cube_index:03}"  # Names like inputCube.001, inputCube.002, etc.
            cube_index += 1

            # Create a material
            mat = bpy.data.materials.new(name=f"Cube_Material_{i}_{j}")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes

            # Get Principled BSDF
            principled_bsdf = nodes.get("Principled BSDF")

            # Set base color and emission strength based on feature value
            feature_value = image_array[i][j]
            color_value = [feature_value]*3 + [1.0]  # RGB + Alpha
            blue_emission_value = [0.362514, 0.677114, 1, 0.433604]
            
            principled_bsdf.inputs["Base Color"].default_value = color_value

            # Set emission to white and modulate the strength
            scaled_emission_value = [x * feature_value for x in blue_emission_value]
            principled_bsdf.inputs["Emission"].default_value = scaled_emission_value
            principled_bsdf.inputs["Emission Strength"].default_value = feature_value * 3

            # Assign it to object
            if len(cube.data.materials) == 0:
                cube.data.materials.append(mat)
            else:
                cube.data.materials[0] = mat
                
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')

    # Select only cube objects
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)

    # Rotate all selected objects by 90 degrees around the Y-axis
    #bpy.ops.transform.rotate(value=np.radians(90), orient_axis='Y')

def create_flat_cube_grid(n, spacing, size, y_position=0):
    cube_locations = []
    cubes = []
    cube_index = 1
    for i in range(n[0]):
        for j in range(n[1]):
            z = j * (spacing + size) - (n[1] - 1) * (spacing + size) / 2
            y = y_position
            x =  (n[0] - 1) * (spacing + size) / 2 - i * (spacing + size)
            
            # Create a new torus
            bpy.ops.mesh.primitive_torus_add(
                align='WORLD',
                location=(x, y, z),
                rotation=(0, 0, 0),
                major_radius=0.4,   # keeping this the same or making it larger
                minor_radius=0.03  # reducing this to make the torus skinny
            )
            cube = bpy.context.active_object
            cube.name = f"OutputCube.{cube_index:03}"  # Names like inputCube.001, inputCube.002, etc.
            cube_index += 1
            
            cube.scale = (size, size, size)
            
            cube_locations.append(Vector((x, y, z, 0)))
            cubes.append(cube)
            
            # Create a material
            mat = bpy.data.materials.new(name=f"OutputNeuron_Material_{i}_{j}")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes

            # Get Principled BSDF
            principled_bsdf = nodes.get("Principled BSDF")
            color_value = (0.03, 0.03, 0.03, 1.0) #dark gray, fully opaque
            principled_bsdf.inputs["Base Color"].default_value = color_value
            
            #Collection
            output_layer_collection = bpy.data.collections["Output Layer"]
            # Move the created torus to the "Input Layer" collection
            output_layer_collection.objects.link(cube)  # Add cube to new collection
            bpy.context.scene.collection.objects.unlink(cube)  # Remove cube from default scene collection
            # Assign material randomly
            #assign_material_randomly(cube, blue_material, pink_material, chance=0.5)

    #return cube_locations, cubes


# Makes a layer of neurons other than the input layer - This needs to be connected to the weights. 
def create_shape_grid(n, spacing, size, y_position=0):
    cube_locations = []
    cubes = []
    cube_index = 1
    for i in range(n[0]):
        for j in range(n[1]):
            
            randomSpacing = random.uniform(spacing - 0.95, spacing + 0.95)
            
            x = j * (randomSpacing + size) - (n[1] - 1) * (randomSpacing + size) / 2
            y = random.uniform(y_position - 0.2, y_position + 0.2)
            z =  (n[0] - 1) * (randomSpacing + size) / 2 - i * (randomSpacing + size)
            
            # Create a new torus
            bpy.ops.mesh.primitive_torus_add(
                align='WORLD',
                location=(x, y, z),
                rotation=(x, y, z),
                major_radius=0.4,   # keeping this the same or making it larger
                minor_radius=0.03  # reducing this to make the torus skinny
            )
            cube = bpy.context.active_object
            cube.name = f"HiddenNeuron.{cube_index:03}"  # Names like inputCube.001, inputCube.002, etc.
            cube_index += 1
            
            cube.scale = (size, size, size)
            
            cube_locations.append(Vector((x, y, z, 0)))
            cubes.append(cube)
            # Create a material
            mat = bpy.data.materials.new(name=f"HiddenNeuron_Material_{i}_{j}")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes

            # Get Principled BSDF
            principled_bsdf = nodes.get("Principled BSDF")
            color_value = (0.2, 0.2, 0.2, 1.0) #light gray, fully opaque
            principled_bsdf.inputs["Base Color"].default_value = color_value
            
            #Collection
            input_layer_collection = bpy.data.collections["Input Layer"]
            # Move the created torus to the "Input Layer" collection
            input_layer_collection.objects.link(cube)  # Add cube to new collection
            bpy.context.scene.collection.objects.unlink(cube)  # Remove cube from default scene collection
            
            # Assign material randomly
            #assign_material_randomly(cube, blue_material, pink_material, chance=0.8)
            
    #return cube_locations, cubes

def get_weights(layer_num):
    """Get the weights of the given layer number."""
    return model.layers[layer_num].get_weights()[0]

def get_biases(layer_num):
    """Get the biases of the given layer number."""
    return model.layers[layer_num].get_weights()[1]

def create_neural_net_layer(layer_num, y_position):
    #y_position = 10 + (6 * layer_num)  # Calculate starting position based on layer number

    biases = get_biases(layer_num) # Load biases
    if biases is not None:  # Check if biases were loaded successfully
        # Convert biases into a square (or near-square) 2D array
        side = math.ceil(math.sqrt(biases.shape[0]))
        n = (side, side)
        
        print(n)
        print("creating shapes grid")
        create_shape_grid(n, spacing=0.5, size=1, y_position=y_position)
    else:
        print(f"Layer {layer_num} not found.")

def create_output_layer(layer_num, y_position):

    biases = get_biases(layer_num)  # Load biases
    if biases is not None:  # Check if biases were loaded successfully

        n = (biases.shape[0], 1)
        
        print(n)
        print("creating shapes grid")
        create_flat_cube_grid(n, 0.5, 4, y_position)
    else:
        print(f"Layer {layer_num} not found.")

def testFunction(layer_num):
    print("************layer biases:************")
    print(model.layers[layer_num].get_weights()[1])
    print("************layer weights:************")
    print(model.layers[layer_num].get_weights()[0])

#-----------------------RUN THE FUNCTIONS----------------------
print("-------------------------")

#delete_materials_and_cubes()
#image_array = make_image_array(image_path=image_path)
#create_input_feature_array(image_array=image_array)

#create_neural_net_layer(layer_num=0, y_position=10)
create_output_layer(layer_num=2, y_position=30)

#testFunction(1)
#for i, layer in enumerate(model.layers):
#    print(f"Layer {i}: {layer.name} - Type: {type(layer)}")