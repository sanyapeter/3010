from helper_functions import camera, computer_vision,sensehat
import time
import os

def main():
    
    camera_i = camera.get_camera() #DO NOT MODIFY, function call must work as is 
    sense = sensehat.get_sensehat() #DO NOT MODIFY, function call must 
    #TO-DO: Should be a user input
    take_background_image = input("Do you want to take a new background image? (y/n): ").strip().lower() == "y"
   
    if take_background_image:
        ### TO-DO: Countdown image capture of background  
        countdown = int(input("Enter countdown time before capturing (seconds): "))
        preview = input("Enable preview? (y/n): ").strip().lower() == "y"
        print("Move out of the camera view. Capturing in:")
        for i in range(countdown, -1, -1):
            print(i)
            time.sleep(1)
            print("\nCapturing background image...")        
        preview = False
        countdown=0
        camera.capture_image(camera_i,"data/images/background.jpg", countdown_time=countdown, preview=preview) #DO NOT MODIFY, function call must work as is 
    
    arm_system = True #TO-DO: Should be a user input

    if arm_system:
        interval = int(input("Enter monitoring interval (seconds): "))
        t1 = int(input("Enter detection threshold t1 (e.g. 40): "))
        
        ### TO-DO: Countdown to monitoring
    
        print("Monitoring will begin in 5 seconds:")
        for i in range(5, -1, -1):
            print(i)
            time.sleep(1)
        print("\nSystem armed. Monitoring for movement...")
       


        count = 0
        while True: #DO NOT MODIFY, function call must work as is 
            camera.capture_image(camera_i,"data/images/image%s.jpg" % count, countdown_time=interval) #DO NOT MODIFY, function call must work as is 
            person_detected = computer_vision.person_detected("data/images/background.jpg","data/images/image%s.jpg" % count, t1)  #DO NOT MODIFY, function call must work as is 
            if person_detected: #DO NOT MODIFY, function call must work as is 
                print("Person Detected") #DO NOT MODIFY, function call must work as is 
                sensehat.alarm(sense,interval)  #DO NOT MODIFY, function call must work as is 
            else:
                print("No Person Detected") #DO NOT MODIFY, function call must work as is 
            count += 1


if __name__ == "__main__":
    main()
