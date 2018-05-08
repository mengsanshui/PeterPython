"""
PyEdit (textEditor.py) user startup configuration module;
"""

Version = '2.1'
import sys, os                                              # platform, args, run tools
from tkinter import *                                       # base widgets, constants
from tkinter.filedialog import Open, SaveAs                 # standard dialogs
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter.simpledialog import askstring, askinteger
from tkinter.colorchooser import askcolor
from guimaker import *                                      # Frame + menu/toolbar builders

try:
    import textConfig               # startup font and colors
    configs = textConfig.__dict__    # work if not on the path or bad
except:                             # define in client app directory
    configs = {}

helptext = "PyEdit version %s"

START = '1.0'                       # index of first char: row=1,col=0
SEL_FIRST = SEL + '.first'          # map sel tag to index
SEL_LAST = SEL + '.last'            # same as 'sel.last'
FontScale = 0                        # use bigger font on Linux
if sys.platform[:3] != 'win':       # and other non-Windows boxes
    FontScale = 3

class TextEditor:                   # mix with menu/toolbar Frame class
    startfiledir = '.'              # for dialogs
    editwindows = []                 # for process-wide quit check

    # Unicode configurations
    # imported in class to allow overrides in subclass or self
    if __name__ == '__main__':
        from textConfig import (
            opensAskUser, opensEncoding,
            savesUseKnownEncoding, savesAskUser, savesEncoding)
    else:
        from textConfig import (
            opensAskUser, opensEncoding,
            savesUseKnownEncoding, savesAskUser, savesEncoding)

    ftypes = [('All files', '*'),  # for file open dialog
              ('Text files', '.txt'),  # customize in subclass
              ('Python files', '.py')]  # or set in each instance

    colors = [{'fg': 'black', 'bg': 'white'},  # color pick list
              {'fg': 'yellow', 'bg': 'black'},  # first item is default
              {'fg': 'white', 'bg': 'blue'},  # tailor me as desired
              {'fg': 'black', 'bg': 'beige'},  # or do PickBg/Fg chooser
              {'fg': 'yellow', 'bg': 'purple'},
              {'fg': 'black', 'bg': 'brown'},
              {'fg': 'lightgreen', 'bg': 'darkgreen'},
              {'fg': 'darkblue', 'bg': 'orange'},
              {'fg': 'orange', 'bg': 'darkblue'}]

    fonts = [('courier', 9 + FontScale, 'normal'),  # platform-neutral fonts
             ('courier', 12 + FontScale, 'normal'),  # (family, size, style)
             ('courier', 10 + FontScale, 'bold'),  # or pop up a listbox
             ('courier', 10 + FontScale, 'italic'),  # make bigger on Linux
             ('times', 10 + FontScale, 'normal'),  # use 'bold italic' for 2
             ('helvetica', 10 + FontScale, 'normal'),  # also 'underline', etc.
             ('ariel', 10 + FontScale, 'normal'),
             ('system', 10 + FontScale, 'normal'),
             ('courier', 20 + FontScale, 'normal')]

    def __init__(self, loadFirst='', loadEncode=''):
        if not isinstance(self, GuiMaker):
            raise TypeError('TextEditor needs a GuiMaker mixin')

        self.setFileName(None)
        self.lastfind = None
        self.openDialog = None
        self.saveDialog = None
        self.knownEncoding = None
        self.text.focus()
        if loadFirst:
            self.update()
            self.onOpen(loadFirst, loadEncode)

    def start(self):  # run by GuiMaker.__init__
        self.menuBar = [  # configure menu/toolbar
            ('File', 0,  # a GuiMaker menu def tree
             [('Open...', 0, self.onOpen),  # build in method for self
              ('Save', 0, self.onSave),  # label, shortcut, callback
              ('Save As...', 5, self.onSaveAs),
              ('New', 0, self.onNew),
              'separator',
              ('Quit...', 0, self.onQuit)]
             ),
            ('Edit', 0,
             [('Undo', 0, self.onUndo),
              ('Redo', 0, self.onRedo),
              'separator',
              ('Cut', 0, self.onCut),
              ('Copy', 1, self.onCopy),
              ('Paste', 0, self.onPaste),
              'separator',
              ('Delete', 0, self.onDelete),
              ('Select All', 0, self.onSelectAll)]
             ),
            ('Search', 0,
             [('Goto...', 0, self.onGoto),
              ('Find...', 0, self.onFind),
              ('Refind', 0, self.onRefind),
              ('Change...', 0, self.onChange),
              ('Grep...', 3, self.onGrep)]
             ),
            ('Tools', 0,
             [('Pick Font...', 6, self.onPickFont),
              ('Font List', 0, self.onFontList),
              'separator',
              ('Pick Bg...', 3, self.onPickBg),
              ('Pick Fg...', 0, self.onPickFg),
              ('Color List', 0, self.onColorList),
              'separator',
              ('Info...', 0, self.onInfo),
              ('Clone', 1, self.onClone),
              ('Run Code', 0, self.onRunCode)]
             )]
        self.toolBar = [
            ('Save', self.onSave, {'side': LEFT}),
            ('Cut', self.onCut, {'side': LEFT}),
            ('Copy', self.onCopy, {'side': LEFT}),
            ('Paste', self.onPaste, {'side': LEFT}),
            ('Find', self.onRefind, {'side': LEFT}),
            ('Help', self.help, {'side': RIGHT}),
            ('Quit', self.onQuit, {'side': RIGHT})]

    def makeWidgets(self):  # run by GuiMaker.__init__
        name = Label(self, bg='black', fg='white')  # add below menu, above tool
        name.pack(side=TOP, fill=X)  # menu/toolbars are packed
        # GuiMaker frame packs itself
        vbar = Scrollbar(self)
        hbar = Scrollbar(self, orient='horizontal')
        text = Text(self, padx=5, wrap='none')  # disable line wrapping
        text.config(undo=1, autoseparators=1)
        vbar.pack(side=RIGHT, fill=Y)
        hbar.pack(side=BOTTOM, fill=X)  # pack text last
        text.pack(side=TOP, fill=BOTH, expand=YES)  # else sbars clipped
        text.config(yscrollcommand=vbar.set)  # call vbar.set on text move
        text.config(xscrollcommand=hbar.set)
        vbar.config(command=text.yview)  # call text.yview on scroll move
        hbar.config(command=text.xview)  # or hbar['command']=text.xview
        # 2.0: apply user configs or defaults
        startfont = configs.get('font', self.fonts[0])
        startbg = configs.get('bg', self.colors[0]['bg'])
        startfg = configs.get('fg', self.colors[0]['fg'])
        text.config(font=startfont, bg=startbg, fg=startfg)
        if 'height' in configs: text.config(height=configs['height'])
        if 'width' in configs: text.config(width=configs['width'])
        self.text = text
        self.filelabel = name

    ############################################################################
    # File menu commands
    ############################################################################
    def my_askopenfilename(self):                           # objects remember last result dir/file
        if not self.openDialog:
            self.openDialog = Open(initialdir=self.startfiledir,
                                   filetypes=self.ftypes)
        return self.openDialog.show()

    def my_asksaveasfilename(self):                         # objects remember last result dir/file
        if not self.saveDialog:
            self.saveDialog = SaveAs(initialdir=self.startfiledir,
                                     filetypes=self.ftypes)
        return self.saveDialog.show()

    def onOpen(self, loadFirst='', loadEncode=''):
        if self.text_edit_modified():
            if not askyesno('PyEdit', 'Text has changed: discard changes?'):
                return
        file = loadFirst or self.my_askopenfilename()
        if not file:
            return
        if not os.path.isfile(file):
            showerror('PyEdit', 'Could not open file ' + file)
            return

        # try known encoding if passed and accurate (e.g., email)
        text = None                             # empty file = '' = False: test for None!
        if loadEncode:
            try:
                text = open(file, 'r', encoding=loadEncode).read()
                self.knownEncoding = loadEncode
            except (UnicodeError, LookupError, IOError):  # lookup: bad name
                pass

        # try user input, prefill with next choice as default
        if text == None and self.opensAskUser:
            self.update()  # else dialog doesn't appear in rare cases
            askuser = askstring('PyEdit', 'Enter Unicode encoding for open',
                            initialvalue=(self.opensEncoding or
                                          sys.getdefaultencoding() or ''))
        if askuser:
            try:
                text = open(file, 'r', encoding=askuser).read()
                self.knownEncoding = askuser
            except (UnicodeError, LookupError, IOError):
                pass

        # try config file (or before ask user?)
        if text == None and self.opensEncoding:
            try:
                text = open(file, 'r', encoding=self.opensEncoding).read()
                self.knownEncoding = self.opensEncoding
            except (UnicodeError, LookupError, IOError):
                pass

        # try platform default (utf-8 on windows; try utf8 always?)
        if text == None:
            try:
                text = open(file, 'r', encoding=sys.getdefaultencoding()).read()
                self.knownEncoding = sys.getdefaultencoding()
            except (UnicodeError, LookupError, IOError):
                pass

        # last resort: use binary bytes and rely on Tk to decode
        if text == None:
            try:
                text = open(file, 'rb').read()  # bytes for Unicode
                text = text.replace(b'\r\n', b'\n')  # for display, saves
                self.knownEncoding = None
            except IOError:
                pass

        if text == None:
            showerror('PyEdit', 'Could not decode and open file ' + file)
        else:
            self.setAllText(text)
            self.setFileName(file)
            self.text.edit_reset()  # 2.0: clear undo/redo stks
            self.text.edit_modified(0)

    def onSave(self):
        self.onSaveAs(self.currfile)  # may be None

    def onSaveAs(self, forcefile=None):
        filename = forcefile or self.my_asksaveasfilename()
        if not filename:
            return
        text = self.getAllText()
        encpick = None                  # even if read/inserted as bytes
        # try known encoding at latest Open or Save, if any
        if self.knownEncoding and (                                         # enc known?
            (forcefile and self.savesUseKnownEncoding >= 1) or      # on Save?
            (not forcefile and self.savesUseKnownEncoding >= 2)):   # on SaveAs?
            try:
                text.encode(self.knownEncoding)
                encpick = self.knownEncoding
            except UnicodeError:
                pass
        # try user input, prefill with known type, else next choice
        if not encpick and self.savesAskUser:
            self.update()  # else dialog doesn't appear in rare cases
        askuser = askstring('PyEdit', 'Enter Unicode encoding for save',
                            initialvalue=(self.knownEncoding or
                                          self.savesEncoding or
                                          sys.getdefaultencoding() or ''))
        if askuser:
            try:
                text.encode(askuser)
                encpick = askuser
            except (UnicodeError, LookupError):     # LookupError: bad name
                pass                                # UnicodeError: can't encode
        # try config file
        if not encpick and self.savesEncoding:
            try:
                text.encode(self.savesEncoding)
                encpick = self.savesEncoding
            except (UnicodeError, LookupError):
                pass
        # try platform default (utf8 on windows)
        if not encpick:
            try:
                text.encode(sys.getdefaultencoding())
                encpick = sys.getdefaultencoding()
            except (UnicodeError, LookupError):
                pass
        # open in text mode for endlines + encoding
        if not encpick:
            showerror('PyEdit', 'Could not encode for file ' + filename)
        else:
            try:
                file = open(filename, 'w', encoding=encpick)
                file.write(text)
                file.close()
            except:
                showerror('PyEdit', 'Could not write file ' + filename)
            else:
                self.setFileName(filename)          # may be newly created
                self.text.edit_modified(0)          # 2.0: clear modified flag
                self.knownEncoding = encpick        # 2.1: keep enc for next save
                                                    # don't clear undo/redo stks!

    def onNew(self):
        if self.text_edit_modified():
            if not askyesno('PyEdit', 'Text has changed: discard changes?'):
                return
        self.setFileName(None)
        self.clearAllText()
        self.text.edit_reset()                      # 2.0: clear undo/redo stks
        self.text.edit_modified(0)                  # 2.0: clear modified flag
        self.knownEncoding = None                  # 2.1: Unicode type unknown

    def onQuit(self):
        assert False, 'onQuit must be defined in window-specific sublass'

    def text_edit_modified(self):
        return self.text.edit_modified()

    ############################################################################
    # Edit menu commands
    ############################################################################
    def onUndo(self):
        try:
            self.text.edit_undo()                                # exception if stacks empty
        except TclError:                                        # menu tear-offs for quick undo
            showinfo('PyEdit', 'Nothing to undo')

    def onRedo(self):                                           # 2.0: redo an undone
        try:
            self.text.edit_redo()
        except TclError:
            showinfo('PyEdit', 'Nothing to redo')

    def onCopy(self):                                           # get text selected by mouse, etc.
        if not self.text.tag_ranges(SEL):                       # save in cross-app clipboard
            showerror('PyEdit', 'No text selected')
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)

    def onDelete(self):                                         # delete selected text, no save
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)

    def onCut(self):
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.onCopy()                                           # save and delete selected text
            self.onDelete()

    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
        except TclError:
            showerror('PyEdit', 'Nothing to paste')
            return
        self.text.insert(INSERT, text)                              # add at current insert cursor
        self.text.tag_remove(SEL, '1.0', END)
        self.text.tag_add(SEL, INSERT + '-%dc' % len(text), INSERT)
        self.text.see(INSERT)                                       # select it, so it can be cut

    def onSelectAll(self):
        self.text.tag_add(SEL, '1.0', END + '-1c')                  # select entire text
        self.text.mark_set(INSERT, '1.0')                            # move insert point to top
        self.text.see(INSERT)                                         # scroll to top

    ############################################################################
    # Search menu commands
    ############################################################################
    def onGoto(self, forceline=None):
        line = forceline or askinteger('PyEdit', 'Enter line number')
        self.text.update()
        self.text.focus()
        if line is not None:
            maxindex = self.text.index(END + '-1c')
            maxline = int(maxindex.split('.')[0])
        if line > 0 and line <= maxline:
            self.text.mark_set(INSERT, '%d.0' % line)  # goto line
            self.text.tag_remove(SEL, '1.0', END)  # delete selects
            self.text.tag_add(SEL, INSERT, 'insert + 1l')  # select line
            self.text.see(INSERT)  # scroll to line
        else:
            showerror('PyEdit', 'Bad line number')

    def onFind(self, lastkey=None):
        key = lastkey or askstring('PyEdit', 'Enter search string')
        self.text.update()
        self.text.focus()
        self.lastfind = key
        if key:
            nocase = configs.get('caseinsens', True)
            where = self.text.search(key, INSERT, END, nocase=nocase)
            if not where:
                showerror('PyEdit', 'String not found')
            else:
                pastkey = where + '+%dc' % len(key)                 # index past key
                self.text.tag_remove(SEL, '1.0', END)               # remove any sel
                self.text.tag_add(SEL, where, pastkey)               # select key
                self.text.mark_set(INSERT, pastkey)                  # for next find
                self.text.see(where)                                 # scroll display

    def onRefind(self):
        self.onFind(self.lastfind)

    def onChange(self):
        new = Toplevel(self)
        new.title('PyEdit - change')
        Label(new, text='Find text?', relief=RIDGE, width=15).grid(row=0, column=0)
        Label(new, text='Change to?', relief=RIDGE, width=15).grid(row=1, column=0)
        entry1 = Entry(new)
        entry2 = Entry(new)
        entry1.grid(row=0, column=1, sticky=EW)
        entry2.grid(row=1, column=1, sticky=EW)

        def onFind():  # use my entry in enclosing scope
            self.onFind(entry1.get())  # runs normal find dialog callback

        def onApply():
            self.onDoChange(entry1.get(), entry2.get())

        Button(new, text='Find', command=onFind).grid(row=0, column=2, sticky=EW)
        Button(new, text='Apply', command=onApply).grid(row=1, column=2, sticky=EW)
        new.columnconfigure(1, weight=1)

    def onDoChange(self, findtext, changeto):
        # on Apply in change dialog: change and refind
        if self.text.tag_ranges(SEL):                           # must find first
            self.text.delete(SEL_FIRST, SEL_LAST)
            self.text.insert(INSERT, changeto)                  # deletes if empty
            self.text.see(INSERT)
            self.onFind(findtext)                               # goto next appear
            self.text.update()                                  # force refresh

    def onGrep(self):
        from formrows import makeFormRow
        popup = Toplevel()
        popup.title('PyEdit - grep')
        var1 = makeFormRow(popup, label='Directory root', width=18, browse=False)
        var2 = makeFormRow(popup, label='Filename pattern', width=18, browse=False)
        var3 = makeFormRow(popup, label='Search string', width=18, browse=False)
        var4 = makeFormRow(popup, label='Content encoding', width=18, browse=False)
        var1.set('.')  # current dir
        var2.set('*.py')  # initial values
        var4.set(sys.getdefaultencoding())  # for file content, not filenames
        cb = lambda: self.onDoGrep(var1.get(), var2.get(), var3.get(), var4.get())
        Button(popup, text='Go', command=cb).pack()

    def onDoGrep(self, dirname, filenamepatt, grepkey, encoding):
        import threading, queue

        # make non-modal un-closeable dialog
        mypopup = Tk()
        mypopup.title('PyEdit - grepping')
        status = Label(mypopup, text='Grep thread searching for: %r...' % grepkey)
        status.pack(padx=20, pady=20)
        mypopup.protocol('WM_DELETE_WINDOW', lambda: None)  # ignore X close
        # start producer thread, consumer loop
        myqueue = queue.Queue()
        threadargs = (filenamepatt, dirname, grepkey, encoding, myqueue)
        threading.Thread(target=self.grepThreadProducer, args=threadargs).start()
        self.grepThreadConsumer(grepkey, encoding, myqueue, mypopup)

    def grepThreadProducer(self, filenamepatt, dirname, grepkey, encoding, myqueue):
        from find import find
        matches = []
        try:
            for filepath in find(pattern=filenamepatt, startdir=dirname):
                try:
                    textfile = open(filepath, encoding=encoding)
                    for (linenum, linestr) in enumerate(textfile):
                        if grepkey in linestr:
                            msg = '%s@%d [%s]' % (filepath, linenum + 1, linestr)
                            matches.append(msg)
                except UnicodeError as X:
                    print('Unicode error in:', filepath, X)  # eg: decode, bom
                except IOError as X:
                    print('IO error in:', filepath, X)  # eg: permission
        finally:
            myqueue.put(matches)  # stop consumer loop on find excs: filenames?

    def grepThreadConsumer(self, grepkey, encoding, myqueue, mypopup):
        import queue
        try:
            matches = myqueue.get(block=False)
        except queue.Empty:
            myargs = (grepkey, encoding, myqueue, mypopup)
            self.after(250, self.grepThreadConsumer, *myargs)
        else:
            mypopup.destroy()  # close status
            self.update()  # erase it now
        if not matches:
            showinfo('PyEdit', 'Grep found no matches for: %r' % grepkey)
        else:
            self.grepMatchesList(matches, grepkey, encoding)

    def grepMatchesList(self, matches, grepkey, encoding):
        from scrolledlist import ScrolledList
        print('Matches for %s: %s' % (grepkey, len(matches)))

        # catch list double-click
        class ScrolledFilenames(ScrolledList):
            def runCommand(self, selection):
                file, line = selection.split(' [', 1)[0].split('@')
                editor = TextEditorMainPopup(
                    loadFirst=file, winTitle=' grep match', loadEncode=encoding)
                editor.onGoto(int(line))
                editor.text.focus_force()

        # new non-modal widnow
        popup = Tk()
        popup.title('PyEdit - grep matches: %r (%s)' % (grepkey, encoding))
        ScrolledFilenames(parent=popup, options=matches)

    ############################################################################
    # Tools menu commands
    ############################################################################
    def onFontList(self):
        self.fonts.append(self.fonts[0])  # pick next font in list
        del self.fonts[0]  # resizes the text area
        self.text.config(font=self.fonts[0])

    def onColorList(self):
        self.colors.append(self.colors[0])  # pick next color in list
        del self.colors[0]  # move current to end
        self.text.config(fg=self.colors[0]['fg'], bg=self.colors[0]['bg'])

    def onPickFg(self):
        self.pickColor('fg')  # added on 10/02/00

    def onPickBg(self):  # select arbitrary color
        self.pickColor('bg')  # in standard color dialog

    def pickColor(self, part):  # this is too easy
        (triple, hexstr) = askcolor()
        if hexstr:
            self.text.config(**{part: hexstr})

    def onInfo(self):
        text = self.getAllText()  # added on 5/3/00 in 15 mins
        bytes = len(text)  # words uses a simple guess:
        lines = len(text.split('\n'))  # any separated by whitespace
        words = len(text.split())  # 3.x: bytes is really chars
        index = self.text.index(INSERT)  # str is unicode code points
        where = tuple(index.split('.'))
        showinfo('PyEdit Information',
                 'Current location:\n\n' +
                 'line:\t%s\ncolumn:\t%s\n\n' % where +
                 'File text statistics:\n\n' +
                 'chars:\t%d\nlines:\t%d\nwords:\t%d\n' % (bytes, lines, words))

    def onClone(self, makewindow=True):
        if not makewindow:
            new = None  # assume class makes its own window
        else:
            new = Toplevel()  # a new edit window in same process
        myclass = self.__class__  # instance's (lowest) class object
        myclass(new)  # attach/run instance of my class

    def onRunCode(self, parallelmode=True):
        def askcmdargs():
            return askstring('PyEdit', 'Commandline arguments?') or ''

        from launchmodes import System, Start, StartArgs, Fork
        filemode = False
        thefile = str(self.getFileName())
        if os.path.exists(thefile):
            filemode = askyesno('PyEdit', 'Run from file?')
            self.update()  # 2.1: run update()
            if not filemode:  # run text string
                cmdargs = askcmdargs()
                namespace = {'__name__': '__main__'}  # run as top-level
                sys.argv = [thefile] + cmdargs.split()  # could use threads
                exec(self.getAllText() + '\n', namespace)  # exceptions ignored
            elif self.text_edit_modified():  # 2.0: changed test
                showerror('PyEdit', 'Text changed: you must save before run')
        else:
            cmdargs = askcmdargs()
            mycwd = os.getcwd()  # cwd may be root
            dirname, filename = os.path.split(thefile)  # get dir, base
            os.chdir(dirname or mycwd)  # cd for filenames
            thecmd = filename + ' ' + cmdargs  # 2.1: not theFile
            if not parallelmode:  # run as file
                System(thecmd, thecmd)()  # block editor
            else:
                if sys.platform[:3] == 'win':  # spawn in parallel
                    run = StartArgs if cmdargs else Start  # 2.1: support args
                    run(thecmd, thecmd)()  # or always Spawn
                else:
                    Fork(thecmd, thecmd)()
            os.chdir(mycwd)

    def onPickFont(self):
        from formrows import makeFormRow

        popup = Toplevel(self)
        popup.title('PyEdit - font')
        var1 = makeFormRow(popup, label='Family', browse=False)
        var2 = makeFormRow(popup, label='Size', browse=False)
        var3 = makeFormRow(popup, label='Style', browse=False)
        var1.set('courier')
        var2.set('12')  # suggested vals
        var3.set('bold italic')  # see pick list for valid inputs
        Button(popup, text='Apply', command=
            lambda: self.onDoFont(var1.get(), var2.get(), var3.get())).pack()

    def onDoFont(self, family, size, style):
        try:
            self.text.config(font=(family, int(size), style))
        except:
            showerror('PyEdit', 'Bad font specification')

