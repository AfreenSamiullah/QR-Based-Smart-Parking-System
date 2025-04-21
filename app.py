import cv2
import serial
import time
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import LabelEncoder

# Load the trained ML model
model = load_model('vit_waste_classifier_150x150_3classes.h5')

# Define the labels that the model predicts
labels = ['metal', 'organic', 'plastic','paper','other']  # Update according to training order
le = LabelEncoder()
le.fit(labels)

# Open serial connection with Arduino
arduino = serial.Serial('COM6', 9600, timeout=1)

# Preprocessing function
def preprocess(img):
    # Resize to model input size
    img = cv2.resize(img, (224, 224))
    
    # Convert to HSV for better color filtering
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define red ranges in HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    # Create masks for both red ranges
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Invert mask to get non-red (object) area
    object_mask = cv2.bitwise_not(red_mask)

    # Apply mask to original image
    masked_img = cv2.bitwise_and(img, img, mask=object_mask)

    # Optional: Replace red background with white
    white_bg = np.full(img.shape, 255, dtype=np.uint8)
    final_img = np.where(masked_img == 0, white_bg, masked_img)

    # Normalize for model
    final_img = img_to_array(final_img)
    final_img = np.expand_dims(final_img / 255.0, 0)

    return final_img


# Use USB camera (camera index 1)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Could not access USB camera.")
    exit()

print("🔄 Waiting for infrared signal from Arduino...")

while True:
    # Show live feed
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Live Feed', frame)

    # Wait for signal from Arduino
    if arduino.in_waiting > 0:
        arduino_input = arduino.readline().decode().strip()
        print(f"📩 Received from Arduino: {arduino_input}")

        if arduino_input == "DETECT":
            print("📸 Object detected! Capturing image...")

            time.sleep(7)
            ret, img = cap.read()
            if not ret:
                print("⚠️ Image capture failed.")
                continue

            # Display captured image (optional)
            cv2.imshow('Captured Image', img)
            cv2.waitKey(1000)
            cv2.destroyWindow('Captured Image')

            # Preprocess and predict
            img1 = preprocess(img)
            prediction = model.predict(img1)
            predicted_index = np.argmax(prediction[0])
            predicted_class = le.classes_[predicted_index]
            confidence = np.max(prediction[0])

          
            print(f"✅ Predicted: {predicted_class}, Confidence: {confidence:.3f}")

            if confidence > 0.2:
                arduino.write(mapped_class.encode())
                print(f"📤 Sent to Arduino: {mapped_class}")

                # Wait for Arduino to confirm
                while True:
                    response = arduino.readline().decode().strip()
                    if response == "OK":
                        print("✅ Arduino confirmed execution")
                        break
            else:
                print("⚠️ Low confidence. Skipping sending.")

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
