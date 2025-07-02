# Fashion MNIST Classification using PyTorch and Keras

This project compares the performance of deep learning models implemented in **PyTorch** and **Keras** on the Fashion MNIST dataset. The goal was to experiment with architecture, tuning learning rates, and benchmarking model accuracy across frameworks.

## 📊 Problem Statement
Classify grayscale 28x28 images of clothing items into one of 10 categories (e.g., T-shirt, Trouser, Coat) using neural networks. Evaluate performance across multiple learning rates and visualize accuracy trends.

## 🧠 Models Built
- **Architecture**: 2 dense layers (ReLU activations) + softmax output layer
- **Frameworks Used**: Keras (TensorFlow backend) and PyTorch
- **Hyperparameters**:  
  - Batch size: 60  
  - Epochs: 16  
  - Learning Rates: 0.0001 to 0.0199 (20+ models trained per framework)

## ✅ Results
- **Best Test Accuracy**: Achieved up to **97%** using Keras and **96.5%** using PyTorch
- **Key Insight**: Keras models were faster to converge, while PyTorch allowed better control for experimentation
- **Visualization**: Accuracy plotted against learning rates for both frameworks

## 🛠️ Technologies Used
- Python, NumPy, Pandas, Matplotlib, Seaborn  
- TensorFlow (Keras API), PyTorch  
- Google Colab (Training Environment)
