import os.path

class lcd:
   
    def lcd_display_string(self, string, line):
        if os.path.exists('l1.txt'):
            if line == 1:
                file = open('l1.txt','w')
            if line == 2:
                file = open('l2.txt','w')
            file.write(string)
            file.close()
        else:
            raise IOError("error")
