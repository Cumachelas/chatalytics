import pandas as pd
from datetime import datetime

with open("data/test0.txt", "r", encoding="utf8") as chat:
    
    list_of_lines = []
    
    raw_file = chat.read()
    raw_lines = raw_file.splitlines()

    for raw_line in raw_lines:
        
        raw_strings_list = raw_line.split(" ", maxsplit=4)
        
        try:
            line = {
                "timestamp": datetime.strptime(raw_strings_list[0] + raw_strings_list[1], "%d/%m/%Y,%H:%M"),
                "sender": raw_strings_list[3].strip(":"),
                "message": raw_strings_list[4]
                }
        except ValueError:
            list_of_lines[len(list_of_lines) - 1] = str(list_of_lines[len(list_of_lines) - 1]) + raw_line

        list_of_lines.append(line)
    
    data = pd.DataFrame(list_of_lines)
    print(data)
