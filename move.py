from map import DetailedMap, Map


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

