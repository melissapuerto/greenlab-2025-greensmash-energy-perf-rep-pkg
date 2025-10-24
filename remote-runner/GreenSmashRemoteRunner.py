from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ProgressManager.Output.OutputProcedure import OutputProcedure as output
import re
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Optional
import psutil
import threading


class RunnerConfig:
    ROOT_DIR = Path(__file__).parent

    # ================================ USER CONFIG ================================
    name: str = "greenlab_remote_run"
    results_output_path: Path = ROOT_DIR / "results"
    operation_type: OperationType = OperationType.AUTO
    time_between_runs_in_ms: int = 1000

    # Raspberry Pi connection info
    PI_USER = "prachisinghal"
    PI_HOST = "192.168.0.113"
    PI_PATH = "~/greenlab-2025-greensmash-energy-perf-rep-pkg"
    PYTHON = "/usr/bin/python"
    PJ_BIN = "/usr/bin/powerjoular"
    SAMPLE_HZ = "1"

    # List of scripts and repetitions
    SCRIPTS = {
        "baseline_bfs": "functions/baseline/breadth_first_search.py",
        "optimized_bfs": "functions/optimized/unrolled_breadth_first_search.py",
        "baseline_equilibrium_index": "functions/baseline/equilibrium_index.py",
        "optimized_equilibrium_index": "functions/optimized/unrolled_equilibrium_index.py",
        "baseline_floyd_warshall": "functions/baseline/floyd_warshall.py",
        "optimized_floyd_warshall": "functions/optimized/unrolled_floyd_warshall.py",
        "baseline_knapsack": "functions/baseline/knapsack.py",
        "optimized_knapsack": "functions/optimized/unrolled_knapsack.py",
        "baseline_max_subarray": "functions/baseline/max_subarray.py",
        "optimized_max_subarray": "functions/optimized/unrolled_max_subarray.py",
        "baseline_mergesort": "functions/baseline/mergesort.py",
        "optimized_mergesort": "functions/optimized/unrolled_mergesort.py",
        "baseline_prefix_sum": "functions/baseline/prefix_sum.py",
        "optimized_prefix_sum": "functions/optimized/unrolled_prefix_sum.py",
        "baseline_product_sum": "functions/baseline/product_sum.py",
        "optimized_product_sum": "functions/optimized/unrolled_product_sum.py",
        "baseline_stock_span": "functions/baseline/stock_span_problem.py",
        "optimized_stock_span": "functions/optimized/unrolled_stock_span_problem.py",
        "baseline_strassen": "functions/baseline/strassen_matrix_multiplication.py",
        "optimized_strassen": "functions/optimized/unrolled_strassen_matrix_multiplication.py",   
    }
    REPS = 30

    def __init__(self):
        # Subscribe to framework events
        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN, self.before_run),
            (RunnerEvents.START_RUN, self.start_run),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT, self.interact),
            (RunnerEvents.STOP_MEASUREMENT, self.stop_measurement),
            (RunnerEvents.STOP_RUN, self.stop_run),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT, self.after_experiment),
        ])
        self.run_table_model = None
        output.console_log("Custom RunnerConfig loaded")

    # ================================ RUN TABLE CREATION ================================
    def create_run_table_model(self) -> RunTableModel:
        """Create and return the RunTableModel."""
        factor_script = FactorModel("script_name", list(self.SCRIPTS.keys()))
        factor_rep = FactorModel("rep", list(range(1, self.REPS + 1)))

        # run_table = RunTableModel(
        #     factors=[factor_script, factor_rep],
        #     exclude_combinations=[],  # Optional
        #     repetitions=1,
        #     data_columns=["wall_seconds","energy_joules"],
        # )
        run_table = RunTableModel(
            factors=[factor_script, factor_rep],
            exclude_combinations=[],
            repetitions=1,
            data_columns = ["wall_seconds", "energy_joules", "avg_cpu_util_percent", "peak_memory_mb"],
        )

        # Build rows manually
        rows = []
        for script_name in self.SCRIPTS.keys():
            for rep in range(1, self.REPS + 1):
                rows.append({
                    "script_name": script_name,
                    "rep": rep
                })
        run_table.data = rows

        self.run_table_model = run_table
        return self.run_table_model

    # ================================ HOOKS ================================
    def before_experiment(self):
        output.console_log("Before experiment")

    def before_run(self):
        output.console_log("Before run")

    def start_run(self, context: RunnerContext):
        output.console_log("Start run")

    def start_measurement(self, context: RunnerContext):
        """Start PowerJoular interactively and log output to a file on the Raspberry Pi."""
        tag = f"{context.execute_run['script_name']}_r{context.execute_run['rep']}"
        remote_csv = f"/tmp/tmp_{tag}.csv"

        # Kill any stale PowerJoular processes first
        subprocess.run(
            ["ssh", f"{self.PI_USER}@{self.PI_HOST}", "sudo pkill -f powerjoular || true"],
            capture_output=True, text=True
        )

        # Start PowerJoular in background, redirecting stdout to file
        cmd = f"nohup sudo powerjoular > {remote_csv} 2>&1 & echo $!"
        proc = subprocess.run(
            ["ssh", f"{self.PI_USER}@{self.PI_HOST}", cmd],
            capture_output=True, text=True
        )
        context.pj_pid = proc.stdout.strip()

        output.console_log(f"✅ Started PowerJoular (PID={context.pj_pid}), logging to {remote_csv}")
        time.sleep(3)  # small warm-up time

    def interact(self, context: RunnerContext):
        """Run the experiment script remotely via SSH and log output, while monitoring CPU and memory."""
        tag = f"{context.execute_run['script_name']}_r{context.execute_run['rep']}"
        script_name = context.execute_run["script_name"]
        script_path = self.SCRIPTS[script_name]
        script = os.path.join(self.PI_PATH, script_path)
        cpu_log = f"/tmp/cpu_log_{tag}.csv"

        log_local = os.path.join(context.run_dir, f"log_{tag}.txt")

        # 🔹 Start remote CPU monitor (runs on Raspberry Pi)
        subprocess.run(
            ["ssh", f"{self.PI_USER}@{self.PI_HOST}",
            f"nohup sudo {self.PYTHON} ~/greenlab-2025-greensmash-energy-perf-rep-pkg/cpu_monitor.py {cpu_log} >/dev/null 2>&1 & echo $!"],
            capture_output=True, text=True
        )
        time.sleep(0.2)  # ensure CPU monitor writes first sample

        # 🔹 Run experiment script remotely
        start = time.time()
        with open(log_local, "w") as f:
            proc = subprocess.Popen(
                ["ssh", f"{self.PI_USER}@{self.PI_HOST}", f"{self.PYTHON} {script}"],
                stdout=f,
                stderr=subprocess.STDOUT
            )

        # 🔹 Start memory monitor locally (same as original)
        results = {}
        stop_event = threading.Event()
        monitor_thread = threading.Thread(target=self._monitor_memory, args=(proc.pid, stop_event, results))
        monitor_thread.start()

        proc.wait()
        stop_event.set()
        monitor_thread.join()

        context.elapsed = time.time() - start
        context.peak_memory_mb = results.get("peak_memory_mb", 0.0)

        # 🔹 Stop CPU monitor
        subprocess.run(
            ["ssh", f"{self.PI_USER}@{self.PI_HOST}", "sudo pkill -f cpu_monitor.py || true"],
            capture_output=True, text=True
        )

        # 🔹 Copy CPU log back to local machine
        local_cpu_csv = os.path.join(context.run_dir, f"cpu_{tag}.csv")
        subprocess.run(
            ["scp", f"{self.PI_USER}@{self.PI_HOST}:{cpu_log}", local_cpu_csv],
            capture_output=True, text=True
        )
        subprocess.run(
            ["ssh", f"{self.PI_USER}@{self.PI_HOST}", f"sudo rm -f {cpu_log}"],
            capture_output=True, text=True
        )

        # 🔹 Parse average CPU%
        try:
            import csv
            with open(local_cpu_csv) as f:
                reader = csv.DictReader(f)
                vals = [float(r["cpu_percent"]) for r in reader if r.get("cpu_percent")]
            context.avg_cpu_util = sum(vals) / len(vals) if vals else 0.0
        except Exception:
            context.avg_cpu_util = 0.0
    def stop_measurement(self, context: RunnerContext):
        """Stop PowerJoular and retrieve its output CSV."""
        tag = f"{context.execute_run['script_name']}_r{context.execute_run['rep']}"
        remote_csv = f"/tmp/tmp_{tag}.csv"
        local_csv = os.path.join(context.run_dir, f"power_{tag}.csv")

        # Stop PowerJoular
        subprocess.run(
            ["ssh", f"{self.PI_USER}@{self.PI_HOST}", f"sudo kill {context.pj_pid} || true"],
            capture_output=True, text=True
        )
        output.console_log(f"🛑 Stopped PowerJoular (PID={context.pj_pid})")

        # Wait until file exists (up to 45 seconds)
        for i in range(45):
            result = subprocess.run(
                ["ssh", f"{self.PI_USER}@{self.PI_HOST}", f"test -f {remote_csv} && echo exists"],
                capture_output=True, text=True
            )
            if "exists" in result.stdout:
                break
            time.sleep(1)
        else:
            output.console_log(f"❌ CSV {remote_csv} not found on remote Pi after 45s")
            return

        # Copy CSV locally
        subprocess.run(
            ["scp", f"{self.PI_USER}@{self.PI_HOST}:{remote_csv}", local_csv],
            capture_output=True, text=True
        )
        output.console_log(f"✅ Copied PowerJoular data to {local_csv}")

        # Clean up remote file
        subprocess.run(
            ["ssh", f"{self.PI_USER}@{self.PI_HOST}", f"sudo rm -f {remote_csv}"],
            capture_output=True, text=True
        )
        output.console_log(f"🧹 Removed remote CSV {remote_csv}")

        time.sleep(5)  # cool-down

    def stop_run(self, context: RunnerContext):
        output.console_log("Stop run")
    
    # def _compute_total_energy(self, csv_path: str) -> float:
    #     """Compute total energy from PowerJoular output (Watts * seconds)."""
    #     total_energy = 0.0
    #     sample_period = 1.0 / float(self.SAMPLE_HZ)
    #     power_regex = re.compile(r"Total Power:\s*([\d\.]+)\s*Watts")

    #     try:
    #         with open(csv_path, "r") as f:
    #             for line in f:
    #                 match = power_regex.search(line)
    #                 if match:
    #                     power_w = float(match.group(1))
    #                     total_energy += power_w * sample_period
    #     except Exception as e:
    #         output.console_log(f"⚠️ Failed to parse {csv_path}: {e}")
    #         return 0.0

    #     return total_energy

    def _compute_energy_and_cpu(self, csv_path: str) -> tuple[float, float]:
        """Compute total energy (J) and average CPU utilization (%) from PowerJoular output."""
        total_energy = 0.0
        cpu_util_sum = 0.0
        sample_count = 0
        sample_period = 1.0 / float(self.SAMPLE_HZ)

        power_regex = re.compile(r"Total Power:\s*([\d\.]+)\s*Watts")
        cpu_regex = re.compile(r"CPU Utilization:\s*([\d\.]+)\s*%")

        try:
            with open(csv_path, "r") as f:
                for line in f:
                    power_match = power_regex.search(line)
                    cpu_match = cpu_regex.search(line)

                    if power_match:
                        power_w = float(power_match.group(1))
                        total_energy += power_w * sample_period
                    if cpu_match:
                        cpu_util_sum += float(cpu_match.group(1))
                        sample_count += 1

            avg_cpu_util = (cpu_util_sum / sample_count) if sample_count > 0 else 0.0
            return total_energy, avg_cpu_util
        except Exception as e:
            output.console_log(f"⚠️ Failed to parse {csv_path}: {e}")
            return 0.0, 0.0
    
    def _monitor_memory(self, pid, stop_event, results):
        """Continuously monitor memory (MB) of a given PID."""
        process = psutil.Process(pid)
        peak_memory = 0.0
        while not stop_event.is_set():
            try:
                mem = process.memory_info().rss / (1024 * 1024)  # MB
                peak_memory = max(peak_memory, mem)
                time.sleep(0.1)
            except psutil.NoSuchProcess:
                break
        results["peak_memory_mb"] = peak_memory


    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, Any]]:
        """Return run metrics including total energy and average CPU from CPU monitor CSV."""
        tag = f"{context.execute_run['script_name']}_r{context.execute_run['rep']}"
        power_csv = os.path.join(context.run_dir, f"power_{tag}.csv")
        cpu_csv = os.path.join(context.run_dir, f"cpu_{tag}.csv")

        energy_joules = 0.0
        avg_cpu_util = 0.0

        # 🔹 Compute energy from PowerJoular CSV if exists
        if os.path.exists(power_csv):
            energy_joules, _ = self._compute_energy_and_cpu(power_csv)
            output.console_log(f"🔋 Total energy for {tag}: {energy_joules:.3f} J")
        else:
            output.console_log(f"⚠️ PowerJoular CSV not found for {tag}")

        # 🔹 Compute average CPU from cpu_monitor CSV if exists
        if os.path.exists(cpu_csv):
            try:
                import csv
                with open(cpu_csv) as f:
                    reader = csv.DictReader(f)
                    vals = [float(r["cpu_percent"]) for r in reader if r.get("cpu_percent")]
                avg_cpu_util = sum(vals) / len(vals) if vals else 0.0
                output.console_log(f"💻 Avg CPU for {tag}: {avg_cpu_util:.2f}%")
            except Exception as e:
                output.console_log(f"⚠️ Failed to read CPU CSV for {tag}: {e}")
                avg_cpu_util = 0.0
        else:
            output.console_log(f"⚠️ CPU CSV not found for {tag}")

        return {
            "wall_seconds": context.elapsed,
            "energy_joules": energy_joules,
            "avg_cpu_util_percent": avg_cpu_util,
            "peak_memory_mb": getattr(context, "peak_memory_mb", 0.0)
        }

    def after_experiment(self):
        output.console_log("After experiment")