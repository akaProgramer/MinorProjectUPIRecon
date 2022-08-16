import tkinter as tk
import pandas as pd
import tkinter.ttk as ttk
main_win = tk.Tk ()
main_win.title ("To Do List")
main_win.geometry ("400x300")
tree = ttk.Treeview (main_win)
#Create columns (3 columns)
tree ["columns"] = (1,2,3)
#Header settings
tree ["show"] = "headings"
tree.heading (1, text = "category")
tree.heading (2, text = "product")
tree.heading (3, text = "amount")
# Width setting for each column
tree.column (1, width = 100)
tree.column (2, width = 100)
tree.column (3, width = 300)
#Data insertion
tree.insert ("", "end", values ​ ("food", "apple", " 500"))
tree.insert ("", "end", values ​​("miscellaneous goods", "toys", " 1,200"))
tree.insert ("", "end", values ​ ("Home appliances", "TV", " 16,500"))
#Table layout
tree.pack ()

def example ():
    data = [tree.item (item) ['values'] for item in tree.get_children ()]
    df = pd.DataFrame (data)
    df.to_csv ('data.csv', encoding ='shift-jis', header = False, index = False)
tk.Button (text ='to_convert', command = example) .pack ()
main_win.mainloop ()
