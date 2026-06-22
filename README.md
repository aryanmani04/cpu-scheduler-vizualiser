CPU Scheduling Algorithm Simulator

A desktop app that simulates CPU scheduling algorithms and shows how processes are executed using Gantt charts. You can add processes yourself and see how different algorithms behave on the same input.

--------Features-----
6 CPU scheduling algorithms:
FCFS
SJF (Non preemptive)
SRTF (Preemptive)
Priority Scheduling (both types)
Round Robin
Add your own processes (arrival time, burst time, priority)
Gantt chart visualization
Waiting time, turnaround time, response time for each process
Average values for comparison
Compare different algorithms on same data


Requirements
Python 3.7 or above
Tkinter (usually already installed)
No external libraries needed

Check Python:
python --version


How to run
Go into the project folder:
cd cpu-scheduler-visualizer
Then run:
python main_gui.py

On Windows, you can also just double click run.bat

How to use
Ad processes (ID, arrival time, burst time, priority)
Pick a scheduling algorithm
Click simulate
See results in:
Table
Gantt chart
comparison section (optional)
🔬 Algorithms
FCFS → runs in order they come
SJF → shortest job goes first
SRTF → like SJF but can interrupt
Priority → based on priority number
Round Robin → each process gets a time slice

About
Made for learning OS scheduling concepts and seeing how CPU scheduling actually works in practice.
