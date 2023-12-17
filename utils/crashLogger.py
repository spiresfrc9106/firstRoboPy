
import os
import logging
from datetime import  datetime
import wpilib

from utils.extDriveManager import ExtDriveManager

class CrashLogger():
    
    """
    Python code has many more issues which are caught at runtime. In case one of these happens while on the field, 
    it's important that we record what happened. This class adds an extra logging handle to record these to uniquely
    named log files on the USB drive for later retrieval
    """

    def update(self):
        if(not self.prefixWritten and wpilib.DriverStation.isFMSAttached() and self.isRunning):

            self.logPrint(f"==========================================")
            self.logPrint(f"== FMS Data Received {datetime.now()}:")
            self.logPrint(f"Event: {wpilib.DriverStation.getEventName()}")
            self.logPrint(f"Match Type: {wpilib.DriverStation.getMatchType()}")
            self.logPrint(f"Match Number: {wpilib.DriverStation.getMatchNumber()}")
            self.logPrint(f"Replay Number: {wpilib.DriverStation.getReplayNumber()}")
            self.logPrint(f"Game Message: {wpilib.DriverStation.getGameSpecificMessage()}")
            self.logPrint(f"Cur FPGA Time: {wpilib.Timer.getFPGATimestamp()}")
            self.logPrint(f"==========================================")
            self.prefixWritten = True

    def logPrint(self, msg):
        self.fileHandler.stream.write(msg)
        self.fileHandler.stream.write("\n")
        self.fileHandler.stream.flush()

    def __init__(self):

        self.prefixWritten = False        
        self.isRunning = ExtDriveManager().isConnected()
        
        if(self.isRunning):
        
            # Iterate till we got a unique log name
            idx=0
            uniqueFileFound = False
            logPath = ""
            while(not uniqueFileFound):
                logFileName = f"crashLog_{idx}.log"
                storagePath = ExtDriveManager().getLogStoragePath()
                #TODO-Chris Some debug code sorting out that I didn't have a USB stick that was formated FAT32
                #TODO-why do these print statements come out backwards
                # See: 2023_12_14 20_45_29 Thu.csv from C:\Users\Public\Documents\FRC\Log Files\2023_12_14 20_45_29 Thu.dslog
                # rootLogger.addHandler got fileHandle
                # got logger found unqiue path
                # trying to open /U/logs crashLog_8.log
                # trying to open /U/logs crashLog_7.log
                # trying to open /U/logs crashLog_6.log
                # trying to open /U/logs crashLog_5.log
                # trying to open /U/logs crashLog_4.log
                # trying to open /U/logs crashLog_3.log
                # trying to open /U/logs crashLog_2.log
                # trying to open /U/logs crashLog_1.log
                # trying to open /U/logs crashLog_0.log
                print(f"trying to open {storagePath} {logFileName}",flush=True)
                logPath = os.path.join(storagePath, logFileName)
                uniqueFileFound = not os.path.isfile(logPath)
                idx += 1
            print("found unqiue path",flush=True)
            # Install a custom logger for all errors. This should include stacktraces
            # if the robot crashes on the field.
            logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
            rootLogger = logging.getLogger()
            print("got logger",flush=True)

            self.fileHandler = logging.FileHandler(logPath)
            print("got fileHandle",flush=True)
            self.fileHandler.setFormatter(logFormatter)
            self.fileHandler.setLevel(logging.ERROR)
            rootLogger.addHandler(self.fileHandler)

            print("rootLogger.addHandler",flush=True)
            self.logPrint(f"\n==============================================")
            print("logPrintf", flush=True)
            self.logPrint(f"Beginning of Log {logPath}")
            self.logPrint(f"Started {datetime.now()}")
