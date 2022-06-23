import logging as log
import pandas as pd
import time

log.basicConfig(filename="logs/engine_main.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S", level=log.INFO)

def loadData(filepath:str, fileEncoding:str="utf8", splitFormat:str=None, timestampFormat:str="%d/%m/%Y,%H:%M"):

    start_time_debug = time.process_time()
    
    try:
        with open(filepath, "r", encoding=fileEncoding) as chat:
            
            list_of_lines = []
            additional_line_debug = 0
            
            raw_file = chat.read()
            raw_lines = raw_file.splitlines()

            log.info("loadData() - file read successful, starting convertion")
            
            for raw_line in raw_lines:
                
                raw_strings_list = raw_line.split(" ", maxsplit=4)
                
                try:
                    pd_ts = pd.to_datetime(raw_strings_list[0] + raw_strings_list[1], format=timestampFormat, infer_datetime_format=True)
                except (IndexError, ValueError) as e:
                    stripped = list_of_lines[-1]["message"].strip(" ")
                    list_of_lines[-1]["message"] = stripped + " " + raw_line
                    additional_line_debug += 1
                else:
                    line = {
                        "pd_timestamp": pd_ts,
                        "index": len(list_of_lines),
                        "date": pd_ts.date(),
                        "sender": raw_strings_list[3].strip(":"),
                        "media": False,
                        "message": raw_strings_list[4]
                        }
                    
                    if raw_strings_list[4] == "<Media omitted>":
                        line["media"] = True

                    list_of_lines.append(line)
                    
            log.info(f"loadData() - file read finished in {time.process_time() - start_time_debug}s with {additional_line_debug} new line checks")
            
            df = pd.DataFrame(list_of_lines)
            return df.set_index(["timestamp"])
    
    except (FileNotFoundError) as fileHandlingError:
        log.error("loadData() - file read FAILED")
        raise fileHandlingError

#def countMsg(df:pd.DataFrame(), date:pd.Timestamp(), duration:pd.Timedelta()=pd.Timedelta(days=1)):
    
    n = len(df.loc[date:date + duration])