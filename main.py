'''
Программа "Телефонный справочник" для создания, удаления, изменения, поиска контактов в телефонном справочнике(текстовый файл).

Пакет ContactsLib включает в себя классы Contacts и Person для работы с контактами.

Gusev Sergey [https://ev1l.site/]
sergey_gusev_007@mail.ru/titanx@internet.ru
'''

from ContactsLib import Contacts, Person
__author__ = "Gusev Sergey"
try:
    from .version import version
except ImportError:
    version = "0.0.0"

__version__ = version

print("Created by " + __author__)

contacts: Contacts = Contacts("contacts.data")
start_index: int = 0
columns = ["Id", "Фамилия", "Имя", "Отчество", "Название организации", "Рабочий номер", "Личный номер"]
examples = ["Гусев", "Сергей", "Александрович", "Evil", "89379612255", "89379612255"]
size: int = 20


def View(view_contacts = contacts):
	'''Выводит переданный фукнции список
 	Перелистывание реализовано переменной start_index
 	
 	Parameters
        ----------
        view_contacts : list, Contacts
        	Список контактов
	'''
	symbol: str = "_" if (view_contacts == contacts) else "+"
	print(symbol * (len(columns) * 23 - 3))
	for i in range(len(columns)):
		print(columns[i].ljust(20 if i != 0 else 6), end = (" | " if (i != (len(columns) - 1)) else "\n"))
	x: int = 0
	while(x < size):
		if((start_index + x) >= len(view_contacts)):
			break
		person: tuple = view_contacts[start_index + x]
		for i in range(len(columns)):
			if(i == 0):
				if(symbol == "+"):
					data = str(person[-1]).ljust(6)
				else:
					data = str(start_index + x).ljust(6)
			else:
				data: str = person[i - 1].ljust(20)
			print(data, end = " | " if i != (len(columns) - 1) else "\n")
		x += 1
	print(symbol * (len(columns) * 23 - 3))

def Create():
	'''Добавляет контакт в contacts: Contacts
	'''
	global contacts
	data: list[str] = []
	abort_flag: bool = False
	for i in range(1, len(columns)):
		while(True):
			text: str = input("Ввод " + columns[i] + '(пример = "' + examples[i - 1] + '"):')
			if(not text):
				abort_flag = True
				break
			if(Person.check(text, columns[i])):
				data.append(text)
				break
			else:
				print("Введено неверное значение.")
		if(abort_flag):
			break
	if(abort_flag):
		print("Создание отклонено.")
		return False
	contacts.add(Person(*data))
	contacts.save()
	print("Контакт успешно добавлен.")

def Delete():
	'''Удаляет контакт из contacts: Contacts
	'''
	global contacts
	while(True):
		index = input("Введите Id для удаления:")
		if(not index):
			print("Удаление отклонено.")
			break
		try:
			index = int(index)
			if((index >= 0) and (index < len(contacts))):
				contacts.pop(index)
				contacts.save()
				print("Контакт успешно удалён.")
				break
		except Exception as e:
			print("Ошибка при удалении:", e)
		else:
			print("Введено неверное значение.")

def Edit():
	'''Изменяет контакт в contacts: Contacts
 	'''
	global contacts
	while(True):
		index = input("Введите Id для изменения:")
		if(not index):
			print("Изменение отклонено.")
			break
		try:
			index = int(index)
			if((index >= 0) and (index < len(contacts))):
				data: list[str] = list(contacts[index])
				print("Введите пустую строку чтобы пропустить изменение поля.")
				for i in range(1, len(columns)):
					while(True):
						text = input("Введите " + columns[i] + ":")
						if(not text):
							break
						if(Person.check(text, columns[i])):
							data[i - 1] = text
							break
						else:
							print("Введено неверное значение.")
				contacts[index] = data
				contacts.save()
				print("Контакт успешно изменён.")
				break
		except Exception as e:
			print("Ошибка при изменении:", e)
		else:
			print("Введено неверное значение.")

def Search():
	'''Выполняет поиск контактов из contacts: Contacts
	'''
	print("Введите пустую строку если не хотите использовать поле при поиске.")
	data = [""] * (len(columns) - 1)
	for i in range(1, len(columns)):
		while(True):
			text = input("Введите " + columns[i] + ":")
			if(not text):
				break
			if(Person.check(text, columns[i])):
				data[i - 1] = text
				break
			else:
				print("Введено неверное значение.")
	search_contacts: list[tuple] = []
	for x in range(len(contacts)):
		flag: bool = True
		person: tuple[str] = contacts[x]
		for i in range(len(data)):
			if(not data[i] in person[i]):
				flag = False
				break
		if(flag):
			search_contacts.append(person + (x,))
	print("Для выхода из поиска введите пустую строку.")
	while(True):
		View(search_contacts)
		command = input("Поиск:")
		if(command == "след"):
			Next(len(search_contacts))
		elif(command == "пред"):
			Prev()
		elif((not command) or (command == "выход")):
			break
		else:
			print("Введено неверное значение.")

def Next(END: int = len(contacts)):
	'''Перелистывает страницу вперёд
 
 	Parameters
        ----------
        END: int
        	Длина списка(по умолчанию contacts: Contacts)
 	'''
	global start_index
	start_index += size
	start_index = min(start_index , END)
	start_index = start_index // size * size
def Prev():
	'''Перелистывает страницу назад
 	'''
	global start_index
	start_index -= size
	start_index = max(start_index , 0)
	start_index = start_index // size * size

print('Введите "помощь" для просмотра доступных команд.')
while(True):
	View()
	command = input("Команда:")
	if(command == "создать"):
		Create()
	elif(command == "удалить"):
		Delete()
	elif(command == "изменить"):
		Edit()
	elif(command == "поиск"):
		Search()
	elif(command == "след"):
		Next()
	elif(command == "пред"):
		Prev()
	elif(command == "помощь"):
		print('''"помощь" - выводит доступные команды.
"выход" - завершает работу программы.(Также как и ввод пустой строки)
"create" - создаёт новый контакт.
"удалить" - удаляет контакт.
"изменить" - редактирует контакт.
"пред"- перемещает на предыдущую страницу.
"след" - перемещает на следующую страницу.
"поиск" - выполняет поиск контакта.''')
	elif((not command) or (command == "выход")):
		break
	else:
		print("Введено неверное значение.")



