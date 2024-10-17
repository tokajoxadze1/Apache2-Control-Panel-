import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import os

class ApacheControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Apache2 Control Panel")
        self.root.geometry("650x650")  # Fixed window size
        self.root.resizable(False, False)  # Disable resizing
        self.root.configure(bg="#1E1E1E")

        # Title Label
        self.title_label = tk.Label(root, text="🚀 Apache2 Control Panel", font=("Arial", 18, 'bold'), fg="#00FF00", bg="#1E1E1E")
        self.title_label.pack(pady=20)

        # Program Description
        self.description_label = tk.Label(root, text="🔧 Control and manage Apache2 server with ease\n"
                                                     "Start, Stop, and Restart Apache on port 80.", 
                                         font=("Arial", 12), fg="#FFFFFF", bg="#1E1E1E", justify="center")
        self.description_label.pack(pady=10)

        # Author Info
        self.author_label = tk.Label(root, text="👨‍💻 Author: T0R (Tornike Jokhadze) \n⚖️ All rights reserved.",
                                     font=("Arial", 10), fg="#FF9800", bg="#1E1E1E", justify="center")
        self.author_label.pack(pady=5)

        # Create a Frame to hold buttons horizontally
        button_frame = tk.Frame(root, bg="#1E1E1E")
        button_frame.pack(pady=20)

        # Start Apache Button
        self.start_button = tk.Button(button_frame, text="🟢 Start Apache", font=("Arial", 12), bg="#4CAF50", fg="#FFFFFF", command=self.start_apache)
        self.start_button.grid(row=0, column=0, padx=10)

        # Restart Apache Button
        self.restart_button = tk.Button(button_frame, text="🔄 Restart Apache", font=("Arial", 12), bg="#FF9800", fg="#FFFFFF", command=self.restart_apache)
        self.restart_button.grid(row=0, column=1, padx=10)

        # Stop Apache Button
        self.stop_button = tk.Button(button_frame, text="🔴 Stop Apache", font=("Arial", 12), bg="#F44336", fg="#FFFFFF", command=self.stop_apache)
        self.stop_button.grid(row=0, column=2, padx=10)

        # Terminal Output
        self.terminal_label = tk.Label(root, text="🖥️ Terminal Output:", font=("Arial", 12), fg="#FFFFFF", bg="#1E1E1E")
        self.terminal_label.pack(pady=5)

        self.terminal_text = tk.Text(root, height=10, width=55, font=("Courier New", 10), bg="#2C2C2C", fg="#FFFFFF")
        self.terminal_text.pack(pady=10)
        self.terminal_text.config(state=tk.DISABLED)

        # Status Label
        self.status_label = tk.Label(root, text="Server Status: Stopped ❌", font=("Arial", 12), fg="red", bg="#1E1E1E")
        self.status_label.pack(pady=10)

        # Loading Bar for Loading Screen
        self.progress = ttk.Progressbar(root, length=400, mode='indeterminate')
        self.progress.pack(pady=20)

        # Start loading screen
        self.loading_screen()

    def loading_screen(self):
        self.progress.start()
        self.root.update_idletasks()

        # Check if Apache and necessary tools are installed
        if not self.is_apache_installed():
            self.terminal_text.config(state=tk.NORMAL)
            self.terminal_text.insert(tk.END, "❌ Apache2 not found. Installing...\n")
            self.terminal_text.config(state=tk.DISABLED)
            self.install_apache()

        self.progress.stop()
        self.root.update_idletasks()
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.insert(tk.END, "✅ All required tools are installed.\n")
        self.terminal_text.config(state=tk.DISABLED)

    def is_apache_installed(self):
        try:
            subprocess.run(["apache2ctl", "-v"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    def install_apache(self):
        try:
            subprocess.run(["sudo", "apt-get", "install", "-y", "apache2"], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("❌ Error", f"Failed to install Apache2: {e}")
            return

    def start_apache(self):
        port = "80"
        localhost = "127.0.0.1"

        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.delete(1.0, tk.END)  # Clear previous logs

        try:
            # Run the command to start Apache2 on port 80
            command = f"sudo apache2ctl -k start -D SERVER_PORT={port}"
            subprocess.run(command, shell=True, check=True)

            # Displaying info in the terminal window
            self.terminal_text.insert(tk.END, f"🚀 Apache2 started on {localhost}:{port} ✅\n")
            self.terminal_text.insert(tk.END, "🔄 Fetching server status...\n")
            self.update_server_status(localhost, port)

            self.status_label.config(text="Server Status: Running ✅", fg="green")
            messagebox.showinfo("✅ Success", f"Apache2 started on {localhost}:{port} 🚀")
        except subprocess.CalledProcessError:
            messagebox.showerror("❌ Error", "Failed to start Apache2. Check if Apache is installed and the configuration is correct.")
            self.terminal_text.insert(tk.END, "❌ Error starting Apache2. Check logs for more details.\n")

        self.terminal_text.config(state=tk.DISABLED)

    def restart_apache(self):
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.delete(1.0, tk.END)  # Clear previous logs
        try:
            subprocess.run(["sudo", "apache2ctl", "restart"], check=True)
            self.terminal_text.insert(tk.END, "🔄 Apache2 restarted successfully ✅\n")
            self.status_label.config(text="Server Status: Running ✅", fg="green")
        except subprocess.CalledProcessError as e:
            self.terminal_text.insert(tk.END, f"❌ Error restarting Apache2: {e}\n")
            self.status_label.config(text="Server Status: Stopped ❌", fg="red")

        self.terminal_text.config(state=tk.DISABLED)

    def stop_apache(self):
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.delete(1.0, tk.END)  # Clear previous logs
        try:
            subprocess.run(["sudo", "apache2ctl", "stop"], check=True)
            self.terminal_text.insert(tk.END, "🛑 Apache2 stopped successfully ✅\n")
            self.status_label.config(text="Server Status: Stopped ❌", fg="red")
        except subprocess.CalledProcessError as e:
            self.terminal_text.insert(tk.END, f"❌ Error stopping Apache2: {e}\n")
            self.status_label.config(text="Server Status: Running ✅", fg="green")

        self.terminal_text.config(state=tk.DISABLED)

    def update_server_status(self, localhost, port):
        try:
            response = subprocess.run(f"curl http://{localhost}:{port}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if response.returncode == 0:
                self.terminal_text.insert(tk.END, f"✅ Apache server is up and running at {localhost}:{port}\n")
            else:
                self.terminal_text.insert(tk.END, "❌ Failed to reach Apache server.\n")
        except subprocess.CalledProcessError as e:
            self.terminal_text.insert(tk.END, f"❌ Error checking server status: {e}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = ApacheControlApp(root)
    root.mainloop()
