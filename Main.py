import tkinter as tk  
from tkinter import filedialog, messagebox, Menu  
import json  
  
# Template for JSON data  
json_template = {  
    "project": {  
        "instsize": 5  
    },  
    "instances": {  
        "add": 1,  
        "read": 1  
    },  
    "Code": {}  
}  
  
# Initialize the main window  
root = tk.Tk()  
  
# Frame to contain the text box and line numbers  
frame = tk.Frame(root)  
frame.pack(fill=tk.BOTH, expand=True)  
  
# Create a Scrollbar  
scrollbar = tk.Scrollbar(frame)  
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  
  
# Create a Text widget for line numbers  
line_numbers = tk.Text(frame, width=4, padx=3, takefocus=0, border=0,  
                       background='lightgray', state='disabled', wrap='none')  
line_numbers.pack(side=tk.LEFT, fill=tk.Y)  
  
# Create a Text widget for user input  
text_box = tk.Text(frame, height=10, width=40, wrap='none', yscrollcommand=scrollbar.set)  
text_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  

# Configure the scrollbar  
scrollbar.config(command=lambda *args: [text_box.yview(*args), line_numbers.yview(*args)])  
  
# Update line numbers in sync with the text box  
def update_line_numbers(event=None):  
    line_numbers.config(state='normal')  
    line_numbers.delete(1.0, tk.END)  
      
    line_count = int(text_box.index('end-1c').split('.')[0])  
    for i in range(1, line_count + 1):  
        line_numbers.insert(tk.END, f"{i}\n")  
      
    line_numbers.config(state='disabled')  
  
text_box.bind('<KeyRelease>', update_line_numbers)  
text_box.bind('<MouseWheel>', update_line_numbers)  
  
def browse_folder():  
    global current_file_path  
    filetypes = (('JSON files', '*.json'), ('All files', '*.*'))  
    file_path = filedialog.askopenfilename(filetypes=filetypes, initialdir="D:/Downloads")  
      
    if file_path:  
        current_file_path = file_path  # Update the current file path  
        with open(file_path, 'r') as file:  
            data = json.load(file)  
            code_content = data.get("Code", {}).get("user_input", "")  
            text_box.delete("1.0", tk.END)  
            text_box.insert(tk.END, code_content)  
        update_line_numbers()  
  
def showoption():  
    response = messagebox.askquestion("askquestion", "Are you sure?")  
    if response == 'yes':  
        print("User selected Yes")  
    else:  
        print("User selected No")  
  
def save():  
    global current_file_path  
    if current_file_path:  
        response = messagebox.askyesno("Save Confirmation", "Do you want to save changes to the current file?")  
        if response:  
            code_content = text_box.get("1.0", tk.END).strip()  
            json_template["Code"] = {"user_input": code_content}  
              
            with open(current_file_path, 'w') as file:  
                json.dump(json_template, file, indent=4)  
            messagebox.showinfo(title="info", message="Changes saved!")  
    else:  
        saveas()  
  
def save2():  
    global current_file_path  
    if current_file_path:  
        code_content = text_box.get("1.0", tk.END).strip()  
        json_template["Code"] = {"user_input": code_content}  
        with open(current_file_path, 'w') as file:  
            json.dump(json_template, file, indent=4)  
    else:  
        saveas()  
  
def saveas():  
    global current_file_path  
    filetypes = (('JSON files', '*.json'), ('All files', '*.*'))  
    f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=filetypes, initialdir="D:/Downloads")  
      
    if f:  
        current_file_path = f  
        code_content = text_box.get("1.0", tk.END).strip()  
        json_template["Code"] = {"user_input": code_content}  
          
        with open(f, 'w') as file:  
            json.dump(json_template, file, indent=4)  
        messagebox.showinfo(title="info", message="File saved!")  
    else:  
        messagebox.showwarning(title="Warning", message="Save operation cancelled.")  
  
def open_settings():  
    settings_window = tk.Toplevel(root)  
    settings_window.title("Settings")  
  
    instsize_var = tk.StringVar(value=json_template["project"]["instsize"])  
    dropdown = tk.Spinbox(settings_window, from_=4, to=32, textvariable=instsize_var)  
    dropdown.pack(pady=10)  
  
    def apply_settings():  
        json_template["project"]["instsize"] = int(instsize_var.get())  
        messagebox.showinfo("Settings", "Changes applied successfully!")  
        save2()  
        settings_window.destroy()  
  
    apply_button = tk.Button(settings_window, text="Apply", command=apply_settings)  
    apply_button.pack(pady=10)  

def open_add_menu():
    add_window = tk.Toplevel(root)  
    add_window.title("Add Instance")

    label = tk.Label(add_window, text="Instance Name:")  
    label.pack(pady=5) 

    instance_text_box = tk.Text(add_window, height=1, width=10)  
    instance_text_box.pack(pady=10) 

    labelp1 = tk.Label(add_window, text="Instance Peraniters:")  
    labelp1.pack(pady=5)

    add_button = tk.Button(add_window, text="Add Instance")  
    add_button.pack(pady=5)




    
    cancel_button = tk.Button(add_window, text="cancel", command=add_window.destroy)  
    cancel_button.pack(pady=5)    
    
     

# Create the menu  
menu = Menu(root)  
root.config(menu=menu)  
  
filemenu = Menu(menu)  
menu.add_cascade(label='File', menu=filemenu)  
  
instance = Menu(menu)  
menu.add_cascade(label='Instance', menu=instance)  
instance.add_command(label='Add', command=open_add_menu)  
instance.add_command(label='Edit')  
instance.add_separator()  
instance.add_command(label='View')  
  
filemenu.add_command(label='New', command=showoption)  
filemenu.add_command(label='Open...', command=browse_folder)  
filemenu.add_command(label='Save', command=save)  
filemenu.add_command(label='Save as', command=saveas)  
  
filemenu.add_separator()  
filemenu.add_command(label='Settings', command=open_settings)  
filemenu.add_command(label='Compile')  
filemenu.add_command(label='Info') 
filemenu.add_separator()  
filemenu.add_command(label='Exit', command=root.quit)  
  
helpmenu = Menu(menu)  
menu.add_cascade(label='Help', menu=helpmenu)  
helpmenu.add_command(label='About')  
  
# Update the line numbers initially  
update_line_numbers()  
  
# Start the main event loop  
root.mainloop()