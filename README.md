<div align="center">

# 🔬 OpenCV & Computer Vision Engineering Journey

### *From Pixels to Perception: Building Robust Vision Systems for Robotics*

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Latest-green.svg)
![Status](https://img.shields.io/badge/Status-Active%20Learning-orange.svg)

</div>

---

## 📖 About This Repository

This repository documents my journey from basic image processing to building **robust Computer Vision pipelines for Robotics**. Unlike typical tutorials that focus on running pre-trained models, this project dives deep into the **mathematical foundations** (Linear Algebra, Geometry) that power computer vision algorithms.

> **Current Focus:** Perception Systems, Contour Analysis, and Real-time Object Tracking

---

## 🛠️ Tech Stack & Engineering Decisions

<table>
<tr>
<td><b>Language</b></td>
<td>Python 3.12 (Strictly enforced)</td>
</tr>
<tr>
<td><b>Core Libraries</b></td>
<td>OpenCV (<code>cv2</code>), NumPy</td>
</tr>
<tr>
<td><b>Package Manager</b></td>
<td><code>uv</code> (Blazing fast environment management)</td>
</tr>
</table>

### ⚠️ Why Python 3.12? The Engineering Reality

I deliberately avoid Python 3.13/3.14 (bleeding edge releases). Here's why:

| Reason | Impact |
|--------|--------|
| **Binary Wheel Compatibility** | Libraries like `opencv-python` and `numpy` rely on pre-compiled C++ binary wheels. These are often unavailable for experimental Python versions, forcing unstable source compilations. |
| **Robotics Ecosystem** | ROS 2 (Robot Operating System) and industry-standard pipelines are optimized for Python 3.10–3.12. Using 3.14 breaks critical dependency graphs. |

---

## 📂 Repository Structure

```
Opencv-Learning/
│
├── 📁 Chapters/              # Source code for lessons and projects
│   ├── chapter1.py           # Basic I/O operations
│   ├── chapter2.py           # Image transformations
│   ├── ...
│   └── project1.py           # Virtual Paint / Document Scanner
│
├── 📁 Data/                  # Raw input data
│   ├── lena.jpg              # Test images
│   └── shapes.png            # Geometric shape samples
│
├── 📁 related output/        # Generated artifacts
│   └── learnings/            # Processed videos, debug images, results
│
└── 📁 .venv/                 # Virtual environment (managed by uv)
```

---

## 🚀 Quick Start Guide

This project uses **[uv](https://github.com/astral-sh/uv)** for dependency management—significantly faster than pip with automatic virtual environment handling.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Halfgods/Opencv-Learning.git
cd Opencv-Learning
```

### Step 2: Create Virtual Environment

*Enforcing Python 3.12 for OpenCV binary wheel compatibility*

```bash
# Create virtual environment with Python 3.12
uv venv --python 3.12

# Activate the environment
# 🪟 Windows:
.venv\Scripts\activate

# 🐧 Linux / 🍎 Mac:
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
uv add opencv-python opencv-contrib-python numpy
```

---

## 🧠 Key Learnings & Technical Deep Dives

### 📐 1. The Mathematics of Vision

<details>
<summary><b>Coordinate Systems</b></summary>

Understanding the critical difference between:
- **NumPy Matrix notation:** `(Height, Width)` — follows mathematical matrix convention
- **OpenCV Cartesian notation:** `(Width, Height)` — follows image coordinate systems

This distinction is crucial for avoiding dimension mismatches in transformations.
</details>

<details>
<summary><b>HSV vs. RGB Color Spaces</b></summary>

- **RGB:** Hardware display standard, but lighting-dependent
- **HSV:** Separates Color from Illumination — essential for robust robotic perception under varying lighting conditions

</details>

### ⚙️ 2. Core Algorithms Implemented

| Algorithm | Application | Key Insight |
|-----------|-------------|-------------|
| **Canny Edge Detection** | Object boundary detection | Tuned thresholds for specific lighting conditions |
| **Homography Transform** | Document scanner, AR | Mathematical plane-to-plane transformation |
| **Contour Detection** | Shape recognition | `RETR_EXTERNAL` vs `RETR_TREE` for hierarchy control |
| **Polygon Approximation** | Shape classification | Using `cv2.approxPolyDP` to classify by vertex count |

---

## 🎯 The Engineering Manifesto

### *Why This Repository Exists*

Most students treat Computer Vision as running a pre-trained YOLO model and calling it done. **I'm going deeper** because my goal is **Robotics & Autonomous Systems**.

### 🔓 1. Escaping "Tutorial Hell"

Copying code is trivial. Understanding **why** a 3×3 kernel outperforms 5×5 for specific noise reduction requires engineering intuition. This repository is my laboratory for those experiments.


This is my proving ground to **break things, fix them**, and document what actually works in production-grade systems.

---

<div align="center">

### 👨‍💻 About Me

**Justin**  
*Engineering Student @ Fr. CRCE*

[![GitHub](https://img.shields.io/badge/GitHub-Halfgods-181717?logo=github)](https://github.com/Halfgods)

---

*"In robotics, vision isn't just seeing—it's understanding geometry in real-time."*

</div>
