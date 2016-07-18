from initiator import Initiator as initiator
from pprint import pprint

"""Super crude but it works for now.
1. Manually set the branch name var
2. run this script
3. at the first pause, copy / paste the dump
   into a python supported text editor
4. track down the prop you want to change and grab the whole dict it's in
5. set the top level prop
6. review the output
7. when ready, don't enter N for the second pause"""

branch_name = input('Enter branch name: ')

svc_mgr = initiator()
svc = svc_mgr.service_data(branch_name)
print('WAS:\n')
#rename a key
# delme = svc['aquired_skills']['advanced_edcuation_2']
# svc['aquired_skills']['advanced_education_2'] = delme
# del svc['aquired_skills']['advanced_edcuation_2']

pprint(svc)

#stomp a dictionary
svc['mustering_out'] = {1: ['Low Passage', 0], 2: ['intelligence', 2], 3: ['education', 2], 4: ['Blade', 0], 5: ['Gun', 0], 6: ['Scout Ship', 0], 7: ['-', 0]}


go = input('Hit enter to continue')

print('------------------------------')
print('------------------------------')
print('WILL BE:\n')

pprint(svc)

go = input('Hit enter to continue, or N to cancel: ')

if go.upper() != 'N':
    svc_mgr.create_service_branch(svc)
    print('Dumped this: ' + str(svc))

else:
    print('dump canceled, no change')
