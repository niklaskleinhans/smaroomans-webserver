import threading 
import ctypes 
import time 
import numpy as np
   
class StopableThread(threading.Thread):
    '''
    A Stopable Thread. For every function you need to define a 
    stopfunction parameter. This function parameter must be your
    stoping criterior. while(not stopfunction())
    @Parameter:
        name: str
        function: function
        args: arguments
    ''' 
    def __init__(self, name, function, args): 
        threading.Thread.__init__(self) 
        self.name = name
        self.function = function
        self._stop = threading.Event()
        self.args = args
    
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
              
    def run(self): 
  
        # target function of the thread class 
        try:
            print('running ' + self.name) 
            self.function(**self.args, stopfunction=self.stopped)
        except Exception as e:
            print(e) 
            print('ended ' + self.name)
        # target function of the thread class 
        finally: 
            print('ended' + self.name) 

   