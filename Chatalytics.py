import logging as log
import pandas as pd
from datetime import datetime

log.basicConfig(filename="cal_main.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S", level=log.DEBUG)

def loadData(filepath:str, fileEncoding:str="utf8", splitFormat:str=None, timestampFormat:str="%d/%m/%Y,%H:%M"):

    try:   
        with open(filepath, "r", encoding=fileEncoding) as chat:
            
            list_of_lines = []
            additional_line_debug = 0
            
            raw_file = chat.read()
            raw_lines = raw_file.splitlines()

            log.debug("loadData() - file read successful, starting convertion")
            
            for raw_line in raw_lines:
                
                raw_strings_list = raw_line.split(" ", maxsplit=4)

                try:
                    ts = datetime.strptime(raw_strings_list[0] + raw_strings_list[1], timestampFormat)
                except (IndexError, ValueError) as e:
                    stripped = list_of_lines[-1]["message"].strip(" ")
                    list_of_lines[-1]["message"] = stripped + " " + raw_line
                    additional_line_debug += 1
                else:
                    line = {
                        "timestamp": ts,
                        "sender": raw_strings_list[3].strip(":"),
                        "message": raw_strings_list[4]
                        }

                    list_of_lines.append(line)
                    
            log.debug(f"loadData() - file read finished with {additional_line_debug} new line checks")
            
            return pd.DataFrame(list_of_lines)
    
    except (FileNotFoundError) as fileHandlingError:
        log.error("loadData() - file read FAILED")
        raise fileHandlingError
    
#def query(dataframe:pd.DataFrame(), viaMessage:str="", viaSender:str="", viaTimestamp:datetime()=datetime.now()):  
    return None