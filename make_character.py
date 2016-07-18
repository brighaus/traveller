from util.prettytable import PrettyTable
from pprint import pprint
from character import Character as char
from initiator import Initiator as initiator
import util.datamule


def term(c):
    prompt = input("Another term? Enter: Y/N.")
    if(prompt == 'Y'):
        #check mission here
        mission = initiator_obj.get_mission_status(c)
        if mission is not None:
            # display mission details
            # initiator_obj.show_mission(mission)
            print(c.name, 'is offered a special mission:')
            print('mission title:', mission.title)
            print('mission_description:', mission.description)
            for reward in mission.reward_package:
                print(reward, mission.reward_package[reward])
            # get user choice go or no?
            user_choice = input('send ' + c.name + ' on this mission? Y/N')
            if user_choice == 'Y':
                mission_info = []
                mission_info.append("{} accepts the perilous mission: {}!".format(c.name, mission.title))
                mission_info.append("-------mission outcome------")
                c.update_status(initiator_obj.get_current_service_term_key(), mission_info)
                mission_outcome = initiator_obj.engage_mission(c, mission)

        c = initiator_obj.doterm(c)
        c.show_status()
        if c.isalive is True and c.isretired is False:
            print('current skills set: ' + str(c.get_skills()))
            print('current UUP: ' + str(c.get_chars_map()))
            term(c)
    if prompt == 'N':
        c.isretired = True
    return c


""" This should allow the user to do the following:
1. Roll a character
2. Attempt to enlist
3. Get drafted if enlist fails
4. Go through terms, adding skills, adjusting attrs, modyfing age, etc
5. End up with a character that has an age, history, military/trade
   background and some cash
"""

# TODO: clean up character reference so that c is only used once to
#    build the Initiator
#    all other references point to initiator_obj.get_character()
#initiator_obj = initiator.Initiator(c)
initiator_obj = initiator()

c = char()
print('First we generate a UPP...')
print("The character's UPP hex is: " + c.get_UPP())
print("777777 is the average")
print("UPP represents these characteristics:")
chrs = c.get_chars_map()
for chr in sorted(chrs, key=chrs.get, reverse=True):
    print (chr + ": " + chrs[chr])

c.name = input("What is the Character\'s name?")
# Is this caracter a noble? Social standing ob 'B' or higher
if c.isnoble() is True:
    print('Congratulations! You are born into nobility!')
    print('Please choose an appropriately snooty title:')
    titles = c.get_nobletitles()
    for title in titles:
        print(title + ': ' + titles[title])
    c.nobletitle = input('Enter a title:')

print('Introducing:')
print('HORN FANFARE!!!')
print(c.nobletitle + " " + c.name)

#Aquire skills and expertise


service_branches = initiator_obj.service_branch_list()

print('Options are:')
print('service branches length', len(service_branches))
for service in service_branches:
    service_info = initiator_obj.prior_service_info(service)
    print(service + '--------------')
    service_values = []
    data_titles = []
    service_table = PrettyTable()

    for key in sorted(service_info.keys()):
        data_titles.append(key)
        service_values.append(service_info[key])

    service_table.add_column('Milestone', data_titles)
    service_table.add_column(service, service_values)
    print(service_table)

#note: need to make it easy to eval between char skills and service cost
# display table? get by name?
# how about display best picks based on character traits?
# also what cash, skills, benefits?...

is_first_term = True  # is this the first time in?
is_in_training = True  # are they still alive and not retired?
character_service = None


# first try to enlist
service_name = ''
while len(service_name) == 0 or service_name not in service_branches:
    service_name = input("Pick a service from the list above:")

if initiator_obj.enlist(c, service_name) is True:
    character_service = service_name
else:
    # if that did not work, get drafted
    character_service = initiator_obj.draft(c)
    status_key = initiator_obj.get_current_service_term_key()
    c.status[status_key].append("Entering draft...")
    out = c.name + ' drafted as: ' + character_service
    c.status[status_key].append(out)
    c.isdrafted = True
c.service = character_service
is_first_term = False
c = initiator_obj.doterm(c)
c.show_status()
if c.isalive is True:
    print('current skills set: ' + str(c.get_skills()))
    c = term(c)

if  c.isretired is True and c.isalive is True:
    print('retired!')
    ch = initiator_obj.musterout(c)
    for ln in ch.status['Muster Out']:
        print(ln)



print("Character final stats:")
print('FINAL skills set: ' + str(c.get_skills()))
print('FINAL UUP: ' + str(c.get_chars_map()))
print('FINAL items: ' + str(c.items))
prompt = 'Save this character? Enter Y to save, anything else does nothing.'
dump_char = input(prompt)
if dump_char == 'Y':
    key = initiator_obj.store_character(c)
    print("dumped this character:", key)
    pprint(vars(initiator_obj.get_character(key, c.service)))


#     yes - 4 year term, age +4
#     survive the term?
#     Commission/promotion?
#     get skills and training
# reenlist?
#    yes - do aging check
#    yes - do above enlist /draft steps again
#    no - retirement?
#    no - muster out
