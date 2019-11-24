MONTH = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
DAY = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
YEAR = ["2014","2015","2016","2017","2018","2019","2020"]
def mon2num(input):
    num = MONTH.index(input) + 1
    if num < 10:
        return "0{}".format(num)
    else:
        return "{}".format(num)

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
            nRooms = "0"
            if len(minPrice.get()) > 0:
                nRooms = numRooms.get()

            searchFilterStr = """
            SELECT DISTINCT L.id, L.name, LEFT(L.description, 25), L.number_of_bedrooms, C.price
            FROM Listings as L, Calendar as C
            WHERE L.id IN
                (SELECT L2.id FROM Listings as L2
                WHERE L2.number_of_bedrooms >= {}""".format(nRooms)

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

            if len(startMonth.get()) > 0 and len(startDay.get()) > 0 and len(startYear.get()) > 0 and len(endMonth.get()) > 0 and len(endDay.get()) > 0 and len(endYear.get()) > 0:
                minDate = "{}/{}/{}".format(mon2num(startMonth.get()), startDay.get(), startYear.get())
                maxDate = "{}/{}/{}".format(mon2num(endMonth.get()), endDay.get(), endYear.get())

                searchFilterStr += """
                EXCEPT
                    (SELECT C3.listing_id FROM Calendar as C3
                    WHERE C3.date BETWEEN '{}' AND '{}'
                    AND C3.available = 1))
            AND C.price = (SELECT MAX(C4.price) FROM Calendar as C4
                    WHERE C4.listing_id = L.id
                    AND C4.date BETWEEN '{}' AND '{}') """.format( minDate, maxDate, minDate, maxDate )

            print(searchFilterStr)

            raiseFrame(resultFrame)
        except ValueError:
            pass

    #create widgets
    minPrice = StringVar()
    maxPrice = StringVar()
    numRooms = StringVar()
    startMonth = StringVar()
    startDay = StringVar()
    startYear = StringVar()
    endMonth = StringVar()
    endDay = StringVar()
    endYear = StringVar()

    ttk.Label(frame, text="Filter:").grid(column=0, row=1, sticky=W)

    ttk.Label(frame, text="Minimum price:").grid(column=0, row=2, sticky=(W, E))
    ttk.Label(frame, text="Maximum price:").grid(column=2, row=2, sticky=(W, E))
    ttk.Label(frame, text="Minimum Rooms").grid(column=0, row=3, sticky=W)
    ttk.Label(frame, text="Stay from").grid(column=0, row=4, sticky=W)
    ttk.Label(frame, text="Stay to").grid(column=0, row=5, sticky=W)
    ttk.Button(frame, width=15, text="search", command=search).grid(column=3, row=6, sticky=(W, E))
    ttk.Entry(frame, width=15, textvariable=minPrice).grid(column=1, row=2, sticky=(W, E))
    ttk.Entry(frame, width=15, textvariable=maxPrice).grid(column=3, row=2, sticky=(W, E))
    ttk.Entry(frame, width=15, textvariable=numRooms).grid(column=1, row=3, sticky=(W, E))
    ttk.Combobox(frame, values=MONTH, width=15, textvariable=startMonth).grid(column=1, row=4, sticky=(W, E))
    ttk.Combobox(frame, values=DAY, width=15, textvariable=startDay).grid(column=2, row=4, sticky=(W, E))
    ttk.Combobox(frame, values=YEAR, width=15, textvariable=startYear).grid(column=3, row=4, sticky=(W, E))
    ttk.Combobox(frame, values=MONTH, width=15, textvariable=endMonth).grid(column=1, row=5, sticky=(W, E))
    ttk.Combobox(frame, values=DAY, width=15, textvariable=endDay).grid(column=2, row=5, sticky=(W, E))
    ttk.Combobox(frame, values=YEAR, width=15, textvariable=endYear).grid(column=3, row=5, sticky=(W, E))

    #padding
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)


