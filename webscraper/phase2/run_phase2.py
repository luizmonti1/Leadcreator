import subprocess
import time

# Paths to the scripts to be run for phase 2
scripts_and_delays = [
    ("C:\\Users\\luizm\\webscraper\\phase2\\result_extract.py", 10),
    ("C:\\Users\\luizm\\webscraper\\phase2\\score_filter.py", 10),
    ("C:\\Users\\luizm\\webscraper\\phase2\\save_score.py", 10),
    ("C:\\Users\\luizm\\webscraper\\phase2\\app.py", 900),  # 15 minutes for app.py to finish
    ("C:\\Users\\luizm\\webscraper\\phase2\\folder_maker.py", 10),
]

def run_script(script_path, delay):
    """Run a script and wait for a specified delay afterwards."""
    try:
        subprocess.run(['python', script_path], check=True)
        print(f"Script {script_path} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_path}: {e}")
        return False
    time.sleep(delay)
    return True

def run_phase_2():
    for script_path, delay in scripts_and_delays:
        success = run_script(script_path, delay)
        if not success:
            break  # If a script fails, stop the sequence

if __name__ == "__main__":
    run_phase_2()
