"""
CPU Scheduling Algorithms Implementation
Contains all scheduling algorithms: FCFS, SJF, SRTF, Priority, Preemptive Priority, Round Robin
"""

from typing import List, Tuple
from copy import deepcopy


class Process:
    """
    Process class to represent a process in CPU scheduling.
    Contains all necessary attributes for scheduling calculations.
    """

    def __init__(self, process_id: str, arrival_time: float,
                 burst_time: float, priority: int):
        """
        Initialize a process.

        Args:
            process_id: Unique identifier for the process
            arrival_time: Time when process arrives
            burst_time: CPU burst time required
            priority: Priority of the process (lower number = higher priority)
        """
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        # Runtime attributes
        self.remaining_time = burst_time
        self.start_time = -1
        self.finish_time = -1
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1  # -1 means not started yet

    def __repr__(self):
        return f"Process({self.process_id}, AT={self.arrival_time}, BT={self.burst_time})"


def fcfs(processes: List[Process]) -> Tuple[List[Process], List[Tuple[str, float, float]]]:
    """
    First Come First Served (FCFS) Scheduling Algorithm.
    Non-preemptive: Processes are executed in order of arrival.

    Args:
        processes: List of Process objects

    Returns:
        Tuple of (updated_processes, gantt_chart)
    """
    # Create deep copy to avoid modifying original
    procs = deepcopy(processes)

    # Sort by arrival time
    procs.sort(key=lambda x: x.arrival_time)

    gantt_chart = []
    current_time = 0

    for proc in procs:
        # If process hasn't arrived yet, wait
        if current_time < proc.arrival_time:
            gantt_chart.append(("IDLE", current_time, proc.arrival_time))
            current_time = proc.arrival_time

        # Set start time and response time (first time process runs)
        if proc.start_time == -1:
            proc.start_time = current_time
            proc.response_time = proc.start_time - proc.arrival_time

        # Execute process
        proc.finish_time = current_time + proc.burst_time
        gantt_chart.append((proc.process_id, current_time, proc.finish_time))

        # Calculate metrics
        proc.turnaround_time = proc.finish_time - proc.arrival_time
        proc.waiting_time = proc.turnaround_time - proc.burst_time

        current_time = proc.finish_time

    return procs, gantt_chart


def sjf(processes: List[Process]) -> Tuple[List[Process], List[Tuple[str, float, float]]]:
    """
    Shortest Job First (SJF) Scheduling Algorithm - Non-Preemptive.
    Selects the process with shortest burst time among arrived processes.

    Args:
        processes: List of Process objects

    Returns:
        Tuple of (updated_processes, gantt_chart)
    """
    procs = deepcopy(processes)
    procs.sort(key=lambda x: x.arrival_time)

    gantt_chart = []
    current_time = 0
    completed = []
    remaining = procs.copy()

    while remaining:
        # Find processes that have arrived
        arrived = [p for p in remaining if p.arrival_time <= current_time]

        if not arrived:
            # No process arrived, wait for next arrival
            next_arrival = min(p.arrival_time for p in remaining)
            gantt_chart.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue

        # Select process with shortest burst time
        selected = min(arrived, key=lambda x: x.burst_time)

        # Set start time and response time
        if selected.start_time == -1:
            selected.start_time = current_time
            selected.response_time = selected.start_time - selected.arrival_time

        # Execute process completely
        selected.finish_time = current_time + selected.burst_time
        gantt_chart.append(
            (selected.process_id, current_time, selected.finish_time))

        # Calculate metrics
        selected.turnaround_time = selected.finish_time - selected.arrival_time
        selected.waiting_time = selected.turnaround_time - selected.burst_time

        current_time = selected.finish_time
        remaining.remove(selected)
        completed.append(selected)

    return completed, gantt_chart


