'''Классы для программы "Контакты".

Пакет os помогает проверить наличие файла.

Gusev Sergey [https://ev1l.site/]
sergey_gusev_007@mail.ru/titanx@internet.ru
'''
from os import path
__author__ = "Gusev Sergey"
try:
    from .version import version
except ImportError:
    version = "0.0.0"

__version__ = version

class Person():
	'''
 	Класс Person представляет собой класс контакта.
	
	Attributes
	----------
	surname : str
 	Фамилия
	name : str
 	Имя
	patronymic : str
	Отчество
	organization_name : str
	Название организации
	work_number : str
	Рабочий номер
	personal_number : str
	Личный номер
 
	Methods
	-------
	set_to_line()
 	Соединяет атрибуты объекта с разделителем "|"
	и возвращает результат в виде строки
	get_data()
 	Возвращает кортеж из атрибутов объекта
 	get_from_line(line: str)
  	Разделяет строку разделителем "|" и возвращает Person
  	check(text: str, column: str)
   	Принимает текст и название столбца
    	Возращает True если текст корректен, иначе False
 	'''
	def __init__(self, surname: str, name: str, patronymic: str, organization_name: str, work_number: str, personal_number: str):
		self.name = name
		self.surname = surname
		self.patronymic = patronymic
		self.organization_name = organization_name
		self.work_number = work_number
		self.personal_number = personal_number

	def set_to_line(self) -> str:
		'''Собирает surname, name, patronymic, organization_name,
  		work_number, personal_number в одну строку разделяя знаком "|"
  		'''
		mass = [self.surname,
			self.name,
			self.patronymic,
			self.organization_name,
			self.work_number,
			self.personal_number]
		output = "|".join(map(str,mass))
		return output

	def get_data(self) -> tuple:
		'''Собирает surname, name, patronymic, organization_name,
  		work_number, personal_number в один кортеж
  		'''
		return (self.surname,
			self.name,
			self.patronymic,
			self.organization_name,
			self.work_number,
			self.personal_number)

	def get_from_line(line: str):
		'''Разделяет строку разделителем "|"
  		и возвращает Person

      		Parameters
	        ----------
	        line : str
	        	строка с данными контакта
  		'''
		output = line.split("|")
		return Person(surname = output[0],
			name = output[1],
			patronymic = output[2],
			organization_name = output[3],
			work_number = output[4],
			personal_number = output[5])
	
	def check(text: str, column: str):
		'''Определяет корректен ли текст для столбца

      		Parameters
	        ----------
	        text : str
	        	строка с данными контакта
	  	column : str
    			название столбца
  		'''
		if((not text) or (" " in text)):
			return False
		if("номер" in column):
			if(text.isdigit() and (len(text) == 11)):
				return True
			return False
		else:
			if(text.isalpha()):
				return True
			return False
		return False


class Contacts():
	'''
 	Класс Contacts представляет собой список контактов.
	
	Attributes
	----------
	PATH_TO_FILE : str
 	Путь к файлу с контактами
	array: list[Person] : str
 	Список контактов
	
 
	Methods
	-------
	add(person: Person)
 	Добавляет контакт в список контактов(array)
	__getitem__(item: int)
 	Возвращает данные контакта по индексу item в array
	__setitem__(item: int, value)
 	Записывает в array по индексу item экземпляр Person
  	созданный из value
	__iter__()
 	Возвращает генератор из данных контактов списка array
	__len__()
 	Возвращает длину списка array
	pop(index: int)
 	Удаляет элемент по индексу index в array
	get_data()
 	Собирает строку из строк сгенерированными Person().set_to_line()
	save()
 	сохраняет данные созданные методом Person().get_data
 	'''
	def __init__(self, PATH_TO_FILE: str = ""):
		self.PATH_TO_FILE: str = PATH_TO_FILE
		self.array: list[Person] = []
		if(self.PATH_TO_FILE):
			try:
				if(not path.exists(self.PATH_TO_FILE)):
					with open(self.PATH_TO_FILE,"w") as f:pass
				else:
					with open(self.PATH_TO_FILE,"r") as f:
						for line in f:
							if(line[-1] == "\n"):
								line = line[:-1]
							if(not line):
								continue
							self.add(Person.get_from_line(line))
			except Exception as e:
				print("Ошибка при чтении контактов из файла:", e)
	
	def add(self, person: Person):
		'''Добавляет в список array экземпляр Person

      		Parameters
	        ----------
	        person : Person
	        	Контакт
  		'''
		self.array.append(person)
	
	def __getitem__(self, item: int):
		'''Возвращает кортеж созданный в array[item].get_data()/Person.get_data()
  		
      		Parameters
	        ----------
	        item : int
	        	Индекс контакта в списке
  		'''
		return self.array[item].get_data()
	
	def __setitem__(self, item: int, value):
		'''Добавляет в список array экземпляр Person

      		Parameters
	        ----------
	        item : int
	        	Индекс контакта
	  	value : tuple | list
    			Данные для создание экземпляра класса Person
  		'''
		self.array[item] = Person(*value)
	
	def __iter__(self):
		'''Возвращает генератор из кортежей созданных в Person.get_data()
  		'''
		for person in self.array:
			yield person.get_data()
	
	def __len__(self) -> int:
		'''Возвращает длину списка array
  		'''
		return len(self.array)
	
	def pop(self, index: int):
		'''Удаляет элемент по индексу index в array

      		Parameters
	        ----------
	        index : int
	        	Индекс контакта
	  	'''
		self.array.pop(index)
	
	def get_data(self) -> str:
		'''Возвращает строку из списка array методом person.set_to_line() разделяя элементы символом "\n"
		'''
		data = ""
		for person in self.array:
			data += person.set_to_line() + "\n"
		return data
	
	def save(self):
		'''Сохраняет данные в файл из Contacts().get_data()
  		'''
		try:
			output: str = self.get_data()
			with open(self.PATH_TO_FILE,"w") as file:
				file.write(output)
		except Exception as e:
			print("Ошбика при сохранении контактов в файл:", e)
