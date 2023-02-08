import time 

  

def start_timer(): 

    start_time = time.time() 

    return start_time 

  

def end_timer(start_time): 

    end_time = time.time() 

    elapsed_time = end_time - start_time 

    print("Elapsed time: ", elapsed_time) 

  

def main(): 

    # start the timer 

    start = start_timer() 

  

    # player moves through the maze here 

    # ... 

  

    # stop the timer 

    end_timer(start) 

  

if __name__ == "__main__": 

    main() 