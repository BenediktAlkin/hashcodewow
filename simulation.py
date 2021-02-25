import numpy as np
import constants


def simulate(data):
    reward = 0
    streets = data["streets"]
    intersections = data["intersections"]
    cars = data["cars"]

    queues = {street["name"]: [] for street in streets.values()}
    cars_on_street = []

    cars_over_intersection = {id_: 0 for id_ in data["intersections"].keys()}
    cars_over_street = {name: 0 for name in data["streets"].keys()}


    for car in cars:
        start_street_name = car["street_names"].pop(0)
        queues[start_street_name].append(car)
        cars_over_street[start_street_name] += 1


    for t in range(data["duration"]):
        #print("timestep", t)
        # drive over intersection
        for street_name, queue in queues.items():
            if len(queue) == 0: continue
            if not streets[street_name]["green_light"]: continue

            car = queue.pop(0)
            cars_on_street.append({
                "car": car,
                "pos": 0,
            })
            if t > 0:
                #print("car ", car["id"], " starts on ", street_name, "; count", streets[street_name]["start_id"])
                cars_over_intersection[streets[street_name]["start_id"]] += 1

        # drive on street
        to_remove = []
        for car_on_street in cars_on_street:
            car_on_street["pos"] += 1
            cur_car = car_on_street["car"]

            if len(cur_car["street_names"]) == 0:
                reward += data["reward"] + data["duration"] - t
                #print("car ", cur_car["id"], " finished on ", t)
                continue

            street_name = cur_car["street_names"][0]
            duration = streets[street_name]["duration"]

            if car_on_street["pos"] == duration:
                cur_car["street_names"].pop(0)
                queues[street_name].append(cur_car)
                to_remove.append(car_on_street)
                cars_over_street[street_name] += 1

        for car_on_street in to_remove:
            cars_on_street.remove(car_on_street)


    # calculate stats
    percentages = []
    for intersection_id in intersections.keys():
        incoming_streets = list(filter(lambda street_: street_["end_id"] == intersection_id, streets.values()))

        total_usage = 0
        for incoming_street in incoming_streets:
            total_usage += cars_over_street[incoming_street["name"]]

        for incoming_street in incoming_streets:
            # print(incoming_street["name"], " usage:", cars_over_street[incoming_street["name"]], " total_usage:", total_usage)
            if total_usage == 0: continue
            percentage = cars_over_street[incoming_street["name"]] / total_usage
            print(incoming_street["name"], " usage:", cars_over_street[incoming_street["name"]], " total_usage:", total_usage, "percent:", percentage)
            if percentage > 0:
                percentages.append(percentage)
            percentage *= constants.max_period

            incoming_street["green_light_duration"] = int(percentage)

    print("max", np.max(percentages))
    print("min", np.min(percentages))


    print(reward)
    print(cars_over_street)
    print(cars_over_intersection)