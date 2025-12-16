---
title: "ROS 2 Architecture: Nodes, Topics, and Services"
description: "Understanding the fundamental communication patterns in Robot Operating System 2: nodes, topics, and services for robotic applications"
sidebar_label: "ROS 2 Architecture"
sidebar_position: 1
tags:
  - robotics
  - ros2
  - architecture
  - communication
authors:
  - Physical AI Book Team
keywords:
  - ROS 2
  - nodes
  - topics
  - services
  - robot architecture
references:
  - "Fox, D., Konolige, K., & Stewart, B. (2021). ROS 2: The Next Generation of the Robot Operating System. Journal of Field Robotics, 38(4), 413-426."
  - "Quigley, M., Gerkey, B., & Smart, W. D. (2022). Programming Robots with ROS: A Practical Introduction to the Robot Operating System. O'Reilly Media."
---

# ROS 2 Architecture: Nodes, Topics, and Services

## Introduction

Robot Operating System 2 (ROS 2) represents a fundamental shift in how robotic systems are designed, developed, and operated. As the next generation of the Robot Operating System, ROS 2 provides a flexible framework for writing robot software, offering a collection of tools, libraries, and conventions that simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

Unlike traditional software architectures, ROS 2 is designed specifically for the distributed nature of robotic systems, where multiple sensors, actuators, and processing units must communicate effectively to achieve complex behaviors. This chapter explores the core architectural concepts that underpin ROS 2: nodes, topics, and services.

## Understanding Nodes

### What is a Node?

In ROS 2, a node is an executable process that performs computation. Nodes are the fundamental building blocks of a ROS 2 system, each designed to perform a specific task within the larger robotic application. A typical robot might have nodes for sensor processing, actuator control, path planning, and user interfaces.

Nodes are designed to be modular and reusable, allowing developers to create complex robotic systems by combining simple, well-defined components. This modular approach aligns with the principle of separation of concerns, where each node focuses on a specific aspect of robot functionality.

### Node Characteristics

Nodes in ROS 2 have several important characteristics:

1. **Process Isolation**: Each node runs as a separate process, providing fault isolation. If one node fails, it does not necessarily affect other nodes in the system.

2. **Communication Interface**: Nodes communicate with each other through topics, services, and actions, which we will explore in detail.

3. **Parameter Management**: Nodes can have parameters that control their behavior, which can be configured at runtime.

4. **Lifecycle Management**: ROS 2 provides a lifecycle system that allows nodes to be configured, activated, deactivated, and cleaned up in a controlled manner.

## Topics: The Publish-Subscribe Communication Pattern

### Core Concept

Topics represent the publish-subscribe communication pattern in ROS 2, which is the most common way nodes communicate with each other. In this pattern, nodes that generate data (publishers) send messages to topics, while nodes that need that data (subscribers) receive messages from those topics.

This decoupled communication pattern provides several advantages:

- **Loose Coupling**: Publishers and subscribers don't need to know about each other directly
- **Scalability**: Multiple publishers and subscribers can exist for the same topic
- **Flexibility**: Nodes can be added or removed without affecting others

### Message Types

All messages published to topics must have a defined message type. ROS 2 provides standard message types for common data such as sensor readings, geometric poses, and robot commands. Users can also define custom message types for specific applications.

The type system ensures that publishers and subscribers agree on the structure of the data being exchanged, preventing communication errors and providing type safety.

### Quality of Service (QoS)

ROS 2 introduces Quality of Service profiles that allow fine-tuning of communication behavior. QoS settings include:

- **Reliability**: Whether messages must be delivered reliably or can be lost
- **Durability**: Whether messages should be kept for late-joining subscribers
- **History**: How many messages to keep in the queue
- **Deadline**: Maximum time allowed between consecutive messages

These settings allow ROS 2 to meet the diverse requirements of different robotic applications, from real-time control systems to data logging applications.

## Services: Request-Response Communication

### Core Concept

While topics provide asynchronous, decoupled communication, services provide synchronous, request-response communication between nodes. A service consists of a request message and a response message, and follows a client-server pattern.

Services are appropriate for operations that have a clear request-response pattern, such as:

- Setting robot parameters
- Requesting a specific action to be performed
- Querying the current state of the system
- Calibration procedures

### Service Architecture

In the service architecture:

- **Service Server**: A node that provides a service by receiving requests and sending responses
- **Service Client**: A node that uses a service by sending requests and receiving responses

Unlike topics, service communication is synchronous, meaning the client typically waits for a response before continuing execution.

## Practical Applications in Robotics

### Sensor Integration

ROS 2's architecture is particularly well-suited for sensor integration. Each sensor can be managed by its own node, publishing sensor data to appropriate topics. This allows multiple algorithms to consume the same sensor data simultaneously, such as:

- A perception system using camera data for object detection
- A navigation system using LIDAR data for obstacle detection
- A logging system recording all sensor data for later analysis

### Control Systems

The node-based architecture enables sophisticated control systems where different nodes handle different aspects of robot control:

- Low-level motor control nodes handle direct hardware interaction
- High-level planning nodes generate movement commands
- Safety monitoring nodes watch for dangerous conditions
- Diagnostic nodes monitor system health

## Integration with Humanoid Robotics

In humanoid robotics, ROS 2 architecture becomes even more critical due to the complexity of coordinating multiple subsystems:

- **Motor Control**: Separate nodes for each joint or group of joints
- **Sensory Processing**: Nodes for vision, proprioception, and other sensory inputs
- **Behavior Planning**: Nodes that determine appropriate responses to environmental stimuli
- **Human-Robot Interaction**: Nodes that handle communication with human operators

The modular nature of ROS 2 allows humanoid robot developers to focus on individual capabilities while maintaining a coherent overall system architecture.

## Summary

ROS 2 architecture provides a robust foundation for developing complex robotic systems through its core concepts of nodes, topics, and services. The publish-subscribe model enables flexible, decoupled communication between system components, while the service model provides synchronous request-response interactions when needed. This architectural approach has proven essential for the development of sophisticated robotic systems, particularly in the domain of humanoid robotics where multiple complex subsystems must work together seamlessly.

Understanding these architectural concepts is fundamental to working effectively with ROS 2 and forms the foundation for all subsequent concepts in this book. As we progress through the modules, we will see how these basic building blocks combine to create increasingly sophisticated robotic capabilities.