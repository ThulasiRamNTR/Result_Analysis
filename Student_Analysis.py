import tkinter as tk
from tkinter.ttk import Notebook #For creating tabs
import tkinter.messagebox as msg #For poping up messageboxes
import numpy as np
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd


colour_schemes = [{"bg":"lightgrey", "fg":"black"}, {"bg":"grey", "fg":"white"}]
semesters = [(1, "Semester 1"), (2, "Semester 2"), (3, "Semester 3"), (4, "Semester 4"), (5, "Semester 5"), (6, "Semester 6"), (7, "Semester 7"), (8, "Semester 8")]
grade_credit_value = {"S" : 10, "A": 9, "B" : 8, "C": 7, "D": 6, "E": 5, "U": 0, "s" : 10, "a": 9, "b" : 8, "c": 7, "d": 6, "e": 5, "u": 0}
regulation_departments_semester = {2008:{},

 2013:{"CSE":{1:[["Technical English - 1", 4], ["Mathematics -1", 4], ["Engineering Physics", 3], ["Engineering Chemistry", 3], ["Computer Programming", 3], ["Engineering Graphics", 4], ["Computer Practices Laboratory", 2], ["Engineering Practices Laboratory", 2], ["Physics and Chemistry Laboratory", 1]],
 2:[["Technical English - 2", 4], ["Mathematics - 2", 4], ["Engineering Physics - 2", 3], ["Enginnering Chemistry - 2", 3], ["Digital Principles and System Design", 3], ["Programming and Data Structures - 1", 3], ["Physics and Chemistry Laboratory - 2", 1], ["Digital Laboratory", 2], ["Programming and Data Structures Laboratory - 1", 2]],
 3:[["Transforms and Partial Differential Equations", 4], ["Programming and Data Structures - 2",3],["Database Management Systems", 3], ["Computer Architecture", 3], ["Analog and Digital Communication", 3],["Environmental Science and Engineering", 3], ["Programming and Data Structures Laboratory - 2", 2], ["Database Management Systems Laboratory", 2]],
 4:[["Probablity and Queuing Theory", 4], ["Computer Networks", 3], ["Operating Systems", 3], ["Design and Analysis of Algorithms", 3], ["Microprocessor and Microcontroller", 3], ["Software Engineering", 3], ["Networks Laboratory", 2], ["Microprocessor and Microcontroller Laboratory", 2], ["Operating Systems Laboratory", 2]],
 5:[["Discrete Mathematics", 4], ["Internet Programming", 4], ["Object Oriented Analysis and Design", 3], ["Theory of Computation", 3], ["Computer Graphics", 3], ["Case Tools Laboratory", 2], ["Internet Programming Laboratory", 2], ["Computer Graphics Laboratory", 2]],
 6:[["Distributed Systems", 3], ["Mobile COmputing", 3], ["Compiler Design", 3], ["Digital Signal Processing", 4], ["Artificial Intelligence", 3], ["Elective - 1", 3], ["Mobile Application Development Laboratory", 2], ["Compiler Laboratory", 2], ["Communication and Soft Skills - Laboratory Based", 2]],
 7:[["Cryptography and Network Security", 3], ["Graph Theory and Applications", 3], ["Grid and Cloud Computing", 3], ["Resource Management Techniques", 3], ["Elective - 2", 3], ["Elective - 3", 3], ["Security Laboratory", 2], ["Grid and Cloud Computing Laboratory", 2]],
 8:[["Multi - Core Architectures and Programming", 3], ["Elective - 4", 3], ["Elective - 5", 3], ["Project Work", 6]],
            },
        "IT":{},
        "EEE":{},
        "ECE":{},
        "EIE":{}
 },

 2018:{}}

