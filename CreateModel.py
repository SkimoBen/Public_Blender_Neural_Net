import tensorflow as tf
from tensorflow.keras import layers, models

# Load MNIST dataset

mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
print("Got MNIST")

# Normalize the data
train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype("float32") / 255

print("preprocessed  trainimages")
test_images = test_images.reshape((10000, 28 * 28))

test_images = test_images.astype("float32") / 255
print("preprocessed images")

train_labels = tf.keras.utils.to_categorical(train_labels)
print("preprocessed train labels")

test_labels = tf.keras.utils.to_categorical(test_labels)
print("preprocessed  test labels")

# Build the model
model = models.Sequential()
model.add(layers.Dense(512, activation="relu", input_shape=(28 * 28,)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(10, activation="softmax"))
print("built model skeleton")

 
# Compile the model
model.compile(optimizer="adam",
              loss="categorical_crossentropy",
              metrics=["accuracy"])

print("created model skeleton. 'compiled model'")
 
# Train the model
model.fit(train_images, train_labels, epochs=5, batch_size=128)
print("trained model, now testing.")
 
# Evaluate the model
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"Test accuracy: {test_acc}")

# Save the model
model.save("mnist_model.h5")

 