#Need to all file operation with example detail step by step
import os
#1. Create a file
def create_file():
    with open("/mnt/d/mthree/notes/week4/Day5", "w") as file:
        file.write("Hello, World!")


#2. Write to a file
def write_to_file():
    with open("/mnt/d/mthree/notes/week4/Day5", "w") as file:
        file.write("Hello, World!")

#3. Read from a file
def read_from_file():
    print(os.getcwd())
    with open("/mnt/d/mthree/notes/week4/Day5", "r") as file:
        print(file.read())

#4. Append to a file
def append_to_file():
    with open("/mnt/d/mthree/notes/week4/Day5", "a") as file:
        file.write("Hello, World!")

#5. Delete a file   
def delete_file():
    os.remove("/mnt/d/mthree/notes/week4/Day5")

#6. Check if a file exists
def check_if_file_exists():
    if os.path.exists("/mnt/d/mthree/notes/week4/Day5"):
        print("File exists")
    else:
        print("File does not exist")

#7. Get the current working directory

def get_current_working_directory():
    print(os.getcwd())

#8. List all files in a directory
def list_files_in_directory():
    print(os.listdir())

#9. Get the size of a file
def get_size_of_file():
    print(os.path.getsize("/mnt/d/mthree/notes/week4/Day5"))

#10. Get the last modified time of a file
def get_last_modified_time_of_file():
    print(os.path.getmtime("/mnt/d/mthree/notes/week4/Day5"))

#11. Get the file type
def get_file_type():
    print(os.path.splitext("/mnt/d/mthree/notes/week4/Day5"))

#12. Get the file name
def get_file_name():
    print(os.path.basename("/mnt/d/mthree/notes/week4/Day5"))

#13. Get the file extension
def get_file_extension():
    print(os.path.splitext("/mnt/d/mthree/notes/week4/Day5"))[1]

#14. Get the file path
def get_file_path():
    print(os.path.abspath("/mnt/d/mthree/notes/week4/Day5"))

#15. Get the file directory
def get_file_directory():
    print(os.path.dirname("/mnt/d/mthree/notes/week4/day4"))

if __name__ == "__main__":
    
    create_file()
    write_to_file() 
    read_from_file()
    append_to_file()
    delete_file()
    create_file()
    write_to_file()
    check_if_file_exists()
    get_current_working_directory()
    list_files_in_directory()
    get_size_of_file()
    get_last_modified_time_of_file()
    get_file_type()
    get_file_name()