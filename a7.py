MONTH = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
DAY = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
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

        self.searchFrame = self.initFrames()
        self.reviewFrame = self.initFrames()
        self.searchEmpty = self.initFrames()
        self.reviewError = self.initFrames()
        self.successPage = self.initFrames()

        self.loginFrame = self.initFrames()     
        self.menuLogin(self.loginFrame)
        self.raiseFrame(self.loginFrame)
        self.root.mainloop()
        conn.close()


    def raiseFrame(self, FRAME):
        if self.reviewFrame == FRAME:
            self.searchUserBooking()
        elif self.searchFrame == FRAME:
            self.searchFilterBooking()
        FRAME.tkraise()

    def initFrames(self):
        FRAME = ttk.Frame(self.root)
        FRAME.grid(column=0, row=0, sticky=(N, W, E, S))
        FRAME.grid_configure(padx=10, pady=10)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        return FRAME

    #called after we hit login with a user name
    def signIn(self):
        self.menuSearch(self.searchFrame)
        self.menuReview(self.reviewFrame)
        self.menuError(self.searchEmpty, 1, self.searchFrame)
        self.menuError(self.reviewError, 2, self.reviewFrame)
        self.menuError(self.successPage, 3, self.searchFrame)

        self.setupMenu(self.searchFrame)
        self.setupMenu(self.reviewFrame)
        self.setupMenu(self.searchEmpty)
        self.setupMenu(self.reviewError)
        self.setupMenu(self.successPage)

        self.raiseFrame(self.searchFrame)

    def setupMenu(self, FRAME):
        ttk.Button(FRAME, width=20, text="Find homes", command=lambda:self.raiseFrame(self.searchFrame)).grid(column=0, row=0, sticky=(W, E))
        ttk.Button(FRAME, width=20, text="Review", command=lambda:self.raiseFrame(self.reviewFrame)).grid(column=1, row=0, sticky=(W, E))


    def createResultViewer(self, FRAME, HEIGHT):
        tree = ttk.Treeview(FRAME, height=HEIGHT)
        tree["columns"] = ("id", "name", "desc", "broom", "price")
        tree.column("#0", width=0, minwidth=0)
        tree.column("id", width=70, minwidth=70)
        tree.column("name", width=200, minwidth=200)
        tree.column("desc", width=135, minwidth=135)
        tree.column("broom", width=45, minwidth=45)
        tree.column("price", width=45, minwidth=45)
        tree.heading("id", text="Id")
        tree.heading("name", text="Name")
        tree.heading("desc", text="Description")
        tree.heading("broom", text="Rooms")
        tree.heading("price", text="Price")
        return tree


    def createReviewViewer(self, FRAME, HEIGHT):
        tree = ttk.Treeview(FRAME, height=HEIGHT)
        tree["columns"] = ("listing_id", "name", "desc", "broom", "stay_from", "stay_to")
        tree.column("#0", width=0, minwidth=0)
        tree.column("listing_id", width=70, minwidth=70)
        tree.column("name", width=130, minwidth=130)
        tree.column("desc", width=135, minwidth=135)
        tree.column("broom", width=40, minwidth=40)
        tree.column("stay_from", width=60, minwidth=60)
        tree.column("stay_to", width=60, minwidth=60)
        tree.heading("listing_id", text="Id")
        tree.heading("name", text="Name")
        tree.heading("desc", text="Description")
        tree.heading("broom", text="Rooms")
        tree.heading("stay_from", text="Arrive")
        tree.heading("stay_to", text="Depart")
        return tree
    

    def resetVariables(self):
        self.resultViewer.delete(*self.resultViewer.get_children())
        self.reviewViewer.delete(*self.reviewViewer.get_children())

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
                self.resetVariables()
                self.raiseFrame(self.searchEmpty)
            else:
                self.resultViewer.delete(*self.resultViewer.get_children())
                while row:
                    self.resultViewer.insert('', 'end', values=(row[0],row[1],row[2],row[3],row[4]))
                    row = cur.fetchone()

        except ValueError:
            pass


    def searchUserBooking(self):

        searchUserBookingStr="""
        SELECT DISTINCT L.id, L.name, LEFT(L.description, 25), L.number_of_bedrooms, B.stay_from, B.stay_to
        FROM Listings as L, Bookings as B
        WHERE B.guest_name = '{}' AND L.id = B.listing_id;
        """.format(self.userName.get())

        print(searchUserBookingStr)
        cur.execute(searchUserBookingStr)
        row = cur.fetchone()
        self.reviewViewer.delete(*self.reviewViewer.get_children())
        while row:
            self.reviewViewer.insert('', 'end', values=(row[0], row[1], row[2],row[3],row[4],row[5]))
            row = cur.fetchone()

    def postReview(self):
        try:
            cur.execute("SELECT MAX(id) FROM Reviews")
            row = cur.fetchone()
            print('MAX ID: ', row[0])
            maxID = 0
            if not row[0]:
                maxID = 0
            else:
                maxID = row[0] + 1

            curItem = self.reviewViewer.item(self.reviewViewer.focus())

            checkStayedStr="""
            SELECT * FROM Bookings
            WHERE guest_name = '{}' AND '{}' <= GETDATE() AND listing_id = {};
            """.format(self.userName.get(), curItem['values'][4], curItem['values'][0])

            print(checkStayedStr)
            cur.execute(checkStayedStr)

            row = cur.fetchone()
            if cur.rowcount == 0:
                self.resetVariables()
                self.raiseFrame(self.reviewError)
            else:
                insertReviewStr="""
                INSERT INTO Reviews VALUES
                ({}, {}, '{}', '{}');
                """.format(maxID, curItem['values'][0], self.comments.get(), self.userName.get())

                print(insertReviewStr)
                cur.execute(insertReviewStr)
                cur.commit()
                self.raiseFrame(self.successPage)
        except ValueError:
            pass


    def bookListing(self):
        try:
            cur.execute("SELECT MAX(id) FROM Bookings")
            row = cur.fetchone()
            print('MAX ID: ', row[0])
            maxID = 0
            if not row[0]:
                maxID = 0
            else:
                maxID = row[0] + 1

            curItem = self.resultViewer.item(self.resultViewer.focus())
            print ('curItem = ', curItem['values'][0])

            minDate = "{}/{}/{}".format(mon2num(self.startMonth.get()), self.startDay.get(), self.startYear.get())
            maxDate = "{}/{}/{}".format(mon2num(self.endMonth.get()), self.endDay.get(), self.endYear.get())

            bookStr = """
            INSERT INTO Bookings VALUES
            ({}, {}, '{}', '{}', '{}', {});
            """.format(maxID, curItem['values'][0], self.userName.get(), minDate, maxDate, self.numGuest.get())

            print(bookStr)
            cur.execute(bookStr)
            cur.commit()
            self.raiseFrame(self.successPage)
        except ValueError:
            pass



        


    def menuLogin(self, FRAME):
        self.userName = StringVar()
        ttk.Label(      FRAME,  text="Username",        width=20)                               .grid(column=0, row=1, sticky=(W,E))
        ttk.Button(     FRAME,  text="Login",   width=20,   command=lambda:self.signIn())          .grid(column=0, row=2, sticky=(W,E))
        ttk.Entry(      FRAME,  width=20,               textvariable=self.userName)             .grid(column=1, row=1, sticky=(W,E))


    def menuSearch(self, FRAME):
        self.minPrice = StringVar()
        self.maxPrice = StringVar()
        self.numRooms = StringVar()
        self.startMonth = StringVar()
        self.startDay = StringVar()
        self.startYear = StringVar()
        self.endMonth = StringVar()
        self.endDay = StringVar()
        self.endYear = StringVar()
        self.numGuest = StringVar()

        ttk.Label(      FRAME,  text="Guest Name:",)                                            .grid(column=0, row=1, sticky=(W,E))
        ttk.Label(      FRAME,  text=self.userName.get())                                       .grid(column=1, row=1, sticky=(W,E))
        ttk.Label(      FRAME,  text="Minimum price:")                                          .grid(column=0, row=2, sticky=(W, E))
        ttk.Label(      FRAME,  text="Maximum price:")                                          .grid(column=2, row=2, sticky=(W, E))
        ttk.Label(      FRAME,  text="Minimum Rooms")                                           .grid(column=0, row=3, sticky=(W, E))
        ttk.Label(      FRAME,  text="Stay from")                                               .grid(column=0, row=4, sticky=(W, E))
        ttk.Label(      FRAME,  text="Stay to")                                                 .grid(column=0, row=5, sticky=(W, E))
        ttk.Button(     FRAME,  text="search",  width=20,   command=self.searchFilterBooking)   .grid(column=3, row=6, sticky=(W, E))
        ttk.Entry(      FRAME,  width=20,                   textvariable=self.minPrice)         .grid(column=1, row=2, sticky=(W,E))
        ttk.Entry(      FRAME,  width=20,                   textvariable=self.maxPrice)         .grid(column=3, row=2, sticky=(W, E))
        ttk.Entry(      FRAME,  width=20,                   textvariable=self.numRooms)         .grid(column=1, row=3, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=MONTH,   width=20,   textvariable=self.startMonth)       .grid(column=1, row=4, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=DAY,     width=20,   textvariable=self.startDay)         .grid(column=2, row=4, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=YEAR,    width=20,   textvariable=self.startYear)        .grid(column=3, row=4, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=MONTH,   width=20,   textvariable=self.endMonth)         .grid(column=1, row=5, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=DAY,     width=20,   textvariable=self.endDay)           .grid(column=2, row=5, sticky=(W, E))
        ttk.Combobox(   FRAME,  values=YEAR,    width=20,   textvariable=self.endYear)          .grid(column=3, row=5, sticky=(W, E))

        self.resultViewer = self.createResultViewer(FRAME, 10)
        self.resultViewer                                                                       .grid(column=0, row=7, columnspan=4, sticky=(N,W,E,S))
        ttk.Label(      FRAME,  text="Number of guest:")                                        .grid(column=0, row=18, sticky=(W,E))
        ttk.Entry(      FRAME,  textvariable=self.numGuest)                                     .grid(column=1, row=18, sticky=(W,E))
        ttk.Button(     FRAME,  text="Book", command=lambda:self.bookListing())                 .grid(column=3, row=18, sticky=(W,E))


    def menuReview(self, FRAME):
        self.comments = StringVar()
        ttk.Label(FRAME, text="", width=23).grid(column=2, row=0, sticky=(W,E))
        ttk.Label(FRAME, text="", width=23).grid(column=3, row=0, sticky=(W,E))


        ttk.Label(      FRAME,  text="Guest Name")                                              .grid(column=0, row=16, sticky=(W,E))
        ttk.Label(      FRAME,  text=self.userName.get(), width=23)                             .grid(column=1, row=16, sticky=(W,E))
        ttk.Label(      FRAME,  text="Comments:")                                                .grid(column=0, row=17, sticky=(W,E))
        ttk.Button(     FRAME,  text="Post", command=lambda:self.postReview())                 .grid(column=3, row=18, sticky=(W,E))
        ttk.Entry(      FRAME,  textvariable=self.comments)                                          .grid(columnspan=2, column=1, row=17, sticky=(W,E))

        ttk.Label(FRAME, text="Your Bookings").grid(column=0,row=1, sticky=(W,E))
        self.reviewViewer = self.createReviewViewer(FRAME, 13)
        self.reviewViewer                                                                       .grid(column=0, row=2, columnspan=4, sticky=(N,W,E,S))


    def menuError(self, FRAME, ERR, LASTFRAME):
        ttk.Label(FRAME, width=20, text="").grid(column=2, row=0) #space the menu properly
        if ERR == 1:
            ttk.Label(FRAME, width=40, text="                   Search returned no results!")       .grid(row=1, column=1, columnspan=2)
        elif ERR == 2:
            ttk.Label(FRAME, width=40, text="               Sorry you can't review that listing!")  .grid(row=1, column=1, columnspan=2)
        elif ERR ==3:
            ttk.Label(FRAME, width=40, text="                       Success!")       .grid(row=1, column=1, columnspan=2)

        ttk.Button(FRAME, width=40, text="Go Back", command=lambda:self.raiseFrame(LASTFRAME)).grid(row=2, column=1, columnspan=2)
        

X = app()
