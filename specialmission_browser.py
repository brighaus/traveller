__author__ = 'brighamhausman'

from specialmission_boss import Specialmission_boss

if __name__ == '__main__':
    smb = Specialmission_boss()
    missions = smb.mission_cache
    for m in missions:
        svcs = 'Any'
        mission = missions[m]
        if len(mission.services) > 0:
            svcs = ''
            for svc in mission.services:
                svcs += svc + ', '

        print(mission.title, m, sep=' :: ')
        print('eligible services:', svcs)
        print('\t' + mission.description)
        print('=========(*Y*)=========')
