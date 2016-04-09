DEBUG = False

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
        self.items = {}
        self.north = None
        self.south = None
        self.east = None
        self.west = None
    
    def describe(self):
        """
        Prints the description of the room to the console.
        """
        print(self.description)
        
        if self.items:
            print("In the room you can see the following items:")
            for item in self.items:
                print(item)
    
    def add_item(self, item):
        """
        Adds an item to the room.
        
        Parameters:
            item: The item to be added.
        """
        self.items[item.name] = item
    
    def join(self, joined_room, direction):
        """
        Joins one room to another, according to the direction given.
        
        Parameters:
            joined_room: The room that this room should be joined to.
            direction: The position of the joined room relative to this room.
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
        self.items = {}
    
    def go(self, direction):
        """
        Moves a player from their current room to another according to the given direction.
        
        Parameters:
            direction: The direction in which the player should move, should be one of north, south, east, west.
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
    
    def get(self, item_name):
        """
        Gets an item from the current room and adds it to the player's inventory.
        
        Parameters:
            item_name: The name of the item to be picked up.
        """
        if item_name in self.items:
            print("You've already collected that item.")
            return
        
        try:
            item = self.current_room.items.pop(item_name)
            self.items[item_name] = item
            print(item.get_text)
        except KeyError:
            print("I can't see that item.")
        
            
    def inventory(self):
        """
        Prints the player's inventory to console.
        """
        print("You have the following items:")
        for item in self.items:
            print(item)

class Item:
    """
    Represents an item in the adventure. Provides functions for interaction with the item.
    """
    
    def __init__(self, name, description, get_text = None):
        """
        Constructor for Item.
        
        Parameters:
            name: A string containing the name of the item.
            get_text: A string to be printed when the item is collected.
            description: A string describing the item.
        """
        self.description = description
        self.name = name
        self.get_text = get_text or "You pick up the " + name
    
    def describe(self):
        """
        Prints a description of the item to the console.
        """
        print(self.description)

class Game:
    """
    Singleton class for encapsulating game loop and related functions.
    """
    
    def __init__(self, initial_room, check_success):
        """
        Contructor for Game.
        
        Parameters:
            initial_room: The inital room of the map. Should be the start room of a pre-constructed board.
            check_success: A function to check if the game has been won.
        """
        self.player = Player(initial_room)
        self.check_success = check_success
    
    def read_command(self):
        """
        Reads in a command and passes it off to the appropriate handler
        """
        command = input(">")
        param = ""
        extra = []
        try:
            command, param, *extra= command.lower().split(" ")
        except ValueError:
            print("I don't know how to do that.")
            return
        
        if command in ["go", "move"]:
            self.player.go(direction = param)
        elif command in ["get", "collect", "grab"]:
            self.player.get(item_name = param)
        elif command in ["describe", "examine", "inspect"]:
            self.handle_describe(param)
        elif command in ["inventory", "bag"]:
            self.player.inventory()
        else:
            print("I don't know how to do that.")
    
    def handle_describe(self, param):
        """
        Handles a call to describe an object.
        
        Parameters:
            param: The parameter passed in by the player from the command line.
        """
        if param in self.player.items:
            print("You look at the", param + ".")
            self.player.items[param].describe()
        elif param in self.player.current_room.items:
            print("You look at the", param + ".")
            self.player.current_room.items[param].describe()
        elif param == "room":
            self.player.current_room.describe()
        else:
            print("I can't see anything like that.")
    
    def read_commands_forever(self):
        while not self.check_success():
            self.read_command()

if DEBUG == True:
    print("---Basic room description---")
    room = Room(description = "Hello world")
    room.describe()
    
    print()
    print("---Addition of rooms---")
    north_room = Room(description = "North")
    south_room = Room(description = "South")
    east_room = Room(description = "East")
    west_room = Room(description = "West")
    
    room.join(north_room, "north")
    room.join(south_room, "south")
    room.join(east_room, "east")
    room.join(west_room, "west")
    print("---Join on invalid direction---")
    try:
        room.join(north_room, "invalid direction")
    except AssertionError as e:
        print("Caught AssertionError, invalid direction handled.")
    
    print("---Decription of rooms in NSEW.---")
    room.north.describe()
    room.south.describe()
    room.east.describe()
    room.west.describe()
    
    print()
    print("---Player tests---")
    player = Player(initial_room = room)
    print("---Movement---")
    player.go("north")
    player.go("east")
    player.go("south")
    
    print()
    print("---Item tests---")
    print("---Creation---")
    item = Item(name = "item", description = "A basic item.")
    item.describe()
    print(item.name)
    
    print("---Adding to room, room descriptions---")
    room.add_item(item)
    room.describe()
    print("---Player pick up---")
    print("---Player in wrong room---")
    player.go("south")
    player.get("item")
    player.go("north")
    print("---Wrong item_name---")
    player.get("invalid item")
    print("---Success and inventory---")
    player.get("item")
    player.inventory()
    print("---Pick up twice---")
    player.get("item")
    print("---Room inventory check---")
    room.describe()

if __name__ == "__main__":
    start_room = Room(description = "A plain white room with a door to the north and a door to the south.")
    start_room.add_item(Item(
        name = "note", 
        description = "A small note. It says:\n \
            Congratulations, you're on to stage 2 of the Made by Many Technologist Internship application process.\n \
            We'd like you to make a text adventure game - get coding!\n\n \
            You think to yourself, 'I could do with a computer to make this on.'",
        get_text = "You pull the note off the wall that it's pinned to."
    ))
    
    desk_room = Room(description = "You come to another white room. There's an empty desk filling up one wall.")
    start_room.join(desk_room, "north")
    
    hallway = Room(description = "You enter a narrow hallway, with doors to the south, east, and west.")
    start_room.join(hallway, "south")
    
    monitor_room = Room(description = "You've come outside, and are surrounded by tall brown cliffs. You feel sand under your feet, and see a sky blue lagoon with a glinting object lying deep under the water.")
    
    
    game = Game(start_room, lambda: False)
    game.read_commands_forever()
