from datetime import datetime
from classes import AddressBook, Record, Birthday, Name, Phone

file_name = "a_book.json"
address_book = AddressBook({})


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except (TypeError, KeyError, ValueError, IndexError) as e: 
            return f"{e} Enter the data correctly"
                    
    return wrapper


input_error
def find_command(*args):
    return address_book.find_data(args[0])


@input_error
def birthday_command(*args):
    name = Name(args[0].capitalize())
    bd = Birthday(args[1])        
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_birthday(bd)        
    else:
        rec = Record(name, birthday=bd)
        address_book.add_record(rec)        
        return f"{name}'s birthday {bd} added"


@input_error
def bd_command(*args):
    name = Name(args[0].capitalize())
    rec: Record = address_book.get(str(name))
    if rec.birthday:
        return rec.days_to_birthday(rec.birthday)
    else:
        return "No birthday record found."


@input_error
def add_command(*args):
    name = Name(args[0].capitalize())
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    else:
        record = Record(name, phone)
        return address_book.add_record(record)
     

@input_error
def change_command(*args): 
    name = Name(args[0].capitalize())
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])  
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"
    

@input_error
def phone_command(*args):    
    name = Name(args[0].capitalize())
    rec: Record = address_book.get(str(name))
    if rec:    
        return f"{rec.name} has phone number {', '.join(str(phone) for phone in rec.phones)}"
    else:
        return f"Name '{name}' was not found"
        
    
def greeting_command(*args):
    return f"How can I help you? \
        \n {help()}"

@input_error
def show_all_command(*args):
    if args:
        count = int(args[0])
    else:
        count = 15
    page = address_book.iterator(count)
    
    while ch := input("Enter any key to browsing (empty to exit): "):
        try:
            result = next(page)
            print("_" * 70)
            print(" {:15} | {:15} | {:60} ".format("name", "birthday", "phones")) 
            print("-" * 70)          
            for record in result:
                phones = ', '.join(str(phone) for phone in record.phones)
                print(" {:<15} | {:<15} | {:<60} ".format(str(record.name),  
                                               str(record.birthday) if record.birthday else "-",
                                               phones))             
        except StopIteration as e:
            return f"The book is over\n"


def exit_command(*args):
    address_book.save_data(file_name)
    return "Good bye!"


def help():
    return "Supported commands\n \
        \nadd name number \
        \nchange name old_number new_number \
        \nphone name \
        \nshow all \
        \nshow all <Number of entries per page> \
        \nbirthday name yyyy-mm-dd \
        \nbd name \
        \nfind name/number \
        \nexit \
        \n"


def no_command(*args):    
    return f"Unknown command. {help()}"


COMMANDS = {
    greeting_command: ("hello", ),
    add_command: ("add", ),
    change_command: ("change", ),
    phone_command: ("phone", ),
    show_all_command: ("show all", ),
    birthday_command: ("birthday", ),    
    bd_command: ("bd", ),
    find_command: ("find", ),
    exit_command: ("good bye", "close", "exit")
}


def parser(text: str):
    for key, value in COMMANDS.items():
        for val in value:
            if text.startswith(val):                                
                return key, text[len(val):].strip().split()
            
    return no_command, ""


def main():
    address_book.load_data(file_name)    
    while True:
        user_input = input(">>>").lower()
        command, data = parser(user_input)
        result = command(*data)
        print(result)

        if result == "Good bye!":
            break
        

if __name__ == "__main__":
    main()
    