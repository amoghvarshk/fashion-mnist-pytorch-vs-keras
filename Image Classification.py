
"""

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

import torch
from torchvision import datasets
from torchvision.transforms import ToTensor
import numpy as np

"""# Read Dataset"""

# read fashion MNist Dataset
# https://keras.io/api/datasets/mnist/
from tensorflow import keras

(data_train, out_train), (data_test, out_test) = keras.datasets.mnist.load_data()
data_train.shape, out_train.shape, data_test.shape, out_test.shape

"""# Preprocessing"""

# Transformation
in_train = data_train.reshape(-1, 28 * 28) / 255.0
in_test = data_test.reshape(-1, 28 * 28) / 255.0
in_train.min(), in_train.max(), in_test.min(), in_test.max()

out_train = keras.utils.to_categorical(out_train, num_classes=10)
out_test = keras.utils.to_categorical(out_test, num_classes=10)

# reshaping data for Torch
import torch
import numpy as np

in_train_torch = torch.tensor(in_train, dtype=torch.float32)
out_train_torch = torch.tensor(np.argmax(out_train, axis=1), dtype=torch.long)

# estimating numbers of units in layers
shape_input = data_train[0].shape
units_output = np.unique(out_train).size
ratio = np.cbrt(np.prod(shape_input) / units_output)
units_layer1 = int(units_output * ratio * ratio)
units_layer2 = int(units_output * ratio)
np.prod(shape_input), units_layer1, units_layer2, units_output

# Setting Parameters
seed = 42
batch_size = 60
epochs = 16

# Setting random seeds
#https://www.tensorflow.org/api_docs/python/tf/keras/utils/set_random_seed
import tensorflow as tf

tf.random.set_seed(seed)
torch.manual_seed(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# create data loaders
from torch.utils.data import DataLoader
train_data = torch.utils.data.TensorDataset(in_train_torch, out_train_torch)
load_trainset = DataLoader(train_data, batch_size=batch_size, shuffle=True)
len(load_trainset)

"""# Keras Model"""

# Keras model creation function
# https://www.tensorflow.org/api_docs/python/tf/keras/activations/relu
def build_keras_model(input_shape, units_layer1, units_layer2):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units_layer1, activation='relu', input_shape=input_shape),
        tf.keras.layers.Dense(units_layer2, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    return model

# Keras model training function
def train_keras_model(model, optimizer, loss_function, x_train, y_train, epochs, lr):
    optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=lr)
    model.compile(optimizer=optimizer, loss=loss_function, metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=0)
    return model

#https://keras.io/api/optimizers/adam/Links
#https://keras.io/api/losses/Links
optimizer_keras = tf.keras.optimizers.Adam()
loss_function_keras = tf.keras.losses.CategoricalCrossentropy()

"""# Torch Model"""

# Torch model creation function
# https://www.tensorflow.org/api_docs/python/tf/keras/activations/relu
def build_torch_model(input_size, units_layer1, units_layer2):
    model = torch.nn.Sequential(
        torch.nn.Linear(input_size, units_layer1),
        torch.nn.ReLU(),
        torch.nn.Linear(units_layer1, units_layer2),
        torch.nn.ReLU(),
        torch.nn.Linear(units_layer2, 10),
        torch.nn.Softmax(dim=1)
    )
    return model

# Torch model training function
def train_torch_model(model, optimizer, loss_function, train_loader, epochs):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_function(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        accuracy = correct / total
        print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss}, Accuracy: {accuracy}")
    return model

#https://keras.io/api/optimizers/adam/Links
#https://keras.io/api/losses/Links
optimizer_torch = torch.optim.Adam
loss_function_torch = torch.nn.CrossEntropyLoss()

"""# Training Accuracies"""

# plotting training accuracies
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_accuracies(learning_rates):
    keras_accuracies = []
    torch_accuracies = []
    for lr in learning_rates:
        keras_model = build_keras_model((784,), units_layer1, units_layer2)
        torch_model = build_torch_model(784, units_layer1, units_layer2)

        optimizer_torch = torch.optim.Adam(torch_model.parameters(), lr=lr)

        trained_keras_model = train_keras_model(keras_model, optimizer_keras, loss_function_keras, in_train, out_train, epochs, lr)
        keras_accuracy = trained_keras_model.evaluate(in_test, out_test, verbose=0)[1]
        keras_accuracies.append(keras_accuracy)

        trained_torch_model = train_torch_model(torch_model, optimizer_torch, loss_function_torch, load_trainset, epochs)
        with torch.no_grad():
            outputs = trained_torch_model(in_train_torch)
            torch_accuracy = (torch.argmax(outputs, dim=1) == out_train_torch).float().mean().item()
            torch_accuracies.append(torch_accuracy)

    return keras_accuracies, torch_accuracies

learning_rates = np.arange(0.0001, 0.0199, 0.0009)

keras_accuracies, torch_accuracies = calculate_accuracies(learning_rates)

def plot_accuracies(keras_accuracies, torch_accuracies, learning_rates):
    plt.figure(figsize=(10, 6))
    sns.set_style("ticks")
    sns.lineplot(x=learning_rates, y=keras_accuracies, label='Keras Model', marker='o', linestyle='-', markersize=8, color='dodgerblue')
    sns.lineplot(x=learning_rates, y=torch_accuracies, label='Torch Model', marker='s', linestyle='--', markersize=8, color='crimson')
    plt.xlabel('Learning Rate', fontsize=12, fontweight='bold')
    plt.ylabel('Training Accuracy', fontsize=12, fontweight='bold')
    plt.title('Keras V/s Torch Model Training Accuracies', fontsize=14, fontweight='bold')
    y_ticks = plt.yticks()[0]
    for y_tick in y_ticks:
        plt.axhline(y=y_tick, color='black', linestyle='-', linewidth=0.7)
    plt.legend(fontsize=12)
    plt.xticks(learning_rates, rotation=45)
    plt.tight_layout()
    plt.show()

plot_accuracies(keras_accuracies, torch_accuracies, learning_rates)
