# Little Application for collecting username and password and encrypting it for the
# USB-Duckie Keys
# Author: R. Sanford
# Date created: 26 march 2019
# Date finished: <HAHA! Never>

import tkinter as tk
from tkinter import Grid, filedialog, messagebox
#import PIL
from PIL import Image, ImageTk
from pathlib import Path
from random import randrange

class Loginer(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master) # root


        self.feilds()

        # configure the first column to have a flexible width
        master.grid_columnconfigure(index=1, weight=1, minsize=98)
        master.title('USB Key Configurator')

    def feilds(self):
        # Label & instructions
        inst="Please enter the username and password to be written to the USB Key.\nYou will then be asked to find the CIRCUITPY drive"
        self.instruct=tk.Label(text=inst)
        self.instruct.grid(row=0,column=0, columnspan=3, sticky='news', padx=3, pady=6)

        #username Label
        self.usernameLab=tk.Label(text='Username:', padx=1, pady=7)
        self.usernameLab.grid(row=1,column=0)
        # username entry
        self.username=tk.Entry(width=46)
        self.username.grid(row=1, column=1, sticky="ew", padx=5, columnspan=2)

        #pasword Label
        self.passwordLab=tk.Label(text='Password:', padx=1, pady=7)
        self.passwordLab.grid(row=2, column=0)
        # password entry
        self.password=tk.Entry(width=46, show=".")
        self.password.bind('<Return>', self.writeToDuckie)
        self.password.grid(row=2, column=1, sticky="ew", padx=5, columnspan=2)

        # modulus label
        self.modulusLab =  tk.Label(text='Modulus:', padx=1, pady=7)
        self.modulusLab.grid(row=3, column=0)
        # modulus setting
        randMod = randrange(2, 1024, 2) # random modulus for each run
        self.modulus = tk.Spinbox(from_=0, to_=1024, increment_=2, width=10)
        self.modulus['textvariable'] = tk.DoubleVar(value=randMod)
        self.modulus.grid(row=3, column=1, sticky='w')


        # Generate button
        self.gen=tk.Button(text="Build Key", command=self.writeToDuckie)
        self.gen.grid(row=3, column=2, columnspan=1, sticky='e')

    def writeDialog(self, document):
        # open a file dialog and navigate to the CIRCUITPY device
        # then it will write the improved lib/bfd.py
        path=filedialog.askdirectory(initialdir="shell:MyComputerFolder", title="Please Find CIRCUITPY")

        #print(path)
        # wrote the new user and pass to the python lib
        if len(path) > 0:
            with open(path+"lib/bfd.py", 'wb') as final:
                final.write(document.encode('utf8'))
                final.close()
        else:
            print('Don\'t do things')



    def writeToDuckie(self, event=None):
        print("Write to duckie")

        # get the Password
        uname=self.username.get()
        pss=self.password.get()

        #the word that will end up on the device
        word=" "+uname+'\t'+pss+'\n'

        # encode to a "safe" format
        binval=self.str2enc(word)
        # now remove the Username adn Password from memory
        uname="j$bnb8)786t2bnv^Tklhtw\t!^,kbvhjce5ou7s^k\';lbvgefbvRmkhjvg\npodFYUc\tdbey6HVvc5ekyv%\n$f"
        pss="kliawef]a\sf09754hlakjc6903\t;hvy6g4ela\';alhv12*534$#i76jikCDHRTik337u54\"$75r96tfvgkjdu"

        # convert the encoded values into a python script that returns the values
        doc="def pws():\n\tg=%s\n\tmod=%s\treturn g, mod"%(str(binval), self.modulus.get())
        #print(doc)

        self.writeDialog(doc)

        messagebox.showinfo("Success?", "No errors occured during write,\nso you should be good to go...")

    def str2enc(self, str):
        # convert the sensitave string to an encoded value
        vals=[]
        gals=[]
        mod = int(self.modulus.get())
        for ch in str:
            gals.append(ord(ch))
            vals.append((ord(ch)*2)-mod)
        #print(vals)
        #print(gals)

        return vals

def run():
    # start the TK window
    root=tk.Tk()
    # open the Icon
    icon = ImageTk.PhotoImage(file='./icon/icon.png')
    root.tk.call('wm', 'iconphoto', root._w, icon)
    passwdmgr=Loginer(master=root)
    passwdmgr.mainloop()

if __name__ == '__main__':
    run()
