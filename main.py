# map.py
from tabulate import tabulate
import random


# overall_map_room
class Map:

    def __init__(self):
        self.overall_map_room = {
            "Hell's Kitchen Docks": [
                "Lookout Point", "Smuggler's Den", "Warehouse",
                "Secret Passage", "Office", "Shipping Bay"
            ],
            "Gang Hideout": [
                "Main Hall", "Weapon Storage", "Leader's Room", "Secret Exit",
                "Surveillance Room", "Torture Chamber"
            ],
            "Hell's Kitchen Downtown": [
                "Bar", "Apartment Block", "Bank",
                "Police Station", "Hospital", "The Pierre"
            ],
            "Alleyway": [
                "Backstreet", "Hidden Nook", "Garbage Dump", "Fire Escape",
                "Dead End", "Underground Entrance"
            ],
            "New York Bulletin Building": [
                "Newsroom", "Editor's Office", "Archive Room",
                "Cubicle", "Printing Press", "Rooftop"
            ],
            "Prison": [
                "Cell Block", "Guard Room", "Warden's Office", "Cafeteria",
                "Gym", "Solitary Confinement"
            ],
            "Wilson Fisk's Penthouse": [
                "Entrance", "Art Gallery", "Safe Room",
                "Master Bedroom", "Private Balcony", "Living Room"
            ]
        }

        self.sub_area_maps = self._create_sub_area_maps()

        self.rooms_clues = {
            "Hell's Kitchen Docks":{ 
                "Office":["Documents", "Letter to Kingpin"],
                "Shipping Bay":["AK-47", "Glock-19", "M4A1"]
            },
            "Gang Hideout":{
                "Weapon Storage":["Illegal shipment papers"],
                "Leader's Room":["Mysterious file"],
                "Surveillance Room":["Recorded Meeting"],
                "Torture Chamber":["Carl Hoffman"]
            },
            "New York Bulletin Building" : {
                "Archive Room":["New York Bulletin Newspaper"],
                "Cubicle":[""]
            },
            "Prison": {
                "Cell Block": ["Inmate information"],
                "Solitary Confinement": ["Isolated Prisoner"],
            },
            "Wilson Fisk's Penthouse": {
                "Entrance": ["Business documents"],
                "Art Gallery": ["Expensive art"],
                "Master Bedroom": ["Personal belongings"],
                "Private Balcony": ["Panoramic view"],
                "Living Room": ["Luxury decor"],
            }
        }

    def _create_sub_area_maps(self):
        sub_area_maps = {}
        for main_area, sub_areas in self.overall_map_room.items():
            sub_area_maps[main_area] = {sub_area: [['' for _ in range(3)] for _ in range(2)]
                                        for sub_area in sub_areas}
        return sub_area_maps

    def print_game_map_table(self, filename="Overall_map.txt"):
        headers = ['Location', 'Rooms']
        table_data = [(location, ', '.join(rooms))
                      for location, rooms in self.overall_map_room.items()]
        table = tabulate(table_data, headers=headers, tablefmt='grid')

        try:
            with open(filename, 'w') as file:
                file.write(table)
        except IOError:
            print("Unable to export map layout")

    def print_location_table(self):
        """
        Prints just the location names in a table. 
        """
        locations = list(self.overall_map_room.keys())
        rows = [locations[i:i + 7] for i in range(0, len(locations), 7)]
        print("Locations: ")
        print(tabulate(rows, tablefmt="grid"))

    def get_location_index(self, location_name):
        """
        Will collect the index of a location in the overall map list
        """
        for index, location in enumerate(self.overall_map_room.keys()):
            if location == location_name:
                return index
        return -1

    def print_sub_area_map(self, main_area, sub_area, filename='Sub_area_map.txt'):
        if main_area not in self.sub_area_maps or sub_area not in self.sub_area_maps[main_area]:
            print(f"No map found for {sub_area} in {main_area}")
            return

        map_data = self.sub_area_maps[main_area][sub_area]
        table = tabulate(map_data, tablefmt="grid")

        try:
            with open(filename, 'w') as file:
                file.write(table)
        except IOError:
            print(f"Unable to export file for {sub_area} in {main_area}")

    def view_map(self, filename="Rooms_map.txt"):

        #Displays the map file content

        try:
            with open(filename, 'r') as file:
                print(file.read())
        except IOError:
            print("Error: Unable to read the map file.")