class GPA_Calculator(tk.Toplevel):
    """
    Calculates the GPA of an individual user
    Expects input of :
        - Regulation
        - Department
        - Semesters
        - Grades obtained in each subject
    Gives the output of GPA of the individual user
    """

    def __init__(self):
        """
        Initializes the Toplevel GPA Calculator Window.
        Initializes the Tkinter variables for holding the regulation, department, semester of the current user
        """

        tk.Toplevel.__init__(self)

        self.title("GPA Calculator")
        self.geometry("600x600")

        self.regulation = tk.IntVar()
        self.regulation.set(2013)
        self.department = tk.StringVar()
        self.department.set("CSE")
        self.semester = tk.IntVar()
        self.semester.set(1)

        self.gpa_frame = tk.Frame(self)
        self.gpa_frame.pack()

        #Initializing the gpa_calculator_tab
        self.initialize_gpa_calculator()

    def initialize_gpa_calculator(self):
        """
        Creates the widgets for getting user inputs:
            - Regulation
            - Department
            - Semester
        """

        self.gpa_regulation_frame = tk.Frame(self.gpa_frame) #Frame for gpa regulation
        self.gpa_department_frame = tk.Frame(self.gpa_frame) #Frame for gpa department
        self.gpa_semester_frame = tk.Frame(self.gpa_frame) #Frame for gpa semester
        self.gpa_subjects_frame = tk.Frame(self.gpa_frame) #Frame for gpa subjects
        self.display_frame = tk.Frame(self.gpa_frame) #Frame for displaying the subjects and grade input bar

        """Regulation Widgets """
        self.gpa_regulation_label = tk.Label(self.gpa_regulation_frame, text = "Select your Syllabus Regulation", bg = "grey", fg ="white")
        self.gpa_regulation_2008 = tk.Radiobutton(self.gpa_regulation_frame, text = "Regulation 2008", variable = self.regulation, value = 2008, indicatoron = 0)
        self.gpa_regulation_2013 = tk.Radiobutton(self.gpa_regulation_frame, text = "Regulation 2013", variable = self.regulation, value = 2013, indicatoron = 0)
        self.gpa_regulation_2018 = tk.Radiobutton(self.gpa_regulation_frame, text = "Regulation 2018", variable = self.regulation, value = 2018, indicatoron = 0)

        """Department Widgets """
        self.gpa_department_label = tk.Label(self.gpa_department_frame, text = "Select your Department", bg="grey", fg = "white")
        self.gpa_department_CSE = tk.Radiobutton(self.gpa_department_frame, text = "CSE", variable = self.department, value = "CSE", indicatoron = 0)
        self.gpa_department_IT = tk.Radiobutton(self.gpa_department_frame, text = "IT", variable = self.department, value = "IT", indicatoron = 0)
        self.gpa_department_EEE = tk.Radiobutton(self.gpa_department_frame, text = "EEE", variable = self.department, value = "EEE", indicatoron = 0)
        self.gpa_department_ECE = tk.Radiobutton(self.gpa_department_frame, text = "ECE", variable = self.department, value = "ECE", indicatoron = 0)
        self.gpa_department_EIE = tk.Radiobutton(self.gpa_department_frame, text = "EIE", variable = self.department, value = "EIE", indicatoron = 0)

        """Semester Widgets """
        self.gpa_semester_label = tk.Label(self.gpa_semester_frame, text = "Select your Semester", bg = "grey", fg ="white")

        """Creating buttons to display subjects_grade_frame"""
        self.gpa_display_frame_button = tk.Button(self.gpa_frame, text = "Display Subjects", command = self.display_subjects)
        self.gpa_frame.bind('<Return>', self.display_subjects)

        """Subjects Widgets"""
        self.gpa_subjects_label = tk.Label(self.gpa_subjects_frame, text = "Enter your Subjects Grade", bg = "grey", fg = "white")

        #Styling the frames
        self.gpa_frame['borderwidth'] = 5

        self.gpa_regulation_frame['borderwidth'] = 5
        self.gpa_department_frame['borderwidth'] = 5
        self.gpa_semester_frame['borderwidth'] = 5
        self.gpa_subjects_frame['borderwidth'] = 5
        self.gpa_display_frame_button['borderwidth'] = 5

        #Packing the widgets
        self.gpa_regulation_frame.pack()
        self.gpa_department_frame.pack()
        self.gpa_semester_frame.pack()
        self.gpa_display_frame_button.pack()
        self.gpa_subjects_frame.pack()

        self.gpa_regulation_label.pack(side = tk.TOP, fill = tk.X)
        self.gpa_regulation_2008.pack(side = tk.LEFT)
        self.gpa_regulation_2013.pack(side = tk.LEFT)
        self.gpa_regulation_2018.pack(side = tk.LEFT)

        self.gpa_department_label.pack(side = tk.TOP, fill = tk.X)
        self.gpa_department_CSE.pack(side = tk.LEFT)
        self.gpa_department_IT.pack(side = tk.LEFT)
        self.gpa_department_EEE.pack(side = tk.LEFT)
        self.gpa_department_ECE.pack(side = tk.LEFT)
        self.gpa_department_EIE.pack(side = tk.LEFT)

        self.gpa_semester_label.pack(side = tk.TOP, fill = tk.X)
        for sem, text in semesters:
            self.semester_radiobutton = tk.Radiobutton(self.gpa_semester_frame, text = text, variable = self.semester, value = sem, indicatoron = 0)
            self.semester_radiobutton.pack(side = tk.LEFT)

        self.gpa_subjects_label.pack(side = tk.TOP, fill = tk.X)


    def display_subjects(self, event = None):
        """
        It displays the subject of the user input Regulation, Department,Semester in the following format:
            - Subject name label : Subject Grade Entry Field
        """

        self.subjects_credits = np.array(regulation_departments_semester[self.regulation.get()][self.department.get()][self.semester.get()])

        self.subjects_name = np.array(self.subjects_credits[...,0])
        self.subject_credit = np.array(self.subjects_credits[...,1], dtype = int)


        """Subject Display Widget"""
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        self.display_frame.pack()

        self.subject_entry = []
        self.subject_entry_grade = []

        index = 0
        for subject,credit in self.subjects_credits:
            self.grade_var = tk.StringVar()
            self.subject_entry_grade.append(self.grade_var)

            self.subject_label = tk.Label(self.display_frame, text = subject)
            self.grade_entry = tk.Entry(self.display_frame, textvariable = self.subject_entry_grade[index])

            self.current_subject_entry = [self.subject_label, self.grade_entry]
            self.subject_entry.append(self.current_subject_entry)

            index += 1

        index = 0
        for label, entry in self.subject_entry:
            label.grid(row = index)
            entry.grid(row = index, column = 1)
            index += 1


        self.display_frame['borderwidth'] = 10

        self.calculate_gpa = tk.Button(self.display_frame, text = "Calculate GPA", command = self.gpa_calculation)
        self.calculate_gpa['borderwidth'] = 5
        self.calculate_gpa.grid(row = index, columnspan = 2)


    def gpa_calculation(self):
        """
        Calculates the GPA for the user who has provided the obtained subject grades in various Entry Fields of each Subject
        The Output GPA is displayed as a pop-up message
        """
        self.grade_credits = np.array([grade_credit_value[self.subject_entry_grade[index].get()] for index in range(len(self.subject_entry_grade))])

        self.cgp_product_sum = sum(self.grade_credits * self.subject_credit)
        self.credit_sum = round(sum(self.subject_credit), 3)

        self.gpa = self.cgp_product_sum / self.credit_sum

        msg.showinfo("GPA", self.gpa)


