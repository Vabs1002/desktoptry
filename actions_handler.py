import pyautogui

def perform_action(action_name):
    actions = {
        "screenshot": lambda: pyautogui.screenshot("shot.png"),
        "volume_up": lambda: pyautogui.press("volumeup"),
        "volume_down": lambda: pyautogui.press("volumedown"),
        "mute": lambda: pyautogui.press("volumemute"),
        "brightness_up": lambda: pyautogui.press("brightnessup"),
        "brightness_down": lambda: pyautogui.press("brightnessdown"),
        "alt_f4": lambda: pyautogui.hotkey('alt', 'f4')
    }
    if action_name in actions:
        actions[action_name]()