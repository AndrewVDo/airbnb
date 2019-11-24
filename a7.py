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
    minPriceEntry = ttk.Entry(frame, width=15, textvariable=minPrice)
    maxPriceEntry = ttk.Entry(frame, width=15, textvariable=maxPrice)
    minPriceEntry.grid(column=1, row=2, sticky=(W, E))
    maxPriceEntry.grid(column=3, row=2, sticky=(W, E))

    ttk.Label(frame, text="Minimum Rooms").grid(column=0, row=3, sticky=W)
    numRoomsEntry = ttk.Entry(frame, width=15, textvariable=numRooms)
    numRoomsEntry.grid(column=1, row=3, sticky=(W, E))

    ttk.Label(frame, text="Stay from").grid(column=0, row=4, sticky=W)
    startMonthBox  = ttk.Combobox(frame, values=MONTH, width=15, textvariable=startMonth)
    startDayBox    = ttk.Combobox(frame, values=DAY, width=15, textvariable=startDay)
    startYearBox   = ttk.Combobox(frame, values=YEAR, width=15, textvariable=startYear)
    startMonthBox.grid(column=1, row=4, sticky=(W, E))
    startDayBox.grid(column=2, row=4, sticky=(W, E))
    startYearBox.grid(column=3, row=4, sticky=(W, E))

    ttk.Label(frame, text="Stay to").grid(column=0, row=5, sticky=W)
    endMonthBox    = ttk.Combobox(frame, values=MONTH, width=15, textvariable=endMonth)
    endDayBox      = ttk.Combobox(frame, values=DAY, width=15, textvariable=endDay)
    endYearBox     = ttk.Combobox(frame, values=YEAR, width=15, textvariable=endYear)
    endMonthBox.grid(column=1, row=5, sticky=(W, E))
    endDayBox.grid(column=2, row=5, sticky=(W, E))
    endYearBox.grid(column=3, row=5, sticky=(W, E))
    
    searchButton = ttk.Button(frame, width=15, text="search", command=search)
    searchButton.grid(column=3, row=6, sticky=(W, E))

    #padding
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    #initial focus
    minPriceEntry.focus()

def reviewMenu(frame):
    print("result menu")

    #padding
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

def resultMenu(frame):
    ttk.Label(frame, text="", width=15).grid(column=2, row=0, sticky=(W,E))
    ttk.Button(frame, text="Book", width=15).grid(column=3, row=0, sticky=(W,E))
    

    tree = ttk.Treeview(frame)
    tree["columns"] = ("name", "desc", "broom", "price")

    tree.column("#0", width=75)
    tree.column("name", width=160)
    tree.column("desc", width=300)
    tree.column("broom", width=75)
    tree.column("price", width=75)

    tree.heading("#0", text="Id")
    tree.heading("name", text="Name")
    tree.heading("desc", text="Description")
    tree.heading("broom", text="Rooms")
    tree.heading("price", text="Price")

    tree.grid(row=1, column=0, columnspan=4)

    #padding
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)


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
    menu1Button = ttk.Button(frame, width=15, text="Find homes", command=lambda:raiseFrame(searchFrame))
    menu1Button.grid(column=0, row=0, sticky=(W, E))
    menu2Button = ttk.Button(frame, width=15, text="Review", command=lambda:raiseFrame(reviewFrame))
    menu2Button.grid(column=1, row=0, sticky=(W, E))

searchMenu(searchFrame, resultFrame)
resultMenu(resultFrame)
reviewMenu(reviewFrame)

raiseFrame(searchFrame)

root.mainloop()

#conn.close()





