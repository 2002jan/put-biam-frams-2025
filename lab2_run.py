#!/usr/bin/env python3
import subprocess
from concurrent.futures import ThreadPoolExecutor
import os


def run_command(command):
    """
    Run a shell command while suppressing its output.
    """
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    # Configure the maximum number of concurrent threads
    MAX_WORKERS = 10  # Adjust this number based on your system capabilities

    # List your shell commands here. Replace the example commands with your own.
    commands = []

    for form in ["0", "1", "4", "9"]:
        for _ in range(10):
            commands.append(
                f"python EvolutionLab2.py  -path  C:\\Users\\2002j\\Desktop\\pliki\\MastersPUT\\sem1\\BIAM\\Framsticks52 -sim \"eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;only-body.sim\"  -opt vertpos -max_numparts 30 -genformat {form} -popsize 50 -generations 200 -hof_size 1 -run-number {_}"
            )

            commands.append(
                f"python EvolutionLab2.py  -path  C:\\Users\\2002j\\Desktop\\pliki\\MastersPUT\\sem1\\BIAM\\Framsticks52 -sim \"eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;only-body.sim\"  -opt vertpos -max_numparts 30 -genformat {form} -popsize 50 -generations 200 -hof_size 1 -new-fitness -run-number {_}"
            )

    print(f"Total commands to execute: {len(commands)}")
    print(f"Maximum concurrent threads: {MAX_WORKERS}")

    # Use ThreadPoolExecutor to limit concurrent threads
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all commands to the thread pool
        futures = [executor.submit(run_command, cmd) for cmd in commands]

        # Wait for all commands to complete
        completed = 0
        for future in futures:
            future.result()  # This will block until the command completes
            completed += 1
            print(f"Completed {completed}/{len(commands)} commands")

    print("All commands completed!")


if __name__ == "__main__":
    main()