class CGPA_Calculator(tk.Toplevel):
    """
    Calculates the CGPA of an individual user
    Expects input of :
        - Regulation
        - Department
        - Semesters
        - Grades obtained in each subject
    Gives the output of CGPA of the individual user
    """

    def __init__(self):
        """
        Initializes the Toplevel CGPA Calculator Window.
        Initializes the Tkinter variables for holding the regulation, department, semester of the current user
        """

        tk.Toplevel.__init__(self)

        self.title("CGPA Calculator")
        self.geometry("600x600")

        self.regulation = tk.IntVar()
        self.regulation.set(2013)
        self.department = tk.StringVar()
        self.department.set("CSE")
        self.semester = tk.IntVar()
        self.semester.set(1)

        self.cgpa_frame = tk.Frame(self)
        self.cgpa_frame.pack()

        #Initializing the cgpa_calculator
        self.initialize_cgpa_calculator()


    def initialize_cgpa_calculator(self):
        """
        Creates the widgets for getting user inputs:
            - Regulation
            - Department
            - Semester
        """
        self.cgpa_regulation_frame = tk.Frame(self.cgpa_frame) #Frame for cgpa regulation
        self.cgpa_department_frame = tk.Frame(self.cgpa_frame) #Frame for cgpa department
        self.cgpa_semester_frame = tk.Frame(self.cgpa_frame) #Frame for cgpa semester
        self.cgpa_subjects_frame = tk.Frame(self.cgpa_frame) #Frame for cgpa subjects
        self.display_sem_frame = tk.Frame(self.cgpa_subjects_frame) #Frame for semesters and gpa input bar

        """Regulation Widgets """
        self.cgpa_regulation_label = tk.Label(self.cgpa_regulation_frame, text = "Select your Syllabus Regulation", bg = "grey", fg ="white")
        self.cgpa_regulation_2008 = tk.Radiobutton(self.cgpa_regulation_frame, text = "Regulation 2008", variable = self.regulation, value = 2008, indicatoron = 0)
        self.cgpa_regulation_2013 = tk.Radiobutton(self.cgpa_regulation_frame, text = "Regulation 2013", variable = self.regulation, value = 2013, indicatoron = 0)
        self.cgpa_regulation_2018 = tk.Radiobutton(self.cgpa_regulation_frame, text = "Regulation 2018", variable = self.regulation, value = 2018, indicatoron = 0)

        """Department Widgets """
        self.cgpa_department_label = tk.Label(self.cgpa_department_frame, text = "Select your Department", bg="grey", fg = "white")
        self.cgpa_department_CSE = tk.Radiobutton(self.cgpa_department_frame, text = "CSE", variable = self.department, value = "CSE", indicatoron = 0)
        self.cgpa_department_IT = tk.Radiobutton(self.cgpa_department_frame, text = "IT", variable = self.department, value = "IT", indicatoron = 0)
        self.cgpa_department_EEE = tk.Radiobutton(self.cgpa_department_frame, text = "EEE", variable = self.department, value = "EEE", indicatoron = 0)
        self.cgpa_department_ECE = tk.Radiobutton(self.cgpa_department_frame, text = "ECE", variable = self.department, value = "ECE", indicatoron = 0)
        self.cgpa_department_EIE = tk.Radiobutton(self.cgpa_department_frame, text = "EIE", variable = self.department, value = "EIE", indicatoron = 0)

        """Semester Widgets """
        self.cgpa_semester_label = tk.Label(self.cgpa_semester_frame, text = "Select your Semester", bg = "grey", fg ="white")

        """Creating buttons to display semester_cgpa_frame"""
        self.cgpa_display_frame_button = tk.Button(self.cgpa_frame, text = "Display Semesters", command = self.display_semester)

        """Subjects Widgets"""
        self.cgpa_subjects_label = tk.Label(self.cgpa_subjects_frame, text = "Enter your Subjects Grade", bg = "grey", fg = "white")


        #Styling the frames
        self.cgpa_frame['borderwidth'] = 5

        self.cgpa_regulation_frame['borderwidth'] = 5
        self.cgpa_department_frame['borderwidth'] = 5
        self.cgpa_semester_frame['borderwidth'] = 5
        self.cgpa_subjects_frame['borderwidth'] = 5
        self.cgpa_display_frame_button['borderwidth'] = 5

        #Packing the widgets
        self.cgpa_regulation_frame.pack()
        self.cgpa_department_frame.pack()
        self.cgpa_semester_frame.pack()
        self.cgpa_display_frame_button.pack()
        self.cgpa_subjects_frame.pack()

        self.cgpa_regulation_label.pack(side = tk.TOP, fill = tk.X)
        self.cgpa_regulation_2008.pack(side = tk.LEFT)
        self.cgpa_regulation_2013.pack(side = tk.LEFT)
        self.cgpa_regulation_2018.pack(side = tk.LEFT)

        self.cgpa_department_label.pack(side = tk.TOP, fill = tk.X)
        self.cgpa_department_CSE.pack(side = tk.LEFT)
        self.cgpa_department_IT.pack(side = tk.LEFT)
        self.cgpa_department_EEE.pack(side = tk.LEFT)
        self.cgpa_department_ECE.pack(side = tk.LEFT)
        self.cgpa_department_EIE.pack(side = tk.LEFT)

        self.cgpa_semester_label.pack(side = tk.TOP, fill = tk.X)

        for sem, text in semesters:
            self.semester_radiobutton = tk.Radiobutton(self.cgpa_semester_frame, text = text, variable = self.semester, value = sem, indicatoron = 0)
            self.semester_radiobutton.pack(side = tk.LEFT)

        self.cgpa_subjects_label.pack(side = tk.TOP, fill = tk.X)


    def display_semester(self):
        """
        It displays the semester of the user input Regulation, Department,Semester in the following format:
            - Semester name label : GPA Entry Field
        """
        self.subjects_credits = np.array(regulation_departments_semester[self.regulation.get()][self.department.get()][self.semester.get()])

        self.credit_value = np.array(self.subjects_credits[...,1], dtype = int)

        """Subject Display Widget"""
        for widget in self.display_sem_frame.winfo_children():
            widget.destroy()
        self.display_sem_frame.pack()

        self.semester_entry = []
        self.semester_gpa_entry = []
        index = 0

        for sem,name in semesters:
            self.gpa_var = tk.DoubleVar()
            self.semester_gpa_entry.append(self.gpa_var)

            self.semester_label = tk.Label(self.display_sem_frame, text = name)
            self.gpa_entry = tk.Entry(self.display_sem_frame, textvariable = self.semester_gpa_entry[index])

            self.current_semester_entry = [self.semester_label, self.gpa_entry]
            self.semester_entry.append(self.current_semester_entry)

            index += 1

            if sem >= self.semester.get():
                break

        index = 0
        for sem, gpa_entry in self.semester_entry:
            sem.grid(row = index)
            gpa_entry.grid(row = index, column = 1)
            index += 1


        self.display_sem_frame['borderwidth'] = 10

        self.calculate_cgpa = tk.Button(self.display_sem_frame, text = "Calculate CGPA", command = self.cgpa_calculation)
        self.calculate_cgpa['borderwidth'] = 5
        self.calculate_cgpa.grid(row = index, columnspan = 2)


    def cgpa_calculation(self):
        """
        Calculates the CGPA for the user who has provided the obtained semester GPA in various Entry Fields of each Subject
        The Output CGPA is displayed as a pop-up message
        """
        self.sem_gpa_total = 0 #Calculates the sum of (subject_grade_value * subject_credit) for a particular semester
        self.credit_value_total = 0 #Sum of sem_gpa_total of all semesters
        self.credit_total = 0 #Sum of subject_credit of all subjects in all semesters
        for current_sem in range(self.semester.get()):
            self.credit_total += sum([credit for subject,credit in regulation_departments_semester[self.regulation.get()][self.department.get()][current_sem+1]])

        for current_sem in range(len(self.semester_gpa_entry)):
            self.sem_gpa_total = self.semester_gpa_entry[current_sem].get() * sum([credit for subject,credit in regulation_departments_semester[self.regulation.get()][self.department.get()][current_sem+1]])
            self.credit_value_total += self.sem_gpa_total

        self.cgpa = round(self.credit_value_total / self.credit_total, 3)

        msg.showinfo("CGPA", self.cgpa)