def srtf(processes: List[Process]) -> Tuple[List[Process], List[Tuple[str, float, float]]]:
    """
    Shortest Remaining Time First (SRTF) Scheduling Algorithm - Preemptive.
    Preempts current process if a new process arrives with shorter remaining time.

    Args:
        processes: List of Process objects

    Returns:
        Tuple of (updated_processes, gantt_chart)
    """
    procs = deepcopy(processes)
    procs.sort(key=lambda x: x.arrival_time)

    gantt_chart = []
    current_time = 0
    remaining = procs.copy()
    current_process = None
    process_start_time = None

    while remaining or current_process:
        # Check for new arrivals
        arrivals = [p for p in remaining if p.arrival_time <= current_time]

        # Select process with shortest remaining time
        candidates = [current_process] if current_process else []
        candidates.extend(arrivals)
        candidates = [c for c in candidates if c and c.remaining_time > 0]

        if not candidates:
            # No process available, wait for next arrival
            if remaining:
                next_arrival = min(p.arrival_time for p in remaining)
                if current_process:
                    # Finish current process segment
                    if process_start_time < current_time:
                        gantt_chart.append((current_process.process_id,
                                            process_start_time, current_time))
                gantt_chart.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
                current_process = None
                process_start_time = None
            else:
                break
            continue

        # Select process with shortest remaining time
        next_process = min(candidates, key=lambda x: x.remaining_time)

        # If switching processes, save previous segment
        if current_process and current_process != next_process:
            if process_start_time < current_time:
                gantt_chart.append((current_process.process_id,
                                    process_start_time, current_time))

        # Start new process if needed
        if current_process != next_process:
            if next_process.start_time == -1:
                next_process.start_time = current_time
                next_process.response_time = next_process.start_time - next_process.arrival_time
            process_start_time = current_time
            current_process = next_process

        # Execute for 1 time unit (or until next event)
        if remaining:
            next_event_time = min([p.arrival_time for p in remaining
                                  if p.arrival_time > current_time],
                                  default=current_time + current_process.remaining_time)
        else:
            next_event_time = current_time + current_process.remaining_time

        execution_time = min(1.0, current_process.remaining_time,
                             next_event_time - current_time)
        current_time += execution_time
        current_process.remaining_time -= execution_time

        # Check if process completed
        if current_process.remaining_time <= 0:
            current_process.finish_time = current_time
            current_process.turnaround_time = current_process.finish_time - \
                current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - \
                current_process.burst_time

            if process_start_time < current_time:
                gantt_chart.append((current_process.process_id,
                                    process_start_time, current_time))

            remaining.remove(current_process)
            current_process = None
            process_start_time = None

    return procs, gantt_chart


def priority_scheduling(processes: List[Process]) -> Tuple[List[Process], List[Tuple[str, float, float]]]:
    """
    Priority Scheduling Algorithm - Non-Preemptive.
    Selects process with highest priority (lowest priority number) among arrived processes.

    Args:
        processes: List of Process objects

    Returns:
        Tuple of (updated_processes, gantt_chart)
    """
    procs = deepcopy(processes)
    procs.sort(key=lambda x: x.arrival_time)

    gantt_chart = []
    current_time = 0
    completed = []
    remaining = procs.copy()

    while remaining:
        # Find processes that have arrived
        arrived = [p for p in remaining if p.arrival_time <= current_time]

        if not arrived:
            # Wait for next arrival
            next_arrival = min(p.arrival_time for p in remaining)
            gantt_chart.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue

        # Select process with highest priority (lowest priority number)
        selected = min(arrived, key=lambda x: x.priority)

        # Set start time and response time
        if selected.start_time == -1:
            selected.start_time = current_time
            selected.response_time = selected.start_time - selected.arrival_time

        # Execute process completely
        selected.finish_time = current_time + selected.burst_time
        gantt_chart.append(
            (selected.process_id, current_time, selected.finish_time))

        # Calculate metrics
        selected.turnaround_time = selected.finish_time - selected.arrival_time
        selected.waiting_time = selected.turnaround_time - selected.burst_time

        current_time = selected.finish_time
        remaining.remove(selected)
        completed.append(selected)

    return completed, gantt_chart


