# QR-Based-Smart-Parking-System
An automated parking management system using IR sensors to trigger dynamic QR code generation (Python), LoRa-enabled communication between Arduino and ESP32-CAM for QR decoding/validation, and servo-actuated parking slots that open/close based on entry-exit scans, optimizing space utilization through real-time slot tracking.

# Vision-Based Intelligent Waste Segregator

An automated waste management system that uses computer vision and deep learning to identify and sort waste items into organic, metal, or plastic categories, integrating real-time hardware control for efficient and contactless segregation.

---

## Features

- **Automated Waste Detection:** Uses IR sensors to detect the presence of waste.
- **Computer Vision Classification:** Captures an image with a webcam and classifies waste using a trained deep learning model.
- **Real-Time Sorting:** Controls stepper and servo motors to direct waste into the correct bin based on classification.
- **Multi-Class Support:** Segregates waste into organic, metal, and plastic.
- **Integrated Hardware:** Seamless communication between Python (for vision and ML) and Arduino (for motor and sensor control).

---

## System Overview

1. **Object Detection:** IR sensor detects an object in the placeholder.
2. **Image Capture:** Webcam is triggered to capture an image of the waste.
3. **Classification:** Image is sent to a deep learning model (ViT) that classifies the waste as organic, metal, or plastic.
4. **Bin Selection:** Based on the model's output, the corresponding bin is positioned under the placeholder using a stepper motor.
5. **Waste Disposal:** A servo motor opens the base of the placeholder to drop the waste into the selected bin.
6. **Reset:** Bins are rotated back to their default position, ready for the next cycle.

---

## Tech Stack

- **Python:** OpenCV, TensorFlow/Keras, NumPy, scikit-learn, pyserial
- **Embedded:** Arduino IDE, C++
- **Hardware:** Arduino Uno, Stepper Motor (NEMA 17), Servo Motor (SG90), IR Sensor, Webcam

---

## Setup Instructions

1. **Hardware Assembly:**  
   - Connect IR sensor to Arduino digital input.
   - Connect stepper motor and servo motor to appropriate Arduino pins (with motor drivers as needed).
   - Connect webcam to the computer running the Python script.

2. **Software Installation:**  
   - Install Python 3.x and required libraries:
     ```
     pip install opencv-python tensorflow keras numpy scikit-learn pyserial
     ```
   - Upload the provided Arduino code to your Arduino board using Arduino IDE.

3. **Model Preparation:**  
   - Place your trained waste classification model (`vit_waste_classifier_150x150_3classes.h5`) in the project directory.

4. **Run the System:**  
   - Start the Arduino and ensure it is connected via USB.
   - Run the Python script:
     ```
     python waste_segregator.py
     ```
   - The system will wait for an object to be detected and then automatically perform the classification and sorting process.

---

## How It Works

- **Image Processing:** The system preprocesses images to filter out backgrounds and enhance object visibility before classification.
- **Machine Learning:** A deep learning model classifies the waste item, and the result is sent to Arduino via serial communication.
- **Motor Control:** Arduino receives the classification and actuates the stepper and servo motors to position the correct bin and release the waste.

---

## Demo

- [Project Demo Video](https://drive.google.com/file/d/1DFNd9AVz3-RA7czPCPDskEgJ56WzeTbc/view?usp=sharing)

---

## Contribution

Contributions, suggestions, and feedback are welcome! Please open an issue or pull request to help improve the project.

---

## Acknowledgments

Inspired by sustainable waste management initiatives and leveraging advances in computer vision and embedded systems.

---
