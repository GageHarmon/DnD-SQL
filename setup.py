import sqlite3
from classes import Character, DungeonMaster, Players

# Define database operations
class Characterdb:
    
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

# ++++++++++++++++++++ Create tables if they don't already exist or were dropped ++++++++++++++++++++
    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS campaigns (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            playerset_id INTEGER,
                            dungeonmaster_id INTEGER,
                            FOREIGN KEY (playerset_id) REFERENCES playerset(id),
                            FOREIGN KEY (dungeonmaster_id) REFERENCES dungeonmaster(id)
                            )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS dungeonmaster (
                            id INTEGER PRIMARY KEY,
                            name TEXT
                            )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS playerset (
                            id INTEGER PRIMARY KEY,
                            player_1_id INTEGER,
                            player_2_id INTEGER,
                            player_3_id INTEGER,
                            player_4_id INTEGER,
                            FOREIGN KEY (player_1_id) REFERENCES players(id),
                            FOREIGN KEY (player_2_id) REFERENCES players(id),
                            FOREIGN KEY (player_3_id) REFERENCES players(id),
                            FOREIGN KEY (player_4_id) REFERENCES players(id)
                            )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS players (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            character_id INTEGER,
                            FOREIGN KEY (character_id) REFERENCES characters(id)
                            )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS characters (
                            id INTEGER PRIMARY KEY,
                            name TEXT, 
                            hp INTEGER,
                            strength INTEGER,
                            dexterity INTEGER,
                            intelligence INTEGER,
                            charisma INTEGER,
                            wisdom INTEGER
                            )''')
        # # Retrieve all players in a playerset that belongs to a campaign with ID 1
        # self.c.execute('''SELECT players.*
        #            FROM players
        #            JOIN playerset ON playerset.player_1_id = players.id OR
        #                             playerset.player_2_id = players.id OR
        #                             playerset.player_3_id = players.id OR
        #                             playerset.player_4_id = players.id
        #            JOIN campaign_playerset ON campaign_playerset.playerset_id = playerset.id
        #            WHERE campaign_playerset.campaign_id = 1''')
        # results = self.c.fetchall()
        # print(results)

        # # Retrieve the dungeon master for a campaign with ID 2
        # self.c.execute('''SELECT dungeonmaster.*
        #            FROM dungeonmaster
        #            JOIN campaign_dungeonmaster ON campaign_dungeonmaster.dungeonmaster_id = dungeonmaster.id
        #            WHERE campaign_dungeonmaster.campaign_id = 2''')
        # results = self.c.fetchall()
        # print(results)
        
        self.conn.commit()
    
#  ++++++++++++++++++++ Dungeon Master Editing ++++++++++++++++++++
    def edit_dungeonmaster(self):
        while True:
            print("Dungeon Master Edit\n")
            print("1. Add Dungeon Master")
            print("2. Display All Dungeon Masters")
            print("3. Update Dungeon Master")
            print("4. Delete Dungeon Master")
            print("5. Quit")
            
            choice = input("Enter choice: ")
            
            if choice == "1":
                name = input("Enter name: ")
                self.add_dungeonmaster(name)
                
            elif choice == "2":
                dungeonmasters = self.get_all_dungeonmasters()
                for dungeonmaster in dungeonmasters:
                    print(dungeonmaster)
                
            elif choice == "3":
                id = int(input("Enter ID: "))
                dungeonmaster = self.get_dungeonmaster(id)
                name = input("Enter new name: ")
                dungeonmaster.name = name
                self.update_dungeonmaster(dungeonmaster)
                print("Dungeon Master updated!")
                
            elif choice == "4":
                id = int(input("Enter ID: "))
                self.delete_dungeonmaster(id)
                print("Dungeon Master deleted!")
                
            elif choice == "5":
                break
    
    def add_dungeonmaster(self, name):
        self.c.execute("INSERT INTO dungeonmaster VALUES (NULL, ?)", (name,))
        self.conn.commit()
    
    def delete_dungeonmaster(self, id):
        self.c.execute("DELETE FROM dungeonmaster WHERE id=?", (id,))
        self.conn.commit()
        # Return the number of rows deleted
        return self.c.rowcount
    
    def get_all_dungeonmasters(self):
        self.c.execute("SELECT * FROM dungeonmaster")
        rows = self.c.fetchall()
        dungeonmasters = []
        for row in rows:
            dungeonmaster = DungeonMaster(row[0], row[1])
            dungeonmasters.append(dungeonmaster)
        return dungeonmasters
    
