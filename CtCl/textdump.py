import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime
from itertools import product
from multiprocessing import Process
from threading import Thread
from time import sleep
import io
from copy import deepcopy

class CreateLot():
    #replaces getattr to remove recursion
    def __getattr__(self, item):
        if item in ['__getstate__', '__setstate__']:
            return object.__getattr__(self, item)

    # creates the starting data set and needed data adjustments
    def __init__(self, File_Path_to_Excel, lot_number, step_begin):
        self.lot_number = lot_number
        data = deepcopy(pd.read_excel(File_Path_to_Excel, header=None, dtype=str))


        self.params = data.iloc[5:16, [1, 2, 4, 5, 7, 8]]  # row, column
        self.inputs = data.iloc[16:, [1, 2, 3, 4, 5, 6, 7, 8]]  # row, column
        self.InstructionSet = [(0, 2, 7, 0, 0),
                                 (0, 3, 2, 0, 0),
                                 (0, 4, 2, 0, 0),
                                 (0, 4, 7, 1, 0),
                                 (0, 5, 2, 0, 0),
                                 (0, 5, 7, 1, 0),
                                 (6, 8, 7, 0, 0),
                                 (6, 9, 2, 0, 0),
                                 (6, 10, 2, 0, 0),
                                 (6, 11, 2, 0, 0),
                                 (6, 11, 7, 1, 0),
                                 (6, 12, 7, 0, 0),
                                 (6, 13, 2, 0, 0),
                                 (6, 14, 2, 0, 0),
                                 (6, 15, 2, 0, 0),
                                 (6, 15, 7, 1, 0),
                                 (6, 16, 7, 0, 0),
                                 (6, 17, 2, 0, 1),
                                 (6, 17, 7, 0, 0),
                                 (6, 18, 2, 0, 1),
                                 (6, 18, 7, 1, 0),
                                 (6, 19, 7, 0, 1),
                                 (6, 20, 7, 1, 0),
                                 (21, 23, 7, 0, 0),
                                 (21, 24, 7, 0, 1),
                                 (21, 25, 7, 0, 1),
                                 (21, 26, 7, 0, 1),
                                 (21, 27, 7, 0, 1),
                                 (21, 28, 7, 0, 0),
                                 (21, 29, 7, 0, 1),
                                 (30, 32, 7, 0, 0),
                                 (30, 33, 2, 0, 0),
                                 (30, 34, 2, 0, 0),
                                 (30, 34, 7, 0, 1),
                                 (30, 35, 7, 1, 0),
                                 (30, 36, 2, 0, 0),
                                 (30, 36, 7, 0, 1),
                                 (30, 37, 7, 1, 0),
                                 (30, 38, 2, 0, 0),
                                 (30, 38, 7, 0, 1),
                                 (30, 39, 7, 1, 0),
                                 (30, 41, 7, 0, 0),
                                 (30, 42, 2, 0, 0),
                                 (30, 43, 2, 0, 1),
                                 (30, 43, 7, 1, 0),
                                 (30, 44, 7, 0, 0),
                                 (30, 45, 2, 0, 1),
                                 (30, 46, 7, 1, 0),
                                 (30, 47, 7, 0, 0),
                                 (30, 48, 7, 1, 0),
                                 (30, 49, 7, 0, 0),
                                 (50, 52, 2, 0, 0),
                                 (50, 53, 7, 0, 1),
                                 (50, 54, 7, 0, 0),
                                 (50, 55, 2, 0, 0),
                                 (50, 55, 7, 1, 0),
                                 (50, 56, 7, 0, 0),
                                 (50, 57, 2, 0, 0),
                                 (50, 57, 7, 0, 1),
                                 (50, 58, 7, 0, 1),
                                 (50, 59, 2, 0, 0),
                                 (50, 59, 7, 1, 0),
                                 (50, 60, 7, 0, 1),
                                 (50, 61, 7, 0, 1),
                                 (50, 62, 2, 0, 0),
                                 (50, 62, 7, 1, 0),
                                 (50, 63, 7, 0, 1),
                                 (50, 64, 2, 0, 0),
                                 (50, 64, 7, 0, 1),
                                 (50, 65, 7, 0, 1),
                                 (50, 66, 2, 0, 0),
                                 (50, 66, 7, 1, 0),
                                 (50, 67, 7, 0, 1),
                                 (50, 68, 2, 0, 0),
                                 (50, 68, 7, 0, 1),
                                 (50, 69, 7, 0, 1),
                                 (50, 70, 2, 0, 0),
                                 (50, 70, 7, 1, 0),
                                 (50, 71, 7, 0, 1),
                                 (50, 72, 7, 0, 1),
                                 (50, 73, 2, 0, 0),
                                 (50, 73, 7, 0, 1),
                                 (50, 74, 7, 0, 1),
                                 (50, 75, 7, 1, 0),
                                 (50, 76, 7, 0, 0),
                                 (50, 77, 7, 0, 0)]

        self.step = int(step_begin)
        self.final_step = len(self.InstructionSet)
        self.outputs = [list(range(self.final_step)),
                        [0]*self.final_step,
                        [0]*self.final_step,
                        [0]*self.final_step,
                        [0]*self.final_step,
                        [0]*self.final_step]  # step_num, step_desc, expected_value, value, start, end
        i = 0
        for _, row, input_position, is_timed, is_checkmark in self.InstructionSet:
            self.outputs[1][i] =(
                " ".join(self.inputs.iloc[row, range(2) if input_position == 2 else range(3, 7)].dropna().to_list()))
            self.outputs[2][i] =("X" if is_checkmark else self.inputs.iloc[row, input_position-1])
            i+=1

        self.step -= 1  # we consider the chem page to be a negative one step

    #runs the script
    def runRecipe(self):
        recipe = Recipe(self)
        recipe.mainloop()
        recipe.destroy()
        return self.outputs




