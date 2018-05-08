"""
Tkinter GUI Application Development Blueprints
"""

from tkinter import *

root = Tk()
root.title('I am a Top Level Widget, parent to other widgets')
# create a frame widget for placing menu
my_menu_bar = Frame(root, relief='raised', bd=2)
my_menu_bar.pack(fill=X)

# Create  Menu Widget 1 and Sub Menu 1
my_menu_button = Menubutton(my_menu_bar, text='Menu Button Widget 1', )
my_menu_button.pack(side=LEFT)
# menu widget
my_menu = Menu(my_menu_button, tearoff=0)
my_menu_button['menu'] = my_menu
my_menu.add('command', label='Menu Widget 1')  # Add Sub Menu 1

# Create  Menu2 and Submenu2
menu_button_2 = Menubutton(my_menu_bar, text='Menu 2', )
menu_button_2.pack(side=LEFT)
my_menu_2 = Menu(menu_button_2, tearoff=0)
menu_button_2['menu'] = my_menu_2
my_menu_2.add('command', label='Sub Menu 2')  # Add Sub Menu 2

#
#
# my_frame_1  and its contents
#


# creating a frame (my_frame_1)
my_frame_1 = Frame(root, bd=2, relief=SUNKEN)
my_frame_1.pack(side=LEFT)

# add label to to my_frame_1
Label(my_frame_1, text='I am a Label widget').pack()

# add entry widget to my_frame_1
tv = StringVar()  # discussed later
Entry(my_frame_1, textvariable=tv).pack()
tv.set('I am an entry widget')

# add button widget to my_frame_1
Button(my_frame_1, text='Button widget').pack()

# add check button widget to my_frame_1
Checkbutton(my_frame_1, text='CheckButton Widget').pack()

# add radio buttons to my_frame_1
Radiobutton(my_frame_1, text='Radio Button  Un', value=1).pack()
Radiobutton(my_frame_1, text='Radio Button  Dos', value=2).pack()
Radiobutton(my_frame_1, text='Radio Button  Tres', value=3).pack()

# OptionMenu Widget
Label(my_frame_1, text='Example of OptionMenu Widget:').pack()
OptionMenu(my_frame_1, '', "Option A", "Option B", "Option C").pack()

# adding my_image image
Label(my_frame_1, text='Image Fun with Bitmap Class:').pack()
my_image = BitmapImage(file="gir.xbm")
my_label = Label(my_frame_1, image=my_image)
my_label.image = my_image  # keep a reference!
my_label.pack()

#
#
# frame2 and widgets it contains.
#
#



# create another frame(my_frame_2) to hold a list box, Spinbox Widget,Scale Widget, :
my_frame_2 = Frame(root, bd=2, relief=GROOVE)
my_frame_2.pack(side=RIGHT)

# add Photimage Class Widget to my_frame_2
Label(my_frame_2, text='Image displayed with \nPhotoImage class widget:').pack()
dance_photo = PhotoImage(file='dance.gif')
dance_photo_label = Label(my_frame_2, image=dance_photo)
dance_photo_label.image = dance_photo
dance_photo_label.pack()

# add my_listbox widget to my_frame_2
Label(my_frame_2, text='Below is an example of my_listbox widget:').pack()
my_listbox = Listbox(my_frame_2, height=4)
for line in ['Listbox Choice 1', 'Choice 2', 'Choice 3', 'Choice 4']:
    my_listbox.insert(END, line)
my_listbox.pack()

# spinbox widget
Label(my_frame_2, text='Below is an example of spinbox widget:').pack()
Spinbox(my_frame_2, values=(1, 2, 4, 8, 10)).pack()

# scale widget
Scale(my_frame_2, from_=0.0, to=100.0, label='Scale widget', orient=HORIZONTAL).pack()

# LabelFrame
label_frame = LabelFrame(my_frame_2, text="Labelframe Widget", padx=10, pady=10)
label_frame.pack(padx=10, pady=10)
Entry(label_frame).pack()

# message widget
Message(my_frame_2, text='I am a Message widget').pack()

#
#
# Frame 3
#
#

my_frame_3 = Frame(root, bd=2, relief=SUNKEN)

# text widget and associated Scrollbar widget
my_text = Text(my_frame_3, height=10, width=40)
file_object = open('textcontent.txt')
file_content = file_object.read()
file_object.close()
my_text.insert(END, file_content)
my_text.pack(side=LEFT, fill=X, padx=5)

# add scrollbar widget to the text widget
my_scrollbar = Scrollbar(my_frame_3, orient=VERTICAL, command=my_text.yview)
my_scrollbar.pack()
my_text.configure(yscrollcommand=my_scrollbar.set)
my_frame_3.pack()

#
#
# Frame 4
#
#
# create another frame(my_frame_4)
my_frame_4 = Frame(root).pack()

my_canvas = Canvas(my_frame_4, bg='white', width=340, height=80)
my_canvas.pack()
my_canvas.create_oval(20, 15, 60, 60, fill='red')
my_canvas.create_oval(40, 15, 60, 60, fill='grey')
my_canvas.create_text(130, 38, text='I am a Canvas Widget', font=('arial', 8, 'bold'))

#
#
# A paned window widget
#
#

Label(root, text='Below is an example of Paned window widget:').pack()
Label(root, text='Notice you can adjust the size of each pane by dragging it').pack()
my_paned_window_1 = PanedWindow()
my_paned_window_1.pack(fill=BOTH, expand=2)
left_pane_text = Text(my_paned_window_1, height=6, width=15)
my_paned_window_1.add(left_pane_text)
my_paned_window_2 = PanedWindow(my_paned_window_1, orient=VERTICAL)
my_paned_window_1.add(my_paned_window_2)
top_pane_text = Text(my_paned_window_2, height=3, width=3)
my_paned_window_2.add(top_pane_text)
bottom_pane_text = Text(my_paned_window_2, height=3, width=3)
my_paned_window_2.add(bottom_pane_text)

root.mainloop()
