'''
This script uses psutil python module.
I decided to use this module as this is not platform specific
'''


import psutil
import time
import thread



global stop,cpu_percent,io_read,io_write,dic
cpu_percent = []
io_read =[]
io_write = []
#This would allow new statistics to be added to the code without 
#any major changes
dic = {'cpu':cpu_percent,'io-rkbps':io_read,'io-wkbps':io_write}
def monitor(threadName,delay):
        global stop,cpu_percent,io_read,io_write
        while stop != 1:
            #Collect the statistics
            
            #It retruns a namedTuple which is used then get Read/write statistics
            k = psutil.disk_io_counters(perdisk=False)
            #Dividing by thousand to get the Moving average in kiloBytes
            io_read.append(k.read_bytes/1000)
            io_write.append(k.write_bytes/1000)
            j =  psutil.cpu_percent(interval = 0)
            cpu_percent.append(j)
            
            #Sleep for a particular amount of time
            time.sleep(delay)
            

class ResourceMonitor():
    def __init__(self):
        global stop
        stop = 0

     
    def Start(self,delay):
        try:
            thread.start_new_thread(monitor, (self,delay))
            return 'Started collecting statistics'
        except:
            return "Unable to start the thread"
        
        
    # Stop monitoring all resources.

    def Stop(self):
        global stop 
        stop = 1
        return 'Stopped collecting statistics'

    # Get the latest value (moving average) for the statistic 'stat_name'.

    def GetStatistic(self, stat_name):
        global cpu_percent,io_read, io_write, dic
        temp = dic[stat_name]
        sma = sum(temp)/len(temp)
        return sma
        
def main():
    cc = ResourceMonitor()
    r = cc.Start(2)
    print r
    time.sleep(10)
    l = cc.Stop()
    print l
    stat = 'io-wkbps'
    s = cc.GetStatistic(stat)
    print "The simple moving average for {0} is {1}".format(stat,s)
if __name__ == "__main__": main()

