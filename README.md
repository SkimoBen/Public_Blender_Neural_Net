# Public_Blender_Neural_Net
This is a repo for the code I used to visualize a neural network in Blender

# How to use it
First use the CreateModel.py script in VSCode to train a CNN. Or train one on your own data. 
Then open the scripting console in Blender and use the files in Blender Scripts. 
First you have to generate the neural net using the MakeNeuralNet, MakeCurves, and AssignMaterials.py scripts. 
Then you can run the model. Use the activation functions to update the materials in your neural net. 

# New versions of Blender don't play well with Tensorflow.
I think I used version 2.8... 

# Notes

This code was never intended for other people to use so it's really messy. I was constantly going back and fort changing things so this probably won't even be super helpful for other people but the basic concept is this: 

- Train a model
- Use the model params to generate 3d objects and curves in Blender. Unless you have a really powerful computer, you should limit this to a ratio so you don't have millions of objects.
- Run the model using tensorflow inside Blender. take the outputs from the activation functions to change the material paramaters of the objects.
