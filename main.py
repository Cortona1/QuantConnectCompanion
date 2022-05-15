import glob
import sys
import json
import csv


def write_file(data):
    """Takes a json content for statistics and outputs the data relevant to
    a csv file with proper headers"""

    with open('cvs_file.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # create headers
        header = data.keys()
        csv_writer.writerow(header)

        csv_writer.writerow(data.values())


if not len(sys.argv) < 2:
    file_list = []
    f = open(sys.argv[-1], "r")  # open up the file designated at run time
    data = json.load(f)
    f.close()

    write_file(data['Statistics'])

else:

    from tkinter import *
    from tkinter import ttk

    user_interface = Tk()

    user_interface.geometry("1400x800")  # keep resizing window available
    user_interface.configure(background='#FFFFC1')

    from os import listdir
    import os

    class Gui:
        """Represents the gui class for QuantConnect lean results"""

        def __init__(self, root):
            """The gui class constructor for initializing the variables it takes as a parameter the root of the
            Tk object created"""
            self.frame = Frame(root)
            self.frame.grid()
            self.selected_algo = None
            self.row_counter = 8

            self.plain_text = StringVar()
            self.total_trades = StringVar()
            self.sharpe_ratio = StringVar()

            self.display_output = Label(user_interface,
                                        textvariable=self.plain_text)
            self.display_trades = Label(user_interface,
                                        textvariable=self.total_trades)
            self.display_sharpe = Label(user_interface,
                                        textvariable=self.sharpe_ratio)

            self.display_output.grid(row=self.row_counter, column=8, padx=10,
                                     pady=10)
            self.display_trades.grid(row=self.row_counter, column=9, padx=10,
                                     pady=10)
            self.display_sharpe.grid(row=self.row_counter + 1, column=8, padx=10,
                                     pady=10)

        def display_headers(self):
            """Will display the headers of the gui"""

            display_header = Label(user_interface,
                                   text="CS-467 QuantConnect Lean CSV Generator ")
            display_creator = Label(user_interface,
                                    text="Developed by: Anthony Corton")
            state_header = Label(user_interface,
                                 text="Please select your file location\nthen "
                                      "choose a corresponding year from the year drop down menu ")

            display_results = Label(user_interface,
                                    text="Your results for the search will be shown below:")

            display_header.grid(row=0, column=4, ipady=10)
            display_creator.grid(row=1, column=4)
            state_header.grid(row=6, column=0, padx=10, pady=30)
            display_results.grid(row=6, column=8)

        def create_display_list(self):
            """Creates the list of options that will be displayed to the gui as a list of available
            algorithms for which the user can generate csv files from"""

            algo_list = ["MultiResolutionAlgorithm", "MultipleSymbolConsolidationAlgorithm"]

            return [algo_list]

        def display_options(self):
            """Will display the options on the gui for selecting state and year"""
            options_list = self.create_display_list()

            algo_variable = StringVar(user_interface)
            algo_variable.set(
                "MultiResolutionAlgorithm")  # set default menu selection to New Jersey 2005

            self.selected_algo = algo_variable

            algo_menu = OptionMenu(user_interface, algo_variable,
                                    *options_list[0])

            algo_menu.grid(row=8, column=0, ipadx=10)

        def create_submit(self):
            """Creates the submit button for clicking search for algorithms"""

            submit = Button(user_interface,
                            text="Click here to create csv_file.csv for results",
                            command=self.submit_search)

            submit_output = Button(user_interface,
                                   text="Click here to create csv_file.csv and"
                                        " to output results on screen",
                                   command=self.submit_search_output)

            another_space = Label(user_interface)
            space = Label(user_interface)
            space.grid(row=10, column=0)
            submit.grid(row=11, column=0)
            another_space.grid(row=12, column=0)
            submit_output.grid(row=13, column=0)

        def pop_up_message(self, text):
            """This function is responsible for showing a pop up message confirming the results of the user's query
            have been successfully written to csv_file.csv"""

            message = Tk()
            message.wm_title("Notification!")
            contents = ttk.Label(message, text=text)

            contents.pack(side="top", fill="x", pady=10)
            x_button = ttk.Button(message, text="Confirm",
                                  command=message.destroy)
            x_button.pack()
            message.mainloop()

        def submit_search(self):
            """Function triggered when user wants to just make a csv"""
            files = os.listdir()

            test = self.selected_algo.get()
            f = open(f'./Launcher/bin/Debug/{test}.json',"r")  # open up the file designated at run time
            data = json.load(f)
            f.close()
            print(data['Statistics'])

            write_file(data['Statistics'])

            self.pop_up_message("csv_file.csv has been created")

        def submit_search_output(self):
            """Function triggered when user submits to create csv and output data"""

            test = self.selected_algo.get()
            f = open(f'./Launcher/bin/Debug/{test}.json',"r")  # open up the file designated at run time
            data = json.load(f)
            f.close()

            write_file(data['Statistics'])

            self.output_information(data['Statistics'])
            self.pop_up_message("csv_file.csv has been created and results are outputted to screen")

        def output_information(self, data):
            """Takes as a parameter data string and outputs that to the gui as a message box"""

            self.plain_text.set('Ticker ' + data['Lowest Capacity Asset'][:4])
            self.total_trades.set('Total Trades ' + data['Total Trades'])
            self.sharpe_ratio.set('Sharpe Ratio ' + data['Sharpe Ratio'])

    test_run = Gui(user_interface)
    test_run.display_headers()
    test_run.display_options()
    test_run.create_submit()
    user_interface.mainloop()