class Recipe(tk.Tk):
    # replaces getattr to remove recursion
    def __getattr__(self, item):
        if item in ['__getstate__', '__setstate__']:
            return object.__getattr__(self, item)
    # __init__ function for class tkinterApp
    def __init__(self, parent):

        self.params = parent.params
        self.inputs = parent.inputs
        self.InstructionSet = parent.InstructionSet
        self.outputs = parent.outputs
        self.step = parent.step
        self.final_step = parent.final_step

        # __init__ function for class Tk
        tk.Tk.__init__(self)
        # creating a container
        self.title(parent.lot_number)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in [ChemPage]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ChemPage)

    # quits and/or prints variables to an excel file
    def FinishUp(self):
        print(self.outputs[3])
        self.quit()

    # loads up the next instruction set
    def refresh(self, cont):
        for widgets in self.winfo_children():
            widgets.destroy()
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        frame = cont(container, self)
        self.frames = {cont: frame}
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(cont)

    # display current frame passed
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # function for chems page text boxes
    def writeChemsInfo(self, entry):
        for (i, j) in product(range(6), range(11)):
            self.params.iloc[j, i] = entry[(i, j)].get()
        self.InstructionCheck()

    # resets the timer
    def startTime(self, label):  # this records the box info
        self.outputs[4][self.step] = datetime.now()  # records current time
        label.configure(text = datetime.now().strftime("%H:%M:%S"))
        self.update()

    # writes the text box to output
    def writeInfo(self, entry):  # this records the box info
        self.outputs[3][self.step] = entry.get()
        self.outputs[5][self.step] = datetime.now()
        self.InstructionCheck()

    # writes the time to output
    def timeInfo(self):  # this records the box info
        self.outputs[3][self.step] = (datetime.now() - self.outputs[4][self.step]) / 60 # in minutes
        self.outputs[5][self.step] = datetime.now()
        self.InstructionCheck()

    # writes an X to output
    def checkboxInfo(self):  # this records the box info
        self.outputs[3].append("X")
        self.outputs[5][self.step] = datetime.now()
        self.InstructionCheck()

    # quick check to see if we should kill the script
    def InstructionCheck(self):
        self.step += 1
        if self.step == self.final_step:
            self.FinishUp()
        else:
            self.outputs[4][self.step] = datetime.now()
            self.refresh(InstructionPage)


