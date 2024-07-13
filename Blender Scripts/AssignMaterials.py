import bpy

def assign_hidden_materials(num_hidden_neurons):
    """Assign materials to hidden neurons."""
    
    for i in range(num_hidden_neurons):
        neuron_name = f"HiddenNeuron.{i+1:03}"
        material_name = f"HiddenNeuronMaterial_{i}"
        
        # Check if material exists, if not create it
        if material_name not in bpy.data.materials:
            mat = bpy.data.materials.new(name=material_name)
        else:
            mat = bpy.data.materials[material_name]
        
        # Enable use of nodes
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        
        # Clear default nodes
        nodes.clear()
        
        # Add a Principled BSDF shader node
        principled = nodes.new(type="ShaderNodeBsdfPrincipled")
        principled.location = (0,0)
        
        # Add a Material Output node and link Principled BSDF to it
        material_output = nodes.new(type="ShaderNodeOutputMaterial")
        material_output.location = (400,0)
        
        # Create a link from the Principled BSDF node to the Material Output node
        mat.node_tree.links.new(principled.outputs["BSDF"], material_output.inputs["Surface"])
        
        # Assign the material to the neuron
        neuron = bpy.data.objects[neuron_name]
        if neuron.data.materials:
            neuron.data.materials[0] = mat
        else:
            neuron.data.materials.append(mat)

def assign_output_materials(num_output_neurons):
    """Assign materials to output neurons."""
    
    for i in range(num_output_neurons):
        neuron_name = f"OutputCube.{i+1:03}"
        material_name = f"OutputNeuronMaterial_{i}"
        
        # Check if material exists, if not create it
        if material_name not in bpy.data.materials:
            mat = bpy.data.materials.new(name=material_name)
        else:
            mat = bpy.data.materials[material_name]
        
        # Enable use of nodes
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        
        # Clear default nodes
        nodes.clear()
        
        # Add a Principled BSDF shader node
        principled = nodes.new(type="ShaderNodeBsdfPrincipled")
        principled.location = (0,0)
        
        # Add a Material Output node and link Principled BSDF to it
        material_output = nodes.new(type="ShaderNodeOutputMaterial")
        material_output.location = (400,0)
        
        # Create a link from the Principled BSDF node to the Material Output node
        mat.node_tree.links.new(principled.outputs["BSDF"], material_output.inputs["Surface"])
        
        # Assign the material to the neuron
        neuron = bpy.data.objects[neuron_name]
        if neuron.data.materials:
            neuron.data.materials[0] = mat
        else:
            neuron.data.materials.append(mat)

# Call the functions
#assign_hidden_materials(num_hidden_neurons=529)
#assign_output_materials(num_output_neurons=10)

def assignCurveMaterials(collectionName):
    # Get the collection named 'Curves 1'
    collection = bpy.data.collections.get(collectionName)

    if collection:
        # Iterate over all objects inside the collection
        for obj in collection.objects:
            # Ensure the object is of type 'CURVE'
            if obj.type == 'CURVE':
                # Create a new material
                mat_name = obj.name + "_mat"
                mat = bpy.data.materials.new(name=mat_name)
                
                # Enable use of nodes
                mat.use_nodes = True
                nodes = mat.node_tree.nodes

                # Clear default nodes
                for node in nodes:
                    nodes.remove(node)

                # Add a Principled BSDF shader and connect it to the Material Output
                shader = nodes.new(type='ShaderNodeBsdfPrincipled')
                shader.location = (0,0)
                output = nodes.new(type='ShaderNodeOutputMaterial')
                output.location = (400,0)
                links = mat.node_tree.links
                link = links.new
                link(shader.outputs["BSDF"], output.inputs["Surface"])

                # Assign it to the object
                obj.data.materials.append(mat)
    else:
        print("Collection 'Curves 1' not found.")

assignCurveMaterials("Curves 2") 