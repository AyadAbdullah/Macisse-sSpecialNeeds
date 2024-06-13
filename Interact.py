from Inventory import Inventory
from map import DetailedMap, Map


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