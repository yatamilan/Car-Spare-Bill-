import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from fpdf import FPDF
import os

# Function to generate a PDF invoice with a table design
def generate_pdf_invoice():
    customer_name = entry_name.get()
    customer_number = entry_number.get()
    car_name = car_combobox.get()
    car_model = model_combobox.get()
    car_number = entry_car_number.get()
    selected_spares = [spare_parts[i] for i in listbox.curselection()]

    if not selected_spares:
        messagebox.showerror("Error", "Please select at least one spare part.")
        return

    total_price = 0
    invoice_items = []
    for spare in selected_spares:
        price = 50  # Example fixed price for simplicity
        total_price += price
        invoice_items.append({"name": spare, "price": price})

    # Create PDF invoice
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Shop Name
    pdf.cell(200, 10, txt="YA Auto Spares", ln=True, align="C")
    pdf.ln(10)

    # Customer Details
    pdf.cell(200, 10, txt=f"Customer Name: {customer_name}", ln=True)
    pdf.cell(200, 10, txt=f"Customer Number: {customer_number}", ln=True)
    pdf.cell(200, 10, txt=f"Car Name: {car_name}", ln=True)
    pdf.cell(200, 10, txt=f"Car Model: {car_model}", ln=True)
    pdf.cell(200, 10, txt=f"Car Number: {car_number}", ln=True)
    pdf.ln(10)

    # Invoice Table Header
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(80, 10, txt="Spare Part", border=1, align="C")
    pdf.cell(40, 10, txt="Price ($)", border=1, align="C")
    pdf.cell(40, 10, txt="Total ($)", border=1, align="C")
    pdf.ln()

    # Table Rows (Invoice Items)
    pdf.set_font("Arial", size=12)
    for item in invoice_items:
        pdf.cell(80, 10, txt=item['name'], border=1)
        pdf.cell(40, 10, txt=str(item['price']), border=1, align="C")
        pdf.cell(40, 10, txt=str(item['price']), border=1, align="C")
        pdf.ln()

    pdf.ln(10)

    # Total Price Row
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(120, 10, txt="Total Price:", border=1, align="C")
    pdf.cell(40, 10, txt=str(total_price), border=1, align="C")
    pdf.ln(10)

    # Create "bill" folder if it doesn't exist
    if not os.path.exists("bill"):
        os.makedirs("bill")

    # Save PDF in the bill folder
    filename = f"bill/{customer_name}_invoice.pdf"
    pdf.output(filename)

    messagebox.showinfo("Success", f"Invoice generated and saved as {filename}")

# Toggle between Light/Dark Mode
def toggle_mode():
    if dark_mode.get():
        apply_theme("dark")
    else:
        apply_theme("light")

# Apply Light/Dark Mode theme
def apply_theme(mode):
    if mode == "dark":
        bg = "#333333"
        fg = "#FFFFFF"
    else:  # light mode
        bg = "#FFFFFF"
        fg = "#000000"
    
    root.configure(bg=bg)
    label_name.configure(bg=bg, fg=fg)
    label_number.configure(bg=bg, fg=fg)
    label_car.configure(bg=bg, fg=fg)
    label_model.configure(bg=bg, fg=fg)
    label_car_number.configure(bg=bg, fg=fg)
    label_spares.configure(bg=bg, fg=fg)
    button_generate.configure(bg=bg, fg=fg)
    button_reset.configure(bg=bg, fg=fg)
    
    entry_name.configure(bg="#FFFFFF", fg="#000000")
    entry_number.configure(bg="#FFFFFF", fg="#000000")
    entry_car_number.configure(bg="#FFFFFF", fg="#000000")
    
    car_combobox.configure(background="#FFFFFF", foreground="#000000")
    model_combobox.configure(background="#FFFFFF", foreground="#000000")
    
    listbox.configure(bg="#FFFFFF", fg="#000000")

# Reset form
def reset_form():
    entry_name.delete(0, tk.END)
    entry_number.delete(0, tk.END)
    car_combobox.set('')
    model_combobox.set('')
    entry_car_number.delete(0, tk.END)
    listbox.selection_clear(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Car Spare Parts Invoice Generator")
root.geometry("600x500")

# Dark mode toggle variable
dark_mode = tk.BooleanVar()

# Customer Details Section
label_name = tk.Label(root, text="Customer Name:")
label_name.grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

label_number = tk.Label(root, text="Customer Number:")
label_number.grid(row=1, column=0, padx=10, pady=5)
entry_number = tk.Entry(root)
entry_number.grid(row=1, column=1, padx=10, pady=5)

# Car Details Section
label_car = tk.Label(root, text="Car Name:")
label_car.grid(row=2, column=0, padx=10, pady=5)
car_combobox = ttk.Combobox(root, values=["Toyota", "Volkswagen", "Ford", "Honda"])
car_combobox.grid(row=2, column=1, padx=10, pady=5)

label_model = tk.Label(root, text="Model Year:")
label_model.grid(row=3, column=0, padx=10, pady=5)
model_combobox = ttk.Combobox(root, values=[str(year) for year in range(1980, 2025)])
model_combobox.grid(row=3, column=1, padx=10, pady=5)

label_car_number = tk.Label(root, text="Car Number:")
label_car_number.grid(row=4, column=0, padx=10, pady=5)
entry_car_number = tk.Entry(root)
entry_car_number.grid(row=4, column=1, padx=10, pady=5)

# Spare Parts Selection Section
label_spares = tk.Label(root, text="Select Spare Parts:")
label_spares.grid(row=5, column=0, padx=10, pady=5)
spare_parts = ["Spark Plugs", "Oil Filter", "Air Filter", "Fuel Filter", "Timing Belt", "Serpentine Belt", "Water Pump"]
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
for part in spare_parts:
    listbox.insert(tk.END, part)
listbox.grid(row=5, column=1, padx=10, pady=5)

# Buttons
button_generate = tk.Button(root, text="Generate Invoice", command=generate_pdf_invoice)
button_generate.grid(row=6, column=0, padx=10, pady=10)

button_reset = tk.Button(root, text="Reset", command=reset_form)
button_reset.grid(row=6, column=1, padx=10, pady=10)

# Dark Mode Toggle
dark_mode_checkbox = tk.Checkbutton(root, text="Dark Mode", variable=dark_mode, command=toggle_mode)
dark_mode_checkbox.grid(row=7, column=0, columnspan=2, pady=10)

# Apply initial theme (Light mode)
apply_theme("light")

root.mainloop()
