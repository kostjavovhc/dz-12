from collections import UserDict
from datetime import date, datetime
import pickle


class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class Birthday(Field):
    def __init__(self, birthday):
        self._birthday = None
        self.birthday = birthday
    
    @property
    def birthday(self):
        return self._birthday
    
    @birthday.setter
    def birthday(self, birthday) -> datetime:
        if birthday:
            self._birthday = date.fromisoformat(birthday)


class Phone(Field):
    def __init__(self, value):
        self._value = None
        self.value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        if len(str(new_value)) != 10:
            raise ValueError
        if not new_value.isdigit():
            raise ValueError
        self._value = new_value
    

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        if phone not in self.phones:
            self.phones.append(Phone(phone))
        else:
            return f"{phone} is already exist in contact {self.name}"

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == phone:
                self.phones[i] = Phone(new_phone)
                return None
        raise ValueError("This phone phone does not exist")
        
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
            else:
                continue
    
    def days_to_birthday(self):
        today = date.today()
        today_year = today.year
        if self.birthday:
            b = date.fromisoformat(str(self.birthday.birthday))
            b = b.replace(year = today_year)
            if today > b:
                b = b.replace(year = today_year + 1)
            res =  (b - today).days
            return f"It's {res} days to {self.name}'s birthday. Call {self.phones[0]} to greeting!"
        return f"There is no birthday input for {self.name}."

    def __repr__(self):
        if self.birthday.birthday == None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday.birthday}"
    
    def __str__(self):
        if self.birthday.birthday == None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday.birthday}"
    
class AddressBook(UserDict):
    def add_record(self, record:Record):
        if str(record.name) not in self.data.keys():
            self.data[record.name.value] = record
        else:
            raise NameError

    def find(self, find_name) -> Record:
        if find_name in self.data.keys():
            return self.data.get(find_name)
        
    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            return ValueError(f"{name} is not exist")
        
    def iterator(self, n = 2):
        num = 0
        result = '\n'
        for k, v in self.data.items():
            result += f'{v}\n'
            num += 1
            if num >= n:
                yield result
                result = '\n'
                num = 0
        yield result

    def serialize(self, filename):
        sorted_data = dict(sorted(self.data.items()))
        with open(filename, "wb") as file:
            pickle.dump(sorted_data, file)

    def deserialize(self, filename):
        with open(filename, "rb") as file:
            self.data =  pickle.load(file)