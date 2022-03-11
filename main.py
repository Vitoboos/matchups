from tkinter import *
import tkinter
import sqlite3
from gui_functions import select_diff, select_result, add, read_games

conn = sqlite3.connect('matchups.db')
cs = conn.cursor()

root = Tk()

# Frames

your_lane = LabelFrame(root, text='Draft details', padx=5)
match_data = LabelFrame(root, text=' Match difficulty', padx=5)
match_data_child = LabelFrame(root, text='Match details')

# Entries

you = Entry(your_lane, width=30)
enemy = Entry(your_lane, width=30)

notes = Entry(match_data_child, width=20)


# Labels

you_label = Label(your_lane, text='Your champion')
enemy_label = Label(your_lane, text='Enemy champion')

notes_label = Label(match_data_child, text='Notes')

# Buttons

add_game = Button(root, text='Add game to database', command= lambda:add(diff, result, you, enemy, notes, dropdown_placeholder))
read_game = Button(root, text='Read games', width=15, command= read_games)

# Dropdown list

choose_lane = ['Top', 'Jungle', 'Mid', 'Bot', 'Supp']
dropdown_placeholder = StringVar()
dropdown_placeholder.set("Choose your lane")
dropdown_menu = tkinter.OptionMenu(your_lane, dropdown_placeholder, *choose_lane)

# Radio buttons

diff = IntVar(value=0)
result = StringVar(value='W')

Diff1 = Radiobutton(match_data, value=1, variable=diff, text='1', command= lambda:select_diff(diff))
Diff2 = Radiobutton(match_data, value=2, variable=diff, text='2', command= lambda:select_diff(diff))
Diff3 = Radiobutton(match_data, value=3, variable=diff, text='3', command= lambda:select_diff(diff))
Diff4 = Radiobutton(match_data, value=4, variable=diff, text='4', command= lambda:select_diff(diff))
Diff5 = Radiobutton(match_data, value=5, variable=diff, text='5', command= lambda:select_diff(diff))

Gresult1 = Radiobutton(match_data_child, value='W', variable=result, text='W', command= lambda:select_result(result))
Gresult2 = Radiobutton(match_data_child, value='L', variable=result, text='L', command= lambda:select_result(result))

# Show on Screen

# Frames

your_lane.grid(row=0, column=0)
match_data.grid(row=0, column=1)
match_data_child.grid(row=1, column=1)

# Entries  

you.grid(row=0, column=1)
enemy.grid(row=1, column=1)

notes.grid(row=0, column=1)

# Labels

you_label.grid(row=0, column=0)
enemy_label.grid(row=1, column=0)

notes_label.grid(row=0, column=0)

# Dropdown

dropdown_menu.grid(row=2, column=0)

# Buttons

add_game.grid(row=1, column=0)
read_game.grid(row=2, column=0)

# Radio Buttons

Diff1.grid(row=1, column=0)
Diff2.grid(row=1, column=1)
Diff3.grid(row=1, column=2)
Diff4.grid(row=1, column=3)
Diff5.grid(row=1, column=4)

Gresult1.grid(row=2, column=0)
Gresult2.grid(row=2, column=1)

conn.commit()
conn.close()

root.mainloop()