class DetailedMap(Map):
    def __init__(self):
        super().__init__()

    def print_detailed_map(self, location, filename='Rooms_map.txt'):
        if location not in self.overall_map_room:
            print(f"No map found for {location}")
            return
        rooms = self.overall_map_room[location]
        rows = [rooms[i: i + 3] for i in range(0, len(rooms), 3)]
        table = tabulate(rows, tablefmt="grid")

        try:
            with open(filename, 'w') as file:
                file.write(table)
        except IOError:
            print(f"Unable to export file for {location}")

    def view_map(self, filename="Rooms_map.txt"):

        #Displays the map file content

        try:
            with open(filename, 'r') as file:
                print(file.read())
        except IOError:
            print("Error: Unable to read the map file.")


class Move:
    def __init__(self):
        self.map = Map()
        self.detailed_map = DetailedMap()
        self.player_position = 0  # Start at the first location
        self.room_position = (0, 0)  # Starting position within the detailed map


    def move_to_location(self, location_name):
        """
        This function will help the user change locations
        """
        location_index = self.map.get_location_index(location_name)
        if location_index != -1:
            self.player_position = location_index
            self.room_position = (0, 0)  # Reset room position when changing locations
            self.describe_current_location()
        else:
            print(f"Invalid location: {location_name}")

    def move_within_location(self, direction):
        location, rooms = (list(self.detailed_map.overall_map_room.items())
                           [self.player_position])
        max_x = len(rooms) // 3
        max_y = 2  # Since each row in the detailed map has 3 rooms

        new_position = self._move(self.room_position, direction, max_x, max_y)
        if new_position:
            self.room_position = new_position
            self.describe_current_room()
        else:
            print("You cannot move in that direction")


    def _move(self, current_position, direction, max_x, max_y):
        x, y = current_position
        if direction == "north" and x > 0:
            return (x - 1, y)
        elif direction == "south" and x < max_x:
            return (x + 1, y)
        elif direction == "west" and y > 0:
            return (x, y - 1)
        elif direction == "east" and y < max_y:
            return (x, y + 1)
        return None


    def describe_current_location(self):
        location, _ = (list(self.detailed_map.overall_map_room.items())
                       [self.player_position])
        print(f"Current location: {location}\n")
        self.detailed_map.print_detailed_map(location)


    def describe_current_room(self):
        location, rooms = (list(self.detailed_map.overall_map_room.items())
                           [self.player_position])
        x, y = self.room_position
        room_index = x * 3 + y

        # Ensure the room index is within the list bounds
        if room_index < len(rooms):
            current_room = rooms[room_index]
            print(f"Current room in {location}: {current_room}\n")

            # Fetch and display clues for the current room
            clues = self.map.rooms_clues.get(location, {}).get(current_room, [])
            if clues:
                print(f"Clues in {current_room}: {', '.join(clues)}")
            else:
                print(f"No clues found in {current_room}.")
        else:
            print("The room index is out of bounds for the current location.")

class Inventory:
    def __init__(self):
        self.items = {"Batons":"2 Batons"}

    def add_item(self, item, description):
        self.items[item] = description
        print(f"Added {item} to inventory")

    def remove_item(self, item):
        if item in self.items:
            del self.items[item]
            print(f"Removed {item} from the inventory.")
        else:
            print(f"You don't have {item} in your inventory")

    def view_inventory(self):
        if not self.items:
            print("Your inventory is empty")
        else:
            for item, description in self.items.items():
                print(f"{item}: {description}")

    def use_item(self, item):
        if item in self.items:
            print(f"You used {item} : {self.items[item]}")
            self.remove_item(item)
        else:
            print(f"You don't have {item} in your inventory.")


class Interact():
    def __init__(self, rooms_clues):
        self.rooms_clues = rooms_clues
        self.inv = Inventory()
        self.gen_list = {
            "Documents":"You read the documents on the desk. It reads:" 
                        +" Weapons delivered. Send this to the boss. Thank"
                        +" us later.\n" 
                        +" Justin Hammer",

            "Letter to Kingpin": "You read the letter beside the documents"+
                                " It reads: Hey boss, we received the weapons"+
                                " They should be headed to the Russians Hideout."+
                                " Yours Truly"+
                                " Turk",

            "Illegal shipment papers": "You look at the shipment paper." +
                                        "They look forged", 

            "Recorded Meeting": "You find a video of a the trade deal between gangs"
            +"You see that the shipment deal goes to plan. However at the end,"
            +" a suited guy in glasses and introduces himself as James Wesley."
            +" The others ask 'Who're you?'. He replies, 'I am here on behalf of'"
            +" the Kingpin", 

            "Inmate information":"You take a look at the paper that checks"
            +" all ins and outs of inmates. You notice that Jasper Evans is"
            +" inside the prison. However using your senses you can't sense his"+
            "hearbeat.",

            "Mysterious File": "You read the mysterious file it say: "
                                +"WE DON'T CARE ABOUT YOUR SECRECY ANYMORE."
                                +" WE KNOW WHO YOU ARE WILSON FISK."
                                +" NO MORE PLAYING IN THE SHADOWS. " 
        }
        self.collected_clues = []

    def take_clue(self, room_name, clue1):
        if room_name in self.rooms_clues and clue1 in self.rooms_clues[room_name]:
            self.collected_clues.append(self.rooms_clues[room_name][clue1])
            del self.rooms_clues[room_name][clue1]
            print(f"You have taken the {clue1} clue from the {room_name}.")
        else:
            print("Invalid room name or clue.")

    def examine_clues(self, clue2):
        if clue2 in self.gen_list:
            print(self.gen_list[clue2])
        else:
            print("No clues collected yet.")


