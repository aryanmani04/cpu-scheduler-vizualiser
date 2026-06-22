"""
CPU Scheduling Algorithm Simulator - Main GUI
Beautiful desktop application for simulating CPU scheduling algorithms
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
try:
    # Prefer package-relative imports when available
    from . import scheduler_logic as scheduler
    from . import utils
except ImportError:
    # Fallback for running the module as a standalone script
    import scheduler_logic as scheduler
    import utils


class CPUSchedulerGUI:
    """
    Main GUI class for CPU Scheduling Simulator.
    Handles all user interactions and displays results.
    """

    def __init__(self, root, embedded: bool = False):
        """
        Initialize the GUI application.

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.embedded = embedded
        if not self.embedded:
            self.root.title("CPU Scheduling Algorithm Simulator")
            self.root.geometry("1200x720")
            self.root.minsize(1000, 660)
        self.root.configure(bg="#050816")

        # Application data
        self.processes: List[scheduler.Process] = []
        self.process_colors: Dict[str, str] = {}

        # Color scheme
        self.colors = {
            "bg": "#050816",
            "primary": "#0F172A",
            "secondary": "#38BDF8",
            "accent": "#F472B6",
            "success": "#0c8a60",
            "warning": "#F59E0B",
            "danger": "#de3131",
            "light": "#111C2D",
            "card": "#0B1220",
            "muted": "#94A3B8",
            "text": "#E2E8F0",
            "border": "#1E293B"
        }

        # Background canvas for aurora gradient
        self.bg_canvas = tk.Canvas(
            self.root,
            highlightthickness=0,
            bd=0,
            bg=self.colors["bg"]
        )
        self.bg_canvas.place(relwidth=1, relheight=1)
        self.draw_background_gradient()
        self.root.bind(
            "<Configure>", lambda event: self.draw_background_gradient())

        self.setup_ui()
        self.setup_styles()

    def setup_styles(self):
        """Configure custom styles for widgets."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook",
                        background=self.colors["primary"],
                        foreground=self.colors["text"],
                        borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=self.colors["light"],
                        foreground=self.colors["muted"],
                        padding=(18, 8),
                        font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", self.colors["secondary"])],
                  foreground=[("selected", self.colors["bg"])])

        style.configure("Treeview",
                        background=self.colors["card"],
                        fieldbackground=self.colors["card"],
                        foreground=self.colors["text"],
                        rowheight=28,
                        borderwidth=0,
                        relief="flat")
        style.map("Treeview",
                  background=[("selected", "#1E293B")],
                  foreground=[("selected", self.colors["text"])])
        style.configure("Treeview.Heading",
                        background=self.colors["primary"],
                        foreground=self.colors["text"],
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0)
        style.map("Treeview.Heading",
                  background=[("active", self.colors["secondary"]),
                              ("pressed", self.colors["secondary"])],
                  foreground=[("active", self.colors["bg"]),
                              ("pressed", self.colors["bg"])])

    def setup_ui(self):
        """Set up the main UI components."""
        # Title frame
        title_frame = tk.Frame(
            self.root, bg=self.colors["card"], height=90, bd=0)
        title_frame.pack(fill=tk.X, padx=0, pady=(0, 10))
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="CPU Scheduling Algorithm Simulator",
            font=("Poppins", 24, "bold"),
            bg=self.colors["card"],
            fg=self.colors["secondary"]
        )
        title_label.pack(pady=(18, 0))

        subtitle = tk.Label(
            title_frame,
            text="Visualize, compare, and understand CPU scheduling strategies.",
            font=("Segoe UI", 11),
            bg=self.colors["card"],
            fg=self.colors["muted"]
        )
        subtitle.pack()
        self.animate_title_glow(title_label)

        # Main container
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Left panel - Input section with scrollbar
        left_panel = tk.Frame(main_container, bg=self.colors["light"],
                              relief=tk.RAISED, bd=2, width=360)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=0)
        left_panel.pack_propagate(False)

        left_canvas = tk.Canvas(
            left_panel,
            bg=self.colors["light"],
            highlightthickness=0,
            borderwidth=0
        )
        left_scrollbar = ttk.Scrollbar(
            left_panel,
            orient=tk.VERTICAL,
            command=left_canvas.yview
        )
        self.left_scrollable_frame = tk.Frame(
            left_canvas,
            bg=self.colors["light"]
        )
        self.left_scrollable_frame.bind(
            "<Configure>",
            lambda e: left_canvas.configure(
                scrollregion=left_canvas.bbox("all")
            )
        )
        left_canvas.create_window(
            (0, 0),
            window=self.left_scrollable_frame,
            anchor="nw"
        )
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Keyboard scrolling for users without mouse wheel
        left_canvas.bind_all(
            "<MouseWheel>",
            lambda event: left_canvas.yview_scroll(
                int(-1*(event.delta/120)), "units"
            )
        )
        left_canvas.bind_all(
            "<Shift-MouseWheel>",
            lambda event: left_canvas.xview_scroll(
                int(-1*(event.delta/120)), "units"
            )
        )

        # Right panel - Output section
        right_panel = tk.Frame(main_container, bg=self.colors["bg"])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_input_section(self.left_scrollable_frame)
        self.setup_output_section(right_panel)

    def setup_input_section(self, parent):
        """Set up the input section with process entry and algorithm selection."""
        # Input section title
        input_title = tk.Label(
            parent,
            text="Process Input",
            font=("Poppins", 16, "bold"),
            bg=self.colors["light"],
            fg=self.colors["text"]
        )
        input_title.pack(pady=(20, 10))

        # Input fields frame
        input_frame = tk.Frame(parent, bg=self.colors["light"])
        input_frame.pack(padx=20, pady=10, fill=tk.X)

        # Process ID
        tk.Label(input_frame, text="Process ID:", font=("Segoe UI", 10, "bold"),
                 bg=self.colors["light"], fg=self.colors["muted"]).grid(
            row=0, column=0, sticky=tk.W, pady=8)
        self.pid_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 10),
            width=20,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            relief=tk.FLAT
        )
        self.pid_entry.grid(row=0, column=1, pady=8, padx=(10, 0))
        self.style_entry(self.pid_entry)

        # Arrival Time
        tk.Label(input_frame, text="Arrival Time:", font=("Segoe UI", 10, "bold"),
                 bg=self.colors["light"], fg=self.colors["muted"]).grid(
            row=1, column=0, sticky=tk.W, pady=8)
        self.arrival_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 10),
            width=20,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            relief=tk.FLAT
        )
        self.arrival_entry.grid(row=1, column=1, pady=8, padx=(10, 0))
        self.style_entry(self.arrival_entry)

        # Burst Time
        tk.Label(input_frame, text="Burst Time:", font=("Segoe UI", 10, "bold"),
                 bg=self.colors["light"], fg=self.colors["muted"]).grid(
            row=2, column=0, sticky=tk.W, pady=8)
        self.burst_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 10),
            width=20,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            relief=tk.FLAT
        )
        self.burst_entry.grid(row=2, column=1, pady=8, padx=(10, 0))
        self.style_entry(self.burst_entry)

        # Priority
        tk.Label(input_frame, text="Priority:", font=("Segoe UI", 10, "bold"),
                 bg=self.colors["light"], fg=self.colors["muted"]).grid(
            row=3, column=0, sticky=tk.W, pady=8)
        self.priority_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 10),
            width=20,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            relief=tk.FLAT
        )
        self.priority_entry.grid(row=3, column=1, pady=8, padx=(10, 0))
        self.style_entry(self.priority_entry)

        # Buttons frame
        button_frame = tk.Frame(parent, bg=self.colors["light"])
        button_frame.pack(padx=20, pady=15, fill=tk.X)

        add_btn = tk.Button(
            button_frame,
            text="➕ Add Process",
            command=self.add_process,
            bg=self.colors["success"],
            fg=self.colors["bg"],
            activebackground=self.colors["success"],
            activeforeground=self.colors["bg"],
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        add_btn.pack(fill=tk.X, pady=5)
        self.apply_hover_effect(add_btn, self.colors["success"], "#2fc267")

        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear List",
            command=self.clear_process_list,
            bg=self.colors["danger"],
            fg=self.colors["bg"],
            activebackground=self.colors["danger"],
            activeforeground=self.colors["bg"],
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        clear_btn.pack(fill=tk.X, pady=5)
        self.apply_hover_effect(clear_btn, self.colors["danger"], "#fa4646")

        # Process list
        list_title = tk.Label(
            parent,
            text="Process List",
            font=("Poppins", 14, "bold"),
            bg=self.colors["light"],
            fg=self.colors["text"]
        )
        list_title.pack(pady=(20, 10))

        # Listbox with scrollbar
        list_frame = tk.Frame(parent, bg=self.colors["light"])
        list_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.process_listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 10),
            bg=self.colors["card"],
            fg=self.colors["text"],
            selectbackground=self.colors["secondary"],
            selectforeground=self.colors["bg"],
            highlightthickness=0,
            borderwidth=0,
            yscrollcommand=scrollbar.set,
            height=8
        )
        self.process_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.process_listbox.yview)

        # Algorithm selection
        algo_title = tk.Label(
            parent,
            text="Algorithm Selection",
            font=("Poppins", 14, "bold"),
            bg=self.colors["light"],
            fg=self.colors["text"]
        )
        algo_title.pack(pady=(20, 10))

        algo_frame = tk.Frame(parent, bg=self.colors["light"])
        algo_frame.pack(padx=20, pady=10, fill=tk.X)

        self.algorithm_var = tk.StringVar(value="FCFS")
        self.algorithm_radios = []
        algorithms = [
            ("FCFS", "FCFS"),
            ("SJF (Non-Preemptive)", "SJF"),
            ("SRTF (Preemptive)", "SRTF"),
            ("Priority (Non-Preemptive)", "Priority"),
            ("Preemptive Priority", "PreemptivePriority"),
            ("Round Robin", "RoundRobin")
        ]

        for text, value in algorithms:
            rb = tk.Radiobutton(
                algo_frame,
                text=text,
                variable=self.algorithm_var,
                value=value,
                font=("Segoe UI", 10),
                bg=self.colors["light"],
                fg=self.colors["muted"],
                selectcolor=self.colors["secondary"],
                activebackground=self.colors["secondary"],
                activeforeground=self.colors["bg"],
                indicatoron=False,
                width=26,
                pady=6,
                bd=0,
                relief=tk.FLAT,
                cursor="hand2",
            )
            rb.pack(anchor=tk.CENTER, pady=4, fill=tk.X)
            self.algorithm_radios.append(rb)
        self.update_radio_styles()

        # Time Quantum input (only for Round Robin)
        self.quantum_frame = tk.Frame(parent, bg=self.colors["light"])
        self.quantum_frame.pack(padx=20, pady=10, fill=tk.X)
        self.quantum_frame.pack_forget()  # Hidden by default

        tk.Label(self.quantum_frame, text="Time Quantum:", font=("Segoe UI", 10, "bold"),
                 bg=self.colors["light"], fg=self.colors["muted"]).pack(side=tk.LEFT)
        self.quantum_entry = tk.Entry(
            self.quantum_frame,
            font=("Segoe UI", 10),
            width=10,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            relief=tk.FLAT
        )
        self.quantum_entry.pack(side=tk.LEFT, padx=(10, 0))
        self.quantum_entry.insert(0, "2")
        self.style_entry(self.quantum_entry)

        # Show/hide quantum input based on algorithm
        self.algorithm_var.trace("w", self.handle_algorithm_change)

        # Simulation buttons
        sim_frame = tk.Frame(parent, bg=self.colors["light"])
        sim_frame.pack(padx=20, pady=15, fill=tk.X)

        simulate_btn = tk.Button(
            sim_frame,
            text="Simulate",
            command=self.simulate,
            bg=self.colors["secondary"],
            fg=self.colors["bg"],
            activebackground=self.colors["secondary"],
            activeforeground=self.colors["bg"],
            font=("Poppins", 13, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2"
        )
        simulate_btn.pack(fill=tk.X, pady=5)
        self.apply_hover_effect(
            simulate_btn, self.colors["secondary"], "#67E8F9")

        compare_btn = tk.Button(
            sim_frame,
            text="Compare All Algorithms",
            command=self.compare_algorithms,
            bg="#9B59B6",
            fg="black",
            activebackground="#A855F7",
            activeforeground=self.colors["text"],
            font=("Poppins", 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        compare_btn.pack(fill=tk.X, pady=5)
        self.apply_hover_effect(compare_btn, "#9B59B6", "#A855F7")

        reset_btn = tk.Button(
            sim_frame,
            text="Reset Project",
            command=self.reset_project,
            bg="#E67E22",
            fg=self.colors["bg"],
            activebackground="#F97316",
            activeforeground=self.colors["bg"],
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        reset_btn.pack(fill=tk.X, pady=5)
        self.apply_hover_effect(reset_btn, "#E67E22", "#F97316")

    def setup_output_section(self, parent):
        """Set up the output section with results, Gantt chart, and comparison tabs."""
        # Create notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Results tab
        results_frame = tk.Frame(notebook, bg=self.colors["primary"])
        notebook.add(results_frame, text="Results")

        # Results table
        table_frame = tk.Frame(results_frame, bg=self.colors["primary"])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview for results table
        columns = ("PID", "Arrival", "Burst", "Priority",
                   "Completion", "Waiting", "Turnaround", "Response")
        self.results_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100, anchor=tk.CENTER)

        scrollbar_table = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar_table.set)

        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_table.pack(side=tk.RIGHT, fill=tk.Y)

        summary_frame = tk.Frame(results_frame, bg=self.colors["primary"])
        summary_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.avg_tat_label = tk.Label(
            summary_frame,
            text="Avg Turnaround Time: --",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["primary"],
            fg=self.colors["text"]
        )
        self.avg_tat_label.pack(side=tk.LEFT, padx=5)
        self.avg_wait_label = tk.Label(
            summary_frame,
            text="Avg Waiting Time: --",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["primary"],
            fg=self.colors["text"]
        )
        self.avg_wait_label.pack(side=tk.LEFT, padx=25)

        # Gantt Chart tab
        gantt_frame = tk.Frame(notebook, bg=self.colors["primary"])
        notebook.add(gantt_frame, text="Gantt Chart")

        # Canvas for Gantt chart
        canvas_frame = tk.Frame(gantt_frame, bg=self.colors["primary"])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollable canvas
        canvas_container = tk.Frame(canvas_frame, bg=self.colors["primary"])
        canvas_container.pack(fill=tk.BOTH, expand=True)

        self.gantt_canvas = tk.Canvas(
            canvas_container,
            bg=self.colors["card"],
            highlightthickness=1,
            highlightbackground=self.colors["border"]
        )

        gantt_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL,
                                        command=self.gantt_canvas.xview)
        self.gantt_canvas.configure(xscrollcommand=gantt_scrollbar.set)

        self.gantt_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        gantt_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Comparison tab
        compare_frame = tk.Frame(notebook, bg=self.colors["primary"])
        notebook.add(compare_frame, text="Comparison")

        compare_table_frame = tk.Frame(
            compare_frame, bg=self.colors["primary"])
        compare_table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        compare_columns = ("Algorithm", "Avg Waiting Time",
                           "Avg Turnaround Time", "Avg Response Time")
        self.compare_tree = ttk.Treeview(
            compare_table_frame, columns=compare_columns, show="headings", height=15)

        for col in compare_columns:
            self.compare_tree.heading(col, text=col)
            self.compare_tree.column(col, width=200, anchor=tk.CENTER)

        compare_scrollbar = ttk.Scrollbar(compare_table_frame, orient=tk.VERTICAL,
                                          command=self.compare_tree.yview)
        self.compare_tree.configure(yscrollcommand=compare_scrollbar.set)

        self.compare_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        compare_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def handle_algorithm_change(self, *args):
        """Wrapper to update UI when algorithm changes."""
        self.on_algorithm_change()
        self.update_radio_styles()

    def update_radio_styles(self):
        """Apply pill styling to algorithm buttons based on selection."""
        if not hasattr(self, "algorithm_radios"):
            return
        selected = self.algorithm_var.get()
        for rb in self.algorithm_radios:
            if rb.cget("value") == selected:
                rb.configure(bg=self.colors["secondary"],
                             fg=self.colors["bg"])
            else:
                rb.configure(bg=self.colors["light"],
                             fg=self.colors["muted"])

    def on_algorithm_change(self, *args):
        """Show/hide time quantum input based on selected algorithm."""
        if self.algorithm_var.get() == "RoundRobin":
            self.quantum_frame.pack(padx=20, pady=10, fill=tk.X)
        else:
            self.quantum_frame.pack_forget()

    def style_entry(self, entry: tk.Entry):
        """Apply consistent styling and focus transitions to Entry widgets."""
        entry.configure(relief=tk.FLAT)

        def on_focus_in(_):
            entry.configure(highlightbackground=self.colors["secondary"],
                            highlightcolor=self.colors["secondary"])

        def on_focus_out(_):
            entry.configure(highlightbackground=self.colors["border"],
                            highlightcolor=self.colors["border"])

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def apply_hover_effect(self, widget, base_color: str, hover_color: str):
        """Apply a simple hover transition for buttons."""
        def on_enter(_):
            widget.configure(bg=hover_color)

        def on_leave(_):
            widget.configure(bg=base_color)

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def animate_title_glow(self, label: tk.Label):
        """Apply a solid accent color to the heading."""
        label.configure(fg=self.colors["secondary"])

    def draw_background_gradient(self):
        """Render a soft aurora-like gradient background."""
        if not hasattr(self, "bg_canvas"):
            return

        self.bg_canvas.delete("gradient")
        width = max(self.root.winfo_width(), 1)
        height = max(self.root.winfo_height(), 1)
        gradient_stops = ["#020617", "#07102C", "#0F172A", "#1D1B4B"]
        steps = 80
        for i in range(steps):
            ratio = i / max(steps - 1, 1)
            # Determine surrounding colors
            lower_index = int(ratio * (len(gradient_stops) - 1))
            upper_index = min(lower_index + 1, len(gradient_stops) - 1)
            inner_ratio = (ratio * (len(gradient_stops) - 1)) - lower_index
            color = self.blend_colors(
                gradient_stops[lower_index],
                gradient_stops[upper_index],
                inner_ratio
            )
            y1 = int((i / steps) * height)
            y2 = int(((i + 1) / steps) * height)
            self.bg_canvas.create_rectangle(
                0, y1, width, y2, fill=color, outline="", tags="gradient")

        # Add soft blobs to mimic aurora lights
        self.bg_canvas.create_oval(
            width * 0.4, -height * 0.3, width * 1.1, height * 0.5,
            fill="#1E40AF", outline="", tags="gradient")
        self.bg_canvas.create_oval(
            -width * 0.2, height * 0.2, width * 0.5, height * 0.9,
            fill="#0EA5E9", outline="", tags="gradient")

    def blend_colors(self, color1: str, color2: str, t: float) -> str:
        """Blend two hex colors."""
        t = max(0.0, min(1.0, t))
        c1 = tuple(int(color1.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        c2 = tuple(int(color2.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        blended = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        return "#{:02X}{:02X}{:02X}".format(*blended)

    def add_process(self):
        """Add a process to the process list."""
        pid = self.pid_entry.get().strip()
        arrival = self.arrival_entry.get().strip()
        burst = self.burst_entry.get().strip()
        priority = self.priority_entry.get().strip()

        # Validate input
        is_valid, error_msg = utils.validate_process_input(
            pid, arrival, burst, priority)
        if not is_valid:
            messagebox.showerror("Invalid Input", error_msg)
            return

        # Check for duplicate process ID
        if any(p.process_id == pid for p in self.processes):
            messagebox.showerror("Duplicate Process ID",
                                 f"Process ID '{pid}' already exists!")
            return

        # Create and add process
        try:
            process = scheduler.Process(
                process_id=pid,
                arrival_time=float(arrival),
                burst_time=float(burst),
                priority=int(priority)
            )
            self.processes.append(process)

            # Generate color for process
            if pid not in self.process_colors:
                colors = utils.generate_unique_colors(len(self.processes))
                self.process_colors[pid] = colors.get(
                    f"P{len(self.processes)}", utils.generate_color())

            # Update listbox
            self.update_process_listbox()

            # Clear input fields
            self.pid_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers")

    def update_process_listbox(self):
        """Update the process listbox display."""
        self.process_listbox.delete(0, tk.END)
        for proc in self.processes:
            display_text = f"{proc.process_id:8s} | AT: {proc.arrival_time:6.1f} | " \
                f"BT: {proc.burst_time:6.1f} | Priority: {proc.priority:3d}"
            self.process_listbox.insert(tk.END, display_text)

    def clear_process_list(self):
        """Clear the process list."""
        if not self.processes:
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to clear all processes?"):
            self.processes.clear()
            self.process_colors.clear()
            self.update_process_listbox()

    def simulate(self):
        """Run the selected scheduling algorithm simulation."""
        if not self.processes:
            messagebox.showwarning(
                "No Processes", "Please add at least one process!")
            return

        algorithm = self.algorithm_var.get()

        # Get time quantum for Round Robin
        time_quantum = 2.0
        if algorithm == "RoundRobin":
            try:
                time_quantum = float(self.quantum_entry.get())
                if time_quantum <= 0:
                    messagebox.showerror(
                        "Invalid Input", "Time quantum must be greater than 0")
                    return
            except ValueError:
                messagebox.showerror(
                    "Invalid Input", "Time quantum must be a valid number")
                return

        # Run algorithm
        try:
            if algorithm == "FCFS":
                updated_processes, gantt_chart = scheduler.fcfs(self.processes)
            elif algorithm == "SJF":
                updated_processes, gantt_chart = scheduler.sjf(self.processes)
            elif algorithm == "SRTF":
                updated_processes, gantt_chart = scheduler.srtf(self.processes)
            elif algorithm == "Priority":
                updated_processes, gantt_chart = scheduler.priority_scheduling(
                    self.processes)
            elif algorithm == "PreemptivePriority":
                updated_processes, gantt_chart = scheduler.preemptive_priority(
                    self.processes)
            elif algorithm == "RoundRobin":
                updated_processes, gantt_chart = scheduler.round_robin(
                    self.processes, time_quantum)
            else:
                messagebox.showerror("Error", "Unknown algorithm selected")
                return

            # Display results
            self.display_results(updated_processes, gantt_chart)

        except Exception as e:
            messagebox.showerror("Simulation Error",
                                 f"An error occurred: {str(e)}")

    def display_results(self, processes: List[scheduler.Process],
                        gantt_chart: List[tuple]):
        """Display simulation results in tables and Gantt chart."""
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Populate results table
        for proc in processes:
            self.results_tree.insert("", tk.END, values=(
                proc.process_id,
                utils.format_time(proc.arrival_time),
                utils.format_time(proc.burst_time),
                proc.priority,
                utils.format_time(proc.finish_time),
                utils.format_time(proc.waiting_time),
                utils.format_time(proc.turnaround_time),
                utils.format_time(proc.response_time)
            ))

        # Draw Gantt chart
        self.draw_gantt_chart(gantt_chart)

        if processes:
            avg_tat = sum(p.turnaround_time for p in processes) / \
                len(processes)
            avg_wait = sum(p.waiting_time for p in processes) / len(processes)
            self.avg_tat_label.config(
                text=f"Avg Turnaround Time: {avg_tat:.2f}")
            self.avg_wait_label.config(
                text=f"Avg Waiting Time: {avg_wait:.2f}")
        else:
            self.avg_tat_label.config(text="Avg Turnaround Time: --")
            self.avg_wait_label.config(text="Avg Waiting Time: --")

    def draw_gantt_chart(self, gantt_chart: List[tuple]):
        """Draw the Gantt chart on canvas."""
        self.gantt_canvas.delete("all")

        if not gantt_chart:
            return

        # Calculate dimensions
        canvas_height = 300
        view_width = max(800, self.gantt_canvas.winfo_width())

        # Bar dimensions
        bar_height = 60
        y_start = 80
        scale = 30  # pixels per time unit

        # Find max time for scaling
        max_time = max(end for _, _, end in gantt_chart)

        x_offset = 50
        content_width = max(
            view_width,
            int(x_offset + max_time * scale + x_offset)
        )
        self.gantt_canvas.config(
            width=view_width,
            height=canvas_height,
            scrollregion=(0, 0, content_width, canvas_height)
        )
        self.gantt_canvas.xview_moveto(0)

        # Draw bars
        for i, (pid, start, end) in enumerate(gantt_chart):
            width = (end - start) * scale
            x1 = x_offset + start * scale
            y1 = y_start
            x2 = x1 + width
            y2 = y1 + bar_height

            # Get color
            if pid == "IDLE":
                color = self.colors.get("muted", utils.get_idle_color())
            else:
                # Use a fixed list of maximally distinct/totally different colors
                # (these are: Red, Blue, Green, Orange, Purple, Teal, Brown, Pink, Gold, Gray, Violet, Navy)
                DISTINCT_COLORS = [
                    "#E74C3C",  # Red
                    "#2980D9",  # Blue
                    "#27AE60",  # Green
                    "#E67E22",  # Orange
                    "#8E44AD",  # Purple
                    "#16A085",  # Teal
                    "#784212",  # Brown
                    "#FFD700",  # Gold
                    "#6C3483",  # Violet
                    "#154360",  # Navy
                ]
                if pid not in self.process_colors:
                    process_idx = len(self.process_colors)
                    color = DISTINCT_COLORS[process_idx % len(DISTINCT_COLORS)]
                    self.process_colors[pid] = color
                color = self.process_colors.get(pid)

            # Draw rectangle
            self.gantt_canvas.create_rectangle(x1, y1, x2, y2, fill=color,
                                               outline=self.colors["bg"], width=2)

            # Draw process ID
            if width > 20:  # Only show text if bar is wide enough
                self.gantt_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                              text=pid, font=(
                                                  "Segoe UI", 9, "bold"),
                                              fill="black")

            # Draw time labels
            if i == 0 or i == len(gantt_chart) - 1:
                self.gantt_canvas.create_text(x1, y1 - 10, text=f"{start:.1f}",
                                              font=("Segoe UI", 8), anchor=tk.S,
                                              fill=self.colors["muted"])
            if i == len(gantt_chart) - 1:
                self.gantt_canvas.create_text(x2, y1 - 10, text=f"{end:.1f}",
                                              font=("Segoe UI", 8), anchor=tk.S,
                                              fill=self.colors["muted"])

        # Draw timeline
        timeline_y = y_start + bar_height + 30
        self.gantt_canvas.create_line(x_offset, timeline_y,
                                      x_offset + max_time * scale, timeline_y,
                                      fill=self.colors["muted"], width=2)

        # Draw time markers
        for t in range(0, int(max_time) + 1, max(1, int(max_time / 10))):
            x = x_offset + t * scale
            self.gantt_canvas.create_line(x, timeline_y - 5, x, timeline_y + 5,
                                          fill=self.colors["muted"], width=1)
            self.gantt_canvas.create_text(x, timeline_y + 15, text=str(t),
                                          font=("Segoe UI", 8),
                                          fill=self.colors["muted"])

        # Draw title
        self.gantt_canvas.create_text(content_width / 2, 30,
                                      text="Gantt Chart - Process Execution Timeline",
                                      font=("Poppins", 14, "bold"),
                                      fill=self.colors["text"])

    def compare_algorithms(self):
        """Compare all algorithms with the same input."""
        if not self.processes:
            messagebox.showwarning(
                "No Processes", "Please add at least one process!")
            return

        # Get time quantum for Round Robin
        time_quantum = 2.0
        try:
            time_quantum = float(self.quantum_entry.get())
            if time_quantum <= 0:
                time_quantum = 2.0
        except ValueError:
            time_quantum = 2.0

        # Clear comparison table
        for item in self.compare_tree.get_children():
            self.compare_tree.delete(item)

        # Test all algorithms
        algorithms = [
            ("FCFS", lambda: scheduler.fcfs(self.processes)),
            ("SJF", lambda: scheduler.sjf(self.processes)),
            ("SRTF", lambda: scheduler.srtf(self.processes)),
            ("Priority", lambda: scheduler.priority_scheduling(self.processes)),
            ("Preemptive Priority", lambda: scheduler.preemptive_priority(self.processes)),
            ("Round Robin", lambda: scheduler.round_robin(
                self.processes, time_quantum))
        ]

        results = []
        for algo_name, algo_func in algorithms:
            try:
                updated_processes, _ = algo_func()
                averages = utils.calculate_averages(updated_processes)
                results.append((algo_name, averages))
            except Exception as e:
                messagebox.showerror("Comparison Error",
                                     f"Error running {algo_name}: {str(e)}")
                return

        # Populate comparison table
        for algo_name, averages in results:
            self.compare_tree.insert("", tk.END, values=(
                algo_name,
                f"{averages['avg_wt']:.2f}",
                f"{averages['avg_tat']:.2f}",
                f"{averages['avg_response']:.2f}"
            ))

    def reset_project(self):
        """Reset the entire project - clear all inputs and outputs."""
        if messagebox.askyesno("Confirm Reset",
                               "Are you sure you want to reset everything? "
                               "This will clear all processes and results."):
            # Clear processes
            self.processes.clear()
            self.process_colors.clear()
            self.update_process_listbox()

            # Clear input fields
            self.pid_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.quantum_entry.delete(0, tk.END)
            self.quantum_entry.insert(0, "2")

            # Clear results
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)

            for item in self.compare_tree.get_children():
                self.compare_tree.delete(item)

            self.gantt_canvas.delete("all")

            # Reset algorithm selection
            self.algorithm_var.set("FCFS")
            self.update_radio_styles()


def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
