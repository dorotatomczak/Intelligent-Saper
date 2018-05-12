from tkinter import *

class TrainingSettingsDialog(Toplevel):

    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        self.title = "Training Settings"
        self.parent = parent
        self.result = {'Games': 1000, 'minHeight': 5, 'maxHeight': 10,
                       'minWidth': 5, 'maxWidth': 10, 'minBombs': 1, 'maxBombs': 5}
        self.predicates_method = False
        self.canceled = False
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        Label(master, text="Games (1-1000):").grid(row=0)
        Label(master, text="Height (1-20):").grid(row=1)
        Label(master, text="Width (1-20):").grid(row=2)
        Label(master, text="Bombs (1-20):").grid(row=3)

        self.e1 = Entry(master)
        self.e2a = Entry(master)
        self.e2b = Entry(master)
        self.e3a = Entry(master)
        self.e3b = Entry(master)
        self.e4a = Entry(master)
        self.e4b = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2a.grid(row=1, column=1)
        self.e2b.grid(row=1, column=2)
        self.e3a.grid(row=2, column=1)
        self.e3b.grid(row=2, column=2)
        self.e4a.grid(row=3, column=1)
        self.e4b.grid(row=3, column=2)

        # default values
        self.e1.insert(END, "1000")
        self.e2a.insert(END, "5")
        self.e2b.insert(END, "10")
        self.e3a.insert(END, "5")
        self.e3b.insert(END, "10")
        self.e4a.insert(END, "1")
        self.e4b.insert(END, "5")
        return self.e1  # initial focus

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="Predicates", width=10, command=self.predicates_ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Neural Network", width=14, command=self.neural_ok)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def predicates_ok(self, event=None):
        self.predicates_method = True
        self.ok()

    def neural_ok(self, event=None):
        self.predicates_method = False
        self.ok()

    def close(self):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def ok(self):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.close()

    def cancel(self, event=None):
        self.canceled = True
        self.close()

    def validate(self):
        try:
            int(self.e1.get())
            int(self.e2a.get())
            int(self.e2b.get())
            int(self.e3a.get())
            int(self.e3b.get())
            int(self.e4a.get())
            int(self.e4b.get())
        except ValueError:
            return False

        if int(self.e1.get()) < 1 or int(self.e1.get()) > 1000:
            return False

        if int(self.e2a.get()) < 1 or int(self.e2a.get()) > 20:
            return False
        if int(self.e2b.get()) < 1 or int(self.e2b.get()) > 20:
            return False
        if int(self.e2a.get()) > int(self.e2b.get()):
            return False

        if int(self.e3a.get()) < 1 or int(self.e3a.get()) > 20:
            return False
        if int(self.e3b.get()) < 1 or int(self.e3b.get()) > 20:
            return False
        if int(self.e3a.get()) > int(self.e3b.get()):
            return False

        if int(self.e4a.get()) < 1 or int(self.e4a.get()) > 20:
            return False
        if int(self.e4b.get()) < 1 or int(self.e4b.get()) > 20:
            return False
        if int(self.e4a.get()) > int(self.e4b.get()):
            return False

        return True

    def apply(self):
        self.result['Games'] = int(self.e1.get())
        self.result['minHeight'] = int(self.e2a.get())
        self.result['maxHeight'] = int(self.e2b.get())
        self.result['minWidth'] = int(self.e3a.get())
        self.result['maxWidth'] = int(self.e3b.get())
        self.result['minBombs'] = int(self.e4a.get())
        self.result['maxBombs'] = int(self.e4b.get())