def preemptive_priority(processes: List[Process]) -> Tuple[List[Process], List[Tuple[str, float, float]]]:
    """
    Preemptive Priority Scheduling Algorithm.
    Preempts current process if a new process arrives with higher priority.

    Args:
        processes: List of Process objects

    Returns:
        Tuple of (updated_processes, gantt_chart)
    """
    procs = deepcopy(processes)
    procs.sort(key=lambda x: x.arrival_time)

    # Initialize remaining_time
    for p in procs:
        p.remaining_time = p.burst_time

    gantt_chart = []
    current_time = 0
    remaining = procs.copy()
    current_process = None
    process_start_time = None

    while remaining or current_process:
        # Check for new arrivals
        arrivals = [p for p in remaining if p.arrival_time <= current_time]

        # Select process with highest priority (lowest priority number)
        candidates = [current_process] if current_process else []
        candidates.extend(arrivals)
        candidates = [c for c in candidates if c and c.remaining_time > 0]

        if not candidates:
            if remaining:
                next_arrival = min(p.arrival_time for p in remaining)
                if current_process:
                    if process_start_time < current_time:
                        gantt_chart.append((current_process.process_id,
                                            process_start_time, current_time))
                gantt_chart.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
                current_process = None
                process_start_time = None
            else:
                break
            continue

        # Select process with highest priority
        next_process = min(candidates, key=lambda x: x.priority)

        # If switching processes, save previous segment
        if current_process and current_process != next_process:
            if process_start_time < current_time:
                gantt_chart.append((current_process.process_id,
                                    process_start_time, current_time))

        # Start new process if needed
        if current_process != next_process:
            if next_process.start_time == -1:
                next_process.start_time = current_time
                next_process.response_time = next_process.start_time - next_process.arrival_time
            process_start_time = current_time
            current_process = next_process

        # Execute for 1 time unit (or until next event)
        if remaining:
            next_event_time = min([p.arrival_time for p in remaining
                                  if p.arrival_time > current_time],
                                  default=current_time + current_process.remaining_time)
        else:
            next_event_time = current_time + current_process.remaining_time

        execution_time = min(1.0, current_process.remaining_time,
                             next_event_time - current_time)
        current_time += execution_time
        current_process.remaining_time -= execution_time

        # Check if process completed
        if current_process.remaining_time <= 0:
            current_process.finish_time = current_time
            current_process.turnaround_time = current_process.finish_time - \
                current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - \
                current_process.burst_time

            if process_start_time < current_time:
                gantt_chart.append((current_process.process_id,
                                    process_start_time, current_time))

            remaining.remove(current_process)
            current_process = None
            process_start_time = None

    return procs, gantt_chart


def round_robin(processes: List[Process], time_quantum: float) -> Tuple[List[Process], List[Tuple[str, float, float]]]:
    """
    Round Robin (RR) Scheduling Algorithm.
    Each process receives up to `time_quantum` time units before being preempted.
    """
    procs = deepcopy(processes)
    procs.sort(key=lambda x: x.arrival_time)

    for proc in procs:
        proc.remaining_time = proc.burst_time

    gantt_chart: List[Tuple[str, float, float]] = []
    current_time = 0.0
    ready_queue: List[Process] = []
    pending = procs.copy()  # arrival-ordered list we can pull from

    while pending or ready_queue:
        # Move newly arrived processes into the ready queue
        while pending and pending[0].arrival_time <= current_time:
            ready_queue.append(pending.pop(0))

        if not ready_queue:
            # CPU idle until next arrival
            if pending:
                next_arrival = pending[0].arrival_time
                if current_time < next_arrival:
                    gantt_chart.append(("IDLE", current_time, next_arrival))
                    current_time = next_arrival
                continue
            else:
                break

        current_process = ready_queue.pop(0)
        if current_process.start_time == -1:
            current_process.start_time = current_time
            current_process.response_time = current_process.start_time - current_process.arrival_time

        slice_time = min(time_quantum, current_process.remaining_time)
        slice_start = current_time
        current_time += slice_time
        current_process.remaining_time -= slice_time
        gantt_chart.append((current_process.process_id, slice_start, current_time))

        # Enqueue any processes that arrived during this time slice
        while pending and pending[0].arrival_time <= current_time:
            ready_queue.append(pending.pop(0))

        if current_process.remaining_time > 0:
            ready_queue.append(current_process)
        else:
            current_process.finish_time = current_time
            current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

    return procs, gantt_chart
