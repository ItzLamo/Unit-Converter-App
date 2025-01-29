import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class UnitConverter:
    def __init__(self):
        # Conversion rates relative to base units (meters, grams, liters)
        self.length_units = {
            'mm': 0.001,
            'cm': 0.01,
            'm': 1,
            'km': 1000,
            'inch': 0.0254,
            'ft': 0.3048,
            'yd': 0.9144,
            'mile': 1609.344
        }
        
        self.weight_units = {
            'mg': 0.001,
            'g': 1,
            'kg': 1000,
            'oz': 28.3495,
            'lb': 453.592,
            'ton': 907185
        }
        
        self.volume_units = {
            'ml': 0.001,
            'l': 1,
            'gal': 3.78541,
            'qt': 0.946353,
            'pt': 0.473176,
            'cup': 0.236588,
            'fl_oz': 0.0295735
        }

        # Temperature conversion requires special handling
        self.temperature_units = ['Celsius', 'Fahrenheit', 'Kelvin']
        
        # Conversion history
        self.history = []

    def convert_length(self, value, from_unit, to_unit):
        if from_unit in self.length_units and to_unit in self.length_units:
            meters = value * self.length_units[from_unit]
            return meters / self.length_units[to_unit]
        return None

    def convert_weight(self, value, from_unit, to_unit):
        if from_unit in self.weight_units and to_unit in self.weight_units:
            grams = value * self.weight_units[from_unit]
            return grams / self.weight_units[to_unit]
        return None

    def convert_volume(self, value, from_unit, to_unit):
        if from_unit in self.volume_units and to_unit in self.volume_units:
            liters = value * self.volume_units[from_unit]
            return liters / self.volume_units[to_unit]
        return None

    def convert_temperature(self, value, from_unit, to_unit):
        # First convert to Kelvin (base unit)
        if from_unit == 'Celsius':
            kelvin = value + 273.15
        elif from_unit == 'Fahrenheit':
            kelvin = (value - 32) * 5/9 + 273.15
        else:  # Kelvin
            kelvin = value
        
        # Then convert from Kelvin to target unit
        if to_unit == 'Celsius':
            return kelvin - 273.15
        elif to_unit == 'Fahrenheit':
            return (kelvin - 273.15) * 9/5 + 32
        else:  # Kelvin
            return kelvin

    def add_to_history(self, conversion_type, value, from_unit, to_unit, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({
            'timestamp': timestamp,
            'type': conversion_type,
            'from_value': value,
            'from_unit': from_unit,
            'to_unit': to_unit,
            'result': result
        })

class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter App")
        self.root.geometry("530x500")
        self.converter = UnitConverter()
        
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Conversion type selection
        ttk.Label(main_frame, text="Conversion Type:").grid(row=0, column=0, padx=5, pady=5)
        self.conversion_type = ttk.Combobox(main_frame, 
            values=['Length', 'Weight', 'Volume', 'Temperature'],
            state='readonly')
        self.conversion_type.grid(row=0, column=1, padx=5, pady=5)
        self.conversion_type.set('Length')
        self.conversion_type.bind('<<ComboboxSelected>>', self.update_units)
        
        # Input value
        ttk.Label(main_frame, text="Value:").grid(row=1, column=0, padx=5, pady=5)
        self.value_entry = ttk.Entry(main_frame)
        self.value_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # From unit
        ttk.Label(main_frame, text="From Unit:").grid(row=2, column=0, padx=5, pady=5)
        self.from_unit = ttk.Combobox(main_frame, state='readonly')
        self.from_unit.grid(row=2, column=1, padx=5, pady=5)
        
        # To unit
        ttk.Label(main_frame, text="To Unit:").grid(row=3, column=0, padx=5, pady=5)
        self.to_unit = ttk.Combobox(main_frame, state='readonly')
        self.to_unit.grid(row=3, column=1, padx=5, pady=5)
        
        # Convert button
        convert_btn = ttk.Button(main_frame, text="Convert", command=self.convert)
        convert_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Result
        self.result_var = tk.StringVar()
        result_label = ttk.Label(main_frame, textvariable=self.result_var,
                               font=('Arial', 12, 'bold'))
        result_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # History
        history_frame = ttk.LabelFrame(main_frame, text="Conversion History", padding="5")
        history_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # History display (using Text widget with scrollbar)
        self.history_text = tk.Text(history_frame, height=10, width=60)
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", 
                                command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Clear history button
        clear_btn = ttk.Button(history_frame, text="Clear History", 
                             command=self.clear_history)
        clear_btn.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Initialize units
        self.update_units()
        
    def update_units(self, event=None):
        conversion_type = self.conversion_type.get()
        
        if conversion_type == 'Length':
            units = list(self.converter.length_units.keys())
        elif conversion_type == 'Weight':
            units = list(self.converter.weight_units.keys())
        elif conversion_type == 'Volume':
            units = list(self.converter.volume_units.keys())
        else:  # Temperature
            units = self.converter.temperature_units
            
        self.from_unit['values'] = units
        self.to_unit['values'] = units
        self.from_unit.set(units[0])
        self.to_unit.set(units[1])
        
    def convert(self):
        try:
            value = float(self.value_entry.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            conversion_type = self.conversion_type.get()
            
            if conversion_type == 'Length':
                result = self.converter.convert_length(value, from_unit, to_unit)
            elif conversion_type == 'Weight':
                result = self.converter.convert_weight(value, from_unit, to_unit)
            elif conversion_type == 'Volume':
                result = self.converter.convert_volume(value, from_unit, to_unit)
            else:  # Temperature
                result = self.converter.convert_temperature(value, from_unit, to_unit)
                
            if result is not None:
                result_text = f"{value} {from_unit} = {result:.4f} {to_unit}"
                self.result_var.set(result_text)
                
                # Add to history
                self.converter.add_to_history(conversion_type, value, 
                                           from_unit, to_unit, result)
                self.update_history_display()
            else:
                messagebox.showerror("Error", "Invalid conversion!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def update_history_display(self):
        self.history_text.delete(1.0, tk.END)
        for entry in reversed(self.converter.history):
            history_entry = (f"{entry['timestamp']} - {entry['type']}: "
                           f"{entry['from_value']} {entry['from_unit']} = "
                           f"{entry['result']:.4f} {entry['to_unit']}\n")
            self.history_text.insert(tk.END, history_entry)
            
    def clear_history(self):
        self.converter.history = []
        self.history_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()