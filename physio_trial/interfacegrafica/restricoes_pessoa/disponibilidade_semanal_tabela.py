import customtkinter as ctk
from datetime import time, datetime
from typing import Dict, List, Any

class DisponibilidadeSemanalTabela(ctk.CTkFrame):
    """
    A table widget for defining weekly availabilities.
    Each row represents a time, and each column represents a day of the week.
    Each cell is a checkbox indicating availability.
    """

    def __init__(self, parent, initial_data: Dict[time, List[bool]] | None = None):
        """
        Initializes the availability table.
        :param parent: The parent widget.
        :param initial_data: A dictionary where keys are time objects and values are lists of 7 booleans
                               (for Mon-Sun availability).
        """
        super().__init__(parent, fg_color="transparent")
        
        # Configure grid columns
        # Column 0 for time, 1-7 for days, 8 for delete button
        self.grid_columnconfigure(list(range(1, 8)), weight=1)
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(8, weight=0)

        self.row_widgets: List[Dict[str, Any]] = []

        # --- Header ---
        for i, day in enumerate(["horário (HH:MM)", "seg", "ter", "qua", "qui", "sex", "sab", "dom", "remover"]):
            header_label = ctk.CTkLabel(self, text=day, font=("Arial", 12, "bold"))
            header_label.grid(row=0, column=i, padx=5, pady=5)
        
        # --- Initial Rows ---
        if initial_data:
            for time_obj, availability in sorted(initial_data.items()):
                self.adicionar_linha(time_obj, availability)

    def adicionar_linha(self, time_obj: time | None = None, availability: List[bool] | None = None):
        """
        Adds a new row to the availability table.
        :param time_obj: Optional time object for the new row.
        :param availability: Optional list of 7 booleans for the checkbox states.
        """
        row_index = len(self.row_widgets)
        grid_row_ui = row_index * 2 + 1
        grid_row_error = row_index * 2 + 2

        time_str = time_obj.strftime("%H:%M") if time_obj else ""
        availability = availability if availability and len(availability) == 7 else [False] * 7

        # Time Entry
        time_entry = ctk.CTkEntry(self, width=60, placeholder_text="HH:MM")
        time_entry.insert(0, time_str)
        time_entry.grid(row=grid_row_ui, column=0, padx=(5, 2), pady=5)

        # Checkboxes for each day
        checkbox_vars = []
        checkboxes = []
        for i in range(7):
            var = ctk.BooleanVar(value=availability[i])
            cb = ctk.CTkCheckBox(self, text="", variable=var, width=20)
            cb.grid(row=grid_row_ui, column=i + 1, padx=2, pady=5)
            checkbox_vars.append(var)
            checkboxes.append(cb)

        # Delete Button
        delete_button = ctk.CTkButton(self, text="X", width=30, command=lambda idx=row_index: self._remover_linha(idx))
        delete_button.grid(row=grid_row_ui, column=8, padx=(5, 5), pady=5)

        # Error Frame (initially empty)
        error_frame = ctk.CTkFrame(self, fg_color="transparent", height=0)
        error_frame.grid(row=grid_row_error, column=0, columnspan=9, sticky="ew")

        self.row_widgets.append({
            "time_entry": time_entry,
            "checkbox_vars": checkbox_vars,
            "checkboxes": checkboxes,
            "delete_button": delete_button,
            "error_frame": error_frame
        })

    def _remover_linha(self, index_to_delete: int):
        """
        Deletes a row and its widgets, then re-grids the subsequent rows.
        """
        # Pop widgets from the list and destroy them
        removed_row = self.row_widgets.pop(index_to_delete)
        removed_row["time_entry"].destroy()
        for checkbox in removed_row["checkboxes"]:
            checkbox.destroy()
        removed_row["delete_button"].destroy()
        removed_row["error_frame"].destroy()

        # Re-grid all subsequent rows to fill the gap
        for i in range(index_to_delete, len(self.row_widgets)):
            widgets = self.row_widgets[i]
            new_grid_row_ui = i * 2 + 1
            new_grid_row_error = i * 2 + 2

            widgets["time_entry"].grid(row=new_grid_row_ui, column=0, padx=(5, 2), pady=5)
            for j, cb in enumerate(widgets["checkboxes"]):
                cb.grid(row=new_grid_row_ui, column=j + 1, padx=2, pady=5)
            widgets["delete_button"].grid(row=new_grid_row_ui, column=8, padx=(5, 5), pady=5)
            widgets["error_frame"].grid(row=new_grid_row_error, column=0, columnspan=9, sticky="ew")
            
            # Update the command for the delete button to reflect its new index
            widgets["delete_button"].configure(command=lambda idx=i: self._remover_linha(idx))

    def get_data(self) -> Dict[time, List[bool]] | None:
        """
        Validates the entire table and returns the availability data if valid.
        Returns a dictionary of {time: [booleans]} or None if there are errors.
        """
        # 1. Clear all previous error messages
        for widgets in self.row_widgets:
            error_frame = widgets["error_frame"]
            for child in error_frame.winfo_children():
                child.destroy()

        # 2. Perform individual row validation
        row_data = []
        has_any_error = False
        for i, widgets in enumerate(self.row_widgets):
            time_str = widgets["time_entry"].get()
            errors = []
            time_obj = None

            if not time_str:
                errors.append("Horário não pode estar vazio.")
            else:
                try:
                    time_obj = datetime.strptime(time_str, "%H:%M").time()
                except ValueError:
                    errors.append("Formato de horário inválido (use HH:MM).")
                
                if time_obj and time_obj >= time(22, 0):
                    errors.append("Horário deve ser anterior às 22:00.")
                    time_obj = None  # Invalidate for further checks

            row_data.append({"time": time_obj, "errors": errors, "index": i})

        # 3. Perform cross-row validation (check for duplicate times)
        time_indices: Dict[time, List[int]] = {}
        for item in row_data:
            if item["time"]:
                if item["time"] not in time_indices:
                    time_indices[item["time"]] = []
                time_indices[item["time"]].append(item["index"])
        
        for t, indices in time_indices.items():
            if len(indices) > 1:
                for index in indices:
                    row_data[index]["errors"].append("Horário duplicado.")

        # 4. Display errors and build the final result dictionary
        result_data = {}
        for item in row_data:
            if item["errors"]:
                has_any_error = True
                error_frame = self.row_widgets[item["index"]]["error_frame"]
                for error_text in item["errors"]:
                    ctk.CTkLabel(error_frame, text=error_text, text_color="red", font=("Arial", 10)).pack(anchor="w", padx=5)
            
            # Only add to result if the time object is valid and there are no errors for this row
            if not item["errors"] and item["time"]:
                checkbox_vars = self.row_widgets[item["index"]]["checkbox_vars"]
                result_data[item["time"]] = [var.get() for var in checkbox_vars]

        return None if has_any_error else result_data
