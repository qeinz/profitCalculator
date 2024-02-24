import tkinter as tk
from tkinter import messagebox
import requests
from tkinter import ttk
from ttkthemes import ThemedTk


def process_input(input_text):
    # Entferne Tausendertrennzeichen und ersetze Komma durch Punkt für Dezimalstellen
    return float(input_text.replace(",", "").replace(".", "."))


def calculate_profit():
    try:
        if mode_switch_var.get() == "Prop Firm Gewinn":
            profit = process_input(profit_entry.get())
            euro_profit = round(profit / euro_rate, 2)
            prop_firm_cut = round(profit * 0.2, 2)
            net_profit = round(euro_profit * 0.8, 2)

            # Berechne die Steuern
            taxes = 0
            if include_taxes_var.get():
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

            prop_firm_label.config(text=f"Prop Firm Einbehalt: {prop_firm_cut:.2f} $")
            if church_tax_var.get():
                church_tax_label.config(text=f"Kirchensteuer: {church_tax:.2f} €")
            else:
                church_tax_label.config(text="")
            if solidarity_surcharge_var.get():
                solidarity_surcharge_label.config(text=f"Solidaritätszuschlag: {solidarity_surcharge:.2f} €")
            else:
                solidarity_surcharge_label.config(text="")
            if include_taxes_var.get():
                taxes_label.config(text=f"Steuern: {taxes:.2f} €")
            else:
                taxes_label.config(text="")
            result_label.config(text=f"Ihr Gewinn: {net_profit_after_taxes:.2f} €")

        elif mode_switch_var.get() == "Gewollter Netto Gewinn":
            desired_net_profit = process_input(profit_entry.get())

            # Berücksichtige die Checkboxen für Kirchensteuer und Solidaritätszuschlag
            taxes = 0
            if church_tax_var.get():
                taxes += round(desired_net_profit * 0.09, 2)  # Kirchensteuer 9%
            if solidarity_surcharge_var.get():
                taxes += round(desired_net_profit * 0.055, 2)  # Solidaritätszuschlag 5.5%

            required_gross_profit = (desired_net_profit + taxes) / (1 - 0.2) / (1 - 0.25)

            # Konvertiere den erforderlichen Profit in Euro
            required_gross_profit_euro = round(required_gross_profit * euro_rate, 2)

            result_label.config(text=f"Erforderlicher Profit: {required_gross_profit_euro:.2f} €")

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


def update_calculation(*args):
    # calculate_profit() nur aufrufen, wenn "Berechnen" geklickt wurde
    if args and args[0] != "button":
        return
    calculate_profit()


# GUI
root = ThemedTk(theme='azure')
root.title("Gewinnrechner")
root.resizable(False, False)  # Fenster nicht resizierbar

# Frames
input_frame = ttk.Frame(root, padding=20)
options_frame = ttk.Frame(root, padding=20)
result_frame = ttk.Frame(root, padding=20)

input_frame.grid(row=0, column=0, sticky="nsew")
options_frame.grid(row=1, column=0, sticky="nsew")
result_frame.grid(row=2, column=0, sticky="nsew")

# Labels
profit_label = ttk.Label(input_frame, text="Betrag ($)")
profit_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

profit_entry = ttk.Entry(input_frame)
profit_entry.grid(row=0, column=1, padx=10, pady=5)

mode_switch_var = tk.StringVar(value="Prop Firm Gewinn")

mode_switch_label = ttk.Label(options_frame, text="Modus:")
mode_switch_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

mode_switch_combobox = ttk.Combobox(options_frame, textvariable=mode_switch_var,
                                    values=["Prop Firm Gewinn", "Gewollter Netto Gewinn"], state="readonly")
mode_switch_combobox.grid(row=0, column=1, padx=10, pady=5)
mode_switch_combobox.bind("<<ComboboxSelected>>", update_calculation)

calculate_button = ttk.Button(input_frame, text="Berechnen", command=lambda: update_calculation("button"))
calculate_button.grid(row=1, columnspan=2, padx=10, pady=5)

# Kontrollkästchen für Kirchensteuer und Solidaritätszuschlag
church_tax_var = tk.BooleanVar()
church_tax_checkbox = ttk.Checkbutton(options_frame, text="Kirchensteuer (9%)", variable=church_tax_var,
                                      command=update_calculation)
church_tax_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="w")

solidarity_surcharge_var = tk.BooleanVar()
solidarity_surcharge_checkbox = ttk.Checkbutton(options_frame, text="Solidaritätszuschlag (5.5%)",
                                                variable=solidarity_surcharge_var, command=update_calculation)
solidarity_surcharge_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="w")

# Kontrollkästchen für die 25% Steuern
include_taxes_var = tk.BooleanVar(value=True)  # Standardmäßig True, um 25% Steuern einzuschließen
include_taxes_checkbox = ttk.Checkbutton(options_frame, text="25% Steuern einschließen",
                                         variable=include_taxes_var, command=update_calculation)
include_taxes_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Ergebnislabels
prop_firm_label = ttk.Label(result_frame, text="")
prop_firm_label.pack(pady=(0, 5))

church_tax_label = ttk.Label(result_frame, text="")
church_tax_label.pack()

solidarity_surcharge_label = ttk.Label(result_frame, text="")
solidarity_surcharge_label.pack()

taxes_label = ttk.Label(result_frame, text="")
taxes_label.pack()

result_label = ttk.Label(result_frame, text="")
result_label.pack(pady=5)

# Start GUI
euro_rate = 1.0  # Default Euro rate
root.mainloop()
