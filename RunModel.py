import numpy as np
import bpy
import math
from PIL import Image

def make_image_array():
    # Load and preprocess image using PIL
    image_path = "YOUR INPUT IMAGE PATH"

    # Open the image file
    with Image.open(image_path) as img:
        # Convert the image to grayscale
        grayscale_img = img.convert("L")
        
        # Convert to numpy array and normalize
        image_array = np.array(grayscale_img) / 255.0

    return image_array

# Full path to where your weights are saved
path_to_weights = "PATH TO YOUR MODEL WEIGHTS"

# Load weights and biases
loaded_weights = []
for i in range(4):  # You have 2 layers: 2 weights and 2 biases
    weight_file_path = f"{path_to_weights}weight_{i}.npy"  # Full path to the weight file
    loaded_weights.append(np.load(weight_file_path))

def relu(x):
    return np.maximum(0, x)

def softmax(x):
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=-1, keepdims=True)

def forward_pass(input_data, weights):
    # First dense layer
    z1 = np.dot(input_data, weights[0]) + weights[1]
    a1 = relu(z1)

    # Dropout is generally turned off at test time, so we skip it
    
    # Output layer
    z2 = np.dot(a1, weights[2]) + weights[3]
    output = softmax(z2)

    return output

image_array = make_image_array()

# Flatten and normalize the 28x28 image to a 784x1 array
input_data = image_array.flatten()
input_data = input_data.astype("float32")

# Reshape data to have a batch dimension
input_data = np.reshape(input_data, (1, 784))

# Perform the forward pass
loaded_weights = None  # Replace with actual loaded weights
output = forward_pass(input_data, loaded_weights)

# Interpret the output (it's a 1x10 array, because we have 10 classes)
predicted_label = np.argmax(output)

print(f"The model predicts the label as {predicted_label}")
