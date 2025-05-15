#!/usr/bin/env python3
import subprocess
import threading


def run_command(command):
    """
    Run a shell command while suppressing its output.
    """
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    # List your shell commands here. Replace the example commands with your own.
    commands = []

    for mut in ["0", "005", "010", "020", "030", "040", "050"]:
        for _ in range(10):
            commands.append(
                f"python FramsticksEvolution.py -sim \"eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;f9-mut-{mut}.sim\" -path  C:\\Users\\2002j\\Desktop\\pliki\\MastersPUT\\sem1\\BIAM\\Framsticks52 -opt vertpos -max_numparts 30 -max_numgenochars 50 -initialgenotype /*9*/BLU -popsize 50 -generations 200 -hof_size 1"
            )

    threads = []

    # Launch each command in its own thread.
    for cmd in commands:
        thread = threading.Thread(target=run_command, args=(cmd,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete.
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
