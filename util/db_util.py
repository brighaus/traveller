__author__ = 'brighamhausman'
"""
Accesses the datamanager to make CRUD manipulations on the db.
+ read db
+ write db
+ get item
+ write item
- update property on item // won't fix. do this in code for now
"""

#!/usr/bin/env python
import sys
import uuid
import pprint

import argparse
import db_config
from data_manager import DataManager
from input_client import Inputclient


class DBUtil:

    __data_manager = DataManager()
    __db_cache = None
    __db_target = None

    def refresh_cache(self):
        self.__db_cache = self.__data_manager.get_cache(shelve_target=self.__db_target)

    def set_db_target(self, target):
        self.__db_target = target
        # reset the local cache
        self.__db_cache = None

    def get_db(self):
        if self.__db_cache is None:
            self.refresh_cache()
        return self.__db_cache

    def write_db(self, repo_data, repo_target, is_append_existing=True):
        #Danger!! dumps repo_data into the repo_target, will silently overwrite
        #   key matches by default
        self.__data_manager.write_db(repo_data, repo_target)

    def get_member(self, id):
        db = self.get_db()
        if id in db:
            return db[id]
        else:
            return None

    def update_member(self, member, id):
        self.__data_manager.update_db_member(member,id, self.__db_target)
        self.refresh_cache()

    def new_member(self, member_data):
        member_id = str(uuid.uuid4())
        # avoid the extremely unlikely event of a dupe ID
        while self.get_member(member_id) is not None:
            member_id = str(uuid.uuid4())
        self.update_member(member_data, member_id)
        return member_id

    def update_member_input(self, id):
        # get db member by id
        member = self.get_member(id)
        # pass member to inputclient
        ic = Inputclient()
        updated_entry_data = ic.get_terminal_input(member)
        # confirm update
        updated_entry = self.format_daily_data(updated_entry_data)
        # return updated db entry or none
        pprint.pprint(updated_entry)
        if self.confirm_update() is True:
            self.update_member(updated_entry, id)
            return id
        else:
            return None


    def confirm_update(self, message='enter Y to save this entry:', match_val='Y'):
        if input(message) == match_val:
            return True
        else:
            return False

def test():
    import random
    import os
    dbu = DBUtil()
    result = []
    # get test db
    dbu.set_db_target(db_config.DB_SHELF_TEST)
    db = dbu.get_db()
    # get keys
    db_keys = list(db.keys())
    # get a single member
    member_id = random.choice(db_keys)
    member = db[member_id]
    result.append('member is {}'.format(str(member)))
    # update a property on a member
    result.append('testing update a member property...')
    updated_value = 'updated value'
    # pick a random property
    member_keys = list(member.keys())
    member_prop = random.choice(member_keys)
    result.append('updated test property key is {}'.format(member_prop))
    result.append('current value of the property to be updated {}'.format(member[member_prop]))
    member[member_prop] = updated_value
    result.append('new value of the property to be updated {}'.format(member[member_prop]))
    # write back to the main db
    dbu.update_member(member,member_id)
    new_member = dbu.get_member(member_id)
    # verify the local cache got the latest version of the db
    result.append('testing {} == {}'.format(new_member[member_prop], updated_value))
    try:
        assert member[member_prop] == updated_value
    except AssertionError:
        result.append('property update test failed')
        return  result
    result.append('asserted {} == {}'.format(member[member_prop], updated_value))

    # write a db to requested db target
    test_db_src = {member_id: member}
    test_db_path = 'test_delete'
    dbu.write_db(test_db_src, test_db_path)
    result.append('wrote db')
    dbu.set_db_target(test_db_path)
    result.append('final db {}'.format(str(dbu.get_db())))
    os.remove(test_db_path)
    return result

def main(argv):

    parser = argparse.ArgumentParser(description='DB CRUD tools')
    # optional arg that sets a default value on the arg. long and short options
    #parser.add_argument('-v', '--verbose', help='make output more verbose',
    #                   action='store_true')
    parser.add_argument('-r', '--readdb', help='gets the db from cache',
                        action='store_true')
    parser.add_argument('-t', '--test', help='execute self test',
                        action='store_true')
    parser.add_argument('-n', '--new', help='enter new database record',
                        action='store_true')
    parser.add_argument('-u', '--update', help='update existing record',
                        action='store_true')
    parser.add_argument('-i', '--id', help='target object id in db')
    parser.add_argument('-td', '--targdb', help='set path to target data src')
    args = parser.parse_args()
    if args.readdb:
        dbu = DBUtil()
        dbu.set_db_target(args.targdb)
        db = dbu.get_db()
        print('db is :' + str(db))
    elif args.test:
        testresult = test()
        for result in testresult:
            print(result)
    elif args.new:
        print('enter new db item not implemented')
        """
        dbu = DBUtil()
        new_entry_id = dbu.enter_item(dictionary_of_kv_pairs)
        if new_entry_id is not None:
            print('entry done')
            print(dbu.get_member(new_entry_id))
        else:
            print('entry not saved')
        """
    elif args.update:
        if args.id:
            targ_id = args.id
            dbu = DBUtil()
            dbu.set_db_target(args.targdb)
            member = dbu.get_member(targ_id)
            print('current member:')
            pprint.pprint(member)
            updated_member_id = dbu.update_member_input(targ_id)
            if updated_member_id is not None:
                print('update complete')
                print(dbu.get_member(updated_member_id))
            else:
                print('no update')
                print(dbu.get_member(targ_id))

        else:
            print('update requires a lookup id')
    elif args.member:
        if args.id:
            targ_id = args.id
            dbu = DBUtil()
            dbu.set_db_target(args.targdb)
            member = dbu.get_member(targ_id)
            print('current member:')
            pprint.pprint(member)
        else:
            print('get member requires a lookup id')

    else:
        print('args' + str(argv))

    return 1

if (__name__ == "__main__"):
    #we call the main function passing a list of args, and exit with the return code passed back.
    sys.exit(main(sys.argv))
