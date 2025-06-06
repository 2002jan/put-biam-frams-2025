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

    for run_type in ["0", "1", "2", "3"]:
        for _ in range(10):
            file_num = run_type if run_type != "3" else "2"

            command = f"python EvolutionLab3.py -path C:\\Users\\2002j\\Desktop\\pliki\\MastersPUT\\sem1\\BIAM\\Framsticks52 -sim \"eval-allcriteria.sim;deterministic.sim;sample-period-longest.sim;my-own-probab-{file_num}.sim\" -opt velocity -max_numparts 15 -max_numjoints 30 -max_numneurons 20 -max_numconnections 30 -genformat 1 -pxov 0 -popsize 50 -generations 150 -hof_size 1 -run-number {_} -run-type {run_type}"

            if run_type == "3":
                command += " -dynamic-params"

            commands.append(
                command
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
