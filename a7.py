#s_ada62ybyb62LhTRGMH42T
#https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15
#import pyodbc
#conn = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;Trusted_Connection=yes;')
#cur = conn.cursor()

#cur.execute('SELECT username, password from dbo.helpdesk')
#row = cur.fetchone()
#while row:
#    print ('SQL Server standard login name = ' + row[0])
#    row = cur.fetchone()



from tkinter import *
from tkinter import ttk

def raiseFrame(frame):
    frame.tkraise()

def searchMenu(frame, resultFrame):
    def search(*args):
        try:
            print("sup")
            searchFilterStr = """
            SELECT DISTINCT L.id, L.name, LEFT(L.description, 25), L.number_of_bedrooms, C.price
                FROM Listings as L, Calendar as C
                WHERE L.id IN
                    (SELECT L2.id FROM Listings as L2
                    WHERE L2.number_of_bedrooms >= {}""".format(int(numRooms.get()))
            
            if len(minPrice.get()) > 0 and len(maxPrice.get()) == 0:
                searchFilterStr += """
                EXCEPT 
                    (SELECT C2.listing_id FROM Calendar as C2
                    WHERE C2.price < {}) """.format(int(minPrice.get()))
            elif len(minPrice.get()) == 0 and len(maxPrice.get()) > 0:
                searchFilterStr += """
                EXCEPT
                    (SELECT C2.listing_id FROM Calendar as C2
                    WHERE C2.price > {}) """.format(int(maxPrice.get()))
            elif len(minPrice.get()) > 0 and len(maxPrice.get()) > 0:
                searchFilterStr += """
                EXCEPT 
                    (SELECT C2.listing_id FROM Calendar as C2
                    WHERE C2.price > {} OR C2.price < {}) """.format(int(maxPrice.get()), int(minPrice.get()))

            searchFilterStr += """
                EXCEPT
                    (SELECT C3.listing_id FROM Calendar as C3
                    WHERE C3.date BETWEEN '{}' AND '{}'
                    AND C3.available = 1))
            AND C.price = (SELECT MAX(C4.price) FROM Calendar as C4
                    WHERE C4.listing_id = L.id
                    AND C4.date BETWEEN '{}' AND '{}') """.format( minDate.get(), maxDate.get(), minDate.get(), maxDate.get() )

            print(searchFilterStr)

            raiseFrame(resultFrame)
        except ValueError:
            pass

    #create widgets
    minPrice = StringVar()
    maxPrice = StringVar()
    numRooms = StringVar()
    minDate = StringVar()
    maxDate = StringVar()

    ttk.Label(frame, text="Filter:").grid(column=1, row=2, sticky=W)

    ttk.Label(frame, text="Price").grid(column=1, row=3, sticky=W)
    minPriceEntry = ttk.Entry(frame, width=10, textvariable=minPrice)
    minPriceEntry.grid(column=2, row=3, sticky=(W, E))
    ttk.Label(frame, text="-").grid(column=3, row=3, sticky=W)
    maxPriceEntry = ttk.Entry(frame, width=10, textvariable=maxPrice)
    maxPriceEntry.grid(column=4, row=3, sticky=(W, E))

    ttk.Label(frame, text="Rooms").grid(column=1, row=4, sticky=W)
    numRoomsEntry = ttk.Entry(frame, width=10, textvariable=numRooms)
    numRoomsEntry.grid(column=2, row=4, sticky=(W, E))

    ttk.Label(frame, text="Stay date").grid(column=1, row=5, sticky=W)
    minDateEntry = ttk.Entry(frame, width=10, textvariable=minDate)
    minDateEntry.grid(column=2, row=5, sticky=(W, E))
    ttk.Label(frame, text="-").grid(column=3, row=5, sticky=W)
    maxDateEntry = ttk.Entry(frame, width=10, textvariable=maxDate)
    maxDateEntry.grid(column=4, row=5, sticky=(W, E))

    searchButton = ttk.Button(frame, width=10, text="search", command=search)
    searchButton.grid(column=4, row=6, sticky=(W, E))

    #padding
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    #initial focus
    minPriceEntry.focus()

def resultMenu(frame):
    print("result menu")

def reviewMenu(frame):
    print("review menu")


#set root characteristics
root = Tk()
root.title("Airbnb Booker")
root.configure(background='#FF5A60')
#root.minsize(640, 640)

searchFrame = ttk.Frame(root)
resultFrame = ttk.Frame(root)
reviewFrame = ttk.Frame(root)


for frame in (searchFrame, resultFrame, reviewFrame):
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    #menu buttons
    menu1Button = ttk.Button(frame, width=10, text="Find homes", command=lambda:raiseFrame(searchFrame))
    menu1Button.grid(column=1, row=1, sticky=(W, E))
    menu2Button = ttk.Button(frame, width=10, text="Review", command=lambda:raiseFrame(reviewFrame))
    menu2Button.grid(column=2, row=1, sticky=(W, E))

searchMenu(searchFrame, resultFrame)
resultMenu(resultFrame)
reviewMenu(reviewFrame)


root.mainloop()

conn.close()





