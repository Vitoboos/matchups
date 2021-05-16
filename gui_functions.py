from sqlite3.dbapi2 import adapt
from tkinter import *
import collections
import sqlite3
from tkinter import messagebox
from tkinter import ttk

def select_diff(number):

    return

def select_result(game):

    return

def add(difficulty, game_result, your_champ, enemy_champ, game_notes, lane):

    conn = sqlite3.connect('matchups.db')
    cs = conn.cursor()

    if your_champ != "":

        cs.execute("""CREATE TABLE if not exists """+your_champ.get()+"""(

            you text,
            enemy text,
            lane text,  
            diff integer,
            notes text,
            result text

        )""")
        conn.commit()

    print(lane.get())
    print(your_champ.get())
    print(enemy_champ.get())
    print(difficulty.get())
    print(game_result.get())
    print(game_notes.get())

    if lane.get() != "" and your_champ.get() != "" and enemy_champ.get() != "" and difficulty != "" and game_result != "":

        cs.execute("""INSERT INTO """+your_champ.get()+""" VALUES (:you, :enemy, :lane, :diff, :notes, :result)""",
            {
                "you": your_champ.get(),
                "enemy": enemy_champ.get(),
                "lane": lane.get(),
                "diff": difficulty.get(),
                "notes": game_notes.get(),
                "result": game_result.get()
            })
        conn.commit()
        messagebox.showinfo(title='Success', message='Game successfully added')

    else:
        messagebox.showerror(title='Error', message='Only notes can be in blank')

    conn.close()

