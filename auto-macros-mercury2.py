import os
import time 
import pyautogui


start_time = time.time() 
while time.time() - start_time < 5:
    x, y = pyautogui.position()
    print(f"Cursor position: {x}, {y}")
print("10 seconds have passed!")




# # Function to open an application by double-clicking its icon
# def open_application(icon_path):
#     # Locate the application icon on the screen
#     icon_location = pyautogui.locateOnScreen(icon_path)
#     if icon_location is None:
#         raise Exception("Application icon not found on the screen.")

#     # Get the center of the icon location
#     icon_center = pyautogui.center(icon_location)
    
#     # Double-click the application icon
#     pyautogui.doubleClick(icon_center)
    
#     # Wait for the application to open
#     time.sleep(2)


# # Function to type text in the application
# def type_in_application(text):
#     # Click on the application window to ensure it is focused
#     pyautogui.click(x=100, y=200)
    
#     # Type the provided text
#     pyautogui.write(text, interval=0.1)


# # Main function
# def main():
#     # Path to the screenshot of the application icon
#     icon_path = "D:\python\python-parser-counter-profile\admintools.png"
    
#     open_application(icon_path)
#     type_in_application("Hello, this is a test message.")


# if __name__ == "__main__":
#     main()