############################################################################
# Utilities, useful outside this class
############################################################################
    def isEmpty(self):
        return not self.getAllText()

    def getAllText(self):
        return self.text.get('1.0', END + '-1c')  # extract text as str string

    def setAllText(self, text):
        self.text.delete('1.0', END)  # store text string in widget
        self.text.insert(END, text)  # or '1.0'; text=bytes or str
        self.text.mark_set(INSERT, '1.0')  # move insert point to top
        self.text.see(INSERT)  # scroll to top, insert set

    def clearAllText(self):
        self.text.delete('1.0', END)  # clear text in widget

    def getFileName(self):
        return self.currfile

    def setFileName(self, name):  # see also: onGoto(linenum)
        self.currfile = name  # for save
        self.filelabel.config(text=str(name))

    def setKnownEncoding(self, encoding='utf-8'):  # 2.1: for saves if inserted
        self.knownEncoding = encoding  # else saves use config, ask?

    def setBg(self, color):
        self.text.config(bg=color)  # to set manually from code

    def setFg(self, color):
        self.text.config(fg=color)  # 'black', hexstring

    def setFont(self, font):
        self.text.config(font=font)  # ('family', size, 'style')

    def setHeight(self, lines):  # default = 24h x 80w
        self.text.config(height=lines)  # may also be from textCongif.py

    def setWidth(self, chars):
        self.text.config(width=chars)

    def clearModified(self):
        self.text.edit_modified(0)  # clear modified flag

    def isModified(self):
        return self.text_edit_modified()  # changed since last reset?

    def help(self):
        showinfo('About PyEdit', helptext % Version)

 ################################################################################
    # Ready-to-use editor classes
    # mixes in a GuiMaker Frame subclass which builds menu and toolbars
    #
    # these classes are common use cases, but other configurations are possible;
    # call TextEditorMain().mainloop() to start PyEdit as a standalone program;
    # redefine/extend onQuit in a subclass to catch exit or destroy (see PyView);
    # caveat: could use windows.py for icons, but quit protocol is custom here.
