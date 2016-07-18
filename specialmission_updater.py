__author__ = 'brighamhausman'

# takes a mission id, updates the value of the mission and stores it back intot he repo

from specialmission_boss import Specialmission_boss
import pprint


smb = Specialmission_boss()


def update_mission(mish_id):
    mission = smb.get_mission(mish_id)

    mission.mission_requirements = {'attributes': {'intelligence': 8},
                                           'terms': 1}

    print('mission', mish_id, 'details')
    pprint.pprint(vars(mission))

    go = input('enter Y to save changes ')
    if go == 'Y':

        final_id = smb.store_mission(mission, mish_id)

        print('original id', mish_id)

        print('final id', final_id)
    else:
        print('write aborted')


if __name__ == '__main__':
    m_ids = ['3c8c9c5c-ea64-452e-8214-ec922f533196']
    for m in m_ids:
        update_mission(m)