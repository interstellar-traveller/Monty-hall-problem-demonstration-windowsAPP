from drawingpanel import *
from tkinter import *
import math
import random

class Montyhall(object):
    
    def __init__(self):
        # defining the playground
        self.panel = DrawingPanel(800, 600, background="#252526")
        self.canvas = self.panel.canvas
        self.panel.title("Monty Hall Problem")
        self.screenwidth = self.panel.winfo_screenwidth()  # 屏幕宽度
        self.screenheight = self.panel.winfo_screenheight()  # 屏幕高度
        self.width = 800
        self.height = 600
        self.x = int((self.screenwidth - self.width) / 2)
        self.y = int((self.screenheight - self.height) / 2)
        self.panel.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        
        # defining the control buttons and the input box
        self.start = self.new_button(self.panel, 'Start', 
                       '#434344', '#DCBA6D', 
                       '#535355', '#DCBA6D', 
                       'flat', 
                       1, 1, 8, 1, 3, 
                       'normal', 'arrow', ('ariel', 20), self.START)
        self.stop = self.new_button(self.panel, 'Stop', 
                       '#434344', '#DCBA6D', 
                       '#535355', '#DCBA6D', 
                       'flat', 
                       1, 1, 8, 1, 3, 
                       'normal', 'arrow', ('ariel', 20), self.STOP)
        self.restart = self.new_button(self.panel, 'Restart', 
                       '#434344', '#DCBA6D', 
                       '#535355', '#DCBA6D', 
                       'flat', 
                       1, 1, 8, 1, 3, 
                       'normal', 'exchange', ('ariel', 20), self.RESTART)
        self.start_window = self.canvas.create_window(120,100,anchor=NW, window=self.start)
        self.stop_window = self.canvas.create_window(340, 100, anchor=NW, window=self.stop)
        self.restart_window = self.canvas.create_window(560, 100, anchor=NW, window=self.restart)
        self.entry = Entry(self.canvas)
        self.canvas.create_text(400, 330, text="Speed Control Panel", fill="#4EBD84")
        self.canvas.create_text(400, 350, text="(100000 to initiate quick run)", fill="#4EBD84")
        self.canvas.create_window(400, 300, window=self.entry, width=60)
        
        # defining the control values of the controlling logic
        self.pause = True
        
        self.door_num = [1, 2, 3]
        self.random_door = 1
        self.goat_door = 2
        self.remain_door = 3
        self.car_door = 0
        self.get_car = 'You got the car! Congrats!'
        self.get_goat = 'Goat appears: Miee.ee...ee...'     
        self.stageDict = {
            'start': 'Choose a door!',
            'choose': f'Door {self.random_door} is chosen.',
            'open': f'Door {self.goat_door}, with a goat behind it, is opened.',
            'decide': 'Do you want to change a door?',
            'keep': 'No, keep.',
            'change': 'Yes, change a door.',
            'car': f'{self.get_car}',
            'goat': f'{self.get_goat}'
        }
        self.stages = ['start', 'choose', 'open', 'decide', 'keep', 'change', 'car', 'goat']
        self.stage_control = 0
        
        self.sum_count = 0
        self.keep_count = 0
        self.keep_car_count = 0
        self.change_count = 0
        self.change_car_count = 0
        
        self.display_num = 0
        self.display_count = 0
        self.loop_speed = self.default(self.entry.get())
        
        self.exit = False
        

    def START(self):
        self.pause = False

    def STOP(self):
        self.pause = True

    def RESTART(self):
        self.STOP()
        self.stage_control = 0
        self.sum_count = 0
        self.keep_count = 0
        self.keep_car_count = 0
        self.change_count = 0
        self.change_car_count = 0

    def new_button(self, master, text, bg, fg, acbg, acfg, 
                   relief, bd, height, width, padx, 
                   pady, state, cursor, font, command):
        button = Button(master=master, text=text, bg=bg, fg=fg, activebackground=acbg, activeforeground=acfg, 
                      relief=relief, bd=bd, height=height, width=width, padx=padx, 
                      pady=pady, state=state, cursor=cursor, font=font, command=command)
        return button

    def display(self):
        while not self.exit:
            self.door_num = [1, 2, 3]
            random.shuffle(self.door_num)
            self.car_door = self.door_num[random.randint(0,2)]
            self.random_door = self.door_num[0]
            if self.car_door == 1:
                self.goat_door = self.door_num[2]
                self.remain_door = self.door_num[1]
            elif self.car_door == 0:
                self.goat_door = random.randint(1,2)
                self.remain_door = self.door_num[3-self.goat_door]
            else:
                self.goat_door = self.door_num[1]
                self.remain_door = self.door_num[2]
            self.refresh_stage_dict()
            while self.stage_control < len(self.stages):
                self.canvas.create_text(400, 330, text="Speed Control Panel", fill="#4EBD84", font=('ariel', 15))
                self.canvas.create_text(400, 350, text="(100000 to initiate quick run)", fill="#4EBD84")
                self.loop_speed = self.default(self.entry.get())
                self.display_num = (60 / self.loop_speed) / 6 / 0.0001
                if self.loop_speed <= 99999:
                    self.canvas.create_text(400,230,text=self.stageDict[self.stages[self.stage_control]], fill='#9CDCFE', font=('ariel', 28))
                    if self.display_count >= self.display_num:
                        if self.stage_control == 3:
                            choice = random.randint(4,5)
                            if choice == 5:
                                self.random_door, self.remain_door = self.remain_door, self.random_door
                                self.change_count += 1
                                self.stage_control += 2
                            else:
                                self.keep_count += 1
                                self.stage_control += 1
                        elif self.stage_control == 4:
                            if self.random_door == self.car_door:
                                self.keep_car_count += 1
                                self.stage_control += 2
                            else:
                                self.stage_control += 3
                        elif self.stage_control == 5:
                            if self.random_door == self.car_door:
                                self.change_car_count += 1
                                self.stage_control += 1
                            else:
                                self.stage_control += 2
                        else:
                            self.stage_control += 1
                        self.display_count = 0
                    self.panel.sleep(0.1)
                    self.panel.clear()
                    if not self.pause:
                        self.display_count += 1
                else:
                    door = [1, 2, 3]
                    random.shuffle(door)
                    car = door[random.randint(0,2)]
                    rand = door[0]
                    if not self.pause:
                        self.canvas.create_text(400,230,text='Processing...', fill='#9CDCFE', font=('ariel', 28))
                        if car == door[1]:
                            goat = door[2]
                            remain = door[1]
                        elif car == door[0]:
                            goat = door[random.randint(1,2)]
                            remain = door[3-door.index(goat)]
                        else:
                            goat = door[1]
                            remain = door[2]
                        change = random.randint(0,1)
                        if change == 0:
                            rand, remain = remain, rand
                            self.change_count += 1
                            if rand == car:
                                self.change_car_count += 1
                        else:
                            self.keep_count += 1
                            if rand == car:
                                self.keep_car_count += 1
                    else:
                        self.canvas.create_text(400,240,text='Paused...', fill='#9CDCFE', font=('ariel', 28))

                    self.panel.sleep(50)
                    self.panel.clear()
                    self.stage_control = len(self.stages) + 1
                self.canvas.create_text(250,400,text="stay:", fill='#B5CEA8', font=('ariel', 24))        
                self.canvas.create_text(250,450,text=f"{self.keep_car_count} / {self.keep_count}", fill='#B5CEA8', font=('ariel', 24))
                self.keep_rate = (self.keep_car_count / self.keep_count) if self.keep_count != 0 else 0
                self.canvas.create_text(250,500,text=f"{'%.4f' % self.keep_rate}", fill='#B5CEA8', font=('ariel', 24))
                
                self.canvas.create_text(550,400,text="change:", fill='#B5CEA8', font=('ariel', 24))
                self.canvas.create_text(550,450,text=f"{self.change_car_count} / {self.change_count}", fill='#B5CEA8', font=('ariel', 24))
                self.change_rate = self.change_car_count / self.change_count if self.change_count != 0 else 0
                self.canvas.create_text(550,500,text=f"{'%.4f' % self.change_rate}", fill='#B5CEA8', font=('ariel', 24))

            self.stage_control = 0
            # self.panel.sleep(10)
            
    def default(self, input):
        try:
            if len(input) == 0:
                return 30000
            input = int(input)
            if input == 0:
                return 30000
            return input
        except ValueError:
            return 30000
        
    def refresh_stage_dict(self):
        self.stageDict = {
            'start': 'Choose a door!',
            'choose': f'Door {self.random_door} is chosen.',
            'open': f'Door {self.goat_door}, with a goat behind it, is opened.',
            'decide': 'Do you want to change a door?',
            'keep': 'No, keep.',
            'change': 'Yes, change a door.',
            'car': f'{self.get_car}',
            'goat': f'{self.get_goat}'
        }
    
    def main(self):
        self.display()
        self.panel.mainloop()
        
demo = Montyhall()
demo.main()