class Bot:
    # Line sensors: 0 = black, 1 = white
    s_lineL = True #left
    s_lineR = False #right
    running = True
    
    def line_following_onoff(self):
        if(self.s_lineL and (not self.s_lineR)):
            self.right()
        elif ((not self.s_lineL) and self.s_lineR):
            self.left()
    
    def left(self):
        print("turning left")
    
    def right(self):
        print("turning right")
    
    def run(self):
        while(self.running):
            self.line_following_onoff()


bot1 = Bot()
bot1.run()