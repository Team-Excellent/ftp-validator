import ftplib
import os
import socket
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import Calendar, DateEntry
from main import download_files
import subprocess
import sys
from datetime import datetime


def invalid_input_popup(message):
    popup = Toplevel(root, pady=10, padx=10)
    popup.resizable(width=False, height=False)
    popup.grid()
    popup.title("Invalid files")
    Label(
        popup,
        text=message,
    ).grid(columnspan=3, row=0)
    Button(popup, text="Close", command=popup.destroy).grid(
        column=2, row=1, pady=(24, 0)
    )
    popup.mainloop()


def set_output_folder():
    directory = filedialog.askdirectory()
    output_directory.set(directory)


def open_file(path):
    if sys.platform == "win32":
        os.popen(f"explorer {path}")
    elif sys.platform.startswith("linux"):
        os.popen(f"xdg-open {path}")
    elif sys.platform.startswith("darwin"):
        os.popen(f"open {path}")


def open_logs():
    open_file(os.path.join(output_directory.get(), "downloads", "log.txt"))


def begin_download():
    start_date = datetime.strptime(start_cal.get(), "%d/%m/%Y")
    end_date = datetime.strptime(end_cal.get(), "%d/%m/%Y")
    invalid_files = False
    try:
        invalid_files = download_files(
            output_directory.get(),
            start_date,
            end_date,
            usr=user_entry.get(),
            pswd=password_entry.get(),
            ip=server_addr_entry.get(),
            pt=int(server_port_entry.get()),
        )
    except FileNotFoundError:
        invalid_input_popup("Invalid output directory")
    except ftplib.error_perm:
        invalid_input_popup("Incorrect credentials")
    except socket.timeout:
        invalid_input_popup(("Connection timed out (are details correct?)"))

    if invalid_files:
        popup = Toplevel(root, pady=10, padx=10)
        popup.resizable(width=False, height=False)
        popup.grid()
        popup.title("Invalid files")
        Label(
            popup,
            text="Some files were found to be invalid",
        ).grid(columnspan=3, row=0)
        Button(popup, text="Close", command=popup.destroy).grid(
            column=0, row=1, pady=(24, 0)
        )
        Button(popup, text="View logs", command=open_logs).grid(
            column=2, row=1, pady=(24, 0)
        )
    open_file(os.path.join(output_directory.get(), "downloads"))


root = Tk(screenName="FTP Getter", baseName="FTP Getter")
root.title("FTP Getter")
frame = ttk.Frame(root, padding=10)
frame.grid()

# Server address and port
ttk.Label(frame, text="IP: ").grid(column=0, row=0, sticky="W")
server_addr_entry = ttk.Entry(frame, width=12)
server_addr_entry.insert(-1, "127.0.0.1")
server_addr_entry.grid(column=1, row=0, sticky="W")

ttk.Label(frame, text="Port: ").grid(column=0, row=1, sticky="W")
server_port_entry = ttk.Entry(frame, width=5)
server_port_entry.insert(-1, "2121")
server_port_entry.grid(column=1, row=1, sticky="W")

# Server username and password
ttk.Label(frame, text="Username: ").grid(column=0, row=2, sticky="W", pady=(32, 0))
user_entry = ttk.Entry(frame, width=16)
user_entry.grid(column=1, row=2, sticky="W", pady=(32, 0))

ttk.Label(frame, text="Password: ").grid(column=0, row=3, sticky="W")
password_entry = ttk.Entry(frame, width=16)
password_entry.grid(column=1, row=3, sticky="W")

# Date entry
ttk.Label(frame, text="Start Date: ").grid(column=0, row=4, sticky="W", pady=(32, 0))
start_cal = DateEntry(frame)
start_cal.grid(column=1, row=4, pady=(32, 0))

ttk.Label(frame, text="End Date: ").grid(column=0, row=5, sticky="W", pady=(0, 32))
end_cal = DateEntry(frame)
end_cal.grid(column=1, row=5, pady=(0, 32))

# Directory methods
ttk.Label(frame, text="Output Directory: ").grid(column=0, row=6, pady=(32, 0))
output_directory = StringVar()
ttk.Label(frame, textvariable=output_directory, width=32).grid(
    column=1, row=6, columnspan=3, sticky="W", rowspan=1, pady=(32, 0)
)
ttk.Button(frame, text="Browse", command=set_output_folder).grid(
    column=4, row=6, pady=(32, 0)
)

# Start Download
ttk.Button(frame, text="Start", command=begin_download).grid(
    column=4, row=7, pady=(32, 0)
)

root.resizable(width=False, height=False)
if __name__ == "__main__":
    root.mainloop()