class ChemPage(tk.Frame):
    def __init__(self, parent, controller):
        # define the frame
        tk.Frame.__init__(self, parent)

        # Just the top label
        label = ttk.Label(self, text="Chem Info")
        label.grid(row=0, column=0, padx=10, pady=10)
        # define the column names
        label_array = {}
        text_array = ['Chems:', 'Part#:', 'Supplier:', 'Lot#:', 'Open Date:', 'Amount:']
        for i in range(6):
            label_array[i] = tk.Label(self, text=text_array[i])
            label_array[i].grid(row=1, column=i, padx=10, pady=10)
        # creates a matrix of text box inputs
        entry = {}
        for (i, j) in product(range(6), range(11)):
            text = tk.StringVar(self)
            text.set("" if pd.isna(controller.params.iloc[j, i]) else controller.params.iloc[j, i])

            entry[(i, j)] = tk.Entry(self, textvariable=text)
            entry[(i, j)].grid(row=1 + j, column=i, padx=10, pady=10)
        # creates a button which saves those inputs and moves on
        button = ttk.Button(self, text="Next", command=lambda: controller.writeChemsInfo(entry))
        button.grid(row=0, column=1, padx=10, pady=10)


class InstructionPage(tk.Frame):
    def __init__(self, parent, controller):

        # unpack instructions
        instruction_row, row, input_position, is_timed, is_checkmark = controller.InstructionSet[controller.step-1]

        # create the frame
        tk.Frame.__init__(self, parent)
        # label which step
        label = ttk.Label(self, text="Instructions step " + str(controller.step))
        label.grid(row=0, column=0, padx=10, pady=10)

        # labels the subsection
        text = controller.inputs.iloc[instruction_row, 0]
        label_subsection = tk.Label(self, text=text)
        label_subsection.grid(row=0, column=5, padx=10, pady=10)

        # labels the columns and rows
        columns = {}
        label_row = {}
        for i in range(8):
            text = "" if pd.isna(controller.inputs.iloc[instruction_row + 1, i]) else controller.inputs.iloc[
                instruction_row + 1, i]
            columns[i] = tk.Label(self, text=text)
            columns[i].grid(row=1, column=i, padx=10, pady=10)

            text = "" if pd.isna(controller.inputs.iloc[row, i]) else controller.inputs.iloc[row, i]
            label_row[i] = tk.Label(self, text=text)
            label_row[i].grid(row=2, column=i, padx=10, pady=10)

        # what type of instruction set are we looking at
        if is_checkmark:  # prints a button
            button = ttk.Button(self, text="Next", command=lambda: controller.checkboxInfo())
            button.grid(row=0, column=1, padx=10, pady=10)

        elif is_timed:  # prints start time and two buttons
            text = tk.StringVar(self, name="timer")
            label_timer = tk.Label(self)
            label_timer.grid(row=0, column=4, padx=10, pady=10)
            controller.startTime(label_timer)

            button1 = ttk.Button(self, text="Start", command=lambda: controller.startTime(label_timer))
            button2 = ttk.Button(self, text="Next", command=lambda: controller.timeInfo())
            button1.grid(row=0, column=2, padx=10, pady=10)
            button2.grid(row=0, column=1, padx=10, pady=10)

        else:  # This prints the text box and a button
            text = tk.StringVar()
            text.set("" if pd.isna(controller.inputs.iloc[row, input_position]) else controller.inputs.iloc[
                row, input_position])

            entry = tk.Entry(self, textvariable=text)
            entry.grid(row=2, column=input_position, padx=10, pady=10)

            button = ttk.Button(self, text="Next", command=lambda: controller.writeInfo(entry))
            button.grid(row=0, column=1, padx=10, pady=10)

if __name__ == "__main__":
    File_Path_to_Excel = r'C:\Users\brody.westberg\OneDrive - Thermo Fisher Scientific\Documents\SMP Batch Run Sheet.xlsx'
    lot_number = "2021-15-xxx"
    step_begin = 84

    l1 = CreateLot(File_Path_to_Excel, lot_number, step_begin)
    lot_1 = Process(target = l1.runRecipe)
    lot_1.start()

    l2 = CreateLot(File_Path_to_Excel, "test", step_begin)
    lot_2 = Process(target = l2.runRecipe)
    lot_2.start()

    lot_1.join()
    lot_2.join()
    ######################################Your struggling to get the output of this thread
    print(lot_1,lot_2)


    #lot = CreateLot(File_Path_to_Excel, lot_number, step_begin)
    #lot.runRecipe()
    #print(lot.outputs)
