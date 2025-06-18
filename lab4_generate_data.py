import pickle
import random
from pathlib import Path
from time import sleep
from typing import List

from FramsticksLib import FramsticksLib
import pandas as pd
import numpy as np
from tqdm import tqdm


def extract_fitness(evaluation_results: List):
    return list(map(lambda x: x['evaluations']['']['vertpos'], evaluation_results))


def main():
    FramsticksLib.DETERMINISTIC = False
    lib = FramsticksLib(
        "../Framsticks52",
        None,
        "eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;only-body.sim"
    )

    output_path = Path('outputs_lab4')

    data = {}

    for f in output_path.iterdir():

        if ".csv" not in f.name:
            continue

        name_split = f.name.split('_')
        representation = name_split[1]

        if representation not in data:
            data[representation] = {
                'std': [],
                'max': [],
                'runtime': [],
                'best_individuals': []
            }

        run_data = pd.read_csv(f)

        data[representation]['std'].append(run_data.stdev.to_numpy())
        data[representation]['max'].append(run_data['max'].to_numpy())
        data[representation]['runtime'].append(run_data['runtime'][0])
        data[representation]['best_individuals'].append(run_data['best_individual'].to_numpy())

    for r in tqdm(data.keys(), desc="Processing representation"):
        selected_individuals = []
        individuals_fitness = []
        mutated_individuals = []
        mutated_pre_fitness = []
        mutated_fitness = []

        j = 0

        max_length = 0

        for run in tqdm(data[r]['best_individuals'], desc="Selecting individuals", leave=False):
            selection = list(run[j::7])
            selected_individuals.append(selection)
            max_length = max(len(selection), max_length)
            j += 1
            j %= 5

            individuals_fitness.append(extract_fitness(lib.evaluate(selection)))

        for i, si in enumerate(tqdm(selected_individuals, "Generating mutations", leave=False)):
            valid = False

            while not valid:
                try:
                    mutated = lib.mutate(si)
                    mutated_fitness.extend(extract_fitness(lib.evaluate(mutated)))
                    mutated_individuals.extend(mutated)
                    mutated_pre_fitness.extend(individuals_fitness[i])
                    valid = True
                except (KeyError, TypeError):
                    valid = False


        parent1_fitness = []
        parent2_fitness = []
        crossover_fitness = []

        choices = list(range(len(selected_individuals)))

        for i in tqdm(range(max_length), desc="Running crossover", leave=False):
            for j in tqdm(range(max_length), leave=False):
                for _ in range(25):
                    valid = False

                    while not valid:
                        try:
                            parent1, parent2 = random.sample(choices, 2)

                            l1 = min(len(selected_individuals[parent1]) - 1, i)
                            l2 = min(len(selected_individuals[parent2]) - 1, j)

                            p1 = selected_individuals[parent1][l1]
                            p2 = selected_individuals[parent2][l2]


                            child = lib.crossOver(p1, p2)
                            crossover_fitness.append(extract_fitness(lib.evaluate([child]))[0])

                            parent1_fitness.append(individuals_fitness[parent1][l1])
                            parent2_fitness.append(individuals_fitness[parent2][l2])

                            valid = True
                        except (KeyError, TypeError):
                            valid = False

        random_walk_fitness = []

        valid = False

        while not valid:
            try:
                fitness = []
                indi = []

                for i in range(len(selected_individuals[0])):
                    fitness.append([individuals_fitness[0][i]])
                    indi.append(selected_individuals[0][i])

                for _ in tqdm(range(30), desc="Running random walk", leave=False):
                    indi = lib.mutate(indi)
                    fit = extract_fitness(lib.evaluate(indi))

                    for i in range(len(selected_individuals[0])):
                        fitness[i].append(fit[i])

                random_walk_fitness = fitness

                valid = True
            except (KeyError, TypeError):
                valid = False

            output_folder = Path("outputs_lab4")

            if not output_folder.exists():
                output_folder.mkdir(exist_ok=True, parents=True)

            output_path = output_folder / f"{r}_generated_data.pkl"

            with open(output_path, 'wb') as f:
                pickle.dump({
                    'task1': {
                        'mutated_pre_fitness': mutated_pre_fitness,
                        'mutated_fitness': mutated_fitness
                    },
                    'task2': {
                        'p1_fitness': parent1_fitness,
                        'p2_fitness': parent2_fitness,
                        'crossover_fitness': crossover_fitness
                    },
                    'task3': {
                        'random_walk_fitness': random_walk_fitness,
                    }
                }, f)


if __name__ == "__main__":
    main()
