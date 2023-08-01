import tkinter as tk
from tkinter import ttk
import pandas as pd
import webbrowser

def update_dropdowns(event, dropdown_index):
    selected_values = {i: dropdowns[i].get() for i in range(dropdown_index + 1)}
    df_filtered = df

    for i in range(dropdown_index + 1):
        mask = df_filtered.iloc[:, i] == selected_values[i]
        df_filtered = df_filtered[mask]

    if not df_filtered.empty:
        for i in range(dropdown_index + 1, len(dropdowns)):  # Update starting from the current dropdown
            dropdowns[i]['values'] = df_filtered.iloc[:, i].unique().tolist()
            dropdowns[i].set('')
            dropdowns[i].config(state='disabled')  # Disable the dropdown

            # Set keyboard focus to the current dropdown
            if i == dropdown_index + 1:
                dropdowns[i].focus()

    # Enable the next dropdown if it exists
    if dropdown_index + 1 < len(dropdowns) and not df_filtered.empty:
        dropdowns[dropdown_index + 1].config(state='readonly')

    # Check if all dropdowns have been selected
    all_dropdowns_selected = all(dropdown.get() for dropdown in dropdowns)

    # Update the text box with selected values and associated message if all dropdowns are selected
    if all_dropdowns_selected:
        selected_text = " > ".join([dropdowns[i].get() for i in range(len(dropdowns))])
        if not df_filtered.empty:
            row_label = df_filtered.index[0]  # Use the row label instead of row index
            message = df.loc[row_label, 'Message']  # Use the column label to retrieve the message
            if pd.notna(message):
                # Replace the pipe symbol with line breaks in the message
                message = message.replace("|", "\n")

                selected_text += "\n\n" + message

        selected_text_entry.config(state='normal')
        selected_text_entry.delete("1.0", tk.END)
        selected_text_entry.insert(tk.END, selected_text)

        # Add a tag to the message text to make it bold
        selected_text_entry.tag_configure("bold", font=("Monospace", 12, "bold"))
        selected_text_entry.tag_add("bold", "3.0", tk.END)  # Assuming the message starts from line 3

        # Add a tag to the hyperlink text
        selected_text_entry.tag_configure("hyperlink", font=("Monospace", 12, "bold"), foreground="blue", underline=True)

        selected_text_entry.config(state='disabled')
    else:
        selected_text_entry.config(state='normal')
        selected_text_entry.delete("1.0", tk.END)
        selected_text_entry.config(state='disabled')

def open_hyperlink(event):
    selected_text = selected_text_entry.get("current linestart", "current lineend")
    if selected_text.startswith("http"):
        webbrowser.open(selected_text)

df = pd.read_csv('data.csv')

root = tk.Tk()
root.title("Old Kid's Cable Selector (v0.1)")

# Set window background
root.configure(bg="#2F3136")

# Variables to store selected values of dropdowns
dropdowns = []

# Extract header labels from the top row of the CSV
header_labels = df.columns.tolist()

# Create and set up dropdown menus
for i, header_label in enumerate(header_labels[:-1]):  # Exclude the last column (Message)
    dropdown_label = ttk.Label(root, text=header_label + ":", background="#2F3136", foreground="#6F85D2", font=("Monospace", 16))
    dropdown_label.grid(row=0, column=i, padx=10, pady=5)

    dropdown = ttk.Combobox(root, state="disabled")
    dropdown.grid(row=1, column=i, padx=10, pady=5)

    if i >= len(dropdowns):
        dropdowns.append(dropdown)
    else:
        dropdowns[i] = dropdown

    # Bind the update_dropdowns function to each dropdown with lambda to pass the dropdown index
    dropdowns[i].bind("<<ComboboxSelected>>", lambda event, idx=i: update_dropdowns(event, idx))

    # Set a fixed width for the dropdowns
    dropdowns[i].config(width=20)

# Disable any remaining dropdowns in the list
for i in range(len(header_labels) - 1, len(dropdowns)):
    dropdowns[i].config(state='disabled')

# Adjust padding and spacing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

# Populate the initial values for the first dropdown
dropdowns[0]['values'] = df.iloc[:, 0].unique().tolist()

# Enable the first dropdown initially
dropdowns[0].config(state='readonly')

# Text box to display selected values and associated message
selected_text_entry = tk.Text(root, width=80, height=5, wrap='word', bg="white", fg="black", cursor="arrow", font=("Monospace", 12))
selected_text_entry.grid(row=2, column=0, columnspan=len(header_labels), padx=10, pady=5, sticky="we")
selected_text_entry.config(state='disabled')

# Bind the "Tab" key to focus on the next dropdown
for i in range(len(dropdowns) - 1):
    dropdowns[i].bind("<Tab>", lambda event, idx=i: dropdowns[idx + 1].focus())

selected_text_entry.bind("<Button-1>", open_hyperlink)
selected_text_entry.bind("<Enter>", lambda event: selected_text_entry.config(cursor="hand2"))
selected_text_entry.bind("<Leave>", lambda event: selected_text_entry.config(cursor="arrow"))

# Set initial focus on the first dropdown
dropdowns[0].focus()

root.mainloop()
