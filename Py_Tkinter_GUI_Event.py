from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.colorchooser import askcolor
from tkinter.messagebox import askokcancel, askquestion, showerror
from tkinter.simpledialog import askfloat
demos = {
    'Open': askopenfilename,
    'Color': askcolor,
    'Query': lambda: askquestion('Warning', 'You typed "rm *"\nConfirm?'),
    'Error': lambda: showerror('Error!', "He's dead, Jim"),
    'Input': lambda: askfloat('Entry', 'Enter credit card number')
}

class Quitter(Frame): # subclass our GUI
    def __init__(self, parent=None): # constructor method
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(side=LEFT, expand=YES, fill=BOTH)
    def quit(self):
        ans = askokcancel('Verify exit', "Really quit?")
        if ans: Frame.quit(self)

class Demo(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.pack()
        Label(self, text="Basic demos").pack()
        for (key, value) in demos.items():
            Button(self, text=key, command=value).pack(side=TOP, fill=BOTH)
        Quitter(self).pack(side=TOP, fill=BOTH)

def showPosEvent(event):
    print('Widget=%s X=%s Y=%s' % (event.widget, event.x, event.y))
def showAllEvent(event):
    print(event)
    for attr in dir(event):
        if not attr.startswith('__'):
            print(attr, '=>', getattr(event, attr))
def onKeyPress(event):
    print('Got key press:', event.char)
def onArrowKey(event):
    print('Got up arrow key press')
def onReturnKey(event):
    print('Got return key press')
def onLeftClick(event):
    print('Got left mouse button click:', end=' ')
    showPosEvent(event)
def onRightClick(event):
    print('Got right mouse button click:', end=' ')
    showPosEvent(event)
def onMiddleClick(event):
    print('Got middle mouse button click:', end=' ')
    showPosEvent(event)
def onLeftDrag(event):
    print('Got left mouse button drag:', end=' ')

def onDoubleLeftClick(event):
    print('Got double left mouse click', end=' ')
    showPosEvent(event)
    tkroot.quit()

tkroot = Tk()
labelfont = ('courier', 20, 'bold') # family, size, style
widget = Label(tkroot, text='Hello bind world')
widget.config(bg='red', font=labelfont) # red background, large font
widget.config(height=5, width=20) # initial size: lines,chars
widget.pack(expand=YES, fill=BOTH)
widget.bind('<Button-1>', onLeftClick) # mouse button clicks
widget.bind('<Button-3>', onRightClick)
widget.bind('<Button-2>', onMiddleClick) # middle=both on some mice
widget.bind('<Double-1>', onDoubleLeftClick) # click left twice
widget.bind('<B1-Motion>', onLeftDrag) # click left and move
widget.bind('<KeyPress>', onKeyPress) # all keyboard presses
widget.bind('<Up>', onArrowKey) # arrow button pressed
widget.bind('<Return>', onReturnKey) # return/enter key pressed
widget.focus() # or bind keypress to tkroot
tkroot.title('Click Me')
#tkroot.mainloop()

def fetch():
    print('Input => "%s"' % ent.get()) # get text
eroot = Tk()
ent = Entry(eroot)
ent.insert(0, 'Type words here') # set text
ent.pack(side=TOP, fill=X) # grow horiz
ent.focus() # save a click
ent.bind('<Return>', (lambda event: fetch())) # on enter key
btn = Button(eroot, text='Fetch', command=fetch) # and on button
btn.pack(side=LEFT)
Quitter(eroot).pack(side=RIGHT)
#root.mainloop()

fields = 'Name', 'Job', 'Pay'
def fetch(entries):
    for entry in entries:
        print('Input => "%s"' % entry.get()) # get text
def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root) # make a new row
        lab = Label(row, width=5, text=field) # add label, entry
        ent = Entry(row)
        row.pack(side=TOP, fill=X) # pack row on top
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X) # grow horizontal
        entries.append(ent)
    return entries

droot = Tk()
ents = makeform(droot, fields)
droot.bind('<Return>', (lambda event: fetch(ents)))
Button(droot, text='Fetch', command= (lambda: fetch(ents))).pack(side=LEFT)
Quitter(droot).pack(side=RIGHT)
#droot.mainloop()

def show(entries, popup):
    fetch(entries) # must fetch before window destroyed!
    popup.destroy() # fails with msgs if stmt order is reversed
def ask():
    popup = Toplevel() # show form in modal dialog window
    ents = makeform(popup, fields)
    Button(popup, text='OK', command=(lambda: show(ents, popup))).pack()
    popup.grab_set()
    popup.focus_set()
    popup.wait_window() # wait for destroy here

froot = Tk()
Button(froot, text='Dialog', command=ask).pack()
froot.mainloop()
#if __name__ == '__main__': Demo().mainloop()
if __name__ == '__main__': froot.mainloop()
