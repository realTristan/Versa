import base64, random, string, time, shutil, subprocess, os, wmi, platform, psutil, stat, pyautogui
from datetime import datetime

class GlobalFunctions:
    
    # // Function to return hash results string
    def hash_results(self, file: str, fileHash: str, enteredHash: str):
        hashStatus = "Different" if fileHash != enteredHash else "Matching"
        fileStatus = 'Edited' if fileHash != enteredHash else "Not Edited"
        return f'Results:\n\nFile Name: {os.path.normpath(file)}\nFile Hash: {fileHash}\nEntered Hash: {enteredHash}\n\nHash Status: {hashStatus}\nFile Status: {fileStatus}'
    
    # // Check if spoofer active
    def check_spoofer(self, hwid: str):
        if '00000000' in hwid:
            return 'HWID'
        return "None"
    
    # // Function to get the user's hwid
    def get_hwid(self):
        return (subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()).replace("-", "")
    
    # // Function to generate a random string
    def generate_random_string(self, length: int):
        return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    # // Function to base64 encode a string
    def base64_encode(self, s: str):
        return base64.b64encode(s.encode('ascii')).decode('ascii')
        
    # // Create Zip File with all logs
    def create_zip_file(self, main):
        zip_file = f"{main.discorduser}_{main.folder_id}"
        try:
            shutil.make_archive(zip_file, 'zip', f"{main.folder_id}")
            main.cursor.insertText(f"\n[LOG] Successfully ZIPPED Logs | {time.ctime()}\n")
        except Exception:
            main.cursor.insertText(f"\n[LOG] Failed to ZIP Logs | {time.ctime()}\n")
        return zip_file
            
    # // Create Logs file
    def create_logs_file(self, main):
        with open(f"{main.folder_id}/{time.strftime('%Y.%m.%d')}_logs.txt", 'w') as f:
            creation_time = time.ctime(os.path.getctime(f"{main.folder_id}/{time.strftime('%Y.%m.%d')}_logs.txt"))
            f.write(f"[Key / Mouse Logs]\n\nUser: {main.discorduser}\nUser ID: {main.hwid}\nFile Created: {creation_time}\n\n\n")
    
    # // Function to create log file
    def create_log_file(self, main, file_id: str):
        log_file = f"{main.folder_id}/programs_{main.discorduser}_{file_id}.txt"
        if not log_file:
            open(log_file, 'w')
        return log_file
    
    # // Function to hash file data
    def hash_file_data(self, file: str, hasher):
        with open(file, 'rb') as f:
            for byte_block in iter(lambda: f.read(65536), b""):
                hasher.update(byte_block)
        return hasher.hexdigest()
    
    # // Creates new log file and screenshot
    def create_new_log_files(self, main, log_file: str, file_id: str):
        file_name: str = time.strftime("%Y.%m.%d.%H.%M") + f"_{file_id}"
        try:
            # // Create new programs.txt file
            with open(log_file,'w') as f:
                f.write(f'[VAC User/File Information]\n\nUser: {main.discorduser}\nUser ID: {main.hwid}\nFile Code: {file_id}\n\nCreated: {time.ctime(os.path.getctime(log_file))}\nFile Modified: {time.ctime(os.path.getmtime(log_file))}\nCurrent Time: {time.ctime()} | {datetime.now()}\n\n\n[Process List]\n' + '-'*14 + '\n\n' + os.popen(f'wmic process list brief').read() + '\n\n\n[Process Executable Path List]\n' + '-'*31 + '\n\n' + os.popen(f'wmic process get Description,ProcessID,ExecutablePath').read() + '\n\n\n[Process Service List]\n' + '-'*22 + '\n\n' + os.popen(f'wmic service list brief').read())
            
            # // Lock the programs.txt file
            os.chmod(log_file, stat.S_IWRITE); os.chmod(log_file, stat.S_IXUSR) 
            
            # // Create new Screenshot
            pyautogui.screenshot().save(f"{main.folder_id}/{file_name}.png")
            
            # // Send Logs
            main.cursor.insertText(f"\n[LOG] Image/File Saved {file_name} | {time.ctime()}\n")
        except Exception:
            main.cursor.insertText(f"\n[LOG] Error {file_name} | {time.ctime()}\n")
    
    
    # // Function to write detailed specs
    def write_detailed_pc_specs(self, main, file: str, file_id: str):
        with open(file,'w') as f:
            f.write(f'[VAC User/File Information]\n\nUser: {main.discorduser}\nUser ID: {main.hwid}\nFile Code: {file_id}\n\nFile Created: {time.ctime(os.path.getctime(file))}\nFile Modified: {time.ctime(os.path.getmtime(file))}\nCurrent Time: {time.ctime()} | {datetime.now()}\n\n\n' +
f'''
[Computer Specs]
----------------
OS Name: {wmi.WMI().Win32_OperatingSystem()[0].Name.encode('utf-8').split(b'|')[0].decode('utf-8')}
Hardware ID: {main.hwid}
Operating System Version: {platform.version()}
CPU: {wmi.WMI().Win32_Processor()[0].Name}
RAM: {float(wmi.WMI().Win32_OperatingSystem()[0].TotalVisibleMemorySize) / 1048576}GB
Graphics Card: {wmi.WMI().Win32_VideoController()[0].Name}
Total RAM Installed: {round(psutil.virtual_memory().total/1000000000, 2)}GB\n
Available RAM: {round(psutil.virtual_memory().available/1000000000, 2)}GB
Used RAM: {round(psutil.virtual_memory().used/1000000000, 2)}GB
RAM Usage: {psutil.virtual_memory().percent}%
Current CPU Utilization: {psutil.cpu_percent(interval=1)}
Current Per-CPU Utilization: {psutil.cpu_percent(interval=1, percpu=True)}
Current CPU Frequency: {psutil.cpu_freq().current}
Min CPU Frequency: {psutil.cpu_freq().min}
Max CPU Frequency: {psutil.cpu_freq().max}
Number of Physical Cores: {psutil.cpu_count(logical=False)}
Number of Logical Cores: {psutil.cpu_count(logical=True)}
Computer Network Name: {platform.node()}
Machine Type: {platform.machine()}
Processor Type: {platform.processor()}
Platform Type: {platform.platform()}
\n\n
[Running Programs]
------------------
''')
            
            
            
    # // Function to send logs from psutil library (it causes a lag spike)
    def send_psutil_logs(self, main):
        for _ in range(1):
            file_id = self.generate_random_string(3)
            log_file = f"{main.folder_id}/programs_{main.discorduser}_{file_id}.txt"
            if not log_file:
                open(log_file, "w")

            self.write_detailed_pc_specs(main, log_file, file_id)
            for proc_count, proc in enumerate(psutil.process_iter()):
                with open(log_file, 'a') as a:
                    try:
                        a.write(f'\nProcess {proc_count}: {proc.name()}\nProcess ID: {proc.pid}\nProcess Status: {proc.status()}\nProcess Started: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(proc.create_time()))}\nFile Directory: {proc.cwd()}\nExecution Module: {proc.exe()}\n\n')
                    except Exception as err:
                        a.write(f'\nProcess {proc_count}: {proc.name()}\nProcess ID: {proc.pid}\nProcess Status: {proc.status()}\nProcess Started: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(proc.create_time()))}\nError Code: {err}\n\n')
            os.chmod(log_file, stat.S_IWRITE)
            os.chmod(log_file, stat.S_IXUSR)
            return file_id