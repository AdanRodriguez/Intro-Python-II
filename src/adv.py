from room import Room
from player import Player
from items import Item
# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

item = {
    'stick': Item('stick', 'You can probably do some damage with it'),
    'rock': Item('rock', 'You can throw it at something'),
    'knife': Item('knife', 'You can use it as a weapon, or to make some lunch')
}

room['outside'].add_item(item['stick'])
room['outside'].add_item(item['rock'])
room['outside'].add_item(item['knife'])

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

def main():
    # make a new player that is currently in the 'outside' room
    player = Player(input("Enter your name: "), room['outside'])
    while True:
        current_room = player.current_room
        # print the current room name
        print(f"\n\033[1;31;40mCurrent location: {current_room.name}\n")
        # print current room description
        print(current_room.description)
        # print all items in the room
        current_room.print_items()
        # wait for user input
        user_input = input(">>> ")
        input_length = len(user_input.split(' '))
        directions = ('n', 's', 'e', 'w')
        print()
        
        if input_length == 1:
            # if user enters a cardinal direction, attempt to move there
            if user_input in directions:
                attempted_room = getattr(
                    current_room, f"{user_input}_to")
                # if movement is allowed, update the current room
                if attempted_room != None:
                    player.change_room(attempted_room)
                # print error message if movement is not allowed
                else:
                    print("You cannot move in that direction")
            # if user enters q, quit the game
            elif user_input == 'q':
                break
            # print error message if user enters invalid input
            else:
                print("Input not valid, please try again")
        
        elif input_length == 2:
            user_input = user_input.split(' ')
            action = user_input[0]
            object_name = user_input[1]

            # picks up items using get or take
            if action == 'get':
                for item in current_room.items:
                    if item.name == object_name:
                        current_room.remove_item(item)
                        player.add_item(item)
                        # print(f"\n{item} picked up\n")
                        item.on_take()
                        break
                    else:
                        print("\nItem doesnt exists\n")
            #drops items using drop            
            elif action == 'drop':
                #check if its in players inventory
                for item in player.inventory:
                    if item.name == object_name:
                        # add to current room and remove from inventory
                        current_room.add_item(item)
                        player.remove_item(item)
                        item.on_drop()
                        break
                    else:
                        print("\nItem not in inventory\n")
                else:
                    print("\nInvalid Input\n")

                print()

if __name__ == '__main__':
    main()