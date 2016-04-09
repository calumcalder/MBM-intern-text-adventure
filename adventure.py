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

class Player:
    """
    Represents the player in the adventure. Maintains an inventory and current position, as well as providing methods for world interaction.
    """
    
    def __init__(self, initial_room):
        """
        Constructor of Player.

        Parameters:
            initial_room: The initial Room for the player to start in.
        """
        self.current_room = initial_room
    
    def go(self, direction):
        """
        Moves a player from their current room to another according to the given direction.
        """
        if direction not in ["north", "south", "east", "west"]:
            print("I don't know how to go", str(direction) + ".")
            return
        
        if direction == "north" and self.current_room.north is not None:
            self.current_room = self.current_room.north
        elif direction == "south" and self.current_room.south is not None:
            self.current_room = self.current_room.south
        elif direction == "east" and self.current_room.east is not None:
            self.current_room = self.current_room.east
        elif direction == "west" and self.current_room.west is not None:
            self.current_room = self.current_room.west
        else:
            print("I can't go that way.")
            return
        
        print("You go", direction + ".")
        self.current_room.describe()

class Item:
    """
    Represents an item in the adventure. Provides functions for interaction with the item.
    """
    
    def __init__(self, name, description):
        """
        Constructor for Item.
        
        Parameters:
            name: A string containing the name of the item.
            description: A string describing the item.
        """
        self.description = description
        self.name = name
    
    def describe(self):
        print(self.description)

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
    
    player = Player(initial_room = room)
    player.go("north")
    player.go("east")
    player.go("south")
    
    item = Item(name = "item", description = "A basic item.")
    item.describe()
    print(item.name)
