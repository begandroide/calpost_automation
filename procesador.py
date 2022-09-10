'''
Automation of execute calpost changing parameters of calpost.template file

RUTA_CALPOST: Absolute path of directory that contains calpost exec file
'''
from datetime import datetime, timedelta
import os
import subprocess

RUTA_CALPOST_EXE = ''
RUTA_CALPOST_INP = ''
RUTA_CALPOST_OUT = ''
MODDATA = ''
PSTLST = ''
PLPATH = ''

'''
Read config from config.xml
'''
def read_config():
    # read config.xml
    config_xml = open('./config.xml', 'r')
    config_str = config_xml.read()

    RUTA_CALPOST_EXE = config_str.split('RUTA_CALPOST_EXE>')[1][:-2]
    RUTA_CALPOST_INP = config_str.split('RUTA_CALPOST_INP>')[1][:-2]
    RUTA_CALPOST_OUT = config_str.split('RUTA_CALPOST_OUT>')[1][:-2]
    MODDATA = config_str.split('MODDATA>')[1][:-2]
    PSTLST = config_str.split('PSTLST>')[1][:-2]
    PLPATH = config_str.split('PLPATH>')[1][:-2]
    print(
        'Config file',
        'RUTA_CALPOST_EXE: ' + RUTA_CALPOST_EXE,
        'RUTA_CALPOST_INP: ' + RUTA_CALPOST_INP,
        'RUTA_CALPOST_OUT: ' + RUTA_CALPOST_OUT,
        'MODDATA: ' + MODDATA,
        'PSTLST: ' + PSTLST,
        'PLPATH: ' + PLPATH,
        sep=' 👽 '
    )

'''
Open template file and replace magic strings
'''
def get_replaced_template(template_objects = dict()):
    # open calpost.template
    template = open('./calpost.template', mode='r')
    template_tmp = template.read()
    template.close()
    for key,val in template_objects.items():
        template_tmp = template_tmp.replace(key, val)
    return template_tmp

'''
Write on disk the new inp file for processing
'''
def write_new_inp_file(template_tmp):
    dir_name = RUTA_CALPOST_OUT + dir_name
    os.mkdir(dir_name)
    new_file = open(RUTA_CALPOST_INP, 'w')
    new_file.write(template_tmp)
    new_file.close()

'''
Tunning variables of calpost.template file and execute processing
'''
def process_day(day, moddata, pstlst, plpath):
    tunam       = day.strftime('%m%d%H')

    start_year  = day.strftime('%Y') # ISYR
    start_month = day.strftime('%m') # ISMO
    start_day   = day.strftime('%d') # ISDY
    start_hour  = day.strftime('%H') # ISHR

    added_day = day + timedelta(hours=1)

    end_year  = added_day.strftime('%Y') # IEYR
    end_month = added_day.strftime('%m') # IEMO
    end_day   = added_day.strftime('%d') # IEDY
    end_hour  = added_day.strftime('%H') # IEHR
    dir_name = day.strftime('%Y%m%d%H')
    template_objects = {
        '%(MODDATA)s': moddata,
        '%(PSTLST)s': pstlst,
        '%(PLPATH)s': plpath,
        '%(DIR_NAME)s': dir_name,
        '%(TUNAM)s': tunam,
        '%(ISYR)s': start_year,
        '%(ISMO)s': start_month,
        '%(ISDY)s': start_day,
        '%(ISHR)s': start_hour,
        '%(IEYR)s': end_year,
        '%(IEMO)s': end_month,
        '%(IEDY)s': end_day,
        '%(IEHR)s': end_hour
    }

    print(template_objects, sep=' - ')
    template_tmp = get_replaced_template(template_objects)
    write_new_inp_file(template_tmp)
    # exec command
    res_exec = subprocess.run([RUTA_CALPOST_EXE, RUTA_CALPOST_INP], capture_output=True)
    print(res_exec)

if __name__ == '__main__':
    try:
        read_config()

        d1 = datetime(2021, 1, 1, 0, 0)
        d2 = datetime(2021, 12, 31, 0, 0)

        # days contains every hour in datetime format from 2021 to 2022 (8761 hours)
        days = [ d1 + timedelta(days=x, hours=h) for x in range((d2 - d1).days + 1) for h in range(0,24) ]
        for day in days:
            process_day(day)
    except Exception as e:
        print ('ERROR: ' + str(e))
        exit()
