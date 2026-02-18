import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load trained model
model = load_model("garbage_cnn_model_updated.h5")

# Class labels (must match your 3 categories)
classes = ["organic", "recyclable", "hazardous"]

# Start webcam
cap = cv2.VideoCapture(0)  # 0 = default camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    img = cv2.resize(frame, (128, 128))  # same size as training
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    # Predict
    prediction = model.predict(img)
    class_index = np.argmax(prediction)
    label = classes[class_index]

    # Show label on frame
    cv2.putText(frame, f"Prediction: {label}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Waste Classification - Live", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
