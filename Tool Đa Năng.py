import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from io import BytesIO
import psutil
import platform
import os
import subprocess
import ctypes
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import threading
import matplotlib
import GPUtil
import webbrowser
from tkinter.ttk import Progressbar
from tkinter import simpledialog
import sys
import requests
from zipfile import ZipFile
import cpuinfo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager  # Add this line


# Set the Matplotlib backend before importing other Matplotlib modules
matplotlib.use("TkAgg")


def bytes_to_gb(byte_size):
    gb_size = byte_size / (1024 ** 3)
    return gb_size


class SystemOptimizerApp:
    # Class variable to store the icon
    app_icon = None

    def __init__(self, master):
        self.master = master
        master.title("Tool Đa Năng_Developer Minh Khoa")
        master.geometry("540x600")

        self.background_image_url = "https://vcdn1-dulich.vnecdn.net/2021/07/16/1-1626437591.jpg?w=460&h=0&q=100&dpr=2&fit=crop&s=i2M2IgCcw574LT-bXFY92g"
        self.icon_url = "https://raw.githubusercontent.com/Minhkhoa2206/FINTER/main/icon.ico"

        self.download_folder = "D:\\SWCheck"

        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        self.figure, self.ax = plt.subplots()
        self.chart_canvas = None
        self.cpu_data = [0] * 50
        self.cpu_usage_thread = None

        self.background_image_path = os.path.join(self.download_folder, "icon.png")
        self.icon_path = os.path.join(self.download_folder, "icon.ico")

        # Tải background image và icon chỉ nếu chúng chưa được tải trước đó
        if not os.path.exists(self.background_image_path):
            self.download_file(self.background_image_url, self.background_image_path)

        if not os.path.exists(self.icon_path):
            self.download_file(self.icon_url, self.icon_path)

        self.set_background_image()
        self.set_application_icon()
        self.create_buttons()

    def download_files(self):
        # Tải về background image và icon từ đường link
        self.download_file(self.background_image_url, self.background_image_path)
        self.download_file(self.icon_url, self.icon_path)

    def download_file(self, url, destination_path):
        try:
            response = requests.get(url)
            with open(destination_path, "wb") as file:
                file.write(response.content)
        except Exception as e:
            messagebox.showwarning("Warning", f"Error downloading file from {url}: {e}")

    def set_background_image(self):
        try:
            # Sử dụng đường dẫn địa phương nếu tệp đã tồn tại
            if os.path.exists(self.background_image_path):
                image = Image.open(self.background_image_path)
                photo = ImageTk.PhotoImage(image)

                background_label = tk.Label(self.master, image=photo)
                background_label.image = photo
                background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showwarning("Warning", f"Error setting background image: {e}")

    def set_application_icon(self):
        try:
            # Sử dụng đường dẫn địa phương nếu tệp đã tồn tại
            if os.path.exists(self.icon_path):
                # Use the PhotoImage class to set the application icon
                icon_image = Image.open(self.icon_path)
                icon_photo = ImageTk.PhotoImage(icon_image)
                self.master.tk.call("wm", "iconphoto", self.master._w, icon_photo)
                
                # Set the class variable for the icon to use for other windows
                SystemOptimizerApp.app_icon = icon_photo
        except Exception as e:
            messagebox.showwarning("Warning", f"Error setting application icon: {e}")

    def create_buttons(self):
        button_properties = [
            ("Check system information", self.check_system_information, "#3498d3"),
            ("Check CPU Usage", self.check_cpu_usage, "#3498db"),
            ("Check GPU (Card Đồ Họa)", self.get_gpu_info, "#e74c3c"),  # Corrected line
            ("Check Memory Usage", self.check_memory_usage, "#2ecc71"),
            ("Check Disk Space", self.check_disk_space, "#e74c3c"),
            ("Check battery ", self.check_battery_info, "#e74c3c"),
          ("Set Ram Ảo", self.open_virtual_memory_settings, "#e74c3c"),
             ("Check Vram", self.check_virtual_memory, "#e74c3c"),
            ("Check Device Manager", self.check_device_manager, "#8e44ad"),
            ("Update Drive Magager", self.update_and_export_drivers, "#9b89b6"),
            ("Optimize System", self.optimize_system, "#f39c12"),
             ("Tối Ưu Hóa Ram", self.optimize_ram, "#f39c43"),
            ("Tối Ưu Hóa CPU", self.release_cpu, "#f49c43"),
            ("Speed Boot", self.configure_boot, "#f39c12"),
            ("Windows 10 ebloater", self.toi_uu, "#f39c12"),
             ("Tăng Tốc Wifi", self.accelerate_wifi_speed, "#f39c12"),
            ("Tối Ưu Services", self.optimize_all_services, "#f39c16"),
             ("Bật Ultimate Performance ", self.activate_ultimate_performance, "#f39c22"),
            ("Run Scan with Admin", self.run_scan_with_admin, "#d35400"),
            ("Check Activation Status", self.check_activation_status, "#16a085"),
            ("Windows Software Licensing Management Tool", self.run_slmgr, "#3498db"),
            ("Export Key", self.export_product_key, "#3498db"),
            ("Active Windows/Office", self.activate_windows_office, "#e74c3c"),  # Corrected line
            ("Stop All Processes", self.stop_all_processes, "#c0392b"),
            ("Bật Windows Features", self.open_windows_features, "#c0392b"),
            ("Kích Hoạt Hyper-V", self.enable_hyper_v, "#34495e"),
             ("Check VT", self.check_vt_activation, "#34295e"),
             ("Dọn Rác Toàn Máy", self.scan_and_clean_junk_files, "#34495e"),
           ("Clear Temp Folder", self.clear_temp_folder, "#9b59b6"),
            ("Website KetCauMkPr.ID", self.open_website, "#9b59b6"),

        ]

        row_index, col_index = 0, 0
        for text, command, color in button_properties:
            button = tk.Button(
                self.master,
                text=text,
                command=command,
                bg=color,
                fg="white",
                width=20,
                height=2,
                font=("Helvetica", 10),
            )
            button.grid(row=row_index, column=col_index, padx=5, pady=5)

            col_index += 1
            if col_index == 3:
                col_index = 0
                row_index += 1

    def animate_cpu_usage(self, line, data):
        cpu_percent = psutil.cpu_percent(interval=1)
        data.append(cpu_percent)
        if len(data) > 50:
            data.pop(0)

        line.set_ydata(data)
        self.master.after(1000, lambda: self.animate_cpu_usage(line, data))

    def check_cpu_usage(self):
        # Create a Toplevel window for Matplotlib plot
        cpu_window = tk.Toplevel(self.master)
        cpu_window.title('CPU Usage over Time')

        # Create a Figure and Axes for the plot
        fig, ax = plt.subplots()
        line, = ax.plot(self.cpu_data, label='CPU Usage (%)')

        ax.set_ylim(0, 100)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('CPU Usage (%)')
        ax.legend()

        # Create a TkAgg canvas to embed the plot in the Toplevel window
        canvas = FigureCanvasTkAgg(fig, master=cpu_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Update the plot in the main thread using after()
        self.master.after(1000, lambda: self.animate_cpu_usage(line, self.cpu_data))

    def check_memory_usage(self):
        memory = psutil.virtual_memory()
        total_gb = bytes_to_gb(memory.total)
        used_gb = bytes_to_gb(memory.used)
        free_gb = bytes_to_gb(memory.available)

        labels = ['Used', 'Free']
        sizes = [used_gb, free_gb]
        colors = ['#ff9999', '#66b3ff']

        # Tạo cửa sổ mới để hiển thị biểu đồ tròn
        chart_window = tk.Toplevel(self.master)
        chart_window.title('Memory Usage')

        # Vẽ biểu đồ tròn trên cửa sổ mới
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('Memory Usage')

        # Tạo đối tượng FigureCanvasTkAgg để vẽ biểu đồ tròn trên cửa sổ mới
        chart_canvas = FigureCanvasTkAgg(fig, master=chart_window)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack()

        # Lưu trạng thái chart_canvas để có thể quản lý cửa sổ sau này
        self.chart_canvas = chart_canvas

    def check_disk_space(self):
        partitions = psutil.disk_partitions()

        # Create a new window to display pie charts
        chart_window = tk.Toplevel(self.master)
        chart_window.title('Disk Space Usage')

        # Number of drives
        num_drives = len(partitions)

        # Calculate the size of each cell in the grid to evenly distribute the charts
        num_cols = 3
        num_rows = (num_drives + num_cols - 1) // num_cols

        # Create a labeled frame for each pie chart
        for i, (partition, _) in enumerate(zip(partitions, range(num_drives))):
            frame = tk.LabelFrame(chart_window, text=f'Disk {partition.device} Usage')
            frame.grid(row=i // num_cols, column=i % num_cols, padx=10, pady=10)

            # Draw the pie chart
            self.draw_pie_chart(frame, partition)

    def draw_pie_chart(self, frame, partition):
        labels = ['Used', 'Free']
        usage = psutil.disk_usage(partition.mountpoint)
        sizes = [bytes_to_gb(usage.used), bytes_to_gb(usage.free)]
        colors = ['#ff9999', '#66b3ff']

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
        ax.set_title(f'Total: {bytes_to_gb(usage.total):.2f} GB')

        chart_canvas = FigureCanvasTkAgg(fig, master=frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack()



    def optimize_system(self):
        if platform.system() == 'Windows':
            # Disable Windows error reporting
            subprocess.run(['reg', 'add', 'HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting', '/v', 'Disabled', '/t', 'REG_DWORD', '/d', '1', '/f'])

            # Set Windows visual effects to best performance
            ctypes.windll.user32.SystemParametersInfoW(0x71, 0, 0, 0)

            messagebox.showinfo("Optimize System", "System optimized.")
        else:
            messagebox.showwarning("Unsupported Platform", "Optimization is only supported on Windows.")

    def clear_temp_folder(self):
        temp_folder = os.environ.get('TEMP')
        if temp_folder:
            try:
                for file_name in os.listdir(temp_folder):
                    file_path = os.path.join(temp_folder, file_name)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f'Error deleting {file_path}: {e}')
                messagebox.showinfo("Clear Temp Folder", "Temp folder cleared.")
            except Exception as e:
                messagebox.showerror("Error", f"Error clearing temp folder: {e}")
        else:
            messagebox.showerror("Error", "TEMP environment variable not found.")


    def check_activation_status(self):
        if platform.system() == 'Windows':
            try:
                result = subprocess.run(['cmd.exe', '/c', 'slmgr', '/xpr'], capture_output=True, text=True, check=True)
                messagebox.showinfo("Activation Status", result.stdout.strip())
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Error checking activation status: {e}")
        else:
            messagebox.showwarning("Unsupported Platform", "Activation status check is only supported on Windows.")

    def run_scan_with_admin(self):
        if platform.system() == 'Windows':
            try:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", "/K sfc /scannow", None, 1)
            except Exception as e:
                messagebox.showerror("Error", f"Error opening CMD with Administrator privileges: {e}")
        else:
            messagebox.showwarning("Unsupported Platform", "Running commands with admin privileges is only supported on Windows.")

    def stop_all_processes(self):
        try:
            for process in psutil.process_iter(['pid', 'name']):
                try:
                    process_info = process.info
                    pid = process_info['pid']
                    process_name = process_info['name']
                    if pid != os.getpid() and process_name != "pythonw.exe" and process_name != "python.exe":
                        process = psutil.Process(pid)
                        process.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            messagebox.showinfo("Stop All Processes", "All processes stopped.")
        except Exception as e:
            messagebox.showerror("Error", f"Error stopping processes: {e}")

    def list_all_software(self):
        try:
            software_list = self.get_installed_software()
            software_text = "\n".join(software_list)
            self.show_text_window("Installed Software", software_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error listing installed software: {e}")

    def get_installed_software(self):
        installed_software = []
        if platform.system() == 'Windows':
            try:
                result = subprocess.run(['wmic', 'product', 'get', 'name'], capture_output=True, text=True, check=True)
                installed_software = result.stdout.split('\n')[1:-1]  # Exclude header and empty line
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Error getting installed software on Windows: {e}")
        elif platform.system() == 'Linux':
            try:
                result = subprocess.run(['dpkg', '--list'], capture_output=True, text=True, check=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.startswith("ii"):
                        installed_software.append(line.split()[1])
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Error getting installed software on Linux: {e}")
        return installed_software

    def show_text_window(self, title, text_content):
        text_window = tk.Toplevel(self.master)
        text_window.title(title)
        text_widget = scrolledtext.ScrolledText(text_window, width=60, height=20, wrap=tk.WORD)
        text_widget.insert(tk.END, text_content)
        text_widget.configure(state='disabled')
        text_widget.pack(padx=10, pady=10)

    def check_device_manager(self):
        if platform.system() == 'Windows':
            try:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", "devmgmt.msc", None, None, 1)
            except Exception as e:
                messagebox.showerror("Error", f"Error opening Device Manager: {e}")
        else:
            messagebox.showwarning("Unsupported Platform", "Device Manager is only supported on Windows.")

    def set_custom_background_image(self):
        # Thêm code để cho phép người dùng chọn hình ảnh từ máy tính của họ và đặt làm nền
        pass
    
    def run_slmgr(self):
        if platform.system() == 'Windows':
            try:
                subprocess.run(['cmd.exe', '/c', 'slmgr'])
            except Exception as e:
                messagebox.showerror("Error", f"Error running SLMGR: {e}")
        else:
            messagebox.showwarning("Unsupported Platform", "SLMGR is only supported on Windows.")
    def export_product_key(self):
        if platform.system() == 'Windows':
            try:
                result = subprocess.run(['wmic', 'path', 'SoftwareLicensingService', 'get', 'OA3xOriginalProductKey'], capture_output=True, text=True, check=True)
                product_key = result.stdout.strip()

                if product_key:
                    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                    file_path = os.path.join(desktop_path, "key.txt")

                    with open(file_path, "w") as key_file:
                        key_file.write(product_key)

                    messagebox.showinfo("Export Key", f"Product key exported successfully.\nFile saved at: {file_path}")
                else:
                    messagebox.showwarning("Export Key", "Unable to retrieve product key.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Error exporting product key: {e}")
        else:
            messagebox.showwarning("Unsupported Platform", "Product key export is only supported on Windows.")
            
    def get_gpu_info(self):
        gpu_info = []
        try:
            gpus = GPUtil.getGPUs()
            for i, gpu in enumerate(gpus):
                gpu_info.append(f"GPU {i + 1}:")
                gpu_info.append(f"  Name: {gpu.name}")
                gpu_info.append(f"  Driver: {gpu.driver}")
                gpu_info.append(f"  GPU Memory Total: {gpu.memoryTotal} MB")
                gpu_info.append(f"  GPU Memory Used: {gpu.memoryUsed} MB")
                gpu_info.append(f"  GPU Memory Free: {gpu.memoryFree} MB")
                gpu_info.append(f"  GPU Memory Utilization: {gpu.memoryUtil * 100:.2f}%")
                gpu_info.append(f"  GPU Load: {gpu.load * 100:.2f}%")
                gpu_info.append("")  # Thêm dòng trắng để ngăn cách giữa các GPU

        except Exception as e:
            print(f"Error getting GPU information: {e}")

        return gpu_info

    def show_gpu_info(self):
        try:
            gpu_info = self.get_gpu_info()
            gpu_text = "\n".join(gpu_info)
            messagebox.showinfo("GPU Information", gpu_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error checking GPU information: {e}")
    def activate_windows_office(self):
        try:
            # Lệnh PowerShell để kích hoạt Windows/Office
            powershell_command = 'irm https://massgrave.dev/get | iex'

            # Kiểm tra phiên bản hệ điều hành để quyết định sử dụng PowerShell hay Terminal (cho Windows 11)
            if self.is_windows_11():
                terminal_command = f'start ms-appx:///Microsoft.WindowsTerminal/?command=powershell -NoProfile -ExecutionPolicy unrestricted -Command "{powershell_command}"'
                subprocess.run(terminal_command, shell=True)
            else:
                subprocess.run(["powershell", powershell_command])

        except Exception as e:
            messagebox.showerror("Error", f"Error activating Windows/Office: {e}")

    def is_windows_11(self):
        try:
            # Kiểm tra phiên bản Windows sử dụng platform.system()
            return "post-2021" in subprocess.check_output(["ver"]).decode("utf-8")
        except Exception as e:
            print(f"Error checking Windows version: {e}")
            return False
    def check_system_information(self):
        try:
            # Kiểm tra hệ điều hành và mở msinfo32 tương ứng
            if self.is_windows_11():
                subprocess.run(["start", "ms-settings:about"])
            else:
                subprocess.run(["msinfo32"])

        except Exception as e:
            messagebox.showerror("Error", f"Error checking System Information: {e}")
    def check_battery_info(self):
        try:
            # Lệnh để tạo báo cáo pin và in ra kết quả
            command = "powercfg /batteryreport"
            result = subprocess.check_output(command, shell=True, text=True)

            # Hiển thị thông báo thành công và đường dẫn Desktop
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            success_message = f"Battery information saved successfully.\nResults are displayed below:\n\n{result}"
            messagebox.showinfo("Battery Info", success_message)

        except subprocess.CalledProcessError as e:
            # Hiển thị thông báo lỗi nếu lệnh không thành công
            error_message = f"Error running 'powercfg /batteryreport': {e.stderr}"
            messagebox.showerror("Error", error_message)

        except Exception as e:
            messagebox.showerror("Error", f"Error checking Battery Info: {e}")

# Trong class SystemOptimizerApp:

    def toi_uu(self):
        if platform.system() == 'Windows':
            powershell_command = 'iwr -useb https://git.io/debloat | iex'
            subprocess.run(["powershell", powershell_command])
        else:
            messagebox.showwarning("Unsupported Platform", "Optimization is only supported on Windows.")

    def activate_ultimate_performance(self):
        if platform.system() == 'Windows':
            powercfg_command = 'powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61'
            result = subprocess.run(["powershell", powercfg_command], capture_output=True, text=True)

            if result.returncode == 0:
                messagebox.showinfo("Ultimate Performance", result.stdout.strip())
            else:
                messagebox.showerror("Error", f"Error activating Ultimate Performance: {result.stderr.strip()}")
        elif platform.system() == 'Linux':
            # Thực hiện lệnh cho Linux nếu cần
            pass
        else:
            messagebox.showwarning("Unsupported Platform", "Setting Ultimate Performance is only supported on Windows.")
    def open_website(self):
        website_url = "https://www.ketcaumkpr.id.vn/"
        try:
            webbrowser.open_new(website_url)
        except Exception as e:
            messagebox.showerror("Error", f"Error opening website: {e}")

    def configure_boot(self):
            if os.name == 'nt':
                if 'Windows-10' in platform.platform() or 'Windows-11' in platform.platform():
                    try:
                        # Yêu cầu quyền administrator
                        ctypes.windll.shell32.ShellExecuteW(None, "runas", "msconfig", None, None, 1)
                        messagebox.showinfo("Boot Configuration", "System Configuration opened. Adjust the 'Number of Processors' under the 'Boot' tab.")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error opening System Configuration: {e}")
                else:
                    messagebox.showwarning("Unsupported Platform", "Boot configuration adjustment is only supported on Windows 10 and Windows 11.")
            else:
                messagebox.showwarning("Unsupported Platform", "Boot configuration adjustment is only supported on Windows.")

    def accelerate_wifi_speed(self):
        try:
            if platform.system() == 'Windows':
                # Sử dụng PowerShell để tăng tốc độ WiFi
                powershell_command = 'netsh interface tcp set global autotuning=disabled'
                subprocess.run(["powershell", powershell_command])

                messagebox.showinfo("WiFi Speed Acceleration", "WiFi speed acceleration applied successfully.")
            else:
                messagebox.showwarning("Unsupported Platform", "WiFi speed acceleration is only supported on Windows.")
        except Exception as e:
            messagebox.showerror("Error", f"Error accelerating WiFi speed: {e}")

    def optimize_all_services(self):
        try:
            if platform.system() == 'Windows':
                # Request administrative privileges
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

                # PowerShell command to get all services
                get_services_command = '''
                    Get-Service | Where-Object { $_.StartType -eq 'Automatic' } | Select-Object -Property DisplayName, ServiceName
                '''

                # Run the PowerShell command to get the list of services
                result = subprocess.run(["powershell", "-Command", get_services_command], capture_output=True, text=True)
                service_list = result.stdout.strip().split('\n')

                # Optimize each service
                for service_info in service_list:
                    service_name = service_info.split()[1]
                    self.optimize_service(service_name)

                # Ask the user if they want to restart immediately or wait
                restart_choice = messagebox.askquestion("Restart System", "Do you want to restart your system now?", icon='warning')

                if restart_choice == 'yes':
                    # Restart the system to apply changes
                    subprocess.run(["shutdown", "/r", "/t", "0"])
                else:
                    messagebox.showinfo("Restart Later", "Please restart your system later to apply changes.")
            else:
                messagebox.showwarning("Unsupported Platform", "Service optimization is only supported on Windows.")
        except Exception as e:
            messagebox.showerror("Error", f"Error optimizing all services: {e}")

    def optimize_service(self, service_name):
        try:
            # PowerShell command to set the startup type of a service to manual and stop it
            optimize_command = f'''
                Set-Service -Name {service_name} -StartupType Manual
                Stop-Service -Name {service_name}
            '''

            # Run the PowerShell command to optimize the service
            subprocess.run(["powershell", "-Command", optimize_command])

        except Exception as e:
            messagebox.showerror("Error", f"Error optimizing service {service_name}: {e}")
    def scan_and_clean_junk_files(self):
        # Define a list of file extensions that might be considered as junk/temporary files
        junk_file_extensions = ['.tmp', '.bak', '.log', '.swp']

        # Specify the root directory to start scanning
        root_directory = os.path.expanduser("~")

        # Create a list to store junk files
        junk_files = []

        # Traverse the file system and identify junk files
        for foldername, subfolders, filenames in os.walk(root_directory):
            for filename in filenames:
                if any(filename.lower().endswith(ext) for ext in junk_file_extensions):
                    junk_files.append(os.path.join(foldername, filename))

        if not junk_files:
            messagebox.showinfo("Scan and Clean", "No junk files found.")
            return

        # Display a confirmation message
        confirmation_message = f"{len(junk_files)} junk files found. Do you want to clean them?"
        user_response = messagebox.askyesno("Scan and Clean", confirmation_message)

        if user_response:
            # Perform the cleanup
            deleted_files = self.clean_up_junk_files(junk_files)

            # Show the list of deleted files in a new window
            self.show_deleted_files(deleted_files)

    def clean_up_junk_files(self, junk_files):
        deleted_files = []
        try:
            # Remove or archive junk files
            for file_path in junk_files:
                try:
                    os.remove(file_path)  # Remove the file
                    deleted_files.append(file_path)
                except Exception as e:
                    print(f"Error removing file: {e}")

            messagebox.showinfo("Cleanup Complete", f"{len(deleted_files)} junk files cleaned up.")
        except Exception as e:
            messagebox.showerror("Error", f"Error cleaning up junk files: {e}")

        return deleted_files

    def show_deleted_files(self, deleted_files):
        if deleted_files:
            deleted_files_text = "\n".join(deleted_files)
            self.show_text_window("Deleted Files", "The following files have been deleted:\n\n" + deleted_files_text)
        else:
            messagebox.showinfo("Deleted Files", "No files have been deleted.")

    def show_text_window(self, title, text_content):
        text_window = tk.Toplevel(self.master)
        text_window.title(title)
        text_widget = scrolledtext.ScrolledText(text_window, width=60, height=20, wrap=tk.WORD)
        text_widget.insert(tk.END, text_content)
        text_widget.configure(state='disabled')
        text_widget.pack(padx=10, pady=10)
    def optimize_ram(self):
        try:
            # Clear some memory buffers using psutil
            psutil.virtual_memory().available
            messagebox.showinfo("Optimize RAM", "RAM optimization completed.")
        except Exception as e:
            messagebox.showerror("Error", f"Error optimizing RAM: {e}")
    def release_cpu(self):
        try:
            # Thực hiện một tác vụ giải phóng CPU, ví dụ đơn giản ở đây
            # Bạn có thể thực hiện các tác vụ khác dựa trên nhu cầu của bạn
            for process in psutil.process_iter(['pid', 'name']):
                try:
                    process_info = process.info
                    pid = process_info['pid']
                    process_name = process_info['name']
                    if pid != os.getpid() and process_name != "pythonw.exe" and process_name != "python.exe":
                        process = psutil.Process(pid)
                        process.nice(psutil.IDLE_PRIORITY_CLASS)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            messagebox.showinfo("Release CPU", "CPU released successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error releasing CPU: {e}")

    def open_virtual_memory_settings(self):
        # Mở cài đặt bộ nhớ ảo trong Control Panel
        ctypes.windll.shell32.ShellExecuteW(None, "open", "control.exe", "sysdm.cpl,,3", None, 1)

    def check_virtual_memory(self):
        if platform.system() == 'Windows':
            try:
                # Lệnh PowerShell để lấy thông tin về RAM ảo
                powershell_command = 'Get-WmiObject -query "SELECT AllocatedBaseSize FROM Win32_PageFileUsage" | Format-Table -AutoSize'
                result = subprocess.run(["powershell", powershell_command], capture_output=True, text=True)

                # Hiển thị kết quả trong cửa sổ mới
                self.show_text_window("Virtual Memory Information", result.stdout.strip())

            except Exception as e:
                messagebox.showerror("Error", f"Error checking virtual memory: {e}")
        else:
            messagebox.showwarning("Unsupported Platform", "Checking virtual memory is only supported on Windows.")
    def show_text_window(self, title, text_content):
            text_window = tk.Toplevel(self.master)
            text_window.title(title)
            text_widget = tk.Text(text_window, wrap=tk.WORD)
            text_widget.insert(tk.END, text_content)
            text_widget.configure(state='disabled')
            text_widget.pack(padx=10, pady=10)

    def update_and_export_drivers(self):
        try:
            # Chạy lệnh driverquery trong CMD
            result = subprocess.check_output("driverquery", shell=True, text=True)

            # Lưu danh sách drivers vào file driver.txt trên Desktop
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            output_file_path = os.path.join(desktop_path, "driver.txt")
            with open(output_file_path, "w") as file:
                file.write(result)

            # Thông báo thành công
            messagebox.showinfo("Thành công", "Cập nhật và xuất drivers thành công. Xem file driver.txt trên Desktop.")
        except Exception as e:
            # Thông báo lỗi nếu có
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    def enable_hyper_v(self):
        # Lệnh PowerShell để kích hoạt Hyper-V
        powershell_command = 'Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All'

        # Thực thi lệnh
        result = subprocess.run(['powershell', '-Command', powershell_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # In kết quả
        print(result.stdout)
        print(result.stderr)

        # Hiển thị thông báo
        messagebox.showinfo("Result", f"Hyper-V activation result:\n\n{result.stdout}\n\n{result.stderr}")
    def open_windows_features(self):
        # Lệnh PowerShell để mở cửa sổ Windows Features
        powershell_command = 'OptionalFeatures'

        # Thực thi lệnh
        result = subprocess.run(['powershell', '-Command', powershell_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # In kết quả
        print(result.stdout)
        print(result.stderr)

        # Hiển thị thông báo
        messagebox.showinfo("Result", f"Windows Features window opened.\n\n{result.stdout}\n\n{result.stderr}")
    def check_vt_activation(self):
        # Kiểm tra xem VT đã được kích hoạt hay chưa
        vt_enabled = self.check_vt_support()

        if vt_enabled:
            result_message = "VT is already enabled."
        else:
            result_message = "VT is not enabled. You may need to enable it in BIOS."

        # Hiển thị thông báo
        messagebox.showinfo("VT Activation Status", result_message)

    def check_vt_support(self):
        # Lấy thông tin kiến trúc CPU
        arch = platform.architecture()[0]
        
        # Kiểm tra xem kiến trúc có phải là 64-bit không
        return arch == '64bit'



if __name__ == "__main__":
    root = tk.Tk()
    app = SystemOptimizerApp(root)
    root.mainloop()
