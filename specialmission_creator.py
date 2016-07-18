__author__ = 'brighamhausman'

from specialmission_boss import Specialmission_boss
from specialmission import Specialmission

if __name__ == '__main__':
    smb = Specialmission_boss()
    spec_mish_config = {'title':                "Hot Marine Drop",
                        'description':          'Your squadron got abandonded after an emergency jump to avoid an ambush. Now all the ships are low on supplies and need fuel to make the jump back home. Mid-range sensors have detected a rogue mining operation in striking range of our armored troop transports. We need your team to descend through armed defenses in transports small enough to avoid detection. You will get one squadron of S.T.I.N.G Gunners to assist you. Select your best pilots, this one will be hot.',
                        'services':             ['Navy'],
                        'survival_roll':        5,
                        'reward_package':       {'cash':        4000,
                                                 'promotion':   1,
                                                 'skills':   {'Pilot': 1, 'Forward Observer': 1},
                                                 'attributes': {'socialstatus': 1},
                                                 'decorations': ['Gunbarrel Rusher']},
                        'failure_cost':         {'cash':         -1000,
                                                 'attributes':   [['socialstatus', -1]],
                                                 'decorations':  ['Dishonorable behavior. Abandoned ship with considerable supplies from the liquor partition.']},
                        'mission_requirements': {'terms':        3,
                                                 'attributes': {'intelligence': 8},
                                                 'skills': {'Pilot': 0, 'Gunnery': 0}}
    }
    spec_mish = Specialmission(spec_mish_config)
    print('this is spec_mish:')
    print('description:', spec_mish.description)
    print('services:', spec_mish.services)
    print('survival roll:', spec_mish.survival_roll)
    print('title:', spec_mish.title)
    print('rewards:', spec_mish.reward_package)
    print('failure cost:', spec_mish.failure_cost)
    print('mission_requirements:', spec_mish.mission_requirements)
    go = input('enter Y to save mission: ')
    if go == "Y":
        print('saving special mission')
        mish_id = smb.store_mission(spec_mish)
        print('mission id is:', mish_id)
        print('fetching mission from repo...')
        mish_from_repo = smb.get_mission(mish_id)
        print('mission from repo details:', dir(mish_from_repo))
    else:
        print('mission dump aborted')