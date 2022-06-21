import itertools
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

def prquery(dataframe:pd.DataFrame(), q, filters=[]):
    
    idx = []
    if type(filters) != list:
        filters = [filters]
    
    if filters == []: 
        
        for col in ["message", "sender", "timestamp"]:
            idx.append(dataframe.index[dataframe[col] == q])
            
        log.debug("prquery() - indexing successful (no filters)")  
        
    else:
        
        for f in filters:
            try:
                idx.append(dataframe.index[dataframe[f] == q].tolist())
            except:
                log.error("prquery() - indexing FAILED, filter does not exist")
                return []  
            
        log.debug(f"prquery() - indexing successful (filter: {f})")
        
    return list(itertools.chain(*idx))

def datequery(dataframe:pd.DataFrame(), q, mode="next"):
    
    if mode == "next":
        closest_date = min(dataframe["timestamp"].tolist(), key=lambda d: abs(d - q)) # Get closest date
        matches_indexes = prquery(dataframe, q=closest_date, filters="timestamp") # Get the index
        
        if max(matches_indexes) + 1 > len(dataframe["timestamp"].tolist()) - 1:
            log.warning(f"datequery() - next index out of range (mode: {mode})")
            return max(matches_indexes)
        elif closest_date < q:
            log.debug(f"datequery() - indexing successful (mode: {mode})")
            return max(matches_indexes) + 1
        else:
            log.debug(f"datequery() - indexing successful (mode: {mode})")
            return min(matches_indexes)
        
    elif mode == "previous":
        closest_date = min(dataframe["timestamp"].tolist(), key=lambda d: abs(d - q)) # Get closest date
        matches_indexes = prquery(dataframe, q=closest_date, filters="timestamp") # Get the index
        
        if 0 in matches_indexes:
            log.warning(f"datequery() - previous index out of range (mode: {mode})")
            return 0
        else:
            log.debug(f"datequery() - indexing successful (mode: {mode})")
            return min(matches_indexes)
        
    elif mode == "last":
        closest_date = min(dataframe["timestamp"].tolist(), key=lambda d: abs(d - q)) # Get closest date
        matches_indexes = prquery(dataframe, q=closest_date, filters="timestamp") # Get the index
        
        log.debug(f"datequery() - indexing successful (mode: {mode})")
        
        return min(matches_indexes)
    
    else:
        log.error(f"datequery() - indexing FAILED, mode unknown")
        return
    
def daterange(dataframe, q_start, q_end):
    
    idx0 = datequery(dataframe, q_start, mode="next")
    idx1 = datequery(dataframe, q_end, mode="last")
    
    return dataframe[idx0:idx1]