################################################################################
###################################
    # when text editor owns the window
###################################

class TextEditorMain(TextEditor, GuiMakerWindowMenu):
    def __init__(self, parent=None, loadFirst='', loadEncode=''):
        # editor fills whole parent window
        GuiMaker.__init__(self, parent)  # use main window menus
        TextEditor.__init__(self, loadFirst, loadEncode)  # GuiMaker frame packs self
        self.master.title('PyEdit ' + Version)  # title, wm X if standalone
        self.master.iconname('PyEdit')
        self.master.protocol('WM_DELETE_WINDOW', self.onQuit)
        TextEditor.editwindows.append(self)

    def onQuit(self):  # on a Quit request in the GUI
        close = not self.text_edit_modified()  # check self, ask?, check others
        if not close:
            close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        if close:
            windows = TextEditor.editwindows
            changed = [w for w in windows if w != self and w.text_edit_modified()]
            if not changed:
                GuiMaker.quit(self)  # quit ends entire app regardless of widget type
            else:
                numchange = len(changed)
                verify = '%s other edit window%s changed: quit and discard anyhow?'
                verify = verify % (numchange, 's' if numchange > 1 else '')
                if askyesno('PyEdit', verify):
                    GuiMaker.quit(self)

class TextEditorMainPopup(TextEditor, GuiMakerWindowMenu):
    def __init__(self, parent=None, loadFirst='', winTitle='', loadEncode=''):
    # create own window
        self.popup = Toplevel(parent)
        GuiMaker.__init__(self, self.popup)  # use main window menus
        TextEditor.__init__(self, loadFirst, loadEncode)  # a frame in a new popup
        assert self.master == self.popup
        self.popup.title('PyEdit ' + Version + winTitle)
        self.popup.iconname('PyEdit')
        self.popup.protocol('WM_DELETE_WINDOW', self.onQuit)
        TextEditor.editwindows.append(self)

    def onQuit(self):
        close = not self.text_edit_modified()
        if not close:
            close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        if close:
            self.popup.destroy()  # kill this window only
        TextEditor.editwindows.remove(self)  # (plus any child windows)

    def onClone(self):
        TextEditor.onClone(self, makewindow=False)  # I make my own pop-up

