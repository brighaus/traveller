from initiator import Initiator as initiator
import util.datamule as dm
import util.data_config as dc
""" This should allow the user to do the following:
create a service branch by passing a valid dictionary
"""

#Aquire skills and expertise
initiator_obj = initiator()

blob = {'service_name': 'Deleteme',
 'prior_service': {'enlistment_roll': 3,
                   'enlistment_mod_+1_min': ['-', 0],
                   'enlistment_mod_+2_min': ['-', 0],
                   'survival_roll': 5,
                   'survival_mod_+2_min': ['intelligence', 9],
                   'commission_roll': 0,
                   'commission_mod_+1_min': ['-', 0],
                   'promotion_roll': 0,
                   'promotion_mod_+1_min': ['-', 0],
                   'reenlist': 5},
 'ranks': [],
 'mustering_out': {1: ['Low Passage', 0],
                    2: ['inteligence', 1],
                    3: ['education', 1],
                    4: ['Gun', 0],
                    5: ['High Passage', 0],
                    6: ['-', 0],
                    7: ['-', 0]},
 'cash_benefits': {1: 1000,
                   2: 5000,
                   3: 10000,
                   4: 10000,
                   5: 10000,
                   6: 50000,
                   7: 100000},
 'aquired_skills': {'personal_development': {1: ['strength', 1],
                                              2: ['dexterity', 1],
                                              3: ['endurance', 1],
                                              4: ['Blade Combat', 1],
                                              5: ['Brawling', 0],
                                              6: ['socialstatus', -1]},
                    'service_skills': {1: ['Vehicle', 0],
                                       2: ['Gambling', 0],
                                       3: ['Brawling', 0],
                                       4: ['Bribery', 0],
                                       5: ['Blade Combat', 0],
                                       6: ['Gun Combat', 0]},
                    'advanced_education': {1: ['Streetwise', 0],
                                            2: ['Mechanical', 0],
                                            3: ['Electronics', 0],
                                            4: ['Gambling', 0],
                                            5: ['Brawling', 0],
                                            6: ['Forgery', 0]},
                    'advanced_education_2': {1: ['Medical', 0], # requires education 8+
                                             2: ['Forgery', 0],
                                             3: ['Electronics', 0],
                                             4: ['Computer', 0],
                                             5: ['Streetwise', 0],
                                             6: ['Jack-o-Trades', 0]}, 
                    },
  'rank_and_service_skills': {0: ['Streetwise', 0]}
 }

#print('blob:')
#print(blob)

print('pickling blob now...')
print("result:" + str(initiator_obj.create_service_branch(blob)))
print('done')
print('this is what I just dumped:')
dcdbs = dc.DB_TARGETS()

print(dm.fetch_dict(dcdbs.service_branches + blob['service_name'] + '.svc'))

