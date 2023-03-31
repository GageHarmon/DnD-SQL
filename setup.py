import sqlite3
from colorama import Fore, Style
from classes import Character, DungeonMaster, Players, Campaigns

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
                            team_id INTEGER,
                            dungeonmaster_id INTEGER,
                            FOREIGN KEY (playerset_id) REFERENCES team(id),
                            FOREIGN KEY (dungeonmaster_id) REFERENCES dungeonmaster(id)
                            )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS dungeonmaster (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            campaign_id INTEGER,
                            FOREIGN KEY (campaign_id) REFERENCES campaign(id)
                            )''')
        
        self.c.execute('''CREATE TABLE IF NOT EXISTS team (
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
        self.conn.commit()
        
# ++++++++++++++++ Campaign Editiing +++++++++++++++++++            
    def add_new_campaign(self, name, dungeonmaster_id, playerset_id,):
        self.c.execute("INSERT INTO campaigns VALUES (NULL, ?, ?, ?)", (name, dungeonmaster_id, playerset_id))
        self.conn.commit()
    
    def get_all_campaigns(self):
        self.c.execute('''SELECT * FROM campaigns''')
        campaigns = self.c.fetchall()
        for campaign in campaigns:
            print(f'''| ID: {campaign[0]} | Name: {campaign[1]}
                    ''')
        return campaigns

    def get_campaign_info(self, campaign_id):
        self.c.execute('''SELECT * FROM campaigns WHERE id=?''', (campaign_id,))
        campaign = self.c.fetchone()
        if not campaign:
            print(f'''Campaign not found!''')
        else:
            print(f'''| Campaign Name: {campaign[1]}''')

            # get dungeon master info
            self.c.execute('''SELECT * FROM dungeonmaster WHERE id=?''', (campaign[3],))
            dm = self.c.fetchone()
            print(f'''| Dungeon Master: {dm[1]}
                  ''')
            
            # get player info
            self.c.execute('''SELECT * FROM team WHERE id=?''', (campaign[2],))
            team = self.c.fetchone()
            print("Players:")
            for i in range(1, 5):
                player_id = team[i]
                if player_id:
                    self.c.execute('''SELECT * FROM players WHERE id=?''', (player_id,))
                    player = self.c.fetchone()
                    print(f'''  - {player[1]} | (Character ID: {player[2]})''')

    def delete_campaigns(self, id):
        self.c.execute("DELETE FROM campaigns WHERE id=?", (id,))
        self.conn.commit()
        # Return the number of rows deleted
        return self.c.rowcount
    
#  ++++++++++++++++++++ Dungeon Master Editing ++++++++++++++++++++
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

    def add_player(self, name, character_id):
        self.c.execute("INSERT INTO players VALUES (NULL, ?, ?)", (name, character_id))
        self.conn.commit()
    
    def update_player(self, player):
        self.c.execute('''UPDATE players
                        SET name = ?,
                            character_id = ?
                         WHERE id = ?''',
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
    
    # +++++++ ANOTHER GPT JOIN +++++++
    def display_character_info(self, player_id):
        self.c.execute("SELECT * FROM players WHERE id=?", (player_id,))
        row = self.c.fetchone()
        if not row:
            print('''No player found with the given ID.''')
            return
        player = Players(row[0], row[1], row[2])
        character_id = player.character_id
        self.c.execute("SELECT * FROM characters WHERE id=?", (character_id,))
        row = self.c.fetchone()
        if not row:
            print('''No character found with the given ID.''')
            return
        character = Character(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        print(character)
        
# ++++++++++++++++++++ TEAM Editing ++++++++++++++++++++
    def add_team(self, player_1_id, player_2_id, player_3_id, player_4_id):
        self.c.execute("INSERT INTO team VALUES (NULL, ?, ?, ?, ?)",
                       (player_1_id, player_2_id, player_3_id, player_4_id))
        team_id = self.c.lastrowid
        self.conn.commit()
        return team_id
    
    def get_all_teams(self):
        self.c.execute("SELECT * FROM team")
        return self.c.fetchall()
    
    def delete_team(self, id):
        self.c.execute("DELETE FROM team WHERE id=?", (id,))
        self.conn.commit()
        return self.c.rowcount
    
    # ++++++ JOIN BUILT WITH THE HELP OF GPT ++++++
    def display_team_info(self, team_id):
        # Retrieve player IDs from the player set
        self.c.execute("SELECT player_1_id, player_2_id, player_3_id, player_4_id FROM team WHERE id=?", (team_id,))
        player_ids = self.c.fetchone()
        if not player_ids:
            print(f'''No player set with ID {team_id} exists.''')
            return

        # ++++++ Retrieve player information for each player in the set +++++++++++
        for player_id in player_ids:
            self.c.execute("SELECT p.name, c.name, c.hp, c.strength, c.dexterity, c.intelligence, c.charisma, c.wisdom "
                        "FROM players p "
                        "JOIN characters c ON p.character_id = c.id "
                        "WHERE p.id=?", (player_id,))
            player_info = self.c.fetchone()
            if player_info:
                print(f'''|| Player: {player_info[0]}''')
                print(f'''|| Character: {player_info[1]}''')
                print(f'''|| HP: {player_info[2]}''')
                print(f'''|| Strength: {player_info[3]}''')
                print(f'''|| Dexterity: {player_info[4]}''')
                print(f'''|| Intelligence: {player_info[5]}''')
                print(f'''|| Charisma: {player_info[6]}''')
                print(f'''|| Wisdom: {player_info[7]}''')
                print()
            else:
                print(f'''|| No player with ID {player_id} exists.''')

# ++++++++++++++++++++ Character Editing ++++++++++++++++++++

    def add_character(self, character):
        self.c.execute("INSERT INTO characters VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                       (character.name, character.hp, character.strength, character.dexterity, character.intelligence, character.charisma, character.wisdom))
        self.conn.commit()
        
    def update_character(self, character):
        self.c.execute('''UPDATE characters
                        SET name = ?,
                            hp = ?,
                            strength = ?,
                            dexterity = ?,
                            intelligence = ?,
                            charisma = ?,
                            wisdom = ?
                         WHERE id = ?''',
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
    
    
    def get_character_by_id(self, character_id):
        self.c.execute("SELECT * FROM characters WHERE id=?", (character_id,))
        row = self.c.fetchone()
        if row:
            character = Character(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            return character
        else:
            return None
    
    def delete_character(self, id):
        self.c.execute("DELETE FROM characters WHERE id=?", (id,))
        self.conn.commit()
        # Return the number of rows deleted
        return self.c.rowcount

# ++++++++++++  initalizes DB +++++++++++  
db =  Characterdb("./dnd.db")

db.create_tables()

# ++++++++++++++ CLI prompts and inputs +++++++++++++++
GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW
MAGENTA = Fore.MAGENTA
RESET = Style.RESET_ALL
print(f'{GREEN}' '''
 _____                                               _____      
|  _  \                                      ___    |  _  \                                
| | | |_   _ _ __   __ _  ___  ___  _ __    ( _ )   | | | |_ __ __ _  __ _  ___  _ __  ___ 
| | | | | | | '_ \ / _` |/ _ \/ _ \| '_ \   / _ \/\ | | | | '__/ _` |/ _` |/ _ \| '_ \/ __|
| |/ /| |_| | | | | (_| |  __/ (_) | | | | | (_>  < | |/ /| | | (_| | (_| | (_) | | | \__ \_
|___/  \__,_|_| |_|\__, |\___|\___/|_| |_|  \___/\/ |___/ |_|  \__,_|\__, |\___/|_| |_|___/
                    __/ |                                             __/ |                
                   |___/                                             |___/                 
 ''' f'{RESET}')                
print(f'{RED}' '''
   _____ _                          _              _____ _               _                 
  /  __ \ |                        | |            /  ___| |             | |                
  | /  \/ |__   __ _ _ __ __ _  ___| |_ ___ _ __  \ `--.| |__   ___  ___| |_ ___           
  | |   | '_ \ / _` | '__/ _` |/ __| __/ _ \ '__|  `--. \ '_ \ / _ \/ _ \ __/ __|          
  | \__/\ | | | (_| | | | (_| | (__| ||  __/ |    /\__/ / | | |  __/  __/ |_\__ \          
   \____/_| |_|\__,_|_|  \__,_|\___|\__\___|_|    \____/|_| |_|\___|\___|\__|___/  
   
''' f'{RESET}')

while True:
    print(f'{MAGENTA}''''\nPlease choose an option:\n''')
    print("\n1. Campaign setup\n")
    print("\n2. Edit Dungeon Masters\n")
    print("\n3. Edit Players\n")
    print("\n4. Edit Teams\n")
    print("\n5. Edit Characters\n")
    print('''6. Quit
          ''' f'{RESET}')
    choice = input(f'''\nEnter your choice (1-6): ''')
# ++++++ CAMPAIGN SELECTION +++++++++
    if choice == "1":
        print(f'{MAGENTA}''''
        1. Add New Campaign
        2. Get All Campaigns
        3. Delete Campaigns
        4. Quit
        '''f'{RESET}')
        campaign_choice = input(f'''Enter choice: ''')
        
        if campaign_choice == "1":
            name = input("Enter campaign name: ")
            dungeonmaster_id = input ("Enter DM ID: ")
            playerset_id = input ("Enter playerset ID: ")
            db.add_new_campaign(name, dungeonmaster_id, playerset_id)
            print(f'''\n{name} has been created!
                  ''')
        
        elif campaign_choice == "2":
            campaigns = db.get_all_campaigns()
            if campaigns:
                campaign_id = input("Enter campaign ID to get info: ")
                
                db.get_campaign_info(campaign_id)
        
        elif campaign_choice == "3":
            id = input("\nEnter Campaign ID: ")
            deleted = db.delete_campaigns(id)
            if deleted:
                print(f'''\nCampaign with id {id} has been deleted from the database.\n''')
            else:
                print(f'''\nCampaign with id {id} not found in the database.\n''')
                
        elif campaign_choice == "4":
            pass
                      
# ++++++ DUNGEON MASTER SELECTION +++++++    
    elif choice == "2":
        print(f'{MAGENTA}''''
        1. Add Dungeon Master
        2. Display All Dungeon Masters
        3. Delete Dungeon Master
        4. Quit
        '''f'{RESET}')
        dungeonmaster_choice = input(f'{YELLOW}''''Enter choice: '''f'{RESET}')
        
        if dungeonmaster_choice == "1":
            name = input("\nEnter Dungeon Master name: ")
            db.add_dungeonmaster(name)
            print(f'''\n{name} has been added as a Dungeon Master.
                  \n''')
        
        elif dungeonmaster_choice == "2":
            dungeonmasters = db.get_all_dungeonmasters()
            if dungeonmasters:
                for dungeonmaster in dungeonmasters:
                    print(dungeonmaster)
            else:
                print('''\nNo Dungeon Masters found\n
                      ''')
                
        elif dungeonmaster_choice == "3":
            id = input("\nEnter Dungeon Master id: ")
            deleted = db.delete_dungeonmaster(id)
            if deleted:
                print(f'''\nDungeon Master with id {id} has been deleted from the database.
                      \n''')
            else:
                print(f'''\nDungeon Master with id {id} not found in the database.
                      \n''')
                
        elif dungeonmaster_choice == "4":
            pass

# ++++++ PLAYER SELECTION +++++++
    elif choice == "3":
        print(f'{MAGENTA}'"""
        1. Add Player
        2. Display All Players
        3. Display Player Character Info
        4. Update Player
        5. Delete Player
        6. Quit
        """f'{RESET}')
        player_choice = input(f'{YELLOW}''''Enter choice: '''f'{RESET}')

        if player_choice == "1":
            name = input("\nEnter player name: ")
            character_id = input("\nEnter character id: ")
            db.add_player(name, character_id)
            print(f'''\n{name} has been added as a player.
                  \n''')
            
        elif player_choice == "2":
            players = db.get_all_players()
            
            if players:
                for player in players:
                    character = db.get_character_by_id(player.character_id)
                    print(f''' || Player ID: {player.id} || Name: {player.name} || Character ID: {character.id}''')
            else:
                print('''\nNo Players found, they must have all died!
                      ''')
         
        elif player_choice == "3":
            character_id = input("\nEnter Player ID: ")
            db.display_character_info(character_id)
                
        elif player_choice == "4":
            id = input("\nEnter player id: ")
            name = input("Enter new name (leave blank if no change): ")
            character_id = input("Enter character id: ")
            
            player = Players(id, name, character_id)
            updated = db.update_player(player)
            
            if updated:
                print(f'''\nPlayer with ID {id} has been updated.
                      \n''')
            else:
                print(f'''\nPlayer with ID {id} not found in the database.
                      \n''') 
            
        elif player_choice == "5":
            id = input("\nEnter Player ID: ")
            deleted = db.delete_player(id)
            
            if deleted:
                print(f'''\nPlayer with ID {id} has been deleted from the database.
                      \n''')
            else:
                print(f'''\nPlayer with ID {id} not found.
                      \n''')
        
        elif player_choice == "6":
            pass   
           
# ++++++PLAYERSET SELECTION +++++++                 
    elif choice == "4":
        print (f'{MAGENTA}'"""
        1. Add Team
        2. Get All Teams
        3. Display Team Info
        4. Delete Team
        5. Quit
        """f'{RESET}')
        team_choice = input(f'{YELLOW}''''Enter choice: '''f'{RESET}')
        
        if team_choice == "1":
            player_1_id = input("Enter player 1 ID: ")
            player_2_id = input("Enter player 2 ID: ")
            player_3_id = input("Enter player 3 ID: ")
            player_4_id = input("Enter player 4 ID: ")
            db.add_team(player_1_id, player_2_id, player_3_id, player_4_id)
            print(f'{RED}''''\n
         _    _      _                            _          _   _            _                                                           _           
        | |  | |    | |                          | |        | | | |          | |                                                         | |          
        | |  | | ___| | ___ ___  _ __ ___   ___  | |_ ___   | |_| |__   ___  | |_ ___  __ _ _ __ ___     ___ ___  _ __ ___  _ __ __ _  __| | ___  ___ 
        | |/\| |/ _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | __| '_ \ / _ \ | __/ _ \/ _` | '_ ` _ \   / __/ _ \| '_ ` _ \| '__/ _` |/ _` |/ _ \/ __|
        \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |_| | | |  __/ | ||  __/ (_| | | | | | | | (_| (_) | | | | | | | | (_| | (_| |  __/\__ \_
         \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \__|_| |_|\___|  \__\___|\__,_|_| |_| |_|  \___\___/|_| |_| |_|_|  \__,_|\__,_|\___||___/                                                                                                             
                  \n'''f'{RESET}')
        
        elif team_choice == '2':
            teams = db.get_all_teams()
            if not teams:
                print("No teams found.")
            else:
                print("Teams:")
                for team in teams:
                    print(f'''| ID: {team[0]} | Player 1 ID: {team[1]} | Player 2 ID: {team[2]} | '''
                    f'''Player 3 ID: {team[3]} | Player 4 ID: {team[4]}''')
                    
        elif team_choice == "3":
            team_id = input("Enter Team ID: ")
            db.display_team_info(team_id)
            
            
        elif team_choice == "4":
            id = input("\nEnter Team ID: ")
            deleted = db.delete_playerset(id)
            
            if deleted:
                print(f'''\nTeam with id {id} has been deleted.
                      \n''')
            else:
                print(f'''\nTeam with id {id} not found in the database.
                      \n''')
        
        elif team_choice == "5":
            pass
        
# ++++++ CREATE CHARACTER SELECTION +++++++
    elif choice == "5":
        print(f'{MAGENTA}'"""
        1. Add Character
        2. Display All Characters
        3. Update Character
        4. Delete Character
        5. Quit
        """f'{RESET}')
        character_choice = input(f'{YELLOW}''''Enter choice: '''f'{RESET}')
        
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
            print(f'''\n{character.name} has been added to the database.
                  \n''')
            
        elif character_choice == "2":
            characters = db.get_all_characters()
            
            if characters:
                for character in characters:
                    print(character)
            else:
                print(f'''\nNo Character found in database!\n''')
                
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
                print(f'''\nCharacter with id {id} has been updated.
                      \n''')
            else:
                print(f'''\nCharacter with id {id} not found in the database.
                      \n''')
                     
        elif character_choice == "4":
            id = input("\nEnter character id: ")
            deleted = db.delete_character(id)
            
            if deleted:
                print(f'''\nCharacter with id {id} has been deleted from the database.
                      \n''')
            else:
                print(f'''\nCharacter with id {id} not found in the database.
                      \n''')
                
        elif character_choice == "5":
            pass
            
# +++++ EXIT +++++     
    elif choice == "6":
        print(f'{BLUE}''''\n
              
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
                    
                    \n'''f'{RESET}')
        break