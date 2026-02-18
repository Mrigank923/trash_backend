import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load trained model
model = load_model("garbage_cnn_model_balanced.h5")
classes = ["organic", "recyclable", "hazardous"]

# Start webcam
cap = cv2.VideoCapture(0)

# Make the window full screen
cv2.namedWindow("Waste Classification - Live", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Waste Classification - Live", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for object segmentation
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours (potential objects)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Filter small objects/noise
        if w > 50 and h > 50:
            roi = frame[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi, (128, 128))  # match training size
            roi_resized = roi_resized.astype("float32") / 255.0
            roi_resized = np.expand_dims(roi_resized, axis=0)

            # Predict class
            prediction = model.predict(roi_resized, verbose=0)
            class_index = np.argmax(prediction)
            label = classes[class_index]

            # Draw bounding box and label
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show result
    cv2.imshow("Waste Classification - Live", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

