# CPU Scheduling Algorithm Simulator

A desktop app that simulates and visualizes 6 classic CPU scheduling algorithms with live Gantt charts, per-process metrics, and side-by-side algorithm comparison.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Usage Guide](#usage-guide)
- [Algorithms Explained](#algorithms-explained)
- [Sample Input & Output](#sample-input--output)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)

## ✨ Features

### Core Features

- **6 Scheduling Algorithms**:

  - FCFS (First Come First Served)
  - SJF (Shortest Job First - Non-Preemptive)
  - SRTF (Shortest Remaining Time First - Preemptive)
  - Priority Scheduling (Non-Preemptive)
  - Preemptive Priority Scheduling
  - Round Robin (with configurable time quantum)

- **Comprehensive Metrics**:

  - Waiting Time for each process
  - Turnaround Time for each process
  - Response Time for each process
  - Average Waiting Time
  - Average Turnaround Time
  - Average Response Time

- **Visual Features**:

  - Color-coded Gantt Chart visualization
  - Interactive results table
  - Summary statistics display
  - Algorithm comparison mode

- **User-Friendly Interface**:
  - Modern and clean GUI design
  - Easy process input
  - Real-time validation
  - Error handling with helpful messages
  - Reset functionality
  - Dark aurora-inspired theme with soft animations and hover transitions

### Additional Features

- **Algorithm Comparison Mode**: Compare all algorithms side-by-side with the same input
- **Input Validation**: Prevents invalid inputs (negative values, empty fields, duplicate IDs)
- **Process Management**: Add, view, and clear processes easily
- **Export-Ready Results**: Well-formatted tables for documentation

## 📦 Requirements

- **Python 3.7 or higher**
- **Tkinter** (usually included with Python)
- **No external dependencies** - uses only Python standard library

### Checking Python Installation

```bash
python --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

## 🚀 Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**

   ```bash
   cd cpu-scheduler-visualizer
   ```

3. **Verify files are present**
   - `main_gui.py`
   - `scheduler_logic.py`
   - `utils.py`
   - `run.bat`
   - `README.md`

## ▶️ How to Run

### Windows

```bash
python main_gui.py
```

Or double-click `run.bat` to launch the simulator.

### Linux/Mac

```bash
python3 main_gui.py
```

## 📖 Usage Guide

### Step 1: Add Processes

1. Enter **Process ID** (e.g., P1, P2, Process1)
2. Enter **Arrival Time** (when the process arrives, e.g., 0, 2, 5)
3. Enter **Burst Time** (CPU time required, e.g., 5, 3, 8)
4. Enter **Priority** (lower number = higher priority, e.g., 1, 2, 3)
5. Click **"➕ Add Process"** button
6. Repeat for all processes

### Step 2: Select Algorithm

Choose one of the available algorithms using radio buttons:

- **FCFS**: First Come First Served
- **SJF**: Shortest Job First (Non-Preemptive)
- **SRTF**: Shortest Remaining Time First (Preemptive)
- **Priority**: Priority Scheduling (Non-Preemptive)
- **Preemptive Priority**: Preemptive Priority Scheduling
- **Round Robin**: Round Robin (Time Quantum input will appear)

**Note**: For Round Robin, enter the **Time Quantum** value when prompted.

### Step 3: Run Simulation

Click the **"▶️ Simulate"** button to run the selected algorithm.

### Step 4: View Results

Results are displayed in three tabs:

1. **📋 Results Tab**:

   - Detailed table showing metrics for each process
   - Summary statistics (averages)

2. **📊 Gantt Chart Tab**:

   - Visual timeline of process execution
   - Color-coded process bars
   - Time markers

3. **⚖️ Comparison Tab**:
   - Use "Compare All Algorithms" button to see side-by-side comparison
   - Shows average metrics for all algorithms

### Additional Actions

- **🗑️ Clear List**: Remove all processes from the list
- **🔄 Reset Project**: Clear everything (processes, results, charts)
- **📊 Compare All Algorithms**: Run all algorithms with current processes and compare results

## 🔬 Algorithms Explained

### 1. FCFS (First Come First Served)

**Type**: Non-Preemptive

**How it works**:

- Processes are executed in the order they arrive
- The first process to arrive gets the CPU first
- Once a process starts, it runs until completion

**Advantages**: Simple, fair, no starvation

**Disadvantages**: May have high waiting time for short processes if long processes arrive first

**Best for**: Batch systems, simple scenarios

---

### 2. SJF (Shortest Job First) - Non-Preemptive

**Type**: Non-Preemptive

**How it works**:

- Among all arrived processes, the one with shortest burst time is selected
- Once selected, it runs to completion
- If no process has arrived, CPU remains idle

**Advantages**: Minimizes average waiting time, optimal for non-preemptive scheduling

**Disadvantages**: May cause starvation for long processes, requires knowledge of burst times

**Best for**: Batch systems where burst times are known

---

### 3. SRTF (Shortest Remaining Time First)

**Type**: Preemptive

**How it works**:

- Similar to SJF but preemptive
- When a new process arrives, if it has shorter remaining time than current process, it preempts
- Process with shortest remaining time always runs

**Advantages**: Optimal for minimizing average waiting time (preemptive version)

**Disadvantages**: Complex implementation, may cause starvation, context switching overhead

**Best for**: Interactive systems where response time matters

---

### 4. Priority Scheduling - Non-Preemptive

**Type**: Non-Preemptive

**How it works**:

- Each process has a priority (lower number = higher priority)
- Among arrived processes, highest priority process is selected
- Runs to completion once selected

**Advantages**: Important processes can be prioritized

**Disadvantages**: May cause starvation for low-priority processes

**Best for**: Systems where priority matters (real-time systems)

---

### 5. Preemptive Priority Scheduling

**Type**: Preemptive

**How it works**:

- Similar to Priority but preemptive
- When a higher priority process arrives, it preempts the current process
- Highest priority process always runs

**Advantages**: Responsive to high-priority processes

**Disadvantages**: Starvation for low-priority processes, context switching overhead

**Best for**: Real-time systems, operating systems

---

### 6. Round Robin

**Type**: Preemptive

**How it works**:

- Each process gets a fixed time quantum to execute
- Processes are arranged in a circular queue
- If process doesn't complete in quantum, it's moved to end of queue
- Next process in queue gets CPU

**Advantages**: Fair, no starvation, good for time-sharing systems

**Disadvantages**: Performance depends on time quantum size

**Best for**: Time-sharing systems, interactive systems

**Time Quantum**: Configurable value (typically 2-10 time units)

## 📊 Sample Input & Output

### Sample Input

Let's simulate with the following processes:

| Process ID | Arrival Time | Burst Time | Priority |
| ---------- | ------------ | ---------- | -------- |
| P1         | 0            | 5          | 3        |
| P2         | 1            | 3          | 1        |
| P3         | 2            | 8          | 2        |
| P4         | 3            | 6          | 4        |

### Expected Outputs

#### FCFS Algorithm

**Gantt Chart**: P1(0-5) → P2(5-8) → P3(8-16) → P4(16-22)

**Results**:

- P1: WT=0, TAT=5, RT=0
- P2: WT=4, TAT=7, RT=4
- P3: WT=6, TAT=14, RT=6
- P4: WT=13, TAT=19, RT=13

**Averages**:

- Avg WT: 5.75
- Avg TAT: 11.25
- Avg RT: 5.75

#### SJF Algorithm

**Gantt Chart**: P1(0-5) → P2(5-8) → P4(8-14) → P3(14-22)

**Results**:

- P1: WT=0, TAT=5, RT=0
- P2: WT=4, TAT=7, RT=4
- P3: WT=6, TAT=14, RT=6
- P4: WT=5, TAT=11, RT=5

**Averages**:

- Avg WT: 3.75
- Avg TAT: 9.25
- Avg RT: 3.75

#### Round Robin (Time Quantum = 2)

**Gantt Chart**: P1(0-2) → P2(2-4) → P3(4-6) → P4(6-8) → P1(8-10) → P2(10-11) → P3(11-13) → P4(13-15) → P3(15-17) → P4(17-19) → P3(19-21) → P4(21-22)

**Note**: Actual output may vary slightly based on implementation details.

## 📁 Project Structure

```
cpu-scheduler-visualizer/
│
├── main_gui.py          # Main GUI application (Tkinter)
├── scheduler_logic.py   # All scheduling algorithms implementation
├── utils.py             # Utility functions (colors, validation, calculations)
├── run.bat              # One-click launcher for Windows
└── README.md            # This file
```

### File Descriptions

- **main_gui.py**:

  - Contains `CPUSchedulerGUI` class
  - Handles all user interface components
  - Manages user interactions and displays results

- **scheduler_logic.py**:

  - Contains `Process` class
  - Implements all 6 scheduling algorithms
  - Returns updated processes and Gantt chart data

- **utils.py**:
  - Color generation for Gantt chart
  - Input validation functions
  - Average calculation helpers
  - Formatting utilities

## 📸 Screenshots

_Note: Screenshots would be added here showing:_

- Main application window
- Process input interface
- Results table display
- Gantt chart visualization
- Algorithm comparison view

## 🐛 Troubleshooting

### Common Issues

1. **"Tkinter not found" error**:

   - Install tkinter: `sudo apt-get install python3-tk` (Linux)
   - On Windows/Mac, tkinter should be included with Python

2. **Application window too small**:

   - Resize the window manually
   - Minimum recommended size: 1000x660

3. **Gantt chart not displaying**:

   - Ensure at least one process is added
   - Run a simulation first
   - Check the "Gantt Chart" tab

4. **Invalid input errors**:
   - Ensure all fields are filled
   - Use positive numbers only
   - Burst time must be > 0
   - Process IDs must be unique

## 🎓 Educational Use

This simulator is perfect for:

- Operating Systems courses
- Understanding CPU scheduling concepts
- Comparing algorithm performance
- Visualizing process execution
- Learning preemptive vs non-preemptive scheduling

## 📝 Notes

- **Priority Convention**: Lower number = Higher priority (e.g., Priority 1 > Priority 5)
- **Time Units**: All times are in arbitrary time units (can represent milliseconds, seconds, etc.)
- **Idle Time**: Shown in gray in Gantt chart when CPU is idle
- **Preemptive Algorithms**: May have multiple segments for same process in Gantt chart

## 🤝 Contributing

Feel free to:

- Report bugs
- Suggest improvements
- Add new features
- Enhance the UI

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Built with ❤️ for students and developers learning CPU scheduling algorithms.

---

**Happy Scheduling! 🚀**
