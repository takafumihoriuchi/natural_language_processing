import os
import time

for i in range(2):
    print("I'm about to be a dad!")
    time.sleep(5)
    pid = os.fork()
    if pid == 0:
        print("I'm process", os.getpid(), ", a newborn that knows to write to the terminal!")
    else:
        print ("I'm the dad of process", pid, ", and he knows to use the terminal!")
        os.waitpid(pid)
