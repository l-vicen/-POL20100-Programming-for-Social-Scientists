from __future__ import annotations

# Performing "chained/double" iteration  
def tallest_pile(piles: list[list[int]]):
    for i in piles:
       pile = 0 # Counter
       for k in i:
        pile += 1
        if (k != 0):
            return pile - 1 # Adjusting counter
        else:
            continue

'''Creates a storage list with the distances. Finds the min() dist,
 then finds the index of the respective dist. Finally, uses index to 
 retrieve actual station from dict keys transformed to list'''
def closest_station(stations: dict[str, int], coordinate: int):

    tmpStorageCalculation = [] # temporary / storage list

    for value in stations.values():
        tmpStorageCalculation.append(abs(value - coordinate)) # Trick: take the absolute value to address the negative dist. cases. abs() method from https://docs.python.org/3/library/functions.html#abs 

    smallest_station_distance = min(tmpStorageCalculation)  # min() method from https://docs.python.org/3/library/functions.html#min
    smallest_station_index = tmpStorageCalculation.index(smallest_station_distance)

    return list(stations.keys())[smallest_station_index]

    

    


if __name__ == "__main__":
    # This will get executed in your IDE e.g. PyCharm but not in the submission system.

    piles = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1],
    ]

    print(tallest_pile(piles))

    stations = {
            "Klinikum Großhadern": 0,
            "Großhadern": 10,
            "Haderner Stern": 20,
    }

    print(closest_station(stations, 7))