def read_games():

    reader_screen = Tk()
    reader_screen.title('Reading Screen')
    reader_screen.geometry('800x600')
    treeview = ttk.Treeview(reader_screen)
    treeview['columns'] = ('ID','You', 'Enemy', 'Lane', 'Difficulty', 'Notes', 'Result')

    # Format

    treeview.column('#0', width=0, stretch=NO)
    treeview.column('ID', anchor=CENTER, width=40)
    treeview.column('You', anchor=CENTER, width=80)
    treeview.column('Enemy', anchor=CENTER, width=80)
    treeview.column('Lane', anchor=CENTER, width=40)
    treeview.column('Difficulty', anchor=CENTER, width=70)
    treeview.column('Notes', anchor=CENTER, width=200)
    treeview.column('Result', anchor=CENTER, width=40)

    # Headers

    treeview.heading('#0', text='', anchor=CENTER)
    treeview.heading('ID', text='ID', anchor=CENTER)
    treeview.heading('You', text='You', anchor=CENTER)
    treeview.heading('Enemy', text='Enemy', anchor=CENTER)
    treeview.heading('Lane', text='Lane', anchor=CENTER)
    treeview.heading('Difficulty', text='Difficulty', anchor=CENTER)
    treeview.heading('Notes', text='Notes', anchor=CENTER)
    treeview.heading('Result', text='Results', anchor=CENTER)

    # Show on screen

    treeview.grid(row=0, column=0, padx=50)

    # Frames

    champonly_frame = LabelFrame(reader_screen, text='All games with a champion')
    champonly_frame.grid(row=1, column=0, pady=15)

    bothchamps_frame = LabelFrame(reader_screen, text='All games vs opponent')
    bothchamps_frame.grid(row=2, column=0, pady=15)

    remove_frame = LabelFrame(reader_screen, text='Remove a game')
    remove_frame.grid(row=4, column=0, pady=10)

    # Entries 1

    your_champ_only = Entry(champonly_frame, width=30)
    your_champ_only_label = Label(champonly_frame, text='Your champion')

    your_champ_only.grid(row=0, column=1)
    your_champ_only_label.grid(row=0, column=0)

    # Entries 2

    your_champ = Entry(bothchamps_frame, width=30)
    enemy_champ = Entry(bothchamps_frame, width=30)
    your_champ_both_label = Label(bothchamps_frame, text='Your champion')
    enemy_champ_both_label = Label(bothchamps_frame, text='Enemy champion')

    your_champ.grid(row=0, column=1)
    enemy_champ.grid(row=1, column=1)
    your_champ_both_label.grid(row=0, column=0)
    enemy_champ_both_label.grid(row=1, column=0)

    # Entries 3

    id_entry = Entry(remove_frame, width=30)
    id_entry.grid(row=1, column=0)

    id_label = Label(remove_frame, text='Insert game ID')
    id_label.grid(row=0, column=0)

    # Functions

    def fetch(onlychamp, yourchamp, enemychamp):
        
        conn = sqlite3.connect('matchups.db')
        cs = conn.cursor()

        if onlychamp.get() != "" and your_champ.get() == "" and enemychamp.get() == "":

            print(onlychamp.get())

            cs.execute("""SELECT *, oid FROM """+onlychamp.get())
            records = cs.fetchall()
            print(records)

            # Insert data into treeview
            
            counter = 0
            for record in records:

                treeview.insert(parent='', index='end', iid=counter, text='', values=(record[6],record[0],record[1],record[2],record[3], record[4], record[5]))
                counter += 1

        elif yourchamp.get() != "" and enemychamp.get() != "" and onlychamp.get() == "":

            print(yourchamp.get())
            print(enemychamp.get())

            cs.execute("SELECT *, oid FROM "+yourchamp.get()+" WHERE enemy= '"+enemychamp.get()+"'")
            records = cs.fetchall()
            print(records)

            counter = 0
            for record in records:

                treeview.insert(parent='', index='end', iid=counter, text='', values=(record[6],record[0],record[1],record[2],record[3], record[4], record[5]))
                counter += 1

        else:

            messagebox.showerror(title='Error', message='You can only fetch from one field')

        conn.commit()
        conn.close()

        return


    def remove(id, yourchamponly, yourchamp):

        if id_entry.get() != "":

            if your_champ_only.get() != "" and your_champ.get() == "":

                champion = yourchamponly.get()

            elif your_champ.get() != "" and your_champ_only.get() == "":

                champion = yourchamp.get()

            else: 

                messagebox.showerror(title='Error', message='Set your champion on one field')

            print("The champion is : " + champion)

            conn = sqlite3.connect('matchups.db')
            cs = conn.cursor()

            cs.execute('DELETE FROM '+champion+' WHERE oid="'+id.get()+'"')
            id_entry.delete(0, END)
            messagebox.showinfo(title='Success', message='Game removed')

            conn.commit()
            conn.close()
        
        else: 

            messagebox.showerror(title='Error', message='Introduce el ID de una tarea')

        return

    def advanced_generic(yourchamp):

        conn = sqlite3.connect('matchups.db')
        cs = conn.cursor()

        advanced_screen = Tk()

        treeview = ttk.Treeview(advanced_screen)

        cs.execute('SELECT * FROM '+yourchamp.get())
        records = cs.fetchall()
        print(records)

        treeview['columns'] = ('You', 'Enemy', 'Games', 'Difficulty', 'Winrate')

        # Format

        treeview.column('#0', width=0, stretch=NO)
        treeview.column('You', anchor=CENTER, width=80)
        treeview.column('Enemy', anchor=CENTER, width=80)
        treeview.column('Games', anchor=CENTER, width=45)
        treeview.column('Difficulty', anchor=CENTER, width=70) 
        treeview.column('Winrate', anchor=CENTER, width=60)

        # Headers

        treeview.heading('#0', text='', anchor=CENTER)
        treeview.heading('You', text='You', anchor=CENTER)
        treeview.heading('Enemy', text='Enemy', anchor=CENTER)
        treeview.heading('Games', text='Games', anchor=CENTER)
        treeview.heading('Difficulty', text='Difficulty', anchor=CENTER)
        treeview.heading('Winrate', text='Winrate', anchor=CENTER)

        # Show on treeview screen

        treeview.grid(row=0, column=0, padx=50)

        # Data setup

        opponents = []

        for record in records:

            opponents.append(record[1])

            
        unique = collections.Counter(opponents)

        unique_opponents = list(unique.keys())
        unique_games = list(unique.values())
        unique_winrates = []
        unique_diff = []

        for opponent in range(len(unique_opponents)):
            
            cs.execute("SELECT * FROM "+yourchamp.get()+" WHERE enemy='"+unique_opponents[opponent]+"'")
            conn.commit()
            register = cs.fetchall()

            results_counter = []
            diff_counter = []

            for opponent in register:
                
                results_counter.append(opponent[5])
                wins = results_counter.count('W')
                losses = results_counter.count('L')

                diff_counter.append(opponent[3]) 

            winrate = wins/(wins+losses) * 100
            unique_winrates.append(format(winrate, '.2f'))

            difficulty = sum(diff_counter) / len(diff_counter)
            unique_diff.append(format(difficulty, '.2f'))


        print(unique_opponents)
        print(unique_games)
        print(unique_winrates)
        print(unique_diff)

        # Insert into treeview 

        counter = 0
        for opponent in unique:

            treeview.insert(parent='', index='end', iid=counter, text='', values=(yourchamp.get(),unique_opponents[counter],unique_games[counter],unique_diff[counter], unique_winrates[counter]))
            counter += 1

        conn.commit()
        conn.close()
        
        return

    def advanced_specific(yourchamp, enemychamp):

        advanced_screen2 = Tk()
        conn = sqlite3.connect('matchups.db')
        cs = conn.cursor()

        cs.execute("SELECT *, oid FROM "+yourchamp.get()+" WHERE enemy= '"+enemychamp.get()+"'")
        records = cs.fetchall()
        conn.commit()

        treeview = ttk.Treeview(advanced_screen2)
        treeview['columns'] = ('You', 'Enemy', 'Lane', 'Games', 'Difficulty', 'Winrate')

        # Format

        treeview.column('#0', width=0, stretch=NO)
        treeview.column('You', anchor=CENTER, width=80)
        treeview.column('Enemy', anchor=CENTER, width=80)
        treeview.column('Lane', anchor=CENTER, width=70)
        treeview.column('Games', anchor=CENTER, width=45)
        treeview.column('Difficulty', anchor=CENTER, width=70) 
        treeview.column('Winrate', anchor=CENTER, width=60)

        # Headers

        treeview.heading('#0', text='', anchor=CENTER)
        treeview.heading('You', text='You', anchor=CENTER)
        treeview.heading('Enemy', text='Enemy', anchor=CENTER)
        treeview.heading('Lane', text='Lane', anchor=CENTER)
        treeview.heading('Games', text='Games', anchor=CENTER)
        treeview.heading('Difficulty', text='Difficulty', anchor=CENTER)
        treeview.heading('Winrate', text='Winrate', anchor=CENTER)

        # Show on treeview screen

        treeview.grid(row=0, column=0, padx=50)

        # Data setup

        lane_counter = []

        for record in records:

            lane_counter.append(record[2])


        lane_games = collections.Counter(lane_counter)

        unique_lanes = list(lane_games.keys())
        unique_games = list(lane_games.values())
        unique_diff = []
        unique_winrates = []

        for lane in unique_lanes:

            print(lane)
            diff_lane = []
            game_count = []

            for record in records:
                
                if record[2] == lane:

                    diff_lane.append(record[3])
                    game_count.append(record[5])

            wins_aux = game_count.count('W')
            loss_aux = game_count.count('L')

            winrate_aux = wins_aux/(wins_aux+loss_aux) * 100
            unique_winrates.append(winrate_aux)

            sum_diff = sum(diff_lane)
            sum_diff = (sum_diff/len(diff_lane))
            unique_diff.append((format(sum_diff, '.2f')))


        # Insert data into treeview
            
        counter = 0
        for lane in unique_lanes:

            treeview.insert(parent='', index='end', iid=counter, text='', values=(your_champ.get(),enemy_champ.get(),unique_games[counter], unique_games[counter], unique_diff[counter], unique_winrates[counter]))
            counter += 1


        print(unique_games)
        print(unique_lanes)
        print(unique_diff)
        print(unique_winrates)

        conn.close()

        return

    # Buttons

    fetch_button = Button(reader_screen, text='Show games', command= lambda:fetch(your_champ_only, your_champ, enemy_champ))
    remove_button = Button(remove_frame, text='Delete game', command= lambda:remove(id_entry, your_champ_only, your_champ))
    advanced_button = Button(champonly_frame, text='General data', command= lambda: advanced_generic(your_champ_only))
    advanced_specific_button = Button(bothchamps_frame, text='General data', command= lambda: advanced_specific(your_champ, enemy_champ))

    # Show screen

    fetch_button.grid(row=3, column=0)
    remove_button.grid(row=2, column=0)
    advanced_button.grid(row=0, column=2)
    advanced_specific_button.grid(row=0, column=2)

    return