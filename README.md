# External PID Control Architecture for Drone Simulation (Gazebo)

This project demonstrates an architecture where a drone’s PID controller is **decoupled from the simulator** and executed on an **external controller device**, while the drone dynamics are simulated in **:contentReference[oaicite:0]{index=0}**.

The goal is to validate whether a PID controller running on a dedicated device can stably control a drone when its outputs are fed back into the simulation.  
This approach follows **SIL / HIL-like principles** and helps bridge the gap between simulation and real hardware.

---

## 🧠 Concept Overview

Instead of running the PID controller inside the simulator:

- Gazebo simulates **physics, motors, and sensors**
- Sensor data is sent to an **external controller**
- The external device computes **PID control outputs**
- Motor commands are sent back to Gazebo
- Drone behavior is observed for stability and performance

This setup closely resembles real-world flight controller architectures.

---

## 🏗️ System Architecture

High-level data flow:

```

Gazebo Simulator
(Drone + Physics)
|
|  Sensor Data (IMU, Pose, Velocity)
v
Interface / Bridge Layer
|
v
External Controller Device
(PID Control Loop)
|
|  Motor Commands (PWM / Thrust / Torque)
v
Interface / Bridge Layer
|
v
Gazebo Motor Plugin

```

---

## 🧩 Components

### 1. Gazebo Simulator
- Drone model (URDF / SDF)
- Physics engine
- Motor and actuator plugins
- Sensor plugins:
  - IMU
  - Position
  - Velocity
  - Attitude

Gazebo is responsible **only for simulation**, not control.

---

### 2. Interface / Bridge Layer
Acts as a communication and translation layer between Gazebo and the external controller.

Responsibilities:
- Message serialization / deserialization
- Coordinate frame conversion (ENU ↔ NED)
- Time synchronization
- Communication protocol handling

Possible implementations:
- **:contentReference[oaicite:1]{index=1}** topics/services
- UDP / TCP sockets
- MAVLink

---

### 3. External Controller Device
A dedicated hardware or software unit running the control logic.

Responsibilities:
- Receive sensor data
- Run PID controllers:
  - Roll PID
  - Pitch PID
  - Yaw PID
  - Altitude PID
- Maintain a fixed control loop rate (e.g. 200–400 Hz)
- Output motor commands

This device emulates a real flight controller behavior.

---

### 4. Motor Command Feedback
Control outputs are sent back to Gazebo, where:
- Motor plugins apply thrust and torque
- Drone motion updates according to physics
- New sensor data is generated

This closes the control loop.

---

## ⏱️ Timing and Control Loop

- The external controller runs on **real time**
- Gazebo may run on **simulated time**
- Control loop frequency must be stable
- Latency directly affects PID stability

Recommended:
- Fixed-rate loop on the controller
- Monitor round-trip delay

---

## ⚠️ Critical Considerations

- **Coordinate Frames**
  - ENU vs NED mismatches can break control logic
- **Latency**
  - Communication delay can cause oscillations
- **Sensor Noise**
  - Should be enabled for realism
- **Scaling**
  - Motor thrust and torque units must match simulation model

---

## 🎯 What This Architecture Enables

- PID tuning before real flight
- Testing under latency and noise
- Validation of control logic on real hardware
- Safer transition to real drone experiments

---

## 🚀 Next Steps

Possible extensions:
- Replace PID with LQR or MPC
- Add state estimation (EKF)
- Transition to real flight controller hardware
- Full Hardware-in-the-Loop (HIL) setup

---

## 📌 Summary

This project provides a clean separation between:
- **Simulation (Gazebo)**
- **Control (External Device)**

It is a practical and scalable approach for developing reliable drone control systems before deploying on real hardware.



