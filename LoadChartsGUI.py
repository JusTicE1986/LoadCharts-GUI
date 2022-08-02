from tkinter import *
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
from tkinter import filedialog
import os
from fpdf import FPDF


class LoadChartGenerator(ttk.Frame):
    def __init__(self,container):
        super().__init__(container)

        #field options
        options = {'padx': 5, 'pady': 5}

        self.path_label = ttk.Label(self, text='Bitte Ordnerpfad auswählen:')
        self.path_label.grid(column=0, row=0, sticky=W, **options)

        self.browse_path_button = ttk.Button(self, text='Pfad wählen...', command=self.on_click_browse)
        self.browse_path_button.grid(column=3, row=1, sticky=N, **options)

        self.create_button = ttk.Button(self, text='LoadCharts erstellen', command=self.create_loadcharts)
        self.create_button.grid(column=3, row=2, sticky=N, **options)

        self.quit_button = ttk.Button(self, text='Beenden', command=app.destroy)
        self.quit_button.grid(column=3, row=3, sticky=N, **options)


        columns = ('Filename')
        self.file_list = ttk.Treeview(self, columns=columns, show='headings', selectmode='none')
        self.file_list.heading('Filename', text='Dateinamen')
        self.file_list.grid(row=1, rowspan=10, columnspan=2, sticky=W, **options)

        scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.file_list.yview)
        self.file_list.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, rowspan=10, column=2, sticky='ns')

        self.grid(padx=10, pady=10, sticky=NSEW)

    def on_click_browse(self):
        global path
        path = filedialog.askdirectory()
        self.list_files()

    def list_files(self):
        for item in self.file_list.get_children():
            self.file_list.delete(item)
        for files in os.listdir(path):
            self.file_list.insert('', END, values=files)

    def create_loadcharts(self):
        pdf = FPDF()
        png_count = 0
        for files in os.listdir(path):
            if files.lower().endswith(".png"):
                png_count += 1
                if png_count % 2 == 1 :
                    pdf.add_page('p', 'A5')
                    pdf.image(fr'{path}\{files.split("-")[0]}-1.png', x=25, y=15, w=102, h=88.5)
                else:
                    pdf.image(fr'{path}\{files.split("-")[0]}-2.png', x=25, y=105, w=102, h=88.5)
        self.save_loadcharts(pdf)

    def save_loadcharts(self, pdf):
        user = os.environ['USERNAME']
        dest_folder = fr'C:\Users\{user}\Desktop\LoadCharts' + '\\'
        if os.path.isdir(dest_folder):
            pdf.output(dest_folder + fr'PGK LoadCharts.pdf')
        else:
            os.mkdir(dest_folder)
            pdf.output(dest_folder + fr'PGK LoadCharts.pdf')

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Load Chart Generator')
        self.geometry('450x400')
        self.resizable(False, True)


if __name__ == "__main__":
    app = App()
    LoadChartGenerator(app)
    app.mainloop()
