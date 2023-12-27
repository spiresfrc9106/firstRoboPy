import wpilib

from utils.signalLogging import log
from utils.singleton import Singleton

# Utilties for tracking how long certain chunks of code take
# including logging overall loop execution time
class SegmentTimeTracker(metaclass=Singleton):
    def __init__(self):
        self.longLoopThresh = 0.003
        self.tracer = wpilib.Tracer()
        self.loopStartTime = wpilib.Timer.getFPGATimestamp()
        self.loopEndTime = wpilib.Timer.getFPGATimestamp()
        self.prevLoopStartTime = self.loopStartTime
        self.curPeriod = 0
        self.curLoopExecDur = 0
        self.numOverRuns = 0
        self.numLoops = 0

    def start(self):
        self.tracer.clearEpochs()
        self.prevLoopStartTime = self.loopStartTime
        self.loopStartTime = wpilib.Timer.getFPGATimestamp()
        self.curPeriod = self.loopStartTime - self.prevLoopStartTime
        log("LoopPeriod", self.curPeriod * 1000.0, "ms")

        
    def mark(self, name):
        self.tracer.addEpoch(name)
        
    def end(self):
        self.loopEndTime = wpilib.Timer.getFPGATimestamp()
        self.curLoopExecDur = self.loopEndTime - self.loopStartTime
        self.numLoops += 1
        if(self.curLoopExecDur > self.longLoopThresh):
            self.numOverRuns += 1
            self.tracer.printEpochs()
        log("LoopDuration", self.curLoopExecDur * 1000.0, "ms")
        log("LoopEndTime", self.loopEndTime*1000.0, "ms")
        log("LoopCount", self.numLoops, "count")
        log("LoopOverRunCount", self.numOverRuns, "count")
