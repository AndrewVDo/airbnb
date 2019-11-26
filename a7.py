MONTH = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
DAY = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"]
YEAR = ["2014","2015","2016","2017","2018","2019","2020"]
def mon2num(input):
    num = MONTH.index(input) + 1
    if num < 10:
        return "0{}".format(num)
    else:
        return "{}".format(num)

#https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15
import pyodbc
conn = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;uid=s_ada62;pwd=ybyb62LhTRGMH42T;database=ada62354')
cur = conn.cursor()

cur.execute('SELECT username, password from dbo.helpdesk')
row = cur.fetchone()
while row:
    print ('SQL Server standard login name = ' + row[0])
    row = cur.fetchone()

from tkinter import *
from tkinter import ttk



class app:
    def __init__(self):
        self.root = Tk()
        self.root.title("Airbnb Booker")
        self.root.configure(background='#FF5A60')

        #declare tk frames
        self.loginFrame = self.menuLogin()
        self.searchFrame = self.menuSearch()
        #self.resultFrame = self.menuResult()
        self.reviewFrame = self.menuReview()
        self.searchEmpty = self.menuError(1, self.searchFrame)
        self.reviewError = self.menuError(2, self.reviewFrame)
        self.raiseFrame(self.loginFrame)
        self.root.mainloop()
        conn.close()


    def raiseFrame(self, FRAME):
        FRAME.tkraise()

    def commonUIPre(self, FRAME):
        #setup grid
        FRAME.grid(column=0, row=0, sticky=(N, W, E, S))
        FRAME.grid_configure(padx=10, pady=10)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        #menu buttons
        ttk.Button(FRAME, width=15, text="Find homes", command=lambda:self.raiseFrame(self.searchFrame)).grid(column=0, row=0, sticky=(W, E))
        ttk.Button(FRAME, width=15, text="Review", command=lambda:self.raiseFrame(self.reviewFrame)).grid(column=1, row=0, sticky=(W, E))


    def commonUIPost(self, FRAME):
        for child in FRAME.winfo_children():
            child.grid_configure(padx=5, pady=5)


    def createDBViewer(self, FRAME, HEIGHT):
        tree = ttk.Treeview(FRAME, height=HEIGHT)
        tree["columns"] = ("id", "name", "desc", "broom", "price")
        tree.column("#0", width=0, minwidth=0)
        tree.column("id", width=75, minwidth=75)
        tree.column("name", width=160, minwidth=230)
        tree.column("desc", width=300, minwidth=230)
        tree.column("broom", width=75, minwidth=75)
        tree.column("price", width=75, minwidth=75)
        tree.heading("id", text="Id")
        tree.heading("name", text="Name")
        tree.heading("desc", text="Description")
        tree.heading("broom", text="Rooms")
        tree.heading("price", text="Price")
        return tree


    def searchFilterBooking(self):
        try:

            minDate = "{}/{}/{}".format(mon2num(self.startMonth.get()), self.startDay.get(), self.startYear.get())
            maxDate = "{}/{}/{}".format(mon2num(self.endMonth.get()), self.endDay.get(), self.endYear.get())
            minPrice = 0
            if len(self.minPrice.get()) > 0:
                minPrice = int(self.minPrice.get())
            maxPrice = 100000
            if len(self.maxPrice.get()) > 0:
                maxPrice = int(self.maxPrice.get())

            searchFilterStr = """
            SELECT id, name, LEFT(description, 25), number_of_bedrooms, MAX(price) FROM Listings, Calendar
            WHERE id = listing_id AND
            number_of_bedrooms >= 0{} AND date BETWEEN '{}' AND '{}' AND
            id NOT IN
            (SELECT listing_id FROM Calendar
            WHERE (price > {} OR price < {} OR available = 0) AND date BETWEEN '{}' AND '{}')
            GROUP BY id, name, LEFT(description, 25), number_of_bedrooms;
            """.format(self.numRooms.get(), minDate, maxDate, maxPrice, minPrice, minDate, maxDate)

            print(searchFilterStr)
            cur.execute(searchFilterStr)
            row = cur.fetchone()
            print("rows: ", cur.rowcount)
            if cur.rowcount == 0:
                print("empty")
                self.raiseFrame(self.searchEmpty)
            else:
                self.resultFrame = self.menuResult()
                self.resultViewer.delete(*self.resultViewer.get_children())
                self.raiseFrame(self.resultFrame)
                while row:
                    self.resultViewer.insert('', 'end', values=(row[0],row[1],row[2],row[3],row[4]))
                    row = cur.fetchone()

        except ValueError:
            pass


    def searchUserBooking(self):
        print("search user bookings")

    def bookListing(self):
        try:
            curItem = self.resultViewer.item(self.resultViewer.focus())
            print ('curItem = ', curItem['values'][0])

            minDate = "{}/{}/{}".format(mon2num(self.startMonth.get()), self.startDay.get(), self.startYear.get())
            maxDate = "{}/{}/{}".format(mon2num(self.endMonth.get()), self.endDay.get(), self.endYear.get())

            bookStr = """
            INSERT INTO Bookings(listing_id, guest_name, stay_from, stay_to, number_of_guest)
            VALUES({}, '{}', '{}', '{}', {});
            """.format(curItem['values'][0], self.userName.get(), minDate, maxDate, self.numGuest.get())

            print(bookStr)
            cur.execute(bookStr)
            print("Success")
        except ValueError:
            pass



        


    def menuLogin(self):
        FRAME = ttk.Frame(self.root)

        FRAME.grid(column=0, row=0, sticky=(N, W, E, S))
        FRAME.grid_configure(padx=10, pady=10)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.userName = StringVar()
        ttk.Label(      FRAME,  text="Username",        width=15)                               .grid(column=0, row=1, sticky=(W,E))
        ttk.Button(     FRAME,  text="Login",   width=15,   command=lambda:self.raiseFrame(self.searchFrame)).grid(column=0, row=2, sticky=(W,E))
        ttk.Entry(      FRAME,  width=15,               textvariable=self.userName)             .grid(column=1, row=1, sticky=(W,E))
        self.commonUIPost(FRAME)
        return FRAME


    def menuSearch(self):
        FRAME = ttk.Frame(self.root)
        self.commonUIPre(FRAME)

        self.minPrice = StringVar()
        self.maxPrice = StringVar()
        self.numRooms = StringVar()
        self.startMonth = StringVar()
        self.startDay = StringVar()
        self.startYear = StringVar()
        self.endMonth = StringVar()
        self.endDay = StringVar()
        self.endYear = StringVar()

        ttk.Label(      FRAME,  text="Filter:")                                                 .grid(column=0, row=1, sticky=(W, E))
        ttk.Label(      FRAME,  text="Minimum price:")                                          .grid(column=0, row=2, sticky=(W, E))
        ttk.Label(      FRAME,  text="Maximum price:")                                          .grid(column=2, row=2, sticky=(W, E))
        ttk.Label(      FRAME,  text="Minimum Rooms")                                           .grid(column=0, row=3, sticky=(W, E))
        ttk.Label(      FRAME,  text="Stay from")                                               .grid(column=0, row=4, sticky=(W, E))
        ttk.Label(      FRAME,  text="Stay to")                                                 .grid(column=0, row=5, sticky=(W, E))
        ttk.Button(     FRAME,  text="search",  width=15,   command=self.searchFilterBooking)   .grid(column=3, row=6, sticky=(W, E))
        ttk.Entry(      FRAME,  width=15,                   textvariable=self.minPrice)         .grid(column=1, row=2, sticky=(W, E))
        ttk.Entry(      FRAME,  width=15,                   textvariable=self.maxPrice)         .grid(column=3, row=2, sticky=(W, E))
        ttk.Entry(      FRAME,  width=15,                   textvariable=self.numRooms)         .grid(column=1, row=3, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=MONTH,   width=15,   textvariable=self.startMonth)       .grid(column=1, row=4, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=DAY,     width=15,   textvariable=self.startDay)         .grid(column=2, row=4, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=YEAR,    width=15,   textvariable=self.startYear)        .grid(column=3, row=4, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=MONTH,   width=15,   textvariable=self.endMonth)         .grid(column=1, row=5, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=DAY,     width=15,   textvariable=self.endDay)           .grid(column=2, row=5, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=YEAR,    width=15,   textvariable=self.endYear)          .grid(column=3, row=5, sticky=(W, E))

        self.commonUIPost(FRAME)
        return FRAME


    def menuResult(self):
        FRAME = ttk.Frame(self.root)
        self.commonUIPre(FRAME)
        self.numGuest = StringVar()

        minDate = "{}/{}/{}".format(mon2num(self.startMonth.get()), self.startDay.get(), self.startYear.get())
        maxDate = "{}/{}/{}".format(mon2num(self.endMonth.get()), self.endDay.get(), self.endYear.get())

        ttk.Label(      FRAME,  text="Guest Name",        width=15)                                       .grid(column=1, row=14, sticky=(W,E))
        ttk.Label(      FRAME,  text=self.userName.get(),        width=15)                                       .grid(column=2, row=14, sticky=(W,E))
        ttk.Label(      FRAME,  text="Date of arrival",        width=15)                                       .grid(column=1, row=15, sticky=(W,E))
        ttk.Label(      FRAME,  text=minDate,        width=15)                                       .grid(column=2, row=14, sticky=(W,E))
        ttk.Label(      FRAME,  text="Date of departure",        width=15)                                       .grid(column=1, row=15, sticky=(W,E))
        ttk.Label(      FRAME,  text=maxDate,        width=15)                                          .grid(column=2, row=15, sticky=(W,E))
        ttk.Label(      FRAME,  text="Number of guest", width=15)                                   .grid(column=1, row=16, sticky=(W,E))
        ttk.Entry(      FRAME,  textvariable=self.numGuest, width=15)                           .grid(column=2, row=16, sticky=(W,E))
        ttk.Button(     FRAME,  text="Book", command=lambda:self.bookListing(), width=15)       .grid(column=3, row=16, sticky=(W,E))
        self.resultViewer = self.createDBViewer(FRAME, 10)
        self.resultViewer                                                                       .grid(column=0, row=1, columnspan=4, sticky=(N,W,E,S))

        self.commonUIPost(FRAME)
        return FRAME


    def menuReview(self):
        FRAME = ttk.Frame(self.root)
        self.commonUIPre(FRAME)

        name = StringVar()
        comments = StringVar()

        ttk.Label(      FRAME,  text="Name")                                                    .grid(column=0, row=1, sticky=(W,E))
        ttk.Label(      FRAME,  text="Comments")                                                .grid(column=0, row=2, sticky=(W,E))
        ttk.Label(      FRAME,  text="")                                                        .grid(column=0, row=3, sticky=(W,E))
        ttk.Button(     FRAME,  text="Post", command=lambda:self.bookListing())                 .grid(column=3, row=0, sticky=(W,E))
        ttk.Entry(      FRAME,  width=15, textvariable=name)                                    .grid(column=1, row=1, sticky=(W,E))
        ttk.Entry(      FRAME,  textvariable=comments)                                          .grid(column=1, row=2, columnspan=4, sticky=(W,E))

        self.reviewViewer = self.createDBViewer(FRAME, 4)
        self.reviewViewer                                                                       .grid(column=0, row=4, columnspan=4, sticky=(N,W,E,S))

        self.commonUIPost(FRAME)
        return FRAME


    def menuError(self, ERR, LASTFRAME):
        FRAME = ttk.Frame(self.root)
        self.commonUIPre(FRAME)

        ttk.Label(FRAME, width=15, text="").grid(column=2, row=0) #space the menu properly
        if ERR == 1:
            ttk.Label(FRAME, width=40, text="                   Search returned no results!")       .grid(row=1, column=1, columnspan=2)
        elif ERR == 2:
            ttk.Label(FRAME, width=40, text="               Sorry you can't review that listing!")  .grid(row=1, column=1, columnspan=2)
        ttk.Button(FRAME, width=40, text="Go Back", command=lambda:self.raiseFrame(LASTFRAME)).grid(row=2, column=1, columnspan=2)
        
        self.commonUIPost(FRAME)
        return FRAME


X = app()
