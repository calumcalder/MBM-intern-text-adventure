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
    
    def describe(self):
        print(self.description)
    
if __name__ == "__main__":
    room = Room(description = "Hello world");
    room.describe()
