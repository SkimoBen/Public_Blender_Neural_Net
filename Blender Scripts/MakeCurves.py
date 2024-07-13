import bpy
import random 

def create_curve_from_points(point1, point2, thickness):
    """Create a poly curve from two points."""
    
    # Create a new curve data block
    curve_data = bpy.data.curves.new(name="NeuronConnection", type='CURVE')
    curve_data.dimensions = '3D'
    
    # Create a new spline in the curve
    spline = curve_data.splines.new('POLY')
    spline.points.add(1)  # Since it starts with one point by default

    # Assign coordinates to the two points of the spline
    spline.points[0].co = (point1.x, point1.y, point1.z, 1)  # The fourth value is for the weight of the point
    spline.points[1].co = (point2.x, point2.y, point2.z, 1)

    # Create a new object using the curve data block and link it to the scene
    curve_obj = bpy.data.objects.new("InputNeuronConnection", curve_data)
    bpy.context.collection.objects.link(curve_obj)
    
    # Set curve thickness
    curve_data.bevel_depth = thickness
    
    return curve_obj


def connect_collections(point_a, point_b, thickness):
    """Connect objects from two collections using curves."""

    coll_a = bpy.data.collections[point_a]
    coll_b = bpy.data.collections[point_b]

    for index_a, obj_a in enumerate(coll_a.objects):
        for index_b, obj_b in enumerate(coll_b.objects):
            
            # Only connect every 400th object
            if index_a % 100 != 0 or index_b % 100 != 0:
                continue

            # Create curve connecting the two objects
            curve_obj = create_curve_from_points(obj_a.location, obj_b.location, thickness)
            
            # Assign default material to the curve
            mat_name = "InputNeuronConnectionMaterial"
            
            # Check if material exists, if not create it
            if mat_name not in bpy.data.materials:
                mat = bpy.data.materials.new(name=mat_name)
                mat.use_nodes = True
            else:
                mat = bpy.data.materials[mat_name]

            # Assign material to curve
            if curve_obj.data.materials:
                curve_obj.data.materials[0] = mat
            else:
                curve_obj.data.materials.append(mat)


def connect_collections_randomly(point_a, point_b, thickness):
    """Connect objects from two collections using curves."""

    coll_a = bpy.data.collections[point_a]
    coll_b = bpy.data.collections[point_b]

    # Probability to connect a pair of objects. Here, approximately every 400th object will be connected.
    probability = 1/100

    for obj_a in coll_a.objects:
        for obj_b in coll_b.objects:
            
            # Connect objects based on probability
            if random.random() > probability:
                continue

            # Create curve connecting the two objects
            create_curve_from_points(obj_a.location, obj_b.location, thickness)              

def get_nearest_objects(curve_obj, coll_a, coll_b):
    # Get curve's start and end points
    spline = curve_obj.data.splines[0]
    start_point = curve_obj.matrix_world @ spline.points[0].co.to_3d()
    end_point = curve_obj.matrix_world @ spline.points[-1].co.to_3d()

    nearest_obj_a = min(coll_a.objects, key=lambda x: (x.location - start_point).length)
    nearest_obj_b = min(coll_b.objects, key=lambda x: (x.location - end_point).length)
    
    return nearest_obj_a, nearest_obj_b


def store_curve_points():
    collection_curves = bpy.data.collections.get('Curves 2')
    collection_a = bpy.data.collections.get('Input Features')
    collection_b = bpy.data.collections.get('Output Layer')

    # This will store the start and end objects for each curve.
    curve_connections = {}

    # Assuming we're running this once to compute and store the connections.
    for curve in collection_curves.objects:
        obj_a, obj_b = get_nearest_objects(curve, collection_a, collection_b)
        curve_connections[curve.name] = (obj_a.name, obj_b.name)

        # Storing the connection data in the curve's custom properties
        curve["Connected_A"] = obj_a.name
        curve["Connected_B"] = obj_b.name
        

def delete_evenly_spaced_curves(collection_name, percentage):
    collection = bpy.data.collections.get(collection_name)
    
    if not collection:
        print(f"Collection {collection_name} not found.")
        return

    # Collect all the curves in the collection
    curve_objs = [obj for obj in collection.objects if obj.type == 'CURVE']
    
    # Calculate step size based on desired percentage to delete
    step_size = max(1, int(1 / percentage))

    # Select every nth curve based on the calculated step size
    to_delete = curve_objs[::step_size]
    print(to_delete)
    
    # Delete the selected curves
    bpy.ops.object.select_all(action='DESELECT')
    for obj in to_delete:
        obj.select_set(True)
    
    bpy.ops.object.delete()
    

# ------RUN FUNCTIONS--------------
#connect_collections_randomly("Input Features", "Input Layer", 0.001)
#delete_evenly_spaced_curves("Curves 2", 1)

store_curve_points()