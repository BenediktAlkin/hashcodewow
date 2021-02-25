import csv
import constants

def read_inputs():
    with open(constants.filepath) as f:
        reader = csv.reader(f, delimiter=" ")

        first_row = next(reader)
        simulation = {
            "duration": int(first_row[0]),
            "n_intersections": int(first_row[1]),
            "n_streets": int(first_row[2]),
            "n_cars": int(first_row[3]),
            "reward": int(first_row[4]),
            "streets": {},
            "cars": [],
            "intersections": {id_: [] for id_ in range(int(first_row[1]))},
        }

        for i in range(simulation["n_streets"]):
            row = next(reader)
            street = {
                "start_id": int(row[0]),
                "end_id": int(row[1]),
                "name": row[2],
                "duration": int(row[3]),
                "green_light": True,
                "green_light_duration": 0,
                "priority": 0,
            }
            simulation["streets"][street["name"]] = street

        for i in range(simulation["n_cars"]):
            row = next(reader)
            car = {
                "id": i,
                "n_streets": int(row[0]),
                "street_names": row[1:]
            }
            simulation["cars"].append(car)

        for street in simulation["streets"].values():
            simulation["intersections"][street["start_id"]].append(street)
            simulation["intersections"][street["end_id"]].append(street)

        return simulation

def write_schedule(simulation):
    intersections = []

    for intersection_id, intersection in simulation["intersections"].items():
        incoming_streets = list(filter(lambda street_: street_["end_id"] == intersection_id, simulation["streets"].values()))
        schedules = []
        for street in incoming_streets:
            # TODO priority

            if street["green_light_duration"] > 0:
                schedules.append([street["name"], street["green_light_duration"]])

        if len(schedules) > 0:
            intersections.append([intersection_id, schedules])



    fname = constants.filepath.replace(".txt", ".result.txt")
    with open(fname, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        writer.writerow([len(intersections)])
        for intersection in intersections:
            writer.writerow([intersection[0]])
            writer.writerow([len(intersection[1])])

            for schedule in intersection[1]:
                writer.writerow(schedule)

