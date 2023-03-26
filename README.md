# AutoMeeter.py

## Описание

Приложение предназначено для составления и просмотра расписания предстоящих онлайн-конференций, а также автоматического входа на эти конференции согласно заданному расписанию.

Функционал приложения:
- предоставляет расписание конференций;
- подключается к конференциям в установленное время;
- автоматически обновляет даты периодических конференций в соответствии в заданным интервалом.

Приложение поддерживает работу в фоновом режиме.

Приложение работает со следующими сервисами: Zoom, FreeConferenceCall, Discord.


## Установка

Для запуска приложения последовательно выполните следующие шаги:
1. Скачайте архив с программой из GitHub.
2. Распакуйте архив в папку.
3. В папке, куда был распакован архив с программой, перейдите в каталог \AutoMeeter.py-master\dist.
4. Запустите AutoMeeter.exe.


## Использование

Добавить новую конференцию:

Для добавления новой конференции в расписание нажмите на кнопку "Add new meeting" (снизу в центре).
Строка конференции имеет следующие поля:
  > "My Name" - имя, под которым Вы хотите зайти в конференцию;
  > "ID" - id конференции;
  > "Password" - пароль для входа в конференцию;
  > "Date" - дата конференции;
  > "Time" - время подключения к конференции;
  > "Iterance" - периодичность конференции (в днях);
  > "Platform" - платформа проведения коференции (Zoom, FCC или Discord);
  > "Delete" - кнопка удаления строки конференции.

Создать шаблон конференции:

Новая конференция добавляется в расписание по шаблону, сохраняя значения всех его полей. Чтобы создать шаблон, нажмите на кнопку "Last row to model" (слева снизу). Шаблоном станет нижняя строка расписания.

Сохранить изменения - кнопка "Save" (справа снизу).

Свернуть приложение - красная кнопка (справа вверху).

Закрыть приложение - скрытые значки на панели задач -> правая кнопка мыши по значку "AutoMeeter" -> "Quit".
