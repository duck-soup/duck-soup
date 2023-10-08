# live update timer in tkinter
# Path: timer.py

# import the tkinter module
import tkinter as tk

# create a window
window = tk.Tk()
window.title("Timer")
window.geometry("75x110")
# color the window with a sepia color
window.config(bg="#f5e9d3")
# create a label to show the time
time_label = tk.Label(window, text="25:00", font=("Monospace", 25), fg="black", bg="#f5e9d3")
time_label.grid(row=0, column=0, columnspan=3)

# create a function to start the timer
def start_timer():
    reset = False
    def reset_timer():
        # reset the time label
        time_label["text"] = "25:00"
        reset = True

        # create a reset button
    reset_button = tk.Button(window, text="Reset", font=("Monospace", 10), fg="black", bg="#f5e9d3", command=reset_timer)
    reset_button.grid(row=2, column=0, sticky="w")
    
    if not reset:
        # get the time from the label
        time = time_label["text"]
        # split the time into minutes and seconds
        minutes, seconds = time.split(":")
        # convert the minutes and seconds to integers
        minutes = int(minutes)
        seconds = int(seconds)
        # check if the seconds are 0
        if seconds == 0:
            # check if the minutes are 0
            if minutes == 0:
                # stop the timer
                return
            # decrement the minutes by 1
            minutes -= 1
            # set the seconds to 59
            seconds = 59
        # decrement the seconds by 1
        else:
            seconds -= 1
            
        # format the time
        time = f"{minutes:02d}:{seconds:02d}"
        # update the time label
        time_label["text"] = time
        # call the function again after 1 second
        window.after(1000, start_timer)

# create a button to start the timer
start_timer_button = tk.Button(window, text="Start", command=start_timer)
start_timer_button.grid(row=1, column=0)



# start the main loop
window.mainloop()