class PuzzleMechanic:
    def __init__(self):
        self.puzzles = self._init_puzzles()

    def _init_puzzles(self):
        return {
            "Warehouse": {
                "puzzle": "What is the code to unlock the hidden safe? (Hint: It's the year Hell's Kitchen was founded)",
                "solution": "1890",
                "reward": "Hidden Safe Contents"
            },
            "Leader's Room": {
                "puzzle": "Solve the riddle to find the hidden drawer: 'I speak without a mouth and hear without ears. I have no body, but I come alive with wind.'",
                "solution": "Echo",
                "reward": "Mysterious Key"
            },
            "Archive Room": {
                "puzzle": "What is the missing number in the sequence: 2, 3, 5, 9, 17, ?",
                "solution": "33",
                "reward": "Secret Document"
            }
        }

    def attempt_puzzle(self, room):
        if room in self.puzzles:
            puzzle = self.puzzles[room]
            print(puzzle["puzzle"])
            answer = input("Enter your answer: ").strip()
            if answer == puzzle["solution"]:
                print(f"Correct! You have obtained: {puzzle['reward']}")
                return puzzle["reward"]
            else:
                print("Incorrect answer.")
        else:
            print("No puzzle in this room.")
        return None


def main():
    move = Move()
    map = Map()
    map2 = DetailedMap()
    int = Interact(map.rooms_clues)
    inv = Inventory()
    puzzle_mechanic = PuzzleMechanic()
    print("Welcome to Daredevil: Man Without Fear")
    print("You are Daredevil, the protector of Hell's Kitchen")
    print("Your mission is to rid the streets of crime.")

    while True:
        map.print_game_map_table()
        move.describe_current_location()
        move.describe_current_room()
        print("\nWhat do you want to do?")
        print("1. Move Up")
        print("2. Move Down")
        print("3. Move Left")
        print("4. Move Right")
        print("5. Search Room")
        print("6. View Inventory")
        print("7. Attempt Puzzle")
        print("8. View Current Location Map")
        print("9. View Main Map")
        print("10. Quit")
        user_choice = input("Enter the number corresponding to your choice: ").strip()

        if user_choice == "1":
            move.move_within_location("north")
        elif user_choice == "2":
            move.move_within_location("south")
        elif user_choice == "3":
            move.move_within_location("west")
        elif user_choice == "4":
            move.move_within_location("east")
        elif user_choice == "5":
            current_location, rooms = (list(move.map.overall_map_room.items())
                                       [move.player_position])
            x, y = move.room_position
            room_index = x * 3 + y

            if room_index < len(rooms):
                current_room = rooms[room_index]
                int.examine_clues(current_room)
        elif user_choice == "6":
            inv.view_inventory()
        elif user_choice == "7":
            current_location, rooms = (list(move.map.overall_map_room.items())
                                       [move.player_position])
            x, y = move.room_position
            room_index = x * 3 + y

            if room_index < len(rooms):
                current_room = rooms[room_index]
                reward = puzzle_mechanic.attempt_puzzle(current_room)
                if reward:
                    inv.add_item(reward, f"Reward from solving puzzle in {current_room}")
        elif user_choice == "8":
            current_location = (list(move.map.overall_map_room.keys())
                                [move.player_position])
            map2.print_detailed_map(current_location)
            map2.view_map()
        elif user_choice == "9":
            map.print_game_map_table()
            map.view_map()
        elif user_choice == "10":
            print("Thanks for playing")
            break 
        else:
            print("Invalid Option.")

if __name__ == "__main__":
    main()