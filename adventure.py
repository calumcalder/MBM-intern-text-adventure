class Room:
    """
    A room in the adventure. Contains items, and connects to other rooms.
    """
    def __init__(self, description):
        """
        Constructor of Room.

        Parameters:
            description: A string containing a description of the room.
        """
        self.description = description
        self.north = None
        self.south = None
        self.east = None
        self.west = None
    
    def describe(self):
        """
        Prints the description of the room to the console.
        """
        print(self.description)
    
    def join(self, joined_room, direction):
        """
        Joins one room to another, according to the direction given.
        """
        assert direction in ["north", "south", "east", "west"], "Direction should be one of: north, south, east, west."
        if direction == "north":
            self.north = joined_room
            joined_room.south = self
        elif direction == "south":
            self.south = joined_room
            joined_room.north = self
        elif direction == "east":
            self.east = joined_room
            joined_room.west = self
        elif direction == "west":
            self.west = joined_room
            joined_room.east = self

if __name__ == "__main__":
    room = Room(description = "Hello world")
    room.describe()
    
    north_room = Room(description = "North")
    south_room = Room(description = "South")
    east_room = Room(description = "East")
    west_room = Room(description = "West")
    
    room.join(north_room, "north")
    room.join(south_room, "south")
    room.join(east_room, "east")
    room.join(west_room, "west")
    try:
        room.join(north_room, "invalid direction")
    except AssertionError as e:
        print("Caught AssertionError")
    
    room.north.describe()
    room.south.describe()
    room.east.describe()
    room.west.describe()
