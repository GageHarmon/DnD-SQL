# Define classes to represent database tables
class Campaigns:
    def __init__(self, id, name, playerset_id, dungeonmaster_id):
        self.id = id
        self.name = name
        self.playerset_id = playerset_id
        self.dungeonmaster_id = dungeonmaster_id
    # def __str__(self):
    #     return f"ID: {self.id} || Name: {self.name} || Playerset ID: {self.playerset_id} || DM ID: {self.dungeonmaster_id}"
    
class DungeonMaster:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __str__(self):
        return f"ID: {self.id} || DM Name: {self.name}"
        
class Playerset:
    def __init__(self, id, player_1_id, player_2_id, player_3_id, player_4_id):
        self.id = id
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id
        self.player_3_id = player_3_id
        self.player_4_id = player_4_id
    
    def __str__(self):
        return f"ID: {self.id} || Player 1: {self.player_1_id} | Player 2: {self.player_2_id} | Player 3: {self.player_3_id} | Player 4: {self.player_4_id}"

class Players:
    def __init__(self, id, name, character_id):
        self.id = id
        self.name = name
        self.character_id = character_id
        
    def __str__(self):
        return f"ID: {self.id} || Player Name: {self.name} | Character ID: {self.character_id}"

class Character:
    def __init__(self, id, name, hp, strength, dexterity, intelligence, charisma, wisdom):
        self.id = id
        self.name = name
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.charisma = charisma
        self.wisdom = wisdom
        
    def __str__(self):
        return f"ID: {self.id} || Name: {self.name} | HP: {self.hp} | Strength: {self.strength} | Dexterity: {self.dexterity} | Intelligence: {self.intelligence} | Charisma: {self.charisma} | Wisdom: {self.wisdom}"