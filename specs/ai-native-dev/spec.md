Project: AI-Native Software Development — Physical AI & Humanoid Robotics Book (~7,000 words)

Goal:
Generate a full research paper / book covering all 4 modules, suitable for Docusaurus conversion and future RAG integration.

Target Audience:
Graduate-level CS / AI students

Constraints:
- Total word count: ~7,000 words
- APA citations for all claims
- Academic tone, Flesch-Kincaid grade 10–12
- Conceptual explanations only; no full code
- Use gathered ≥15 sources (≥50% peer-reviewed)

Instructions for Gemini:
- Treat all 4 modules as one cohesive book
- Revise Module 1 if needed for consistency
- Draft Modules 2–4 based on the following details
- Maintain logical flow across chapters
- Include APA-style citations and reference all claims
- Output in Markdown for Docusaurus

Chapter Outline & Word Distribution:

Module 1: The Robotic Nervous System (ROS 2) — 1,500–2,000 words
- ROS 2 middleware for humanoid control
- Nodes, topics, and services
- Bridging Python AI agents using rclpy
- URDF for humanoid modeling
- Conceptual control flow example
- Key sources: ROS 2 peer-reviewed papers, official documentation

Module 2: The Digital Twin (Gazebo & Unity) — ~1,000–1,200 words
- Physics simulation and environment building
- Simulating gravity, collisions in Gazebo
- High-fidelity human-robot interaction in Unity
- Sensor simulation: LiDAR, Depth Cameras, IMUs
- Key sources: Gazebo & Unity docs, peer-reviewed simulation papers

Module 3: The AI-Robot Brain (NVIDIA Isaac™) — ~1,500–1,800 words
- NVIDIA Isaac Sim: photorealistic simulation, synthetic data generation
- Isaac ROS: hardware-accelerated VSLAM and navigation
- Nav2: path planning for bipedal humanoids
- Integration with AI agents and control logic
- Key sources: NVIDIA Isaac docs, robotics AI papers

Module 4: Vision-Language-Action (VLA) — ~1,500–1,800 words
- Convergence of LLMs and robotics
- Voice-to-Action using OpenAI Whisper
- Cognitive planning: translating natural language to ROS 2 actions
- Conceptual Capstone: autonomous humanoid performs tasks using perception and planning
- Key sources: LLM robotics papers, OpenAI Whisper docs, peer-reviewed AI papers

Chapter Guidelines:
- Include headings and subheadings for each concept
- Maintain clarity and logical flow across modules
- Embed APA citations for every claim
- Conceptual diagrams and workflows can be described in text
- Ensure all content is traceable and reproducible

Output:
- Full draft of research paper / book in Markdown
- Ready for Docusaurus conversion
- Approximately 7,000 words total
- Citation-ready for APA formatting