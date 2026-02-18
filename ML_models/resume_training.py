import os
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
tf.config.threading.set_intra_op_parallelism_threads(2)
tf.config.threading.set_inter_op_parallelism_threads(2)


# =========================
# Paths
# =========================
MODEL_PATH = "garbage_cnn_model.h5"           # existing model
UPDATED_MODEL_PATH = "garbage_cnn_model_updated.h5"
HISTORY_PATH = "history.pkl"
DATASET_DIR = "dataset_3class-2"                # your 3-class dataset

# =========================
# Load existing model
# =========================
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found.")

model = load_model(MODEL_PATH)
print("Loaded model:", MODEL_PATH)

# =========================
# Compile model (needed after loading)
# =========================
model.compile(
    optimizer=Adam(learning_rate=1e-4),  # smaller LR for fine-tuning
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# =========================
# Data Generators
# =========================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(128, 128),
    batch_size=16,
    class_mode='categorical',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(128, 128),
    batch_size=8,
    class_mode='categorical',
    subset='validation'
)

# =========================
# Continue Training
# =========================
history = model.fit(
    train_generator,
    epochs=10,  # number of additional epochs
    validation_data=val_generator
)

# =========================
# Save updated model
# =========================
model.save(UPDATED_MODEL_PATH)
print("Updated model saved as:", UPDATED_MODEL_PATH)

# =========================
# Save training history for plotting
# =========================
with open(HISTORY_PATH, "wb") as f:
    pickle.dump(history.history, f)

print("Training history saved as:", HISTORY_PATH)
