from os import path

class Person():
	def __init__(self, surname: str, name: str, patronymic: str, organization_name: str, work_number: str, personal_number: str):
		self.name = name
		self.surname = surname
		self.patronymic = patronymic
		self.organization_name = organization_name
		self.work_number = work_number
		self.personal_number = personal_number

	def set_to_line(self) -> str:
		mass = [self.surname,
			self.name,
			self.patronymic,
			self.organization_name,
			self.work_number,
			self.personal_number]
		output = "|".join(map(str,mass))
		return output

	def get_data(self) -> tuple:
		return (self.surname,
			self.name,
			self.patronymic,
			self.organization_name,
			self.work_number,
			self.personal_number)

	def get_from_line(line: str):
		output = line.split("|")
		return Person(surname = output[0],
			name = output[1],
			patronymic = output[2],
			organization_name = output[3],
			work_number = output[4],
			personal_number = output[5])
	
	def check(text: str, column: str):
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
		self.array.append(person)
	
	def __getitem__(self, item: int):
		return self.array[item].get_data()
	
	def __setitem__(self, item: int, value):
		self.array[item] = Person(*value)
	
	def __iter__(self):
		for person in self.array:
			yield person.get_data()
	
	def __len__(self) -> int:
		return len(self.array)
	
	def pop(self, index: int):
		self.array.pop(index)
	
	def get_data(self) -> str:
		data = ""
		for person in self.array:
			data += person.set_to_line() + "\n"
		return data
	
	def save(self):
		try:
			output: str = self.get_data()
			with open(self.PATH_TO_FILE,"w") as file:
				file.write(output)
		except Exception as e:
			print("Ошбика при сохранении контактов в файл:", e)