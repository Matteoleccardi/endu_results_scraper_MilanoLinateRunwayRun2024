import os
import numpy
import matplotlib.pyplot as plt

from get_results import FILES_FOLDER
RESULTS_FILE = "results.csv"

def get_positions(total_secons_array, sorted_idxs_array):
    positions = numpy.arange(1, len(sorted_idxs_array) + 1)
    for i, pos in enumerate(positions):
        if i > 0 and total_secons_array[sorted_idxs_array[i]] == total_secons_array[sorted_idxs_array[i - 1]]:
            positions[i] = positions[i - 1]
    return positions

if __name__ == "__main__":
    # open csv with separator | and one header row
    # this file has mixed data types, ike ints and strings
    data = numpy.loadtxt(RESULTS_FILE, delimiter="|", skiprows=1, dtype=str)
    dataset = {
        "id": data[:, 0].astype(int),
        "name": data[:, 1],
        "yob": data[:, 2].astype(int), # year of birth
        "gender": data[:, 3], # "M" or "F" or "U"
        "hours": data[:, 4].astype(int),
        "minutes": data[:, 5].astype(int),
        "seconds": data[:, 6].astype(int),
        "total_seconds": data[:, 7].astype(int)
    }
    # overall classification
    # sort by total_seconds
    file_name = "classification.csv"
    sorted_indices = numpy.argsort(dataset["total_seconds"])
    positions = get_positions(dataset["total_seconds"], sorted_indices)
    with open(file_name, "w", encoding="utf8") as file:
        file.write("position,name,year of birth,gender,hours:minutes:seconds\n")
        for i, idx in enumerate(sorted_indices):
            file.write(
                f"{positions[i]},{dataset['name'][idx]},{dataset['yob'][idx]},{dataset['gender'][idx]},{dataset['hours'][idx]}:{dataset['minutes'][idx]}:{dataset['seconds'][idx]}\n"
            )
    # classification males
    file_name = "classification_males.csv"
    mask = dataset["gender"] == "M"
    sorted_indices = numpy.argsort(dataset["total_seconds"][mask])
    positions = get_positions(dataset["total_seconds"][mask], sorted_indices)
    with open(file_name, "w", encoding="utf8") as file:
        file.write("position,name,year of birth,gender,hours:minutes:seconds\n")
        for i, idx in enumerate(sorted_indices):
            file.write(
                f"{positions[i]},{dataset['name'][mask][idx]},{dataset['yob'][mask][idx]},{dataset['gender'][mask][idx]},{dataset['hours'][mask][idx]}:{dataset['minutes'][mask][idx]}:{dataset['seconds'][mask][idx]}\n"
            )
    # classification females
    file_name = "classification_females.csv"
    mask = dataset["gender"] == "F"
    sorted_indices = numpy.argsort(dataset["total_seconds"][mask])
    positions = get_positions(dataset["total_seconds"][mask], sorted_indices)
    with open(file_name, "w", encoding="utf8") as file:
        file.write("position,name,year of birth,gender,hours:minutes:seconds\n")
        for i, idx in enumerate(sorted_indices):
            file.write(
                f"{positions[i]},{dataset['name'][mask][idx]},{dataset['yob'][mask][idx]},{dataset['gender'][mask][idx]},{dataset['hours'][mask][idx]}:{dataset['minutes'][mask][idx]}:{dataset['seconds'][mask][idx]}\n"
            )
    # classification over the typical age intervals for running sports events:
    age_cathegories_dict = [
        (0, 19),
        (20, 29),
        (30, 39),
        (40, 49),
        (50, 59),
        (60, 69),
        (70, 79),
        (80, 89),
        (90, 99)
    ]
    year_at_time_of_event = 2024
    for age_cathegory in age_cathegories_dict:
        file_name = f"classification_by_age_{age_cathegory[0]}_{age_cathegory[1]}.csv"
        mask = (dataset["yob"] <= year_at_time_of_event - age_cathegory[0]) & (dataset["yob"] > year_at_time_of_event - age_cathegory[1])
        sorted_indices = numpy.argsort(dataset["total_seconds"][mask])
        positions = get_positions(dataset["total_seconds"][mask], sorted_indices)
        with open(file_name, "w", encoding="utf8") as file:
            file.write("position,name,year of birth,gender,hours:minutes:seconds\n")
            for i, idx in enumerate(sorted_indices):
                file.write(
                    f"{positions[i]},{dataset['name'][mask][idx]},{dataset['yob'][mask][idx]},{dataset['gender'][mask][idx]},{dataset['hours'][mask][idx]}:{dataset['minutes'][mask][idx]}:{dataset['seconds'][mask][idx]}\n"
                )
    # plots
    matteo = ("Matteo", "Leccardi")
    guido = ("Guido", "Leccardi")
    martina = ("Martina", "Corda")
    plt.hist(
        dataset["total_seconds"], 
        bins=100, 
        color="navy",
        alpha=0.9,
        density=True
    )
    plt.xlabel("Total time H:M:S")
    x_ticks = numpy.arange(min(dataset["total_seconds"]), max(dataset["total_seconds"]), 60*10)
    x_labels = [f"{int(x/3600)}:{int(x/60)%60}:{x%60}" for x in x_ticks]
    plt.xticks(x_ticks, x_labels, rotation=45)
    for i, name_ in enumerate(dataset["name"]):
        if (matteo[0] in name_ and matteo[1] in name_) or (guido[0] in name_ and guido[1] in name_):
            plt.vlines(
                dataset["total_seconds"][i],
                ymin=0,
                ymax=0.001,
                color="forestgreen",
                label=name_
            )
        if martina[0] in name_ and martina[1] in name_:
            plt.vlines(
                dataset["total_seconds"][i],
                ymin=0,
                ymax=0.001,
                color="pink",
                label=name_
            )
    plt.legend()
    plt.show()
        