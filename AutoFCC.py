
from pywinauto.application import Application


def start_fcc_meeting(my_name='', conference_id='', conference_pass='', username='User'):

    path_to_exe = f"C:/Users/{username}/AppData/Local/FCC/FreeConferenceCall.exe"

    Application(backend='uia').start(path_to_exe)

    print("Работа потока встречи завершена в штатном режиме")
    exit(0)
