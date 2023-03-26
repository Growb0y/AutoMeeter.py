
from pywinauto.application import Application
import time


def start_zoom_meeting(my_name='', conference_id='', conference_pass='', username='User'):

    path_to_exe = f"D:/AppData/Zoom/bin/Zoom.exe"
    zoom_win = Application(backend='uia').start(path_to_exe)
    zoom_win.connect(title='Zoom', found_index=0)

    while True:

        try:
            join_btn = zoom_win.Zoom.child_window(title="Войти", control_type="Button").wrapper_object()
            join_btn.click_input()
            join_win = Application(backend='uia').connect(title="Войти в конференцию", timeout=1)
        except:
            join_win = 0
            print("Работа потока встречи завершена в штатном режиме")
            exit(0)

        print('Выполнение операции входа в конференцию...')

        id_box = join_win.ВойтиВКонференцию.child_window(title="Введите ваш идентификатор конференции или имя персональной ссылки", control_type="Edit").wrapper_object()
        id_box.type_keys(conference_id, with_spaces=True)

        name_box = join_win.ВойтиВКонференцию.child_window(title="Введите ваше имя", control_type="Edit").wrapper_object()
        name_box.click_input()
        name_box.type_keys("^a^a^a{BACKSPACE}")
        name_box.type_keys(my_name, with_spaces=True)
        join_btn = join_win.ВойтиВКонференцию.child_window(title="Войти", control_type="Button").wrapper_object()
        join_btn.click_input()

        password_win = Application(backend='uia').connect(title="Введите код доступа конференции", timeout=99)
        password_box = password_win.ВведитеКодДоступаКонференции.child_window(title='Введите код доступа конференции', control_type="Edit").wrapper_object()
        password_box.type_keys(conference_pass, with_spaces=True)
        meeting_join_btn = password_win.ВведитеКодДоступаКонференции.child_window(title='Войти в конференцию', control_type="Button").wrapper_object()
        meeting_join_btn.click_input()

        print("Подключение к конференции...")
        conference_win = Application(backend='uia').connect(title="Zoom Конференция", timeout=900)
        conference_win.ZoomКонференция.wait_not('exists', timeout=99)

        conference_win = Application(backend='uia').connect(title="Zoom Конференция", timeout=99)
        conference_win.ZoomКонференция.wait('exists', timeout=99)
        print("Подключено")

        print("Идёт конференция...")
        conference_win.ZoomКонференция.wait_not('exists', timeout=3000)
        print("Соединение разорвано")
        print('Операция повторного входа в конференцию будет выполнена через 10 секунд')
        time.sleep(10)
