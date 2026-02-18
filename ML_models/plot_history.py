import pickle
import matplotlib.pyplot as plt

# =========================
# Load saved training history
# =========================
HISTORY_PATH = "history.pkl"

with open(HISTORY_PATH, "rb") as f:
    history = pickle.load(f)

# =========================
# Plot Training & Validation Accuracy
# =========================
plt.figure(figsize=(8, 6))
plt.plot(history['accuracy'], label='Training Accuracy')
plt.plot(history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()

# =========================
# Plot Training & Validation Loss
# =========================
plt.figure(figsize=(8, 6))
plt.plot(history['loss'], label='Training Loss')
plt.plot(history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()
