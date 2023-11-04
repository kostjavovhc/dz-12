from classes import Name, Field, Phone, Record, Birthday, AddressBook


contacts = AddressBook()


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. Use help."
        except KeyError:
            return "Unknown name. Try another or use help."
        except TypeError:
            return "Unknow type. Try another or use help."
        except ValueError:
            return f"{args[1:]} is wrong value. Phone must be 10 numbers, date format - yyyy-mm-dd"
        except NameError:
            return f"{args[0]} is already in DataBook."
        except AttributeError:
            return f"{args[0]} does not exist in DataBook. Use 'add' to add it"
    return inner


@user_error
def add_contact(*args):
    name = args[0].capitalize()
    phone = args[1]
    
    try:
        birthday = args[2]
    except:
        IndexError
        birthday = None

    record = Record(name, birthday)
    record.add_phone(phone)
    contacts.add_record(record)
    return f"{record.name} was succesfully added to Databook"

@user_error
def add_phone(*args):
    name = args[0].capitalize()
    phone_to_add = args[1]
    contacts.find(name).add_phone(phone_to_add)
    return f"New phone added to {name} - {phone_to_add}"


@user_error
def change_phone(*args):
    name = args[0].capitalize()
    old_phone = args[1]
    new_phone = args[2]
    contacts.find(name).edit_phone(old_phone, new_phone)
    return f"{name} has new phone - {new_phone}"


@user_error
def show_num(*arg):
    cap_arg = arg[0].capitalize()
    if cap_arg in contacts.data.keys():
        return f"{cap_arg}'s phones: {contacts[cap_arg].phones}"
    else:
        return f"I don't know {arg}'s number. If you want to add it - print 'add'"
 

@user_error
def greeting_hello():
    return f"Hello!\nI support this commands: {[p for p in COMMANDS.values()]}\nHow can i help you?"


@user_error 
def show_all_nums():
   sorted_data = dict(sorted(contacts.data.items()))
   line = "_"*50 + "\n"
   for p in sorted_data.values():
       line +=  str(p) + "\n"
   return line


@user_error
def days_bd(arg):
    name = arg.capitalize()
    if name in contacts.data.keys():
        rec = contacts[name]
        return rec.days_to_birthday()
    else:
        return f"{name} don`t have a birthday"


@user_error
def show_nums(*args):
    num = int(args[0])
    for res in contacts.iterator(num):
        print("_" * 30)
        return res
    
@user_error
def finder(arg:str):
    find_info = ""
    for contact in contacts:
        rec_str = str(contacts[contact].name).lower() + str(contacts[contact].phones).lower()
        if arg.lower() in rec_str:
            find_info += str(contacts[contact]) + "\n"
        else:
            continue
    return find_info if len(find_info) > 0 else f"No matches with {arg}"


def unknown(*args):
    return "Unknown or not enough params. Try again."


COMMANDS = {add_contact: "add",
            add_phone:"another phone",
            change_phone: "change",
            greeting_hello: "hello",
            show_num: "phone",
            show_all_nums: "show all",
            show_nums: "show nums",
            days_bd: "days bd",
            finder: "find"
            }


def parser(text: str):
    for func, kw in COMMANDS.items():
        if text.lower().startswith(kw):
            return func, text[len(kw):].strip().split()
    return unknown, []


def main():
    try:
        contacts.deserialize("contacts.bin")
    except:
        FileNotFoundError("DataBook does not exist yet")

    print("Type 'Hello' for more info about me")

    while True:
        user_input = input(">>>")
        if user_input.lower() in ["good bye", "close", "exit"]:
            print("Good bye!")
            contacts.serialize("contacts.bin")
            return False
        else:
            func, data = parser(user_input)
            print(func(*data))


if __name__ == '__main__':
    main()
