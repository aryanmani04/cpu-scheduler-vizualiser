"""
Utility functions for CPU Scheduling Simulator
Provides color generation, formatting, and calculation helpers
"""

import random
from typing import Any, List, Dict, Tuple

# Bold, high-contrast palette so Gantt bars pop visually
VIVID_PALETTE = [
    "#FF6B00", "#FF1D25", "#2962FF", "#00C853", "#FFD600",
    "#AA00FF", "#FF4081", "#00B8D4", "#FFAB00", "#C51162",
    "#00C3FF", "#76FF03", "#FF1744", "#00E676", "#FF9100",
    "#6200EA", "#00BFA5", "#FF6D00", "#D50000", "#64DD17"
]


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def _tint_color(hex_color: str, factor: float) -> str:
    """Blend the given color towards white by `factor` (0-1)."""
    factor = max(0.0, min(1.0, factor))
    r, g, b = _hex_to_rgb(hex_color)
    tinted = (
        int(r + (255 - r) * factor),
        int(g + (255 - g) * factor),
        int(b + (255 - b) * factor),
    )
    return _rgb_to_hex(tinted)


def generate_color() -> str:
    """
    Generate a vivid color for process visualization.
    """
    return random.choice(VIVID_PALETTE)


def generate_unique_colors(count: int) -> Dict[str, str]:
    """
    Generate unique colors for multiple processes.

    Args:
        count: Number of unique colors needed

    Returns:
        Dict mapping process IDs to color hex codes
    """
    colors = {}
    used_colors = set[Any]()

    for i in range(count):
        base = VIVID_PALETTE[i % len(VIVID_PALETTE)]
        color = base
        # Ensure uniqueness if palette repeats
        while color in used_colors:
            color = random.choice(VIVID_PALETTE)
        used_colors.add(color)
        colors[f"P{i+1}"] = color

    return colors


def calculate_averages(processes: List) -> Dict[str, float]:
    """
    Calculate average waiting time, turnaround time, and response time.

    Args:
        processes: List of Process objects

    Returns:
        Dictionary with average WT, TAT, and Response Time
    """
    if not processes:
        return {"avg_wt": 0.0, "avg_tat": 0.0, "avg_response": 0.0}

    total_wt = sum(p.waiting_time for p in processes)
    total_tat = sum(p.turnaround_time for p in processes)
    total_response = sum(p.response_time for p in processes)
    count = len(processes)

    return {
        "avg_wt": round(total_wt / count, 2),
        "avg_tat": round(total_tat / count, 2),
        "avg_response": round(total_response / count, 2)
    }


def format_time(time: float) -> str:
    """
    Format time value for display.

    Args:
        time: Time value to format

    Returns:
        Formatted time string
    """
    if time == int(time):
        return str(int(time))
    return f"{time:.1f}"


def validate_process_input(process_id: str, arrival_time: str,
                           burst_time: str, priority: str) -> Tuple[bool, str]:
    """
    Validate process input fields.

    Args:
        process_id: Process ID string
        arrival_time: Arrival time string
        burst_time: Burst time string
        priority: Priority string

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not process_id.strip():
        return False, "Process ID cannot be empty"

    try:
        at = float(arrival_time)
        if at < 0:
            return False, "Arrival time cannot be negative"
    except ValueError:
        return False, "Arrival time must be a valid number"

    try:
        bt = float(burst_time)
        if bt <= 0:
            return False, "Burst time must be greater than 0"
    except ValueError:
        return False, "Burst time must be a valid number"

    try:
        prio = int(priority)
        if prio < 0:
            return False, "Priority cannot be negative"
    except ValueError:
        return False, "Priority must be a valid integer"

    return True, ""


def get_idle_color() -> str:
    """
    Get the color for idle periods in Gantt chart.

    Returns:
        Hex color code for idle periods
    """
    return "#E0E0E0"  # Light gray for idle
