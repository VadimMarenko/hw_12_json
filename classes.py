from datetime import datetime
from collections import UserDict
import json



class Field():
    def __init__(self, value=None):
        self.__value = None
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)    
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if value:
            self.__value = value
        
class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = Phone.__test_phone(value)        

    @staticmethod
    def __test_phone(value):
        if value:
            if value.startswith("+"):
                value = value[1:]
            
            if value.isdigit():
                return value
            else:
                raise ValueError("Phone must be a number.")
        else:            
            raise ValueError("Enter phone number.")


class Birthday(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = Birthday.__test_date(value)
           
    @staticmethod
    def __test_date(value):
        if value:
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()                
            except ValueError as e:
                raise ValueError(f"{e} \nPlease enter the date in the format dd-mm-yyyy.")
        else:
            raise TypeError("Please enter birthday.")

class Record():
    def __init__(self, name:Name, phone: Phone=None, birthday: Birthday=None):
        self.name = name        
        self.phones = []
        self.birthday = birthday        
        if phone:
            self.add_phone(phone)

    def __str__(self):
        return f"{str(self.name).lower()}  {', '.join(str(phone) for phone in self.phones)}  {str(self.birthday) if self.birthday else ''}"
        
    def __repr__(self):
        return f"{self.name}: [{', '.join(str(phone) for phone in self.phones)}]"
        #return f"{str(self.name).lower()}  {', '.join(str(phone) for phone in self.phones)}  {str(self.birthday) if self.birthday else ''}"
        
        
    def add_phone(self, phone: Phone):
        if phone.value not in [phone.value for phone in self.phones]:
            self.phones.append(phone)
            return f"Phone {phone} add to contact {self.name}"
        return f"Phone {phone} present in phones of contact {self.name}"

    def delete_phone(self, phone):
        for item in self.phones:
            if item.value == phone.value:
                self.phones.remove(item)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        self.delete_phone(old_phone)
        self.phones.append(new_phone)
        return f"phone {old_phone} was replaced by {new_phone}"
    
    def add_birthday(self, birthday: Birthday):
        if self.birthday:
            return f"The contact {self.name} contains a birthday {self.birthday}"
        
        else:
            self.birthday = birthday
            return f"Birthday {self.birthday} add to contact {self.name}"

    
    def days_to_birthday(self, birthday):
        date_now = datetime.now().date()
        date_bd = birthday.value.replace(year=date_now.year)
        if date_bd >= date_now:            
            result = date_bd - date_now
        else:
            date_bd = birthday.value.replace(year=date_now.year + 1)
            result = date_bd - date_now
        return f"{self.name}'s birthday will be in {result.days} days"


class AddressBook(UserDict):    
    def add_record(self, record: Record):
        if record.name.value not in self.keys():
            self.data[record.name.value] = record 
            return f"Added {record.name.value} with phone number {', '.join(str(phone) for phone in record.phones)}"
        else:            
            return f"Record {record.name.value} alredy exists"
    

    def iterator(self, group_size):
        records = list(self.data.values())
        self.current_index = 0

        while self.current_index < len(records):
            group_items = records[self.current_index:self.current_index + group_size]
            group = [rec for rec in group_items]
            self.current_index += group_size
            yield group

        
    def save_data(self, filename):
        with open(filename, 'w') as f:
            json.dump({str(record.name): (','.join(str(phone) for phone in record.phones), (str(record.birthday) if record.birthday else "")) for name, record in self.items()}, f)
        return f"The address_book is saved."

    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                data_dict = json.load(f)
                for key, value in data_dict.items():
                    name = Name(key)
                    phones_data, birthday = value[:-1], value[-1]

                    if birthday: 
                        birth_day = True 
                    else:   
                        birth_day = False

                    phones = []
                    for i in phones_data:
                        if i.find(',') > 0: 
                            phones_lst = i.split(',') 
                            for p in phones_lst:
                                phones.append(Phone(p)) 
                        if phones:
                            continue
                        else:
                            phones.append(Phone(i))
                    if birth_day:
                        record = Record(name, birthday=Birthday(birthday))
                    else:
                        record = Record(name)   
                    record.phones = phones
                    self.data[record.name.value] = record
                    
            if isinstance(self.data, dict):
                print(f"The address_book is loaded.")
            else:
                print("The file does not contain a valid address_book.")
        except FileNotFoundError as e:
            print(f"{e}")

        
        
    def find_data(self, fragment:str):
        count = 0
        result = ""
        for rec in self.values():                
            line = str(rec) + "\n"            
            if fragment in line:
                result += line
                count += 1
        if result:
            result = f"The following {str(count)} records were found on the fragment '{fragment}' \n\n" + result
        else:
            result = f"No records was found for the fragment '{fragment}' \n"
        return result    