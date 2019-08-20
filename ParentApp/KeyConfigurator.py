# prog info shows up in the "About" button, also, this is the information for this sotware:
progInfo = """
 Little Application for collecting username and password and scrambling it for
 use by the Adafruit Trinket M0 duckies.

 YOUR CREDENTIALS ARE NEVER STORED OR TRANSMITTED BY THIS SOFTWARE.
 If you loose your key, RESET YOUR PASSWORD IMMEDIATLY. You are responsible for
 your security, use at your own risk.

 GNU GPL v3:
 Copyright (C) 2019  Rowdy S. "AwsomeChicken"

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Is your loginer not working?
Flashing:
    - Purple-Green: Credentials are corrupted, try re-configuring your key.
    - Yellow-White: Error converting credentials to keystrokes, try re-configuring your key.
        --> If reconfiguring doesn't work, go to the GitHub and report a bug
"""

import tkinter as tk
from tkinter import Grid, filedialog, messagebox, ttk
#import PIL
from PIL import Image, ImageTk
from pathlib import Path
from random import randrange
import os, TrinketCode

def popupWindow(msg, title):
    popup = tk.Tk()
    popup.wm_title(title)
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Close", command = popup.destroy)
    B1.pack()
    popup.mainloop()

class Loginer(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master) # root


        self.feilds()

        # configure the first column to have a flexible width
        master.grid_columnconfigure(index=1, weight=1, minsize=98)
        master.title('Loginer Key Configurator')

    def feilds(self):
        # Label & instructions
        inst="Please enter the username and password to be written to the USB Key.\nYou will then be asked to find the CIRCUITPY drive"
        self.instruct=tk.Label(text=inst)
        self.instruct.grid(row=0,column=0, columnspan=2, sticky='news', padx=3, pady=6)

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

        # About button:
        self.aboutProg = tk.Button(text="About", command=lambda:popupWindow(msg = progInfo, title = "About: Loginer Configurator"))
        self.aboutProg.grid(row=0, column = 2, sticky="e", padx=3, pady=6)

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

    def writeCreds(self, document):
        # open a file dialog and navigate to the CIRCUITPY device
        # then it will write the improved lib/bfd.py
        path=filedialog.askdirectory(initialdir="shell:MyComputerFolder", title="Please Find CIRCUITPY")

        #print(path)
        # wrote the new user and pass to the python lib
        if len(path) > 0:
            os.remove(path+"lib/bfd.py") # delete the old file
            final = os.open(path+"lib/bfd.py", os.O_WRONLY|os.O_CREAT) # use OS to open
            os.write(final, document.encode('utf8')) # write using the OS dialog
            self.writeCode(path) # write the code.py file
            os.fsync(final) # fsync to prevent corruption of the Trinket
            os.close(final) # close the file
            return True
        else:
            print('Don\'t do things')
            return False

    def writeCode(self, path):
        code = TrinketCode.get()
        os.remove(path+"main.py")
        codefile = os.open(path+"main.py", os.O_WRONLY|os.O_CREAT) # use OS to open
        os.write(codefile, code.encode('utf8')) # write using the OS dialog
        os.fsync(codefile) # fsync to prevent corruption of the Trinket
        os.close(codefile) # close the file

    def writeToDuckie(self, event=None):
        print("Write to duckie")

        # get the Password
        uname=self.username.get()
        pss=self.password.get()

        #the word that will end up on the device
        word=" "+uname+'\t'+pss+'\n'

        # encode to a "safe" format
        binval=self.str2enc(word)
        # now remove the Username and Password from memory
        uname="j$bnb8)786t2bnv^Tklhtw\t!^,kbvhjce5ou7s^k\';lbvgefbvRmkhjvg\npodFYUc\tdbey6HVvc5ekyv%\n$f"
        pss="kliawef]a\sf09754hlakjc6903\t;hvy6g4ela\';alhv12*534$#i76jikCDHRTik337u54\"$75r96tfvgkjdu"

        # convert the encoded values into a python script that returns the values
        doc="def pws():\n\tg=%s\n\tmod=%s\n\treturn g, mod"%(str(binval), self.modulus.get())
        #code =
        #print(doc)

        success = self.writeCreds(doc)
        if success:
            messagebox.showinfo("Success?", "No errors occured during write,\nso you should be good to go...")
        else:
            messagebox.showinfo("Nothing written", "Nothing was written, either you canceled\nor something went wrong in the write process")
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
    try:
        # open the Icon
        icon = ImageTk.PhotoImage(file='./icon.ico')
        root.tk.call('wm', 'iconphoto', root._w, icon)
    except:
        pass
    passwdmgr=Loginer(master=root)
    passwdmgr.mainloop()

if __name__ == '__main__':
    run()
