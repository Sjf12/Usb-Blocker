import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Define the password
PASSWORD = "" # Replace you desired password

# Function to block USB ports
def block_usb():
    try:
        subprocess.run(r'block_usb.bat', text=True, check=True)
        messagebox.showinfo("USB Security", "USB Ports Disabled Successfully")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to block USB ports: {e}")

# Function to unblock USB ports
def unblock_usb():
    # Create a password prompt dialog box
    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x200")
    password_window.grab_set()  # Ensure the password window has focus

    password_label = tk.Label(password_window, text="Enter Password:")
    password_label.pack(pady=10)

    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack(pady=10)

    def ok_button():
        if password_entry.get() == PASSWORD:
            try:
                subprocess.run(r'unblock_usb.bat', text=True, check=True)
                password_window.destroy()
                messagebox.showinfo("USB Security", "USB Ports Enabled Successfully")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to unblock USB ports: {e}")
        else:
            error_label.config(text="Incorrect password. Please try again.")
            password_entry.delete(0, tk.END)

    ok_button = tk.Button(password_window, text="OK", command=ok_button)
    ok_button.pack(pady=10)

    error_label = tk.Label(password_window, text="", font=("Arial", 12), fg="red")
    error_label.pack()

# Main window
root = tk.Tk()
root.title("USB Security")
root.geometry("300x150")

# Block USB button
block_button = tk.Button(root, text="Block USB Ports", command=block_usb, width=25)
block_button.pack(pady=10)

# Unblock USB button
unblock_button = tk.Button(root, text="Unblock USB Ports", command=unblock_usb, width=25)
unblock_button.pack(pady=10)

# Start the Tkinter loop
root.mainloop()
