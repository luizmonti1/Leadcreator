import subprocess
import time
import sys
import os

# Add import statements for the required modules
# Define the paths to the scripts for phase 1
scripts_and_delays = [
    ("main.py", 10),  # Replace with actual paths and delays
    ("phase2\run_phase2.py", 10),
    # Add more scripts and delays as needed
]

def run_script(script_path, delay):
    """Run a script and wait for a specified delay afterwards."""
    try:
        subprocess.run([sys.executable, script_path], check=True)
        print(f"Script {script_path} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_path}: {e}")
        return False
    time.sleep(delay)
    return True

def run_phase1():
    for script_path, delay in scripts_and_delays:
        success = run_script(script_path, delay)
        if not success:
            break  # If a script fails, stop the sequence

if __name__ == "__main__":
    run_phase1()
