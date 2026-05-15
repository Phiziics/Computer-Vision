import pyautogui


class ComputerController:
    def __init__(self, smoothing=0.25):
        self.screen_width, self.screen_height = pyautogui.size()
        self.smoothing = smoothing
        self.previous_x = 0
        self.previous_y = 0
        self.control_enabled = True

    def move_mouse(self, hand_x, hand_y, camera_width, camera_height):
        if not self.control_enabled:
            return

        screen_x = int(hand_x * self.screen_width / camera_width)
        screen_y = int(hand_y * self.screen_height / camera_height)

        current_x = self.previous_x + (screen_x - self.previous_x) * self.smoothing
        current_y = self.previous_y + (screen_y - self.previous_y) * self.smoothing

        pyautogui.moveTo(current_x, current_y)

        self.previous_x = current_x
        self.previous_y = current_y

    def left_click(self):
        pyautogui.click()

    def right_click(self):
        pyautogui.rightClick()

    def pause_control(self):
        self.control_enabled = False

    def resume_control(self):
        self.control_enabled = True