# ++++++++++++++++++++ Player Editing ++++++++++++++++++++
    def edit_players(self):
        while True:
            print("Player Edit\n")
            print("1. Add Player")
            print("2. Display All Players")
            print("3. Update Player")
            print("4. Delete Player")
            print("5. Quit")
            
            choice = input("Enter choice: ")
            
            if choice == "1":
                name = input("Enter name: ")
                self.add_player(name)
                
            elif choice == "2":
                players = self.get_all_players()
                for player in players:
                    print(player)
                
            elif choice == "3":
                id = int(input("Enter ID: "))
                player = self.get_player(id)
                name = input("Enter new name: ")
                player.name = name
                self.update_player(player)
                print("Player updated!")
                
            elif choice == "4":
                id = int(input("Enter ID: "))
                self.delete_player(id)
                print("Player deleted!")
                
            elif choice == "5":
                break

    def add_player(self, name, character_id):
        self.c.execute("INSERT INTO players VALUES (NULL, ?, ?)", (name, character_id))
        self.conn.commit()
    
    def update_player(self, player):
        self.c.execute("""UPDATE players
                        SET name = ?,
                            character_id = ?
                         WHERE id = ?""",
                   (player.name,
                    player.character_id,
                    player.id))
        self.conn.commit()
        # Return the number of rows modified
        return self.c.rowcount
    
    def delete_player(self, id):
        self.c.execute("DELETE FROM players WHERE id=?", (id,))
        self.conn.commit()
        return self.c.rowcount
    
    def get_all_players(self):
        self.c.execute("SELECT * FROM players")
        rows = self.c.fetchall()
        players = []
        for row in rows:
            player = Players(row[0], row[1], row[2])
            players.append(player)
        return players
        
