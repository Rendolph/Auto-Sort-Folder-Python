import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime

#place filepath here
folder_path = 'file_path'

#place folder name for created folders here
folder_names = ['folder_name_1', 'folder_name_2', 'folder_name_3', 'folder_name_4']

#assign file type to folder name, must be on the same index
folder_file_types = [['.pdf'], ['.jpg', '.jpeg', '.png', '.gif', '.bmp'], ['.mp4', '.mov', '.wav'], ['.mp3'], ['.exe', '.msi'], ['doc', 'docx', 'xls', 'xlsx']]
now = datetime.now()

def create_folder():
    for folder_name in folder_names:
            folder_path_extended = folder_path + folder_name
            if not(folder_name in make_list_of_files()):
                try: 
                    os.mkdir(folder_path_extended) 
                except OSError as error: 
                    with open(folder_path + "/python_log.txt", "a") as f:
                        print(now.strftime("%d.%m.%Y, %H:%M:%S") + ': ' + error, file=f)

def move_files():
    time.sleep(2)
    for list_of_file in make_list_of_files():
        for index, folder_file_type_list in enumerate(folder_file_types, start=0): 
            for folder_file_type in folder_file_type_list:
                if(folder_file_type in list_of_file):
                    try: 
                        shutil.move((folder_path + list_of_file), (folder_path + folder_names[index] + '/' + list_of_file))
                        with open(folder_path + "/python_log.txt", "a") as f:
                            print(now.strftime("%d.%m.%Y, %H:%M:%S") + ': moved', file=f)
                    except OSError as error: 
                        with open(folder_path + "/python_log.txt", "a") as f:
                            print(now + ': ' + error, file=f)

def make_list_of_files():
    return os.listdir(folder_path)

def on_created(event):
    move_files()

def on_moved(event):
    move_files()

if __name__ == "__main__":
    
    with open(folder_path + "/python_log.txt", "a") as f:
        print(now.strftime("%d.%m.%Y, %H:%M:%S") + ': started', file=f)

    create_folder()
    move_files()

    #create event handler
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_moved = on_moved
    
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, folder_path, recursive=go_recursively)

    #start observer
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()