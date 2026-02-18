import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

tf.config.threading.set_intra_op_parallelism_threads(2)
tf.config.threading.set_inter_op_parallelism_threads(2)


# -----------------------
# 1. Dataset Preparation
# -----------------------
# Assuming you have a folder structure like:
# dataset/
#    train/
#       organic/
#       recyclable/
#       hazardous/
#    val/
#       organic/
#       recyclable/
#       hazardous/

train_dir = "dataset_3class"
val_dir = "dataset_3class"

# Data Augmentation + Normalization
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),
    batch_size=8,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical'
)

# -----------------------
# 2. Build CNN Model
# -----------------------
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(train_generator.num_classes, activation='softmax')
])

# -----------------------
# 3. Compile Model
# -----------------------
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# -----------------------
# 4. Train Model
# -----------------------
history = model.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator
)

# -----------------------
# 5. Save Model
# -----------------------
model.save("garbage_cnn_model.h5")
print("Model saved as garbage_cnn_model.h5")

