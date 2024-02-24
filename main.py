import tkinter as tk
from tkinter import messagebox
import requests
from tkinter import ttk


def process_input(input_text):
    # Entferne Tausendertrennzeichen und ersetze Komma durch Punkt für Dezimalstellen
    return float(input_text.replace(",", "").replace(".", "."))


def calculate_profit():
    try:
        profit = process_input(profit_entry.get())
        euro_profit = round(profit / euro_rate, 2)
        prop_firm_cut = round(profit * 0.2, 2)
        net_profit = round(euro_profit * 0.8, 2)
        taxes = round(net_profit * 0.25, 2)

        if church_tax_var.get():
            church_tax = round(net_profit * 0.09, 2)  # Kirchensteuer 9%
        else:
            church_tax = 0

        if solidarity_surcharge_var.get():
            solidarity_surcharge = round(net_profit * 0.055, 2)  # Solidaritätszuschlag 5.5%
        else:
            solidarity_surcharge = 0

        net_profit_after_taxes = net_profit - taxes - church_tax - solidarity_surcharge

        result_label.config(text=f"Ihr Gewinn nach Steuern: {net_profit_after_taxes:.2f} €")
        taxes_label.config(text=f"Steuern: {taxes:.2f} €")
        prop_firm_label.config(text=f"Prop Firm Einbehalt: {prop_firm_cut:.2f} $")
        church_tax_label.config(text=f"Kirchensteuer: {church_tax:.2f} €")
        solidarity_surcharge_label.config(text=f"Solidaritätszuschlag: {solidarity_surcharge:.2f} €")
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl ein.")


def update_euro_rate():
    try:
        global euro_rate
        response = requests.get(f"https://open.er-api.com/v6/latest/USD")
        data = response.json()
        euro_rate = data["rates"]["EUR"]
        messagebox.showinfo("Erfolg", "Euro-Kurs erfolgreich aktualisiert.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Abrufen des Euro-Kurses: {str(e)}")


# GUI
root = tk.Tk()
root.title("Gewinnrechner")
root.geometry("500x450")
root.resizable(False, False)  # Fenster nicht resizierbar

# Setze das Tkinter-Theme
style = ttk.Style(root)
style.theme_use("clam")

# Frames
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

options_frame = tk.Frame(root)
options_frame.pack(pady=10)

result_frame = tk.Frame(root)
result_frame.pack(pady=10)

# Labels
profit_label = tk.Label(input_frame, text="Wie viel $ Profit ist auf Ihrem Konto?")
profit_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

profit_entry = tk.Entry(input_frame)
profit_entry.grid(row=0, column=1, padx=10, pady=5)

calculate_button = tk.Button(input_frame, text="Berechnen", command=calculate_profit)
calculate_button.grid(row=1, columnspan=2, padx=10, pady=5)

church_tax_var = tk.BooleanVar()
church_tax_checkbox = tk.Checkbutton(options_frame, text="Kirchensteuer (9%)", variable=church_tax_var)
church_tax_checkbox.grid(row=0, column=0, padx=10, pady=5, sticky="w")

solidarity_surcharge_var = tk.BooleanVar()
solidarity_surcharge_checkbox = tk.Checkbutton(options_frame, text="Solidaritätszuschlag (5.5%)",
                                               variable=solidarity_surcharge_var)
solidarity_surcharge_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="w")

result_label = tk.Label(result_frame, text="")
result_label.pack(pady=5)

taxes_label = tk.Label(result_frame, text="")
taxes_label.pack()

prop_firm_label = tk.Label(result_frame, text="")
prop_firm_label.pack()

church_tax_label = tk.Label(result_frame, text="")
church_tax_label.pack()

solidarity_surcharge_label = tk.Label(result_frame, text="")
solidarity_surcharge_label.pack()

# Start GUI
euro_rate = 1.0  # Default Euro rate
root.mainloop()