# ++++++++++++++++++++ Character Editing ++++++++++++++++++++
    def edit_characters(self):
        while True:
            print("Character Edit\n")
            print("1. Add Character")
            print("2. Display All characters")
            print("3. Update Character")
            print("4. Delete Character")
            print("5. Quit")
            
            choice = input("Enter choice: ")
            
            if choice == "1":
                name = input("Enter name: ")
                self.add_character(name)
                
            elif choice == "2":
                characters = self.get_all_characters()
                for character in characters:
                    print(character)
                
            elif choice == "3":
                id = int(input("Enter ID: "))
                character = self.get_character(id)
                name = input("Enter new name: ")
                character.name = name
                self.update_character(character)
                print("Character updated!")
                
            elif choice == "4":
                id = int(input("Enter ID: "))
                self.delete_character(id)
                print("Character deleted!")
                
            elif choice == "5":
                break

    def add_character(self, character):
        self.c.execute("INSERT INTO characters VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                       (character.name, character.hp, character.strength, character.dexterity, character.intelligence, character.charisma, character.wisdom))
        self.conn.commit()
        
    def update_character(self, character):
        self.c.execute("""UPDATE characters
                        SET name = ?,
                            hp = ?,
                            strength = ?,
                            dexterity = ?,
                            intelligence = ?,
                            charisma = ?,
                            wisdom = ?
                         WHERE id = ?""",
                   (character.name,
                    character.hp,
                    character.strength,
                    character.dexterity,
                    character.intelligence,
                    character.charisma,
                    character.wisdom,
                    character.id))
        self.conn.commit()
        # Return the number of rows modified
        return self.c.rowcount

    def get_all_characters(self):
        self.c.execute("SELECT * FROM characters")
        rows = self.c.fetchall()
        characters = []
        for row in rows:
            character = Character(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row [7])
            characters.append(character)
        return characters
    
    def delete_character(self, id):
        self.c.execute("DELETE FROM characters WHERE id=?", (id,))
        self.conn.commit()
        # Return the number of rows deleted
        return self.c.rowcount
 
# ++++++++++++  initalizes DB +++++++++++  
db =  Characterdb("./dnd.db")

db.create_tables()

# ++++++++++++++ CLI prompts and inputs +++++++++++++++
print('''
 _____                                               _____      
|  _  \                                      ___    |  _  \                                
| | | |_   _ _ __   __ _  ___  ___  _ __    ( _ )   | | | |_ __ __ _  __ _  ___  _ __  ___ 
| | | | | | | '_ \ / _` |/ _ \/ _ \| '_ \   / _ \/\ | | | | '__/ _` |/ _` |/ _ \| '_ \/ __|
| |/ /| |_| | | | | (_| |  __/ (_) | | | | | (_>  < | |/ /| | | (_| | (_| | (_) | | | \__ \_
|___/  \__,_|_| |_|\__, |\___|\___/|_| |_|  \___/\/ |___/ |_|  \__,_|\__, |\___/|_| |_|___/
                    __/ |                                             __/ |                
                   |___/                                             |___/                 
                   
   _____ _                          _              _____ _               _                 
  /  __ \ |                        | |            /  ___| |             | |                
  | /  \/ |__   __ _ _ __ __ _  ___| |_ ___ _ __  \ `--.| |__   ___  ___| |_ ___           
  | |   | '_ \ / _` | '__/ _` |/ __| __/ _ \ '__|  `--. \ '_ \ / _ \/ _ \ __/ __|          
  | \__/\ | | | (_| | | | (_| | (__| ||  __/ |    /\__/ / | | |  __/  __/ |_\__ \          
   \____/_| |_|\__,_|_|  \__,_|\___|\__\___|_|    \____/|_| |_|\___|\___|\__|___/  
   
''')

while True:
    print("\nPlease choose an option:\n")
    print("\n1. Edit Dungeon Masters\n")
    print("\n2. Edit Players\n")
    print("\n3. Edit Characters\n")
    print("4. Quit")
    
    choice = input("\nEnter your choice (1-4): ")
# ++++++ DUNGEON MASTER SELECTION +++++++    
    if choice == "1":
        print("""
        1. Add Dungeon Master
        2. Display All Dungeon Masters
        3. Delete Dungeon Master
        """)
        dungeonmaster_choice = input("Enter choice: ")
        
        if dungeonmaster_choice == "1":
            name = input("\nEnter Dungeon Master name: ")
            db.add_dungeonmaster(name)
            print(f"\n{name} has been added as a Dungeon Master.\n")
        
        elif dungeonmaster_choice == "2":
            dungeonmasters = db.get_all_dungeonmasters()
            if dungeonmasters:
                for dungeonmaster in dungeonmasters:
                    print(dungeonmaster)
            else:
                print('''\n
                      
                      
        _   _        _________  ____      ______                    _                                                                          
        | \ | |       |  _  \  \/  ( )     |  ___|                  | |                                                                         
        |  \| | ___   | | | | .  . |/ ___  | |_ ___  _   _ _ __   __| |                                                                         
        | . ` |/ _ \  | | | | |\/| | / __| |  _/ _ \| | | | '_ \ / _` |                                                                         
        | |\  | (_) | | |/ /| |  | | \__ \ | || (_) | |_| | | | | (_| |_                                                                        
        \_| \_/\___/  |___/ \_|  |_/ |___/ \_| \___/ \__,_|_| |_|\__,_(_)                                                                       
                                                                                                                                                
                                                                                                                                                
       _____ _                                      _   _              __                      _  ______                ___       _         _ 
      |_   _| |                                    | | ( )            / _|                    | | |  _  \              |_  |     | |       | |
        | | | |__   ___ _   _   _ __ ___  _   _ ___| |_|/__   _____  | |_ ___  _   _ _ __   __| | | | | |__ _ _   _      | | ___ | |__  ___| |
        | | | '_ \ / _ \ | | | | '_ ` _ \| | | / __| __| \ \ / / _ \ |  _/ _ \| | | | '_ \ / _` | | | | / _` | | | |     | |/ _ \| '_ \/ __| |
        | | | | | |  __/ |_| | | | | | | | |_| \__ \ |_   \ V /  __/ | || (_) | |_| | | | | (_| | | |/ / (_| | |_| | /\__/ / (_) | |_) \__ \_|
        \_/ |_| |_|\___|\__, | |_| |_| |_|\__,_|___/\__|   \_/ \___| |_| \___/ \__,_|_| |_|\__,_| |___/ \__,_|\__, | \____/ \___/|_.__/|___(_)
                        __/ |                                                                                 __/ |                          
                        |___/                                                                                 |___/                           
                      
                                                                Z             
                                     Z                   
                         .,.,        z           
                     (((((())    z             
                    ((('_  _`) '               
                    ((G   \ |)                 
                    (((`   " ,                  
                    .((\.:~:          .--------------.    
                    __.| `"'.__      | \              |     
                .~~   `---'   ~.    |  .             :     
                /                `   |   `-.__________)     
                |             ~       |  :             :   
                |                     |  :  |              
                |    _                |     |   [ ##   :   
                \    ~~-.            |  ,   oo_______.'   
                `_   ( \) _____/~~~~ `--___              
                | ~`-)  ) `-.   `---   ( - a:f -         
                |   '///`  | `-.                         
                |     | |  |    `-.                      
                |     | |  |       `-.                   
                |     | |\ |                             
                |     | | \|                             
                `-.  | |  |                             
                    `-| '
                      
                      \n''')
                
        elif dungeonmaster_choice == "3":
            id = input("\nEnter Dungeon Master id: ")
            deleted = db.delete_dungeonmaster(id)
            if deleted:
                print(f"\nDungeon Master with id {id} has been deleted from the database.\n")
            else:
                print(f"\nDungeon Master with id {id} not found in the database.\n")

# ++++++ PLAYER SELECTION +++++++
    if choice == "2":
        print("""
        1. Add Player
        2. Display All Players
        3. Update Player
        4. Delete Player
        """)
        player_choice = input("Enter choice: ")

        if player_choice == "1":
            name = input("\nEnter player name: ")
            character_id = input("\nEnter character id: ")
            db.add_player(name, character_id)
            print(f"\n{name} has been added as a player.\n")
            
        elif player_choice == "2":
            players = db.get_all_players()
            
            if players:
                for player in players:
                    print(player)
            else:
                print('''\nNo Players found, they must have all died!
                      
                                    .:=+*#%%%%%%#*+=:.                                    
                                 -*%@@@@@@@@@@@@@@@@@@%*-                                 
                              .*@@@@@@@@@@@@@@@@@@@@@@@@@@*.                              
                             =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+                             
                            =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+                            
                           .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.                           
                           -@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=                           
                           =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=                           
                           :@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-                           
                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                            
                            +@%@@=.    :=#@@@@@@%=:    .=@@%@*                            
                            .*@@+         =@@@@+         =@@*.                            
                             %@@+          @@@@.         =@@@.                            
                            +@@@@-        +@@@@*        -@@@@*                            
                            *@@@@@@%*+++#@@@%%@@@#+++*#@@@@@@@                            
                             *@@@@@@@@@@@@@@:.%@@@@@@@@@@@@@%-                            
                               :-+#@@@@@@@@ :: %@@@@@@@#+=-.                              
                                   -@@@@@@@@@@@@@@@@@@-                                   
                        =+=         @@@@@@@@@@@@@@@@@@         =+=.                       
                       *@@@@+       =@@@@@@@@@@@@@@@@+       +@@@@#                       
                        @@@@@@=      ..:+.+#--#+.+- .      =%@@@@@.                       
                     =@@@@@@@@@@*=:                    :=*@@@@@@@@@@+                     
                     *@@@@@@@@@@@@@@%*=-.        .-=*%@@@@@@@@@@@@@@*                     
                       .:::::-=+*%@@@@@@@@#*==+#@@@@@@@@%*+=-::::::                       
                                   .:+%@@@@@@@@@@@@%+:.                                   
                              .:-+*%@@@@@@@@##%@@@@@@@%*+-:.                              
                     -#%@@@%@@@@@@@@@@%*=:      :=*#@@@@@@@@@@%@@@%#-                     
                     #@@@@@@@@@@@%*-.                .-+#@@@@@@@@@@@#                     
                      --@@@@@@#-                          -#@@@@@@--                      
                       =@@@@%:                              :%@@@@+                       
                       -#@#-                                  -#@%-                       
                                                                                          
                                                                                        
                      ''')
                
        elif player_choice == "3":
            id = input("\nEnter player id: ")
            name = input("Enter new name (leave blank if no change): ")
            character_id = input("Enter character id: ")
            
            player = Players(id, name, character_id)
            updated = db.update_player(player)
            
            if updated:
                print(f"\nPlayer with id {id} has been updated.\n")
            else:
                print(f"\nPlayer with id {id} not found in the database.\n") 
                
        elif player_choice == "4":
            id = input("\nEnter player id: ")
            deleted = db.delete_player(id)
            
            if deleted:
                print(f"\nPlayer with id {id} has been deleted from the database.\n")
            else:
                print(f"\nPlayer with id {id} not found.\n")
                

# ++++++ CREATE CHARACTER SELECTION +++++++
    if choice == "3":
        print("""
        1. Add Character
        2. Display All Characters
        3. Update Character
        4. Delete Character
        """)
        character_choice = input("Enter choice: ")
        
        if character_choice == "1":
            name = input("\nEnter character name: ")
            hp = input("Enter character hp: ")
            strength = input("Enter character strength: ")
            dexterity = input("Enter character dexterity: ")
            intelligence = input("Enter character intelligence: ")
            charisma = input("Enter character charisma: ")
            wisdom = input("Enter character wisdom: ")
            
            character = Character(None, name, hp, strength, dexterity, intelligence, charisma, wisdom)
            db.add_character(character)
            print(f"\n{character.name} has been added to the database.\n")
            
        
        elif character_choice == "2":
            characters = db.get_all_characters()
            
            if characters:
                for character in characters:
                    print(character)
            else:
                print('''\n
                      
         _   _         _____ _                          _                  ______                   _                                          
        | \ | |       /  __ \ |                        | |                |  ___|                  | |                                         
        |  \| | ___   | /  \/ |__   __ _ _ __ __ _  ___| |_ ___ _ __ ___  | |_ ___  _   _ _ __   __| |                                         
        | . ` |/ _ \  | |   | '_ \ / _` | '__/ _` |/ __| __/ _ \ '__/ __| |  _/ _ \| | | | '_ \ / _` |                                         
        | |\  | (_) | | \__/\ | | | (_| | | | (_| | (__| ||  __/ |  \__ \ | || (_) | |_| | | | | (_| |_                                        
        \_| \_/\___/   \____/_| |_|\__,_|_|  \__,_|\___|\__\___|_|  |___/ \_| \___/ \__,_|_| |_|\__,_(_)                                       
                                                                                                                                            
                                                                                                                                            
         _____                           _          _            _            _    _                                   _   _       _ _         
        /  ___|                         | |        | |          | |          | |  (_)                                 | | (_)     (_) |        
        \ `--.  ___  ___ _ __ ___  ___  | |_ ___   | |__   ___  | | __ _  ___| | ___ _ __   __ _    ___ _ __ ___  __ _| |_ ___   ___| |_ _   _ 
         `--. \/ _ \/ _ \ '_ ` _ \/ __| | __/ _ \  | '_ \ / _ \ | |/ _` |/ __| |/ / | '_ \ / _` |  / __| '__/ _ \/ _` | __| \ \ / / | __| | | |
        /\__/ /  __/  __/ | | | | \__ \ | || (_) | | |_) |  __/ | | (_| | (__|   <| | | | | (_| | | (__| | |  __/ (_| | |_| |\ V /| | |_| |_| |
        \____/ \___|\___|_| |_| |_|___/  \__\___/  |_.__/ \___| |_|\__,_|\___|_|\_\_|_| |_|\__, |  \___|_|  \___|\__,_|\__|_| \_/ |_|\__|\__, |
                                                                                            __/ |                                         __/ |
                                                                                           |___/                                         |___/ 
                      
                                    .....:::------:::.                                 
                             .:::------:----:...::::::--====--:.                          
                        .::::::......::::.................:::--==-:.                      
                     .:-:.......................................::-==-:.                  
                  .::...............................................:--=-:                
                .:.....................................................:-==-              
               :......................................::-.......... .....::-=-            
             :: .................:................::....:-:.................:-=:          
            -.    ......... ....:-.......     .....-......--.................:-=-         
          .: ...................:-.................:=......:-:.................:==        
         :. .........::.........--..................+-.......-:.................:==       
        :. .........:-..........--..:...............-*-:......-:.................:==      
       -. ..........=:.......::.+=:.-...............:#+-:......--.................:==     
      -. ..........==:.......=::#=:.=:...............+#=-:......--.................-=-    
     :. ..........:+-.......:-.=#=-.==:..............-*#==:......-:...........::...:-+.   
    :. ...........==:......:=:.*#==:++-:.............:***==-......=::-::....--::-...:==   
   .: ...........:+=:......=-.-**+=:=*=-:.............+*+*==-:....:==:-----=--::=....-=:  
   -  ...........-+-......:+-:**=*=--#*=-:............-#++*==-:....-=-::-=+*-:::=:...-==  
  .: ...:-.......==-......+=:=*+=+==-##+=-:...........:**=+*==-:....==::-*-:==-:=:...:=+. 
  -::-:--=:......==-.....=*--#+===+=-***==-:...........+*==+*+==:...-=--*=:..:=+=.....==- 
  --:-+=-+:......+=:....:#=-**=====+==*+*===:........:-=*====*+==-:..=-=-.............-== 
 :.:-+::--.......+=:...:*+=**======++-**+*===-:.......+=#+====**===:.-:...............-=+ 
 : .-:...........+=:..:+*=**========+==*+=*====-:.-==-++#*+++++*#*++=:=...............-=+ 
 : .............:+=:..+#+#*++++++++++****==++==+=-::..-+**=======**===+...............-=+ 
 :..............:+=::*#*#+============++*+===+==**+=--=+*#++======+*+=+:..............-=+ 
 :..............:+=:+*#*+======++++++===*+=====++*+++**#%%##%%%%%%%%%%#+..............-== 
 -...............+=+***=++**####%%##*=======++++=++==+*+--+%@@@@@@%====+..............-=- 
 ::..:...........+**#%###*#%@@@@@@%===========++=======-:+%####*###+===+..............-=- 
  -..-:..........=**===:  :+%%%##%%+=====================**+======#====+.............:=+. 
  -..:=:.........-#+======#*++++++*+=========++++=========*======+*====+.............:=+  
  .:.:+-..........**======*+======*========================+++==+=====-=.............:==  
   -:.==:.........=*=======++====++============================--::....-.............==:  
    -.=+-.........:*================================----:::............=.............=+   
     -:==:..:..::.:=+.................................................:=::.......:..:==   
      -=:=::::::::::*=................................................+-:-:::::::::::-:   
       ----:::::::::=+-..............................................=*::-:::::::::::::   
        = =::::::::::*+:...........................................:++*::-::::::::::::-   
          .-:::::::::=++-....................--======............-+++++::-::::::::::::-   
           +:::::::::-*+++=:.................-::::::..........-=+**++++:-:::::::::::::=   
           =-:::::::::*++++**+==-:........................:-=*+++*+++++:=:::::::::::::=   
           -::::::::::++++**++++++*++=-::.............:-===--+++++*++++:=:::::::::::::-:  
           -:-::::::::=+++**+++++++*++++**==---:::-====------+=-++*++++:=::::::::::::::-  
           -:=::::::::=+++*++++++++*++++=++-----==------::..::...:-+*++:=::::::::::::::=  
           -:=::::::::-++++++++++++**=:..-=:::::::::......:-.......:***:=::::::::::::::=. 
           -:--::::::::*++=++++****=:.....:-:...........:-..........=+*:=:::::::::::::::- 
           =:-=::::::::*++-+***++=:.........:-.........-:...........-+*:=:::::::::::::::- 
                      
                      \n''')
                
            
        elif character_choice == "3":
            id = input("\nEnter character id: ")
            name = input("Enter new name (leave blank if no change): ")
            hp = input("Enter new hp (leave blank if no change): ")
            strength = input("Enter new strength (leave blank if no change): ")
            dexterity = input("Enter new dexterity (leave blank if no change): ")
            intelligence = input("Enter new intelligence (leave blank if no change): ")
            charisma = input("Enter new charisma (leave blank if no change): ")
            wisdom = input("Enter new wisdom (leave blank if no change): ")
            
            character = Character(id, name, hp, strength, dexterity, intelligence, charisma, wisdom)
            updated = db.update_character(character)
            
            if updated:
                print(f"\nCharacter with id {id} has been updated.\n")
            else:
                print(f"\nCharacter with id {id} not found in the database.\n")
                
                
        elif character_choice == "4":
            id = input("\nEnter character id: ")
            deleted = db.delete_character(id)
            
            if deleted:
                print(f"\nCharacter with id {id} has been deleted from the database.\n")
            else:
                print(f"\nCharacter with id {id} not found in the database.\n")
            
# +++++ EXIT +++++     
    elif choice == "4":
        print('''\n
              
       _____ _                 _           __                       _                                    
      |_   _| |               | |         / _|                     (_)                                   
        | | | |__   __ _ _ __ | | _____  | |_ ___  _ __   _   _ ___ _ _ __   __ _                        
        | | | '_ \ / _` | '_ \| |/ / __| |  _/ _ \| '__| | | | / __| | '_ \ / _` |                       
        | | | | | | (_| | | | |   <\__ \ | || (_) | |    | |_| \__ \ | | | | (_| |                       
        \_/ |_| |_|\__,_|_| |_|_|\_\___/ |_| \___/|_|     \__,_|___/_|_| |_|\__, |                       
                                                                            __/ |                       
                                                                            |___/                        
        ______      ______   _____ _                          _              _____ _               _       
        |  _  \     |  _  \ /  __ \ |                        | |            /  ___| |             | |      
        | | | |_ __ | | | | | /  \/ |__   __ _ _ __ __ _  ___| |_ ___ _ __  \ `--.| |__   ___  ___| |_ ___ 
        | | | | '_ \| | | | | |   | '_ \ / _` | '__/ _` |/ __| __/ _ \ '__|  `--. \ '_ \ / _ \/ _ \ __/ __|
        | |/ /| | | | |/ /  | \__/\ | | | (_| | | | (_| | (__| ||  __/ |    /\__/ / | | |  __/  __/ |_\__ \_
        |___/ |_| |_|___/    \____/_| |_|\__,_|_|  \__,_|\___|\__\___|_|    \____/|_| |_|\___|\___|\__|___/
              
                             ^\    ^                  
                            / \\  / \                 
           _______          /.  \\/   \       |\___/|   
          /      /           / / |  \\    \  __/  O  O\   
          |     /          /  /  |   \\    \_\/  \     \     
         /   /\/         /   /   |    \\   _\/    '@___@      
        /   /          /    /    |     \\ _\/       |U
        |   |        /     /     |      \\\/        |
        \   |      /_     /      |       \\  )   \ _|_
        \   \        ~-./_ _    |    .- ; (  \_ _ _,\'
        ~    ~.            .-~-.|.-*      _        {-,
         \      ~-. _ .-~                 \      /\'
           \                   }            {   .*
            ~.                 '-/        /.-~----.
              ~- _             /        >..----.\\\_
                  ~ - - - - ^}_ _ _ _ _ _ _.-\\\_
                    
                    \n''')
        break
    
    # else:
    #     print("\nInvalid choice. Please try again.\n")