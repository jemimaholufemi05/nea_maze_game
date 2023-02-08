import time, os
class Timer:
    def start():
        input("press enter to continue and ctrl + C to exit")  
        
        start_time = time.time()
        print("timer has started")
        while True:
            try:
                print("time spent: ",Timer.convert(time.time()-start_time), "secs", end = "\n") 
                time.sleep(1)
                Timer.clear()
            except KeyboardInterrupt:
                print("timer has stopped")
                end_time = time.time()
                print("the time spent: ", round(end_time-start_time, 2), "secs")
                break
        
    def clear():
        os.system('cls')
    
    def convert(secs):
        mins = secs // 60 
        secs = secs % 60 
        hours = mins // 60
        mins = mins % 60 
        return f"{int(hours)}:{int(mins)}:{secs}"
    
    
    
if __name__ == "__main__":
    def main():
        print(Timer.start())

main()