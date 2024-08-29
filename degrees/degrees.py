import csv
import sys
import os

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    """if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    """
    if input("1-large or 2-small?") == "1":
        directory = os.path.abspath(os.getcwd()) + "/degrees/large"
    else:
        directory = os.path.abspath(os.getcwd()) + "/degrees/small"
    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    while True:
        source = person_id_for_name(input("Name: "))
        if source is None:
            sys.exit("Person not found.")
        target = person_id_for_name(input("Name: "))
        if target is None:
            sys.exit("Person not found.")

        path = shortest_path(source, target)

        if path is None:
            print("Not connected.")
        else:
            degrees = len(path)
            print(f"{degrees} degrees of separation.")
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    if source == target:
        return []
    
    source_node = Node((None, source), None)
    queue = QueueFrontier()
    queue.add(source_node)
    while True:
        current_node = queue.frontier[0]
        for pair in neighbors_for_person(current_node.data[1]):
            node = Node(pair, current_node)
            if not queue.contains_data(pair):
                queue.add(node)
            if pair[1] == target:
                current_node = node
                path = []
                while current_node.parent != None:
                    path.append(current_node.data)
                    current_node = current_node.parent
                path = path[::-1]
                return path
        print(len(queue.frontier))
        queue.remove()
        if queue.empty() or len(queue.frontier) == len(names):
            break
    return None     


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    source = person_id
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            if person_id != source:
                neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