class Plot_Window(tk.Toplevel):
    """
    """
    def __init__(self, fig, master = None):
        tk.Toplevel.__init__(self)

        self.title("Analysis Plot")
        self.geometry("600x600")

        self.canvas = FigureCanvasTkAgg(fig, master = self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        self.canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

        self.canvas.mpl_connect("key_press_event", self.on_key_press)

    def on_key_press(self, event):
        """
        """
        print("you pressed {}".format(event.key))
        key_press_handler(event, self.canvas, self.toolbar)

    def quit(self):
        """
        """
        self.quit()
        self.destroy()


class Analysis(tk.Toplevel):
    """
    Initializes the Analysis Window
    It contains a Notebook for holding the following tabs:
        - Department Analysis tab
    """
    def __init__(self):
        """
        """
        tk.Toplevel.__init__(self)

        self.title("Analysis")
        self.geometry("600x600")

        self.analysis_notebook = Notebook(self)

        self.dept_analysis_frame = tk.Frame(self)

        self.add_file_name_frame()

        self.analysis_notebook.add(self.dept_analysis_frame, text = "Dept-Analysis")
        self.analysis_notebook.pack(fill = tk.BOTH, expand = 1)



    def sin_test_function(self):
        """
        """

        self.fig = Figure(figsize=(5,4), dpi=1000)
        self.t = np.arange(0,3,.01)
        a = self.fig.add_subplot(111)
        a.plot(self.t, 2* np.sin(2 * np.pi * self.t))

        self.sin_test_plot = Plot_Window(self.fig, master = self)

    def gpa_statistics_function(self):
        """

        """

        self.gpa_statistics_fig = Figure(figsize=(5,4), dpi = 1000)
        self.data.iloc[:,0]=self.data.iloc[:,0]%1000
        plt.xlabel('Reg.No.')
        plt.ylabel('GPA')
        plt.title('GPA-Statistics')
        plt.plot(self.data.iloc[:114,0],self.data.iloc[:114,-1])
        plt.show()

        #self.gpa_statistics_plot = Plot_Window(self.gpa_statistics_fig, master = self)

    def subject_analysis_statistics_function(self):
        """
        """
        self.data.iloc[:,0]=self.data.iloc[:,0]%1000
        plt.title(self.data.columns.values[5])
        plt.xlabel('Grade')
        plt.ylabel('Reg.No')
        plt.scatter(self.data.iloc[:114,5],self.data.iloc[:114,0])
        plt.show()


    def gender_analysis_statistics_function(self):
        """
        """
        self.data.iloc[:,0]=self.data.iloc[:,0]%1000
        self.data=self.data.iloc[:114,:]
        male=self.data.loc[self.data['Gender']=='M']
        female=self.data.loc[self.data['Gender']=='F']
        plt.xlabel('GPA')
        plt.ylabel('Reg. No.')
        plt.scatter(male.iloc[:114,-1],male.iloc[:114,0],label='Male')
        plt.scatter(female.iloc[:114,-1],female.iloc[:114,0],label='Female')
        plt.legend()
        plt.show()


    def add_analysis_button_frames(self):
        """
        It consists of a series of button for generating various plots to visualize the data-sets.
        The series of plots visualizing buttons are as follows:
            - GPA_Statistics
            - Subject_Analysis
        """

        self.analysis_button_frame = tk.Frame(self.dept_analysis_frame, borderwidth = 5)


        self.sin_test_button = tk.Button(self.analysis_button_frame, text = "test", borderwidth = 5, command = self.sin_test_function)
        #self.sin_test_button.pack(side = tk.LEFT)

        #Add other buttons for respective analysis and add its respective functions

        self.gpa_statistics = tk.Button(self.analysis_button_frame, text = "GPA_Statistics", borderwidth = 5, command = self.gpa_statistics_function)
        self.gpa_statistics.pack(side = tk.TOP)

        self.subject_analysis_frame = tk.Frame(self.analysis_button_frame)
        self.subject_analysis_frame.pack()

        self.subject_variable = tk.StringVar()
        self.subject_variable.set("EE6401")

        self.subject_label = tk.Label(self.subject_analysis_frame, text = "Select your subjects")


        self.subject_analysis_statistics = tk.Button(self.analysis_button_frame, text = "Subject_Analysis_Statistics", borderwidth = 5, command = self.subject_analysis_statistics_function)
        self.subject_analysis_statistics.pack(side = tk.TOP)

        self.gender_analysis_statistics = tk.Button(self.analysis_button_frame, text = "Gender_Analysis_Statistics", borderwidth = 5, command = self.gender_analysis_statistics_function)
        self.gender_analysis_statistics.pack(side = tk.TOP)


        self.analysis_button_frame.pack()


    def read_excel_file(self):
        """

        """
        self.data = pd.read_excel(self.excel_file_name)


    def open_excel_file(self):
        self.excel_file_name = filedialog.askopenfilename() #self.excel_file_name is the excel file_name that user has selected

        while self.excel_file_name and not self.excel_file_name.endswith(".xlsx"):
            msg.showerror("Wrong FileType", "Please select an excel file!")
            self.excel_file_name = filedialog.askopenfilename()

        if self.excel_file_name:
            self.file_name_var.set(self.excel_file_name)
            msg.showinfo("Success", "Excel file successfully opened")

        #your function call for doing the excel reading part (importing of data from excel file )
        self.read_excel_file()

        self.add_analysis_button_frames()


    def add_file_name_frame(self):
        """
        """
        self.file_name_frame = tk.Frame(self.dept_analysis_frame, borderwidth = 5)
        self.file_name_frame.pack()
        self.open_file_button = tk.Button(self.file_name_frame, text = "Open Excel File for Analysis", command = self.open_excel_file, borderwidth = 5)
        self.open_file_button.pack(side = tk.TOP)

        self.file_name_var = tk.StringVar()
        self.file_name_var.set("No Excel File Selected, Select an excel file for doing the analysis")

        self.file_name_label = tk.Label(self.file_name_frame, textvariable = self.file_name_var, bg = "grey", fg = "black")
        self.file_name_label.pack(side = tk.TOP, fill = tk.X)





class Student_Analysis(tk.Tk):
    def __init__(self):
        """
        Initializes the Student Analysis Window.
        It contains :
            - File Menubar.
            - GPA and CGPA Calculator Window emulating buttons.
        """

        super().__init__()

        #Window geometry and title
        self.title("Student Analysis")
        self.geometry("600x600")
        self.resizable(False, False)

        #Creating the File Menu
        self.create_file_menu()

        self.add_task_frames()


    def create_file_menu(self):
        """
        Creates the File Menu.
        File Menu consists of sub-menu's like:
            -> File Menu
                It consists of following options:
                    - Open
                    - Save
            -> Insert Menu
                It consists of following options:
                    - Insert
            -> Analysis Menu
            -> Help Menu
        """
        #Creating Menubar to hold the Menu's
        self.menu_bar = tk.Menu(self, bg="lightgrey", fg="black")

        #Creating File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff = 0, bg = "lightgrey", fg = "black")
        self.file_menu.add_command(label = "Open", command = lambda e: None, accelerator="Ctrl+O")
        self.file_menu.add_command(label = "Save", command = lambda e: None, accelerator="Ctrl+S")

        #Creating Insert Menu
        self.insert_menu = tk.Menu(self.menu_bar, tearoff=0, bg="lightgrey", fg="black")
        self.insert_menu.add_command(label = "Insert", command = lambda e: None, accelerator="Ctrl+I")

        #Creating Analysis Menu
        self.analysis_menu = tk.Menu(self.menu_bar, tearoff=0, bg="lightgrey", fg="black")

        #Creating help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0, bg="lightgrey", fg="black")

        #Adding sub-menus to MenuBar
        self.menu_bar.add_cascade(label = "File", menu = self.file_menu)
        self.menu_bar.add_cascade(label = "Insert", menu = self.insert_menu)
        self.menu_bar.add_cascade(label = "Analysis", menu = self.analysis_menu)
        self.menu_bar.add_cascade(label = "Help", menu = self.help_menu)

        self.config(menu=self.menu_bar)


    def add_task_frames(self):
        """
        Adds the tasks Frames to the window
        Task Frame consist of GPA CGPA Button for opening the GPA Calculator and CGPA Calculator window to
            calculate the GPA and CGPA of an individual user respectively.
        """
        #GPA_CGPA Calculator Frame
        self.calc_frame = tk.Frame(self, width = 100, height = 600, borderwidth = 5)
        self.gpa_calc_button = tk.Button(self.calc_frame, text = "GPA", command = self.gpa_calculator, borderwidth = 5)
        self.cgpa_calc_button = tk.Button(self.calc_frame, text = "CGPA", command = self.cgpa_calculator, borderwidth = 5)
        self.gpa_calc_button.pack(side=tk.LEFT)
        self.cgpa_calc_button.pack(side=tk.LEFT)
        self.calc_frame.pack()

        #Analysis Frame
        self.analysis_frame = tk.Frame(self, width = 100, height = 600, borderwidth = 5)
        self.anal_button = tk.Button(self.analysis_frame, text = "Analysis", command = self.open_analysis_tab, borderwidth = 5)
        self.anal_button.pack(side=tk.LEFT)
        self.analysis_frame.pack()


    def gpa_calculator(self):
        """
        Pops up the GPA Calculator Window
        """
        self.gpa = GPA_Calculator()

    def cgpa_calculator(self):
        """
        Pops up the CGPA Calculator Window
        """
        self.cgpa = CGPA_Calculator()

    def open_analysis_tab(self):
        """
        Pops up the Analysis Window for performing :
            - Department wise analysis
        """
        self.analysis = Analysis()






analyzer = Student_Analysis()  # Creating an object of the Student_Analysis class
analyzer.mainloop() # Running the object of the Student_Analysis class
