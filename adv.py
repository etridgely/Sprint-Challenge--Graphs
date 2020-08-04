from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# Pull the Stack class

class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

traversal_path = []
# Create a dictionary for this adventure, it'll help
graph = {}
# Create a Stack from the class above
stack = Stack()
# Create a set to record where our player will have gone
visited_rooms = set()

# Transform the graph into a dictionary
for i in range(len(room_graph)):
    graph[i] = {}

# The graph has no more than 500 rooms. Therefore, we can set this as a limit while traversing.
while len(visited_rooms) < 500:
    # Create a variable for where our player is
    current_room = player.current_room
    # Map out the location to where that room is in our dictionary
    current_vertex = graph[current_room.id]
    # For any room we do not see, add them to our set
    if current_room.id not in visited_rooms:
        visited_rooms.add(current_room.id)

    # Identify all the exits in our current room using the get_exits method established in room.py
    exits = [direction for direction in current_room.get_exits()]

    for direction in exits:
        if direction not in current_vertex:
            # If our desired direction is not in the location, put a placeholder there.
            current_vertex[direction] = '?'

    # If the placeholder cannot be found, then let's go ahead and remove that bad boy from our Stack.
    # Then we'll add the direction to our path.
    # Finally, update the player's direction as they move along
    if '?' not in current_vertex.values():
        direction = stack.pop()
        traversal_path.append(direction)
        player.current_room = current_room.get_room_in_direction(direction)

    else:
        for direction in exits:
            if current_vertex[direction] == '?':
                # Using the next room in the place, let's update using our placeholder
                next_room = current_room.get_room_in_direction(direction)
                # Create an opposite direction
                opposite_direction = ''
                # Add the next vertex to our dictionary
                next_vertex = graph[next_room.id]
                #map out the directions so we know what's possible
                if direction == 'n':
                    opposite_direction = 's'
                
                elif direction == 's':
                    opposite_direction = 'n'
                
                elif direction == 'e':
                    opposite_direction = 'w'
                
                elif direction == 'w':
                    opposite_direction = 'e'
                
                # Move onto the next one
                current_vertex[direction] = next_room.id
                next_vertex[opposite_direction] = current_room.id
                player.current_room = next_room

                # Add the direction to our path
                traversal_path.append(direction)
                # Add the opposite direction to our Stack
                stack.push(opposite_direction)
                
                break

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