#########################################
# when editor embedded in another window
#########################################

class TextEditorComponent(TextEditor, GuiMakerFrameMenu):
    def __init__(self, parent=None, loadFirst='', loadEncode=''):
        # use Frame-based menus
        GuiMaker.__init__(self, parent)  # all menus, buttons on
        TextEditor.__init__(self, loadFirst, loadEncode)  # GuiMaker must init 1st

    def onQuit(self):
        close = not self.text_edit_modified()
        if not close:
            close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        if close:
            self.destroy()  # erase self Frame but do not quit enclosing app

class TextEditorComponentMinimal(TextEditor, GuiMakerFrameMenu):
    def __init__(self, parent=None, loadFirst='', deleteFile=True, loadEncode=''):
        self.deleteFile = deleteFile
        GuiMaker.__init__(self, parent)  # GuiMaker frame packs self
        TextEditor.__init__(self, loadFirst, loadEncode)  # TextEditor adds middle

    def start(self):
        TextEditor.start(self)  # GuiMaker start call
        for i in range(len(self.toolBar)):  # delete quit in toolbar
            if self.toolBar[i][0] == 'Quit':  # delete file menu items,
                del self.toolBar[i]  # or just disable file
                break
        if self.deleteFile:
            for i in range(len(self.menuBar)):
                if self.menuBar[i][0] == 'File':
                    del self.menuBar[i]
                    break
        else:
            for (name, key, items) in self.menuBar:
                if name == 'File':
                    items.append([1, 2, 3, 4, 6])

################################################################################
# standalone program run
################################################################################
def testPopup():
    # see PyView and PyMail for component tests
    root = Tk()
    TextEditorMainPopup(root)
    TextEditorMainPopup(root)
    Button(root, text='More', command=TextEditorMainPopup).pack(fill=X)
    Button(root, text='Quit', command=root.quit).pack(fill=X)
    root.mainloop()

def main(): # may be typed or clicked
    try: # or associated on Windows
        fname = sys.argv[1] # arg = optional filename
    except IndexError: # build in default Tk root
        fname = None
    TextEditorMain(loadFirst=fname).pack(expand=YES, fill=BOTH) # pack optional
    mainloop()

if __name__ == '__main__': # when run as a script
    #testPopup()
    main()