def reviewMenu(frame):
    def post():
        raiseFrame(errorReview)

    name = StringVar()
    currentMonth = StringVar()
    currentDay = StringVar()
    currentYear = StringVar()
    comments = StringVar()

    ttk.Label(frame, text="Name").grid(column=0, row=1, sticky=(W,E))
    ttk.Label(frame, text="Current date").grid(column=0, row=2, sticky=(W,E))
    ttk.Label(frame, text="Comments").grid(column=0, row=3, sticky=(W,E))
    ttk.Button(frame, text="Post", command=post).grid(column=3, row=0, sticky=(W,E))
    ttk.Label(frame, text="").grid(column=0, row=4, sticky=(W,E))
    ttk.Entry(frame, width=15, textvariable=name).grid(column=1, row=1, sticky=(W,E))
    ttk.Combobox(frame, values=MONTH, width=15, textvariable=currentMonth).grid(column=1, row=2, sticky=(W,E))
    ttk.Combobox(frame, values=DAY, width=15, textvariable=currentDay).grid(column=2, row=2, sticky=(W,E))
    ttk.Combobox(frame, values=YEAR, width=15, textvariable=currentYear).grid(column=3, row=2, sticky=(W,E))
    ttk.Entry(frame, textvariable=comments).grid(column=1, row=3, columnspan=4, sticky=(W,E))

    tree = ttk.Treeview(frame)
    tree["columns"] = ("id", "name", "desc", "broom", "price")
    tree.column("#0", width=0, minwidth=0)
    tree.column("id", width=75, minwidth=75)
    tree.column("name", width=160, minwidth=160)
    tree.column("desc", width=300, minwidth=300)
    tree.column("broom", width=75, minwidth=75)
    tree.column("price", width=75, minwidth=75)
    tree.heading("id", text="Id")
    tree.heading("name", text="Name")
    tree.heading("desc", text="Description")
    tree.heading("broom", text="Rooms")
    tree.heading("price", text="Price")
    tree.grid(row=4, column=0, columnspan=4, sticky=(N,E,S,W))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('1','2','3','4','5'))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('a','b','c','d','e'))
    tree.insert('', 'end', values=('a','b','c','d','e'))

    #padding
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

def resultMenu(frame):
    ttk.Label(frame, text="", width=15).grid(column=2, row=0, sticky=(W,E))
    ttk.Button(frame, text="Book", width=15).grid(column=3, row=0, sticky=(W,E))
    
    tree = ttk.Treeview(frame, height=16)
    tree["columns"] = ("id", "name", "desc", "broom", "price")
    tree.column("#0", width=0, minwidth=0)
    tree.column("id", width=75, minwidth=75)
    tree.column("name", width=160, minwidth=160)
    tree.column("desc", width=300, minwidth=300)
    tree.column("broom", width=75, minwidth=75)
    tree.column("price", width=75, minwidth=75)
    tree.heading("id", text="Id")
    tree.heading("name", text="Name")
    tree.heading("desc", text="Description")
    tree.heading("broom", text="Rooms")
    tree.heading("price", text="Price")
    tree.grid(row=1, column=0, columnspan=4, sticky=(N,E,S,W))
    tree.insert('', 'end', values=('a','b','c','d','e'))

    #padding
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

def errorScreen(frame, errorCode):
    ttk.Label(frame, width=15, text="").grid(column=2, row=0)
    if errorCode == 1:
        ttk.Label(frame, width=40, text="                   Search returned no results!").grid(row=1, column=1, columnspan=2)
        ttk.Button(frame, width=40, text="Go Back", command=lambda:raiseFrame(searchFrame)).grid(row=2, column=1, columnspan=2)
    elif errorCode == 2:
        ttk.Label(frame, width=40, text="               Sorry you can't review that listing!").grid(row=1, column=1, columnspan=2)
        ttk.Button(frame, width=40, text="Go Back", command=lambda:raiseFrame(reviewFrame)).grid(row=2, column=1, columnspan=2)

#set root characteristics
root = Tk()
root.title("Airbnb Booker")
root.configure(background='#FF5A60')
#root.minsize(640, 640)

searchFrame = ttk.Frame(root)
resultFrame = ttk.Frame(root)
reviewFrame = ttk.Frame(root)
errorSearch = ttk.Frame(root)
errorReview = ttk.Frame(root)


for frame in (searchFrame, resultFrame, reviewFrame, errorSearch, errorReview):
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    frame.grid_configure(padx=10, pady=10)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    #menu buttons
    ttk.Button(frame, width=15, text="Find homes", command=lambda:raiseFrame(searchFrame)).grid(column=0, row=0, sticky=(W, E))
    ttk.Button(frame, width=15, text="Review", command=lambda:raiseFrame(reviewFrame)).grid(column=1, row=0, sticky=(W, E))

searchMenu(searchFrame, resultFrame)
resultMenu(resultFrame)
reviewMenu(reviewFrame)
errorScreen(errorSearch, 1)
errorScreen(errorReview, 2)

raiseFrame(searchFrame)

root.mainloop()

#conn.close()





