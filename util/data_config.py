__author__ = 'brighamhausman'
import glob

LOG_PATH = './traveller.log'
character_dir = 'data/characters'
character_dbs = glob.glob(character_dir + "/*_DB")
character_db_targets = {}
for db in character_dbs:
    # characters/Army_DB
    # separate db name from file path
    db_name = db.split('/')[-1]
    #separate the '_DB' extension from the file name
    db_name = db_name.split('_')[0]
    db_name = db_name.lower()
    character_db_targets[db_name] = db

class DB_TARGETS:
    def __init__(self):
        self.data_dir = "data/"
        self.characters = self.data_dir + "characters/"
        self.character_dbs = character_db_targets
        #ref to directory
        self.mission_data_dir = self.data_dir + "special_missions/"
        # ref to bytecode
        self.missions = self.mission_data_dir + "special_missions"
        self.service_branches = self.data_dir + "service_branches/"

def show_db_targets():
    print(DB_TARGETS)

def runtest():
    print('showing db targets')
    show_db_targets()

if __name__ == '__main__':
    runtest()