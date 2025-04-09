import os
from tkinter import *
from tkinter import ttk
import mysql.connector as m
from email.message import EmailMessage
import smtplib
import random
import ssl
from datetime import date
import reportlab.platypus
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import time
from dotenv import load_dotenv
load_dotenv()

ddb = m.connect(host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'))
cc = ddb.cursor()

def allsqldata():
    cc.execute("create database if not exists LittleTomecustomerdata;")
    try:
        cc.execute("create database LittleTome;")
        cc.execute("use LittleTome;")
    except:
        cc.execute("use LittleTome;")
    try:
        cc.execute("create table couponcodes(code varchar(50),discount_perecentage int);")
        cc.execute("insert into couponcodes values('qqzz',5),('zzqq',10);")
        ddb.commit()
    except:
        pass
    cc.execute("create table if not exists purchasedata(sno int,customername varchar(40),amountpaid int,purchasedate date,purchasetime time);")
    cc.execute("create table if not exists credentials(username varchar(50),password varchar(50));")
    try:
        cc.execute("CREATE TABLE biography (object INT,name VARCHAR(50),price INT);")
        cc.execute("INSERT INTO biography VALUES(1,'The Diary of a yong girl',100),(2,'Einstein',499),(3,'David Mccullough',388),(4,'Elizabeth The Queen',397),(5,'The Last Lion',499),(6,'Steve Jobs',529),(7,'Hamilton',400),(8,'The Happiest Man on Earth',247);")
    except:
        pass
    try:
        cc.execute("CREATE TABLE comics (object INT,name VARCHAR(50),price INT);")
        cc.execute("INSERT INTO comics VALUES(1,'Avengers Forever',999),(2,'Stranger Things',1299),(3,'The Joker',899),(4,'Ms.Marvel',499),(5,'Spiderman',299),(6,'Timeless Tales',829),(7,'Scooby Doo',729),(8,'Thor',329);")
    except:
        pass
    try:
        cc.execute("CREATE TABLE crimethriller  (object INT,name VARCHAR(50),price INT);")
        cc.execute("INSERT INTO crimethriller VALUES(1,'The Serenity Murder',1399),(2,'The Innocent Man',375),(3,'Mind Hunter',999),(4,'Purity Pursuit',499),(5,'Then She Was Gone',799),(6,'The Suspect',899),(7,'The Push',422),(8,'Point of no return',299);")
    except:
        pass
    try:
        cc.execute("CREATE TABLE fiction(object INT,name VARCHAR(50),price INT);")
        cc.execute("INSERT INTO fiction VALUES(1,'The Beast from the East',499),(2,'Ghosts of The Silent Hills',189),(3,'Harry Potter and the Philosopher''s Stone',289),(4,'The Mystry of the School on Fire',149),(5,'Get in Trouble',399),(6,'Blue Ticket',499),(7,'The Girl Who Drank The Moon',259),(8,'Kite Runner',299);")
    except:
        pass
    try:
        cc.execute("CREATE TABLE indianwriting(object INT,name VARCHAR(50),price INT);")
        cc.execute("INSERT INTO indianwriting values(1,'The White Tiger',227),(2,'The Arugumentative Indian',387),(3,'The Palace of Illusions',174),(4,'Last Queen',387),(5,'This is not your story',400),(6,'Swami Vivekanda',300),(7,'A P J Abdul Kalam',200),(8,'The Great War',499);")
    except:
        pass
    try:
        cc.execute("CREATE TABLE novel(object INT,name VARCHAR(60),price INT);")
        cc.execute("INSERT INTO novel values(1,'Cigatha Christic',350),(2,'Neil Gaiman',149),(3,'Harry Potter',284),(4,'To Kill A Mocking Bird',198),(5,'A tale of two Cities',124),(6,'The Spanish Love Deception',452),(7,' The Glass hotel',339),(8,'Everything happens for a reason',587);")
    except:
        pass
    try:
        cc.execute("CREATE TABLE bookmarks(object INT,name VARCHAR(60),price INT);")
        cc.execute("INSERT INTO bookmarks values(1,'Wooden Bookmark',699),(2,'Resin Bookmark(pack of 2)',399),(3,'Feather Bookmark Metal Finish',599),(4,'Glastic Finish Bookmark',799),(5,'Golden Bookmark',999),(6,'Geometric Flower Bookmark',399),(7,'Mesh Styled BookMark',599),(8,'Corner Fabric Bookmark',79);")
    except:
        pass
    ddb.commit()

allsqldata()
db = m.connect(host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'), database='LittleTome')
db1 = m.connect(host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'), database='LittleTomecustomerdata')
c = db.cursor()
c1 = db1.cursor()
l1=[]
l2=[]
l3=[]
l4=[]
l5=[]
l6=[]
l7=[]
total=0
ogp=0
cartcount = 0
onevariable=0
onevariable1=0
c.execute("select * from couponcodes;")
codes=c.fetchall()


def sendpdf():
    global forpdf
    e = os.getenv("SENDER_EMAIL")
    epass = os.getenv("API_KEY")
    er = forpdf
    subject = 'Invoice'
    body = '''Thank you for choosing LittleTome.\nYou'll have a great reading experience.\nThe invoice is attached below.'''
    
    em = EmailMessage()
    em['From'] = e
    em['To'] = er
    em['Subject'] = subject
    em.set_content(body)

    text = ssl.create_default_context()
    with open('invoice.pdf', 'rb') as contentfile:
        content = contentfile.read()
        em.add_attachment(content, maintype='application', subtype='pdf', filename='invoice.pdf')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=text) as smtp:
        smtp.login(e, epass)
        smtp.sendmail(e, er, em.as_string())

    os.remove("invoice.pdf")

def invoice():
    global cartcount,booknames,bookprice,ogp,total,discountp,customern,today,ctime
    tableData = [["SNO.", "Book ", "Price"]]
    for i in range(0,len(booknames)):
        l=[str(i+1),booknames[i],bookprice[i]]
        tableData.append(l)
    if total==ogp:
        dtext="0"
    else:
        discount=ogp-total
        dtext ="-"+str(int(discount)) + " (" + str(discountp) + "% OFF)"

    docu = SimpleDocTemplate("invoice.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    doc_style = styles["Heading1"]
    doc_style.alignment = 2
    doc_style2 = styles["Heading2"]
    doc_style2.alignment = 0

    tableData.append((["Subtotal","--------",str(ogp)]))
    tableData.append((["Discount","--------",dtext]))
    tableData.append((["Total","--------",str(int(total))]))

    something=reportlab.platypus.Image("logo.png",width=None, height=None, kind='direct',
                 mask="auto", lazy=1, hAlign="CENTER", useDPI=False)
    totext = Paragraph("To:"+customern,doc_style2)
    text2 = Paragraph("Date:"+str(today),doc_style2)
    text3=Paragraph("Time:"+str(ctime),doc_style2)
    space = Paragraph("", doc_style)
    style = TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("GRID", (0, 0), (cartcount+3, cartcount+3), 1, colors.black),
        ("BACKGROUND", (0, 0), (3, 0), colors.skyblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.aliceblue),
    ])
    table = Table(tableData, style=style)
    docu.build([something,totext,text2,text3,space,table])
    sendpdf()

def purchasedata():
    global total,customern,l1,l2,l3,l4,l5,l6,l7,booknames,bookprice,today,ctime
    today=date.today()
    t = time.localtime()
    ctime = time.strftime("%H:%M:%S", t)
    c.execute("select max(sno) from purchasedata;")
    num=c.fetchall()
    num=num[0][0]
    if num:
        num+=1
    else:
        num=1
    query="insert into purchasedata(sno,customername,amountpaid,purchasedate,purchasetime) values(%s,%s,%s,%s,%s);"
    data=(num,customern,int(total),str(today),str(ctime))
    c.execute(query,data)

    c1.execute(("create table if not exists {} (sno int, book varchar(50),genre varchar(20),price int,date date,time time);").format(customern))
    genre=[]
    booknames=[]
    bookprice=[]
    for i in l1:
        c.execute(('select name,price from fiction where object= ({});').format(i))
        a=c.fetchall()
        a=a[0]
        booknames.append(a[0])
        bookprice.append(a[1])
        genre.append("Fiction")
    for i in l2:
        c.execute(('select name,price from novel where object= ({});').format(i))
        a = c.fetchall()
        a = a[0]
        booknames.append(a[0])
        bookprice.append(a[1])
        genre.append("Novel")
    for i in l3:
        c.execute(('select name,price from comics where object= ({});').format(i))
        a = c.fetchall()
        a = a[0]
        booknames.append(a[0])
        bookprice.append(a[1])
        genre.append("Comics")
    for i in l4:
        c.execute(('select name,price from biography where object= ({});').format(i))
        a = c.fetchall()
        a = a[0]
        booknames.append(a[0])
        bookprice.append(a[1])
        genre.append("Biography")
    for i in l5:
        c.execute(('select name,price from crimethriller where object= ({});').format(i))
        a = c.fetchall()
        a = a[0]
        booknames.append(a[0])
        bookprice.append(a[1])
        genre.append("Crime Thriller")
    for i in l6:
        c.execute(('select name,price from indianwriting where object= ({});').format(i))
        a = c.fetchall()
        a = a[0]
        booknames.append(a[0])
        bookprice.append(a[1])
        genre.append("Indian Writing")
    for i in l7:
        c.execute(('select name,price from bookmarks where object= ({});').format(i))
        a = c.fetchall()
        a = a[0]
        booknames.append(a[0])
        bookprice.append(a[1])
        genre.append("Bookmarks")

    query1="insert into "+str(customern)+"(sno,book,price,genre,date,time) values(%s,%s,%s,%s,%s,%s);"
    c1.execute(("select max(sno) from ({}) ;").format(customern))
    count=c1.fetchall()
    count=count[0][0]
    if count!=None:
        count+=1
    else:
        count=1
    a=len(booknames)
    for i in range(0,a):
        data1=(count,booknames[i],bookprice[i],genre[i],str(today),str(ctime))
        c1.execute(query1,data1)
        count+=1
    db.commit()
    db1.commit()

def all_children (window) :
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

def ps():
    global masterwin,pscanvas
    widget_list = all_children(masterwin)
    for item in widget_list:
        item.place_forget()
    purchasedata()
    pscanvas = Canvas(
        masterwin,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    pscanvas.place(x=0, y=0)

    backgroundimgq = PhotoImage(file=f"psbg.png")
    pscanvas.create_image(
        500.0, 300.0,
        image=backgroundimgq)

    pscanvas.create_text(
        675, 260,
        text="₹" + str(int(total)),
        fill="#1e1e1e",
        font=("UrbanistRoman-Regular", int(45.0)))

    img0q = PhotoImage(file=f"emailinvoiceb.png")
    b0q = Button(
        image=img0q,
        borderwidth=0,
        highlightthickness=0,
        command=invoice,
        relief="flat")

    b0q.place(
        x=516, y=483,
        width=126,
        height=82)

    img1q = PhotoImage(file=f"mainmenub.png")
    b1q = Button(
        image=img1q,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:selectionmenu(2),
        relief="flat")

    b1q.place(
        x=358, y=483,
        width=126,
        height=82)
    mainloop()

def payment():
    global entry00, entry11, ttt, otp, entry11,pcanvas,masterwin,ttt1,ttt2
    def OTP():
        global onevariable, total, otp, entry11, pcanvas, ttt1, ttt2, paymentui, onevariable1,forpdf
        if onevariable != 0:
            entry11.delete(0, END)
            pcanvas.delete(ttt)
            if onevariable1 != 0:
                pcanvas.delete(ttt1)
                pcanvas.delete(ttt2)
                b22.place_forget()
                onevariable1 -= 1
            onevariable -= 1
            b00.configure(state=DISABLED)
        total = total // 1
        a = entry00.get()
        b = a[-1:-5:-1][::-1]
        if b == ".com":
            otp = random.randint(123456, 987654)
            e = os.getenv("SENDER_EMAIL")        
            epass = os.getenv("API_KEY")
            forpdf=a
            er = a
            subject = 'One Time Password'
            body =str(otp)+" is your OTP for the purchase of INR "+str(total)+" at LittleTome. Do not share this with anyone"
            em = EmailMessage()
            em['From'] = e
            em['To'] = er
            em['Subject'] = subject
            em.set_content(body)
            text = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=text) as smtp:
                    smtp.login(e, epass)
                    smtp.sendmail(e, er, em.as_string())
                onevariable += 1
                b00.configure(state=ACTIVE)
                abcd = pcanvas.create_text(
                    700, 210,
                    text="OTP sent successfully",
                    fill="black",
                    font=("UrbanistRoman-Light", int(12.0)))
                masterwin.after(2700, pcanvas.delete, abcd)
            except:
                abcd = pcanvas.create_text(
                    740, 210,
                    text="Please check your internet connection and try again",
                    fill="black",
                    font=("UrbanistRoman-Light", int(12.0)))
                masterwin.after(2700, pcanvas.delete, abcd)

        else:
            warning(0)
    def warning(x):
        if x == 0:
            abc = pcanvas.create_text(
                705, 430,
                text="Enter a valid EMAIL ID",
                fill="white",
                font=("UrbanistRoman-Light", int(12.0)))
            masterwin.after(2700, pcanvas.delete, abc)
        elif x == 1:
            abc = pcanvas.create_text(
                705, 430,
                text="Enter the 6-digit otp sent to your GMAIL ID",
                fill="white",
                font=("UrbanistRoman-Light", int(11.0)))
            masterwin.after(2700, pcanvas.delete, abc)
    def checkotp():
        global entry11, pcanvas, ttt, pcanvas, otp, paymentui, ttt1, ttt2,onevariable1
        b = entry11.get()
        if len(b)==6:
            pcanvas.delete(ttt,ttt1,ttt2)
            if otp == int(b):
                ttt = pcanvas.create_text(
                    705, 400,
                    text="OTP Verified",
                    fill="white",
                    font=("UrbanistRoman-Light", int(13.0)))
                ttt1 = pcanvas.create_text(
                    235, 327,
                    text="You are about to pay",
                    fill="white",
                    font=("UrbanistRoman-Light", int(35.0)))
                ttt2 = pcanvas.create_text(
                    230, 390,
                    text='₹' + str(total),
                    fill="white",
                    font=("UrbanistRoman-Light", int(30.0)))
                b22.place(
                    x=348, y=495,
                    width=317,
                    height=69)
                onevariable1 += 1
            else:
                ttt = pcanvas.create_text(
                    705, 400,
                    text="Invalid OTP",
                    fill="white",
                    font=("UrbanistRoman-Light", int(13.0)))
                if onevariable1 != 0:
                    pcanvas.delete(ttt1)
                    pcanvas.delete(ttt2)
                    b22.place_forget()
                    onevariable1 -= 1
        else:
            if onevariable1!=0:
                pcanvas.delete(ttt)
                pcanvas.delete(ttt1)
                pcanvas.delete(ttt2)
                b22.place_forget()
                ttt = pcanvas.create_text(
                    705, 400,
                    text="Invalid OTP",
                    fill="white",
                    font=("UrbanistRoman-Light", int(13.0)))

                onevariable1 -= 1
            warning(1)
    widget_list = all_children(masterwin)
    for item in widget_list:
        item.place_forget()
    pcanvas = Canvas(
        masterwin,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    pcanvas.place(x=0, y=0)

    backgroundimg = PhotoImage(file=f"pbg.png")
    background = pcanvas.create_image(
        500.0, 300.0,
        image=backgroundimg)

    img00 = PhotoImage(file=f"checkb.png")
    b00 = Button(
        image=img00,
        borderwidth=0,
        highlightthickness=0,
        command=checkotp,
        relief="flat",state=DISABLED)

    b00.place(
        x=859, y=346,
        width=72,
        height=27)

    img11 = PhotoImage(file=f"sendb.png")
    b11 = Button(
        image=img11,
        borderwidth=0,
        highlightthickness=0,
        command=OTP,
        relief="flat")

    b11.place(
        x=859, y=267,
        width=72,
        height=27)

    entry0img = PhotoImage(file=f"img_textBox0.png")
    entry0bg = pcanvas.create_image(
        700.0, 280.5,
        image=entry0img)

    entry00 = Entry(
        bd=0,
        bg="#b6bdcf",
        highlightthickness=0)

    entry00.place(
        x=570.0, y=261,
        width=260.0,
        height=37)

    entry1img = PhotoImage(file=f"img_textBox1.png")
    entry1bg = pcanvas.create_image(
        700.0, 359.5,
        image=entry1img)

    entry11 = Entry(
        bd=0,
        bg="#b6bdcf",
        highlightthickness=0)

    entry11.place(
        x=570.0, y=340,
        width=260.0,
        height=37)

    img22 = PhotoImage(file=f"payb.png")
    b22 = Button(
        image=img22,
        borderwidth=0,
        highlightthickness=0,
        command=ps,
        relief="flat")


    img33 = PhotoImage(file=f"cancelb.png")
    b33 = Button(
        image=img33,
        borderwidth=0,
        highlightthickness=0,
        command=lambda :checkout(1),
        relief="flat")

    b33.place(
        x=23, y=17,
        width=124,
        height=36)
    ttt = pcanvas.create_text(
        705, 400,
        text="",
        fill="#000000",
        font=("UrbanistRoman-Light", int(13.0)))
    ttt1 = pcanvas.create_text(
        235, 327,
        text="",
        fill="white",
        font=("UrbanistRoman-Light", int(35.0)))
    ttt2 = pcanvas.create_text(
        230, 390,
        text="",
        fill="white",
        font=("UrbanistRoman-Light", int(30.0)))
    mainloop()

def bookmarks():
    global bk, p1, p2, p3, p4, p5, p6, p7, p8, n1, n2, n3, n4, n5, n6, n7, n8
    bk = 'Bookmarks'
    c.execute('select price from bookmarks where object=1;')
    aq = c.fetchall()
    p1 = aq[0]
    c.execute('select price from bookmarks where object=2;')
    bq = c.fetchall()
    p2 = bq[0]
    c.execute('select price from bookmarks where object=3;')
    cq = c.fetchall()
    p3 = cq[0]
    c.execute('select price from bookmarks where object=4;')
    dq = c.fetchall()
    p4 = dq[0]
    c.execute('select price from bookmarks where object=5;')
    eq = c.fetchall()
    p5 = eq[0]
    c.execute('select price from bookmarks where object=6;')
    fq = c.fetchall()
    p6 = fq[0]
    c.execute('select price from bookmarks where object=7;')
    gq = c.fetchall()
    p7 = gq[0]
    c.execute('select price from bookmarks where object=8;')
    hq = c.fetchall()
    p8 = hq[0]
    c.execute('select name from bookmarks where object=1;')
    aw = c.fetchall()
    n1 = aw[0]
    c.execute('select name from bookmarks where object=2;')
    bw = c.fetchall()
    n2 = bw[0]
    c.execute('select name from bookmarks where object=3;')
    cw = c.fetchall()
    n3 = cw[0]
    c.execute('select name from bookmarks where object=4;')
    dw = c.fetchall()
    n4 = dw[0]
    c.execute('select name from bookmarks where object=5;')
    ew = c.fetchall()
    n5 = ew[0]
    c.execute('select name from bookmarks where object=6;')
    fw = c.fetchall()
    n6 = fw[0]
    c.execute('select name from bookmarks where object=7;')
    gw = c.fetchall()
    n7 = gw[0]
    c.execute('select name from bookmarks where object=8;')
    hw = c.fetchall()
    n8 = hw[0]
    ui()

def fiction():
    global bk, p1, p2, p3, p4, p5, p6, p7, p8, n1, n2, n3, n4, n5, n6, n7, n8
    bk = 'Fiction'
    c.execute('select price from fiction where object=1;')
    aq = c.fetchall()
    p1 = aq[0]
    c.execute('select price from fiction where object=2;')
    bq = c.fetchall()
    p2 = bq[0]
    c.execute('select price from fiction where object=3;')
    cq = c.fetchall()
    p3 = cq[0]
    c.execute('select price from fiction where object=4;')
    dq = c.fetchall()
    p4 = dq[0]
    c.execute('select price from fiction where object=5;')
    eq = c.fetchall()
    p5 = eq[0]
    c.execute('select price from fiction where object=6;')
    fq = c.fetchall()
    p6 = fq[0]
    c.execute('select price from fiction where object=7;')
    gq = c.fetchall()
    p7 = gq[0]
    c.execute('select price from fiction where object=8;')
    hq = c.fetchall()
    p8 = hq[0]
    c.execute('select name from fiction where object=1;')
    aw = c.fetchall()
    n1 = aw[0]
    c.execute('select name from fiction where object=2;')
    bw = c.fetchall()
    n2 = bw[0]
    c.execute('select name from fiction where object=3;')
    cw = c.fetchall()
    n3 = cw[0]
    c.execute('select name from fiction where object=4;')
    dw = c.fetchall()
    n4 = dw[0]
    c.execute('select name from fiction where object=5;')
    ew = c.fetchall()
    n5 = ew[0]
    c.execute('select name from fiction where object=6;')
    fw = c.fetchall()
    n6 = fw[0]
    c.execute('select name from fiction where object=7;')
    gw = c.fetchall()
    n7 = gw[0]
    c.execute('select name from fiction where object=8;')
    hw = c.fetchall()
    n8 = hw[0]
    ui()

def novel():
    global bk, p1, p2, p3, p4, p5, p6, p7, p8, n1, n2, n3, n4, n5, n6, n7, n8
    bk = 'Novel'
    c.execute('select price from novel where object=1;')
    aq = c.fetchall()
    p1 = aq[0]
    c.execute('select price from novel where object=2;')
    bq = c.fetchall()
    p2 = bq[0]
    c.execute('select price from novel where object=3;')
    cq = c.fetchall()
    p3 = cq[0]
    c.execute('select price from novel where object=4;')
    dq = c.fetchall()
    p4 = dq[0]
    c.execute('select price from novel where object=5;')
    eq = c.fetchall()
    p5 = eq[0]
    c.execute('select price from novel where object=6;')
    fq = c.fetchall()
    p6 = fq[0]
    c.execute('select price from novel where object=7;')
    gq = c.fetchall()
    p7 = gq[0]
    c.execute('select price from novel where object=8;')
    hq = c.fetchall()
    p8 = hq[0]
    c.execute('select name from novel where object=1;')
    aw = c.fetchall()
    n1 = aw[0]
    c.execute('select name from novel where object=2;')
    bw = c.fetchall()
    n2 = bw[0]
    c.execute('select name from novel where object=3;')
    cw = c.fetchall()
    n3 = cw[0]
    c.execute('select name from novel where object=4;')
    dw = c.fetchall()
    n4 = dw[0]
    c.execute('select name from novel where object=5;')
    ew = c.fetchall()
    n5 = ew[0]
    c.execute('select name from novel where object=6;')
    fw = c.fetchall()
    n6 = fw[0]
    c.execute('select name from novel where object=7;')
    gw = c.fetchall()
    n7 = gw[0]
    c.execute('select name from novel where object=8;')
    hw = c.fetchall()
    n8 = hw[0]
    ui()

def comics():
    global bk, p1, p2, p3, p4, p5, p6, p7, p8, n1, n2, n3, n4, n5, n6, n7, n8
    bk = 'Comics'
    c.execute('select price from comics where object=1;')
    aq = c.fetchall()
    p1 = aq[0]
    c.execute('select price from comics where object=2;')
    bq = c.fetchall()
    p2 = bq[0]
    c.execute('select price from comics where object=3;')
    cq = c.fetchall()
    p3 = cq[0]
    c.execute('select price from comics where object=4;')
    dq = c.fetchall()
    p4 = dq[0]
    c.execute('select price from comics where object=5;')
    eq = c.fetchall()
    p5 = eq[0]
    c.execute('select price from comics where object=6;')
    fq = c.fetchall()
    p6 = fq[0]
    c.execute('select price from comics where object=7;')
    gq = c.fetchall()
    p7 = gq[0]
    c.execute('select price from comics where object=8;')
    hq = c.fetchall()
    p8 = hq[0]
    c.execute('select name from comics where object=1;')
    aw = c.fetchall()
    n1 = aw[0]
    c.execute('select name from comics where object=2;')
    bw = c.fetchall()
    n2 = bw[0]
    c.execute('select name from comics where object=3;')
    cw = c.fetchall()
    n3 = cw[0]
    c.execute('select name from comics where object=4;')
    dw = c.fetchall()
    n4 = dw[0]
    c.execute('select name from comics where object=5;')
    ew = c.fetchall()
    n5 = ew[0]
    c.execute('select name from comics where object=6;')
    fw = c.fetchall()
    n6 = fw[0]
    c.execute('select name from comics where object=7;')
    gw = c.fetchall()
    n7 = gw[0]
    c.execute('select name from comics where object=8;')
    hw = c.fetchall()
    n8 = hw[0]
    ui()

def biography():
    global bk, p1, p2, p3, p4, p5, p6, p7, p8, n1, n2, n3, n4, n5, n6, n7, n8
    bk = 'Biography'
    c.execute('select price from biography where object=1;')
    aq = c.fetchall()
    p1 = aq[0]
    c.execute('select price from biography where object=2;')
    bq = c.fetchall()
    p2 = bq[0]
    c.execute('select price from biography where object=3;')
    cq = c.fetchall()
    p3 = cq[0]
    c.execute('select price from biography where object=4;')
    dq = c.fetchall()
    p4 = dq[0]
    c.execute('select price from biography where object=5;')
    eq = c.fetchall()
    p5 = eq[0]
    c.execute('select price from biography where object=6;')
    fq = c.fetchall()
    p6 = fq[0]
    c.execute('select price from biography where object=7;')
    gq = c.fetchall()
    p7 = gq[0]
    c.execute('select price from biography where object=8;')
    hq = c.fetchall()
    p8 = hq[0]
    c.execute('select name from biography where object=1;')
    aw = c.fetchall()
    n1 = aw[0]
    c.execute('select name from biography where object=2;')
    bw = c.fetchall()
    n2 = bw[0]
    c.execute('select name from biography where object=3;')
    cw = c.fetchall()
    n3 = cw[0]
    c.execute('select name from biography where object=4;')
    dw = c.fetchall()
    n4 = dw[0]
    c.execute('select name from biography where object=5;')
    ew = c.fetchall()
    n5 = ew[0]
    c.execute('select name from biography where object=6;')
    fw = c.fetchall()
    n6 = fw[0]
    c.execute('select name from biography where object=7;')
    gw = c.fetchall()
    n7 = gw[0]
    c.execute('select name from biography where object=8;')
    hw = c.fetchall()
    n8 = hw[0]
    ui()

def crimethriller():
    global bk, p1, p2, p3, p4, p5, p6, p7, p8, n1, n2, n3, n4, n5, n6, n7, n8
    bk = 'Crime Thriller'
    c.execute('select price from crimethriller where object=1;')
    aq = c.fetchall()
    p1 = aq[0]
    c.execute('select price from crimethriller where object=2;')
    bq = c.fetchall()
    p2 = bq[0]
    c.execute('select price from crimethriller where object=3;')
    cq = c.fetchall()
    p3 = cq[0]
    c.execute('select price from crimethriller where object=4;')
    dq = c.fetchall()
    p4 = dq[0]
    c.execute('select price from crimethriller where object=5;')
    eq = c.fetchall()
    p5 = eq[0]
    c.execute('select price from crimethriller where object=6;')
    fq = c.fetchall()
    p6 = fq[0]
    c.execute('select price from crimethriller where object=7;')
    gq = c.fetchall()
    p7 = gq[0]
    c.execute('select price from crimethriller where object=8;')
    hq = c.fetchall()
    p8 = hq[0]
    c.execute('select name from crimethriller where object=1;')
    aw = c.fetchall()
    n1 = aw[0]
    c.execute('select name from crimethriller where object=2;')
    bw = c.fetchall()
    n2 = bw[0]
    c.execute('select name from crimethriller where object=3;')
    cw = c.fetchall()
    n3 = cw[0]
    c.execute('select name from crimethriller where object=4;')
    dw = c.fetchall()
    n4 = dw[0]
    c.execute('select name from crimethriller where object=5;')
    ew = c.fetchall()
    n5 = ew[0]
    c.execute('select name from crimethriller where object=6;')
    fw = c.fetchall()
    n6 = fw[0]
    c.execute('select name from crimethriller where object=7;')
    gw = c.fetchall()
    n7 = gw[0]
    c.execute('select name from crimethriller where object=8;')
    hw = c.fetchall()
    n8 = hw[0]
    ui()

def indianwriting():
    global bk, p1, p2, p3, p4, p5, p6, p7, p8, n1, n2, n3, n4, n5, n6, n7, n8
    bk = 'Indian Writing'
    c.execute('select price from indianwriting where object=1;')
    aq = c.fetchall()
    p1 = aq[0]
    c.execute('select price from indianwriting where object=2;')
    bq = c.fetchall()
    p2 = bq[0]
    c.execute('select price from indianwriting where object=3;')
    cq = c.fetchall()
    p3 = cq[0]
    c.execute('select price from indianwriting where object=4;')
    dq = c.fetchall()
    p4 = dq[0]
    c.execute('select price from indianwriting where object=5;')
    eq = c.fetchall()
    p5 = eq[0]
    c.execute('select price from indianwriting where object=6;')
    fq = c.fetchall()
    p6 = fq[0]
    c.execute('select price from indianwriting where object=7;')
    gq = c.fetchall()
    p7 = gq[0]
    c.execute('select price from indianwriting where object=8;')
    hq = c.fetchall()
    p8 = hq[0]
    c.execute('select name from indianwriting where object=1;')
    aw = c.fetchall()
    n1 = aw[0]
    c.execute('select name from indianwriting where object=2;')
    bw = c.fetchall()
    n2 = bw[0]
    c.execute('select name from indianwriting where object=3;')
    cw = c.fetchall()
    n3 = cw[0]
    c.execute('select name from indianwriting where object=4;')
    dw = c.fetchall()
    n4 = dw[0]
    c.execute('select name from indianwriting where object=5;')
    ew = c.fetchall()
    n5 = ew[0]
    c.execute('select name from indianwriting where object=6;')
    fw = c.fetchall()
    n6 = fw[0]
    c.execute('select name from indianwriting where object=7;')
    gw = c.fetchall()
    n7 = gw[0]
    c.execute('select name from indianwriting where object=8;')
    hw = c.fetchall()
    n8 = hw[0]
    ui()

def couponcheck():
    def displayoffer(response):
        global totaltext, otext,total,discountp
        total=int(total)
        a='coupon code applied!'
        b='coupon code invalid'
        c='enter a coupon code to apply'
        if response==1:
            d = currentcode[1]
            discountp=d
            total = ogp
            total = total - ((d / 100) * ogp)
            ccanvas.delete(totaltext)
            ccanvas.delete(otext)
            totaltext = ccanvas.create_text(855, 383,
                                           text="₹" + str(int(total)),
                                           fill="#000000",
                                           font=("UrbanistRoman-Regular", int(35.0)))
            otext = ccanvas.create_text(
                905, 280,
                text=a,
                fill="#000000",
                font=("None", int(15.0)), width=100)

        elif response==0:
            total = ogp
            ccanvas.delete(totaltext)
            ccanvas.delete(otext)
            totaltext = ccanvas.create_text(855, 383,
                                           text="₹" + str(int(total)),
                                           fill="#000000",
                                           font=("UrbanistRoman-Regular", int(35.0)))
            otext = ccanvas.create_text(
                905, 280,
                text=b,
                fill="#000000",
                font=("None", int(15.0)), width=100)
        elif response==2:
            total = ogp
            ccanvas.delete(totaltext)
            ccanvas.delete(otext)
            totaltext = ccanvas.create_text(855, 383,
                                           text="₹" + str(int(total)),
                                           fill="#000000",
                                           font=("UrbanistRoman-Regular", int(35.0)))
            otext = ccanvas.create_text(
                905, 280,
                text=c,
                fill="#000000",
                font=("None", int(11.0)), width=100)
    global couponcode,totaltext,total,otext,ogp,codes
    a=couponcode.get()
    currentcode=[]
    if len(a)!=0:
        for i in codes:
            if i[0] == a:
                currentcode.append(i[0])
                currentcode.append(i[1])
                displayoffer(1)
                break
            elif i[0]!=a:
                displayoffer(0)
    else:
        displayoffer(2)

def redirecttockeckout(y,y1):
    global ogp
    if y < 2:
        if y1==0:
            abcde = bcanvas.create_text(
                443, 573,
                text="Please select at least 2 books or bookmarks to checkout",
                fill="white",
                font=("UrbanistRoman-Light", int(20.0)))
        elif y1==1:
            abcde = scanvas.create_text(
                500, 573,
                text="Please select at least 2 books or bookmarks to checkout",
                fill="black",
                font=("UrbanistRoman-Light", int(20.0)))

    else:
        ogp = total
        checkout()

def checkout(x=0):
    global couponcode, totaltext, otext, ogp, l1, l2, l3,l4,l5,l6,total,masterwin,ccanvas
    widget_list = all_children(masterwin)
    for item in widget_list:
        item.place_forget()
    if x==1:
        total=ogp

    ccanvas = Canvas(
        masterwin,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    ckbg = PhotoImage(file=f'background.png')
    ccanvas.create_image(500, 300, image=ckbg)
    totaltext=ccanvas.create_text(855, 383,
        text="₹" + str(total),
        fill="#000000",
        font=("UrbanistRoman-Regular", int(35.0)))
    img0 = PhotoImage(file=f"img0.png")
    b0 = Button(
        image=img0,
        borderwidth=0,
        highlightthickness=0,
        command=payment,
        relief="flat")

    b0.place(
        x=618.25, y=466.5,
        width=313,
        height=83)
    couponcode_img = PhotoImage(file=f"imgtextBox0.png")
    ccanvas.create_image(
        670, 287.5,
        image=couponcode_img)
    couponcode = Entry(
        bd=0,
        bg="#a9d4dd",
        highlightthickness=0)

    couponcode.place(
        x=600, y=270,
        width=139.0,
        height=35)
    ccanvas.place(x=0, y=0)
    otext = ccanvas.create_text(
        905, 280,
        text="",
        fill="#000000",
        font=("None", int(15.0)), width=100)

    img1 = PhotoImage(file=f"img1.png")
    b1 = Button(
        image=img1,
        borderwidth=0,
        highlightthickness=0,
        command=couponcheck,
        relief="flat")

    b1.place(
        x=770, y=268,
        width=88,
        height=37)


    img2 = PhotoImage(file=f"img2.png")
    b2 = Button(
        image=img2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:selectionmenu(1),
        relief="flat")

    b2.place(
        x=49, y=10,
        width=108,
        height=29)
    ccanvas.create_text(
        280, 573,
        text="You have added "+str(cartcount)+" items to your cart",
        fill="black",
        font=("UrbanistRoman-Light", int(15.0)))


    wrapper=LabelFrame(masterwin)
    mycanvas=Canvas(wrapper,height=470,width=450,bd=0,highlightthickness=0)
    mycanvas.pack(side='left',fill='y')
    scrollbar=ttk.Scrollbar(wrapper,orient='vertical',command=mycanvas.yview)
    scrollbar.pack(side='right',fill='y')
    mycanvas.configure(yscrollcommand=scrollbar.set)
    myframe=Frame(mycanvas,height=0,width=0,borderwidth=0,highlightthickness=0,relief='flat')
    mycanvas.bind('<Configure>',lambda e:mycanvas.configure(scrollregion=mycanvas.bbox('all')))
    mycanvas.create_window((0,0),window=myframe,anchor='nw')
    wrapper.place(x=50,y=65)

    pricegap=0
    textgap=0
    bookgap=0
    bookbgtemplate=PhotoImage(file=f"frame.png")
    noofbooks=len(l1)+len(l2)+len(l3)+len(l4)+len(l5)+len(l6)+len(l7)
    templatelenght=0
    for i in range(noofbooks):
        mycanvas.create_image(
            0, templatelenght,
            image=bookbgtemplate)
        templatelenght+=235

    if len(l1)!=0:
        pht1_fic = PhotoImage(file=f"images/fiction/picture1.png", width=110, height=145)
        pht2_fic = PhotoImage(file=f"images/fiction/picture2.png", width=110, height=145)
        pht3_fic = PhotoImage(file=f"images/fiction/picture3.png", width=110, height=145)
        pht4_fic = PhotoImage(file=f"images/fiction/picture4.png", width=110, height=145)
        pht5_fic = PhotoImage(file=f"images/fiction/picture5.png", width=110, height=145)
        pht6_fic = PhotoImage(file=f"images/fiction/picture6.png", width=110, height=145)
        pht7_fic = PhotoImage(file=f"images/fiction/picture7.png", width=110, height=145)
        pht8_fic = PhotoImage(file=f"images/fiction/picture8.png", width=110, height=145)


        photolistf=[pht1_fic,pht2_fic,pht3_fic,pht4_fic,pht5_fic,pht6_fic,pht7_fic,pht8_fic]
        anotherlist=[]
        anotheronelist=[]
        anotheranotherlist=[]
        for i in l1:
            qqq=i-1
            anotherlist.append(photolistf[qqq])
            c.execute(('select name from fiction where object= ({});').format(i))
            a=c.fetchall()
            anotheronelist.append(a[0][0])
            c.execute(('select price from fiction where object= ({});').format(i))
            a = c.fetchall()
            anotheranotherlist.append(a[0][0])
        for i in anotherlist:
            mycanvas.create_image(-110 ,bookgap, image=i)
            bookgap+=235
        for i in anotheronelist:
            mycanvas.create_text(30, textgap,
                                 text=i,
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(15.0)),width=140)
            textgap+=235
        for i in anotheranotherlist:
            mycanvas.create_text(150, pricegap,
                                 text='₹'+str(i),
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(20.0)), width=140)
            pricegap+=235

    if len(l2)!=0:
        pht1_n = PhotoImage(file=f"images/novel/picture1.png", width=110, height=145)
        pht2_n = PhotoImage(file=f"images/novel/picture2.png", width=110, height=145)
        pht3_n = PhotoImage(file=f"images/novel/picture3.png", width=110, height=145)
        pht4_n = PhotoImage(file=f"images/novel/picture4.png", width=110, height=145)
        pht5_n = PhotoImage(file=f"images/novel/picture5.png", width=110, height=145)
        pht6_n = PhotoImage(file=f"images/novel/picture6.png", width=110, height=145)
        pht7_n = PhotoImage(file=f"images/novel/picture7.png", width=110, height=145)
        pht8_n = PhotoImage(file=f"images/novel/picture8.png", width=110, height=145)
        photolistn=[pht1_n,pht2_n,pht3_n,pht4_n,pht5_n,pht6_n,pht7_n,pht8_n]
        anotherlist=[]
        anotheronelist = []
        anotheranotherlist = []
        for i in l2:
            qqq=i-1
            anotherlist.append(photolistn[qqq])
            c.execute(('select name from novel where object= ({});').format(i))
            a = c.fetchall()
            anotheronelist.append(a[0][0])
            c.execute(('select price from novel where object= ({});').format(i))
            a = c.fetchall()
            anotheranotherlist.append(a[0][0])
        for i in anotherlist:
            mycanvas.create_image(-110 ,bookgap, image=i)
            bookgap+=235
        for i in anotheronelist:
            mycanvas.create_text(30, textgap,
                                 text=i,
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(15.0)),width=140)
            textgap+=235
        for i in anotheranotherlist:
            mycanvas.create_text(150, pricegap,
                                 text='₹'+str(i),
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(20.0)), width=140)
            pricegap+=235

    if len(l3)!=0:
        pht1_comics = PhotoImage(file=f"images/comics/picture1.png", width=110, height=145)
        pht2_comics = PhotoImage(file=f"images/comics/picture2.png", width=110, height=145)
        pht3_comics = PhotoImage(file=f"images/comics/picture3.png", width=110, height=145)
        pht4_comics = PhotoImage(file=f"images/comics/picture4.png", width=110, height=145)
        pht5_comics = PhotoImage(file=f"images/comics/picture5.png", width=110, height=145)
        pht6_comics = PhotoImage(file=f"images/comics/picture6.png", width=110, height=145)
        pht7_comics = PhotoImage(file=f"images/comics/picture7.png", width=110, height=145)
        pht8_comics = PhotoImage(file=f"images/comics/picture8.png", width=110, height=145)
        photolistc=[pht1_comics,pht2_comics,pht3_comics,pht4_comics,pht5_comics,pht6_comics,pht7_comics,pht8_comics]
        anotherlist=[]
        anotheronelist = []
        anotheranotherlist = []
        for i in l3:
            qqq=i-1
            anotherlist.append(photolistc[qqq])
            c.execute(('select name from comics where object= ({});').format(i))
            a = c.fetchall()
            anotheronelist.append(a[0][0])
            c.execute(('select price from comics where object= ({});').format(i))
            a = c.fetchall()
            anotheranotherlist.append(a[0][0])
        for i in anotherlist:
            mycanvas.create_image(-110, bookgap, image=i)
            bookgap += 235
        for i in anotheronelist:
            mycanvas.create_text(30, textgap,
                                 text=i,
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(15.0)),width=140)
            textgap+=235
        for i in anotheranotherlist:
            mycanvas.create_text(150, pricegap,
                                 text='₹'+str(i),
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(20.0)), width=140)
            pricegap+=235

    if len(l4)!=0:
        pht1_b = PhotoImage(file=f"images/biography/picture1.png", width=110, height=145)
        pht2_b = PhotoImage(file=f"images/biography/picture2.png", width=110, height=145)
        pht3_b = PhotoImage(file=f"images/biography/picture3.png", width=110, height=145)
        pht4_b = PhotoImage(file=f"images/biography/picture4.png", width=110, height=145)
        pht5_b = PhotoImage(file=f"images/biography/picture5.png", width=110, height=145)
        pht6_b = PhotoImage(file=f"images/biography/picture6.png", width=110, height=145)
        pht7_b = PhotoImage(file=f"images/biography/picture7.png", width=110, height=145)
        pht8_b = PhotoImage(file=f"images/biography/picture8.png", width=110, height=145)


        photolistf=[pht1_b,pht2_b,pht3_b,pht4_b,pht5_b,pht6_b,pht7_b,pht8_b]
        anotherlist=[]
        anotheronelist=[]
        anotheranotherlist=[]
        for i in l4:
            qqq=i-1
            anotherlist.append(photolistf[qqq])
            c.execute(('select name from biography where object= ({});').format(i))
            a=c.fetchall()
            anotheronelist.append(a[0][0])
            c.execute(('select price from biography where object= ({});').format(i))
            a = c.fetchall()
            anotheranotherlist.append(a[0][0])
        for i in anotherlist:
            mycanvas.create_image(-110 ,bookgap, image=i)
            bookgap+=235
        for i in anotheronelist:
            mycanvas.create_text(30, textgap,
                                 text=i,
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(15.0)),width=140)
            textgap+=235
        for i in anotheranotherlist:
            mycanvas.create_text(150, pricegap,
                                 text='₹'+str(i),
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(20.0)), width=140)
            pricegap+=235

    if len(l5)!=0:
        pht1_ct = PhotoImage(file=f"images/crimethriller/picture1.png", width=110, height=145)
        pht2_ct = PhotoImage(file=f"images/crimethriller/picture2.png", width=110, height=145)
        pht3_ct = PhotoImage(file=f"images/crimethriller/picture3.png", width=110, height=145)
        pht4_ct = PhotoImage(file=f"images/crimethriller/picture4.png", width=110, height=145)
        pht5_ct = PhotoImage(file=f"images/crimethriller/picture5.png", width=110, height=145)
        pht6_ct = PhotoImage(file=f"images/crimethriller/picture6.png", width=110, height=145)
        pht7_ct = PhotoImage(file=f"images/crimethriller/picture7.png", width=110, height=145)
        pht8_ct = PhotoImage(file=f"images/crimethriller/picture8.png", width=110, height=145)


        photolistf=[pht1_ct,pht2_ct,pht3_ct,pht4_ct,pht5_ct,pht6_ct,pht7_ct,pht8_ct]
        anotherlist=[]
        anotheronelist=[]
        anotheranotherlist=[]
        for i in l5:
            qqq=i-1
            anotherlist.append(photolistf[qqq])
            c.execute(('select name from crimethriller where object= ({});').format(i))
            a=c.fetchall()
            anotheronelist.append(a[0][0])
            c.execute(('select price from crimethriller where object= ({});').format(i))
            a = c.fetchall()
            anotheranotherlist.append(a[0][0])
        for i in anotherlist:
            mycanvas.create_image(-110 ,bookgap, image=i)
            bookgap+=235
        for i in anotheronelist:
            mycanvas.create_text(30, textgap,
                                 text=i,
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(15.0)),width=140)
            textgap+=235
        for i in anotheranotherlist:
            mycanvas.create_text(150, pricegap,
                                 text='₹'+str(i),
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(20.0)), width=140)
            pricegap+=235

    if len(l6)!=0:
        pht1_iw = PhotoImage(file=f"images/indianwriting/picture1.png", width=110, height=145)
        pht2_iw = PhotoImage(file=f"images/indianwriting/picture2.png", width=110, height=145)
        pht3_iw = PhotoImage(file=f"images/indianwriting/picture3.png", width=110, height=145)
        pht4_iw = PhotoImage(file=f"images/indianwriting/picture4.png", width=110, height=145)
        pht5_iw = PhotoImage(file=f"images/indianwriting/picture5.png", width=110, height=145)
        pht6_iw = PhotoImage(file=f"images/indianwriting/picture6.png", width=110, height=145)
        pht7_iw = PhotoImage(file=f"images/indianwriting/picture7.png", width=110, height=145)
        pht8_iw = PhotoImage(file=f"images/indianwriting/picture8.png", width=110, height=145)


        photolistf=[pht1_iw,pht2_iw,pht3_iw,pht4_iw,pht5_iw,pht6_iw,pht7_iw,pht8_iw]
        anotherlist=[]
        anotheronelist=[]
        anotheranotherlist=[]
        for i in l6:
            qqq=i-1
            anotherlist.append(photolistf[qqq])
            c.execute(('select name from indianwriting where object= ({});').format(i))
            a=c.fetchall()
            anotheronelist.append(a[0][0])
            c.execute(('select price from indianwriting where object= ({});').format(i))
            a = c.fetchall()
            anotheranotherlist.append(a[0][0])
        for i in anotherlist:
            mycanvas.create_image(-110 ,bookgap, image=i)
            bookgap+=235
        for i in anotheronelist:
            mycanvas.create_text(30, textgap,
                                 text=i,
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(15.0)),width=140)
            textgap+=235
        for i in anotheranotherlist:
            mycanvas.create_text(150, pricegap,
                                 text='₹'+str(i),
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(20.0)), width=140)
            pricegap+=235
    if len(l7)!=0:
        pht1_bb = PhotoImage(file=f"images/bookmarks/picture1.png", width=110, height=145)
        pht2_bb = PhotoImage(file=f"images/bookmarks/picture2.png", width=110, height=145)
        pht3_bb = PhotoImage(file=f"images/bookmarks/picture3.png", width=110, height=145)
        pht4_bb = PhotoImage(file=f"images/bookmarks/picture4.png", width=110, height=145)
        pht5_bb = PhotoImage(file=f"images/bookmarks/picture5.png", width=110, height=145)
        pht6_bb = PhotoImage(file=f"images/bookmarks/picture6.png", width=110, height=145)
        pht7_bb = PhotoImage(file=f"images/bookmarks/picture7.png", width=110, height=145)
        pht8_bb = PhotoImage(file=f"images/bookmarks/picture8.png", width=110, height=145)
        photolistn=[pht1_bb,pht2_bb,pht3_bb,pht4_bb,pht5_bb,pht6_bb,pht7_bb,pht8_bb]
        anotherlist=[]
        anotheronelist = []
        anotheranotherlist = []
        for i in l7:
            qqq=i-1
            anotherlist.append(photolistn[qqq])
            c.execute(('select name from bookmarks where object= ({});').format(i))
            a = c.fetchall()
            anotheronelist.append(a[0][0])
            c.execute(('select price from bookmarks where object= ({});').format(i))
            a = c.fetchall()
            anotheranotherlist.append(a[0][0])
        for i in anotherlist:
            mycanvas.create_image(-110 ,bookgap, image=i)
            bookgap+=235
        for i in anotheronelist:
            mycanvas.create_text(30, textgap,
                                 text=i,
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(15.0)),width=140)
            textgap+=235
        for i in anotheranotherlist:
            mycanvas.create_text(150, pricegap,
                                 text='₹'+str(i),
                                 fill="#000000",
                                 font=("UrbanistRoman-Regular", int(20.0)), width=140)
            pricegap+=235

    mainloop()

def ui():
    global masterwin, w, booktype, cartcount, buyimage, buyimage1,bcanvas,l1,l2,l3,l4,l5,l6
    scanvas.delete("all")
    widget_list = all_children(masterwin)
    for item in widget_list:
        item.place_forget()
    def refcartcount():
        global w
        w.configure(text=newcount)
    def buybutton(z):
        global cartcount, newcount, l1, l2, l3,l4,l5,l6,total,uiwin,buyimage,buyimage1
        if booktype == 'Fiction':
            if z not in l1:
                cartcount = cartcount + 1
                newcount = cartcount
                refcartcount()
                l1.append(z)
                c.execute(('select price from fiction where object= ({});').format(z))
                aq = c.fetchall()
                total=total+ (aq[0][0])
                blist[z-1].configure(image=buyimage)

            else:
                cartcount = cartcount - 1
                newcount = cartcount
                refcartcount()
                l1.remove(z)
                c.execute(('select price from fiction where object= ({});').format(z))
                aq = c.fetchall()
                total = total - (aq[0][0])
                blist[z - 1].configure(image=buyimage1)

        elif booktype == 'Novel':
            if z not in l2:
                cartcount = cartcount + 1
                newcount = cartcount
                refcartcount()
                l2.append(z)
                c.execute(('select price from novel where object= ({});').format(z))
                aq = c.fetchall()
                total = total + (aq[0][0])
                blist[z - 1].configure(image=buyimage)
            else:
                cartcount = cartcount - 1
                newcount = cartcount
                refcartcount()
                l2.remove(z)
                c.execute(('select price from novel where object= ({});').format(z))
                aq = c.fetchall()
                total = total - (aq[0][0])
                blist[z - 1].configure(image=buyimage1)
        elif booktype == 'Comics':
            if z not in l3:
                cartcount = cartcount + 1
                newcount = cartcount
                refcartcount()
                l3.append(z)
                c.execute(('select price from comics where object= ({});').format(z))
                aq = c.fetchall()
                total = total + (aq[0][0])
                blist[z - 1].configure(image=buyimage)
            else:
                cartcount = cartcount - 1
                newcount = cartcount
                refcartcount()
                l3.remove(z)
                c.execute(('select price from comics where object= ({});').format(z))
                aq = c.fetchall()
                total = total - (aq[0][0])
                blist[z - 1].configure(image=buyimage1)
        elif booktype == 'Biography':
            if z not in l4:
                cartcount = cartcount + 1
                newcount = cartcount
                refcartcount()
                l4.append(z)
                c.execute(('select price from biography where object= ({});').format(z))
                aq = c.fetchall()
                total = total + (aq[0][0])
                blist[z - 1].configure(image=buyimage)
            else:
                cartcount = cartcount - 1
                newcount = cartcount
                refcartcount()
                l4.remove(z)
                c.execute(('select price from biography where object= ({});').format(z))
                aq = c.fetchall()
                total = total - (aq[0][0])
                blist[z - 1].configure(image=buyimage1)
        elif booktype == 'Crime Thriller':
            if z not in l5:
                cartcount = cartcount + 1
                newcount = cartcount
                refcartcount()
                l5.append(z)
                c.execute(('select price from crimethriller where object= ({});').format(z))
                aq = c.fetchall()
                total = total + (aq[0][0])
                blist[z - 1].configure(image=buyimage)

            else:
                cartcount = cartcount - 1
                newcount = cartcount
                refcartcount()
                l5.remove(z)
                c.execute(('select price from crimethriller where object= ({});').format(z))
                aq = c.fetchall()
                total = total - (aq[0][0])
                blist[z - 1].configure(image=buyimage1)

        elif booktype == 'Indian Writing':
            if z not in l6:
                cartcount = cartcount + 1
                newcount = cartcount
                refcartcount()
                l6.append(z)
                c.execute(('select price from indianwriting where object= ({});').format(z))
                aq = c.fetchall()
                total = total + (aq[0][0])
                blist[z - 1].configure(image=buyimage)
            else:
                cartcount = cartcount - 1
                newcount = cartcount
                refcartcount()
                l6.remove(z)
                c.execute(('select price from indianwriting where object= ({});').format(z))
                aq = c.fetchall()
                total = total - (aq[0][0])
                blist[z - 1].configure(image=buyimage1)
        elif booktype == 'Bookmarks':
            if z not in l7:
                cartcount = cartcount + 1
                newcount = cartcount
                refcartcount()
                l7.append(z)
                c.execute(('select price from bookmarks where object= ({});').format(z))
                aq = c.fetchall()
                total = total + (aq[0][0])
                blist[z - 1].configure(image=buyimage)
            else:
                cartcount = cartcount - 1
                newcount = cartcount
                refcartcount()
                l7.remove(z)
                c.execute(('select price from bookmarks where object= ({});').format(z))
                aq = c.fetchall()
                total = total - (aq[0][0])
                blist[z - 1].configure(image=buyimage1)
    booktype = bk
    price1 = p1
    price2 = p2
    price3 = p3
    price4 = p4
    price5 = p5
    price6 = p6
    price7 = p7
    price8 = p8
    name1 = n1[0]
    name2 = n2[0]
    name3 = n3[0]
    name4 = n4[0]
    name5 = n5[0]
    name6 = n6[0]
    name7 = n7[0]
    name8 = n8[0]
    buyimage = PhotoImage(file=f"uiimgr.png")
    buyimage1= PhotoImage(file=f"uiimg0.png")

    if booktype == "Fiction":
        pht1_img = PhotoImage(file=f"images/fiction/picture1.png", width=110, height=145)
        pht2_img = PhotoImage(file=f"images/fiction/picture2.png", width=110, height=145)
        pht3_img = PhotoImage(file=f"images/fiction/picture3.png", width=110, height=145)
        pht4_img = PhotoImage(file=f"images/fiction/picture4.png", width=110, height=145)
        pht5_img = PhotoImage(file=f"images/fiction/picture5.png", width=110, height=145)
        pht6_img = PhotoImage(file=f"images/fiction/picture6.png", width=110, height=145)
        pht7_img = PhotoImage(file=f"images/fiction/picture7.png", width=110, height=145)
        pht8_img = PhotoImage(file=f"images/fiction/picture8.png", width=110, height=145)
        uiimg0 = PhotoImage(file=f"uiimg0.png")
        uiimg1 = PhotoImage(file=f"uiimg0.png")
        uiimg2 = PhotoImage(file=f"uiimg0.png")
        uiimg3 = PhotoImage(file=f"uiimg0.png")
        uiimg4 = PhotoImage(file=f"uiimg0.png")
        uiimg5 = PhotoImage(file=f"uiimg0.png")
        uiimg6 = PhotoImage(file=f"uiimg0.png")
        uiimg7 = PhotoImage(file=f"uiimg0.png")
        if len(l1)!=0:
            for i in l1:
                tn=i-1
                if tn == 0:
                    uiimg0 = PhotoImage(file=f"uiimgr.png")
                if tn == 1:
                    uiimg1 = PhotoImage(file=f"uiimgr.png")
                if tn == 2:
                    uiimg2 = PhotoImage(file=f"uiimgr.png")
                if tn == 3:
                    uiimg3 = PhotoImage(file=f"uiimgr.png")
                if tn == 4:
                    uiimg4 = PhotoImage(file=f"uiimgr.png")
                if tn == 5:
                    uiimg5 = PhotoImage(file=f"uiimgr.png")
                if tn == 6:
                    uiimg6 = PhotoImage(file=f"uiimgr.png")
                if tn == 7:
                    uiimg7 = PhotoImage(file=f"uiimgr.png")
    elif booktype == 'Comics':
        pht1_img = PhotoImage(file=f"images/comics/picture1.png", width=110, height=145)
        pht2_img = PhotoImage(file=f"images/comics/picture2.png", width=110, height=145)
        pht3_img = PhotoImage(file=f"images/comics/picture3.png", width=110, height=145)
        pht4_img = PhotoImage(file=f"images/comics/picture4.png", width=110, height=145)
        pht5_img = PhotoImage(file=f"images/comics/picture5.png", width=110, height=145)
        pht6_img = PhotoImage(file=f"images/comics/picture6.png", width=110, height=145)
        pht7_img = PhotoImage(file=f"images/comics/picture7.png", width=110, height=145)
        pht8_img = PhotoImage(file=f"images/comics/picture8.png", width=110, height=145)
        uiimg0 = PhotoImage(file=f"uiimg0.png")
        uiimg1 = PhotoImage(file=f"uiimg0.png")
        uiimg2 = PhotoImage(file=f"uiimg0.png")
        uiimg3 = PhotoImage(file=f"uiimg0.png")
        uiimg4 = PhotoImage(file=f"uiimg0.png")
        uiimg5 = PhotoImage(file=f"uiimg0.png")
        uiimg6 = PhotoImage(file=f"uiimg0.png")
        uiimg7 = PhotoImage(file=f"uiimg0.png")
        if len(l3)!=0:
            for i in l3:
                tn=i-1
                if tn == 0:
                    uiimg0 = PhotoImage(file=f"uiimgr.png")
                if tn == 1:
                    uiimg1 = PhotoImage(file=f"uiimgr.png")
                if tn == 2:
                    uiimg2 = PhotoImage(file=f"uiimgr.png")
                if tn == 3:
                    uiimg3 = PhotoImage(file=f"uiimgr.png")
                if tn == 4:
                    uiimg4 = PhotoImage(file=f"uiimgr.png")
                if tn == 5:
                    uiimg5 = PhotoImage(file=f"uiimgr.png")
                if tn == 6:
                    uiimg6 = PhotoImage(file=f"uiimgr.png")
                if tn == 7:
                    uiimg7 = PhotoImage(file=f"uiimgr.png")
    elif booktype == "Novel":
        pht1_img = PhotoImage(file=f"images/novel/picture1.png", width=110, height=145)
        pht2_img = PhotoImage(file=f"images/novel/picture2.png", width=110, height=145)
        pht3_img = PhotoImage(file=f"images/novel/picture3.png", width=110, height=145)
        pht4_img = PhotoImage(file=f"images/novel/picture4.png", width=110, height=145)
        pht5_img = PhotoImage(file=f"images/novel/picture5.png", width=110, height=145)
        pht6_img = PhotoImage(file=f"images/novel/picture6.png", width=110, height=145)
        pht7_img = PhotoImage(file=f"images/novel/picture7.png", width=110, height=145)
        pht8_img = PhotoImage(file=f"images/novel/picture8.png", width=110, height=145)
        uiimg0 = PhotoImage(file=f"uiimg0.png")
        uiimg1 = PhotoImage(file=f"uiimg0.png")
        uiimg2 = PhotoImage(file=f"uiimg0.png")
        uiimg3 = PhotoImage(file=f"uiimg0.png")
        uiimg4 = PhotoImage(file=f"uiimg0.png")
        uiimg5 = PhotoImage(file=f"uiimg0.png")
        uiimg6 = PhotoImage(file=f"uiimg0.png")
        uiimg7 = PhotoImage(file=f"uiimg0.png")
        if len(l2) != 0:
            for i in l2:
                tn = i - 1
                if tn == 0:
                    uiimg0 = PhotoImage(file=f"uiimgr.png")
                if tn == 1:
                    uiimg1 = PhotoImage(file=f"uiimgr.png")
                if tn == 2:
                    uiimg2 = PhotoImage(file=f"uiimgr.png")
                if tn == 3:
                    uiimg3 = PhotoImage(file=f"uiimgr.png")
                if tn == 4:
                    uiimg4 = PhotoImage(file=f"uiimgr.png")
                if tn == 5:
                    uiimg5 = PhotoImage(file=f"uiimgr.png")
                if tn == 6:
                    uiimg6 = PhotoImage(file=f"uiimgr.png")
                if tn == 7:
                    uiimg7 = PhotoImage(file=f"uiimgr.png")
    elif booktype == "Biography":
        pht1_img = PhotoImage(file=f"images/biography/picture1.png", width=110, height=145)
        pht2_img = PhotoImage(file=f"images/biography/picture2.png", width=110, height=145)
        pht3_img = PhotoImage(file=f"images/biography/picture3.png", width=110, height=145)
        pht4_img = PhotoImage(file=f"images/biography/picture4.png", width=110, height=145)
        pht5_img = PhotoImage(file=f"images/biography/picture5.png", width=110, height=145)
        pht6_img = PhotoImage(file=f"images/biography/picture6.png", width=110, height=145)
        pht7_img = PhotoImage(file=f"images/biography/picture7.png", width=110, height=145)
        pht8_img = PhotoImage(file=f"images/biography/picture8.png", width=110, height=145)
        uiimg0 = PhotoImage(file=f"uiimg0.png")
        uiimg1 = PhotoImage(file=f"uiimg0.png")
        uiimg2 = PhotoImage(file=f"uiimg0.png")
        uiimg3 = PhotoImage(file=f"uiimg0.png")
        uiimg4 = PhotoImage(file=f"uiimg0.png")
        uiimg5 = PhotoImage(file=f"uiimg0.png")
        uiimg6 = PhotoImage(file=f"uiimg0.png")
        uiimg7 = PhotoImage(file=f"uiimg0.png")
        if len(l4) != 0:
            for i in l4:
                tn = i - 1
                if tn == 0:
                    uiimg0 = PhotoImage(file=f"uiimgr.png")
                if tn == 1:
                    uiimg1 = PhotoImage(file=f"uiimgr.png")
                if tn == 2:
                    uiimg2 = PhotoImage(file=f"uiimgr.png")
                if tn == 3:
                    uiimg3 = PhotoImage(file=f"uiimgr.png")
                if tn == 4:
                    uiimg4 = PhotoImage(file=f"uiimgr.png")
                if tn == 5:
                    uiimg5 = PhotoImage(file=f"uiimgr.png")
                if tn == 6:
                    uiimg6 = PhotoImage(file=f"uiimgr.png")
                if tn == 7:
                    uiimg7 = PhotoImage(file=f"uiimgr.png")
    elif booktype == "Crime Thriller":
        pht1_img = PhotoImage(file=f"images/crimethriller/picture1.png", width=110, height=145)
        pht2_img = PhotoImage(file=f"images/crimethriller/picture2.png", width=110, height=145)
        pht3_img = PhotoImage(file=f"images/crimethriller/picture3.png", width=110, height=145)
        pht4_img = PhotoImage(file=f"images/crimethriller/picture4.png", width=110, height=145)
        pht5_img = PhotoImage(file=f"images/crimethriller/picture5.png", width=110, height=145)
        pht6_img = PhotoImage(file=f"images/crimethriller/picture6.png", width=110, height=145)
        pht7_img = PhotoImage(file=f"images/crimethriller/picture7.png", width=110, height=145)
        pht8_img = PhotoImage(file=f"images/crimethriller/picture8.png", width=110, height=145)
        uiimg0 = PhotoImage(file=f"uiimg0.png")
        uiimg1 = PhotoImage(file=f"uiimg0.png")
        uiimg2 = PhotoImage(file=f"uiimg0.png")
        uiimg3 = PhotoImage(file=f"uiimg0.png")
        uiimg4 = PhotoImage(file=f"uiimg0.png")
        uiimg5 = PhotoImage(file=f"uiimg0.png")
        uiimg6 = PhotoImage(file=f"uiimg0.png")
        uiimg7 = PhotoImage(file=f"uiimg0.png")
        if len(l5) != 0:
            for i in l5:
                tn = i - 1
                if tn == 0:
                    uiimg0 = PhotoImage(file=f"uiimgr.png")
                if tn == 1:
                    uiimg1 = PhotoImage(file=f"uiimgr.png")
                if tn == 2:
                    uiimg2 = PhotoImage(file=f"uiimgr.png")
                if tn == 3:
                    uiimg3 = PhotoImage(file=f"uiimgr.png")
                if tn == 4:
                    uiimg4 = PhotoImage(file=f"uiimgr.png")
                if tn == 5:
                    uiimg5 = PhotoImage(file=f"uiimgr.png")
                if tn == 6:
                    uiimg6 = PhotoImage(file=f"uiimgr.png")
                if tn == 7:
                    uiimg7 = PhotoImage(file=f"uiimgr.png")
    elif booktype == "Indian Writing":
        pht1_img = PhotoImage(file=f"images/indianwriting/picture1.png", width=110, height=145)
        pht2_img = PhotoImage(file=f"images/indianwriting/picture2.png", width=110, height=145)
        pht3_img = PhotoImage(file=f"images/indianwriting/picture3.png", width=110, height=145)
        pht4_img = PhotoImage(file=f"images/indianwriting/picture4.png", width=110, height=145)
        pht5_img = PhotoImage(file=f"images/indianwriting/picture5.png", width=110, height=145)
        pht6_img = PhotoImage(file=f"images/indianwriting/picture6.png", width=110, height=145)
        pht7_img = PhotoImage(file=f"images/indianwriting/picture7.png", width=110, height=145)
        pht8_img = PhotoImage(file=f"images/indianwriting/picture8.png", width=110, height=145)
        uiimg0 = PhotoImage(file=f"uiimg0.png")
        uiimg1 = PhotoImage(file=f"uiimg0.png")
        uiimg2 = PhotoImage(file=f"uiimg0.png")
        uiimg3 = PhotoImage(file=f"uiimg0.png")
        uiimg4 = PhotoImage(file=f"uiimg0.png")
        uiimg5 = PhotoImage(file=f"uiimg0.png")
        uiimg6 = PhotoImage(file=f"uiimg0.png")
        uiimg7 = PhotoImage(file=f"uiimg0.png")
        if len(l6) != 0:
            for i in l6:
                tn = i - 1
                if tn == 0:
                    uiimg0 = PhotoImage(file=f"uiimgr.png")
                if tn == 1:
                    uiimg1 = PhotoImage(file=f"uiimgr.png")
                if tn == 2:
                    uiimg2 = PhotoImage(file=f"uiimgr.png")
                if tn == 3:
                    uiimg3 = PhotoImage(file=f"uiimgr.png")
                if tn == 4:
                    uiimg4 = PhotoImage(file=f"uiimgr.png")
                if tn == 5:
                    uiimg5 = PhotoImage(file=f"uiimgr.png")
                if tn == 6:
                    uiimg6 = PhotoImage(file=f"uiimgr.png")
                if tn == 7:
                    uiimg7 = PhotoImage(file=f"uiimgr.png")
    elif booktype == "Bookmarks":
        pht1_img = PhotoImage(file=f"images/bookmarks/picture1.png", width=120, height=120)
        pht2_img = PhotoImage(file=f"images/bookmarks/picture2.png", width=120, height=116)
        pht3_img = PhotoImage(file=f"images/bookmarks/picture3.png", width=120, height=120)
        pht4_img = PhotoImage(file=f"images/bookmarks/picture4.png", width=110, height=147)
        pht5_img = PhotoImage(file=f"images/bookmarks/picture5.png", width=120, height=120)
        pht6_img = PhotoImage(file=f"images/bookmarks/picture6.png", width=120, height=120)
        pht7_img = PhotoImage(file=f"images/bookmarks/picture7.png", width=120, height=120)
        pht8_img = PhotoImage(file=f"images/bookmarks/picture8.png", width=120, height=116)
        uiimg0 = PhotoImage(file=f"uiimg0.png")
        uiimg1 = PhotoImage(file=f"uiimg0.png")
        uiimg2 = PhotoImage(file=f"uiimg0.png")
        uiimg3 = PhotoImage(file=f"uiimg0.png")
        uiimg4 = PhotoImage(file=f"uiimg0.png")
        uiimg5 = PhotoImage(file=f"uiimg0.png")
        uiimg6 = PhotoImage(file=f"uiimg0.png")
        uiimg7 = PhotoImage(file=f"uiimg0.png")
        if len(l7) != 0:
            for i in l7:
                tn = i - 1
                if tn == 0:
                    uiimg0 = PhotoImage(file=f"uiimgr.png")
                if tn == 1:
                    uiimg1 = PhotoImage(file=f"uiimgr.png")
                if tn == 2:
                    uiimg2 = PhotoImage(file=f"uiimgr.png")
                if tn == 3:
                    uiimg3 = PhotoImage(file=f"uiimgr.png")
                if tn == 4:
                    uiimg4 = PhotoImage(file=f"uiimgr.png")
                if tn == 5:
                    uiimg5 = PhotoImage(file=f"uiimgr.png")
                if tn == 6:
                    uiimg6 = PhotoImage(file=f"uiimgr.png")
                if tn == 7:
                    uiimg7 = PhotoImage(file=f"uiimgr.png")
    bcanvas = Canvas(
        masterwin,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    bcanvas.place(x=0, y=0)

    uibg_img = PhotoImage(file=f"uibg.png")
    bcanvas.create_image(
        500.0, 300.0,
        image=uibg_img)
    if booktype=="Fiction":
        someimage = PhotoImage(file=f"fiction.png")
        bcanvas.create_image(
            920, 335,
            image=someimage)
    elif booktype=="Novel":
        someimage = PhotoImage(file=f"Novel.png")
        bcanvas.create_image(
            920, 335,
            image=someimage)
    elif booktype=="Comics":
        someimage = PhotoImage(file=f"Comics.png")
        bcanvas.create_image(
            920, 335,
            image=someimage)
    elif booktype=="Biography":
        someimage = PhotoImage(file=f"Biography.png")
        bcanvas.create_image(
            920, 335,
            image=someimage)
    elif booktype=="Crime Thriller":
        someimage = PhotoImage(file=f"Crime Thriller.png")
        bcanvas.create_image(
            920, 335,
            image=someimage)
    elif booktype=="Indian Writing":
        someimage = PhotoImage(file=f"Indian Writing.png")
        bcanvas.create_image(
            920, 335,
            image=someimage)
    elif booktype=="Bookmarks":
        someimage = PhotoImage(file=f"bkmr.png")
        bcanvas.create_image(
            920, 335,
            image=someimage)

    b0 = Button(
        image=uiimg0,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: buybutton(1),
        relief="flat",activebackground='#CAD1DB')
    b1 = Button(
        image=uiimg1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: buybutton(2),
        relief="flat",activebackground='#CAD1DB')
    b2 = Button(
        image=uiimg2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: buybutton(3),
        relief="flat",activebackground='#CAD1DB')
    b3 = Button(
        image=uiimg3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: buybutton(4),
        relief="flat",activebackground='#CAD1DB')
    b4 = Button(
        image=uiimg4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: buybutton(5),
        relief="flat",activebackground='#CAD1DB')
    b5 = Button(
        image=uiimg5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: buybutton(6),
        relief="flat",activebackground='#CAD1DB')
    b6 = Button(
        image=uiimg6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: buybutton(7),
        relief="flat",activebackground='#CAD1DB')
    b7 = Button(
        image=uiimg7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: buybutton(8),
        relief="flat",activebackground='#CAD1DB')

    b0.place(
        x=125, y=293.5,
        width=80.5,
        height=27)

    b1.place(
        x=332, y=293.5,
        width=80.5,
        height=27)

    b2.place(
        x=539, y=293.5,
        width=80.5,
        height=27)

    b3.place(
        x=746, y=293.5,
        width=80.5,
        height=27)

    b4.place(
        x=125, y=520,
        width=80.5,
        height=27)

    b5.place(
        x=332, y=520,
        width=80.5,
        height=27)

    b6.place(
        x=539, y=520,
        width=80.5,
        height=27)

    b7.place(
        x=746, y=520,
        width=80.5,
        height=27)

    bcanvas.create_text(
        86.5, 305.5,
        text="₹"+str(price1[0]),
        fill="#000000",
        font=("UrbanistRoman-Regular", int(14.0)))

    bcanvas.create_text(
        128.5, 283,
        text=name1,
        fill="#000000",
        font=("UrbanistRoman-Regular", int(8.0)), width=200)

    bcanvas.create_text(
        707.5, 304.5,
        text="₹"+str(price4[0]),
        fill="#000000",
        font=("UrbanistRoman-Regular", int(14.0)))

    bcanvas.create_text(
        749.5, 283,
        text=name4,
        fill="#000000",
        font=("UrbanistRoman-Regular", int(8.0)), width=200)

    bcanvas.create_text(
        500.5, 306,
        text="₹"+str(price3[0]),
        fill="#000000",
        font=("UrbanistRoman-Regular", int(14.0)))

    bcanvas.create_text(
        293.5, 304.5,
        text="₹"+str(price2[0]),
        fill="#000000",
        font=("UrbanistRoman-Regular", int(14.0)))

    bcanvas.create_text(
        335.5, 283,
        text=name2,
        fill="#000000",
        font=("UrbanistRoman-Regular", int(8.0)), width=200)

    bcanvas.create_text(
        544.5, 281,
        text=name3,
        fill="#000000",
        font=("UrbanistRoman-Regular", int(8.0)), width=175, anchor='center')

    bcanvas.create_text(
        86.5, 530.5,
        text="₹"+str(price5[0]),
        fill="#000000",
        font=("UrbanistRoman-Regular", int(14.0)))

    bcanvas.create_text(
        128.5, 509,
        text=name5,
        fill="#000000",
        font=("UrbanistRoman-Regular", int(8.0)), width=200)

    bcanvas.create_text(
        707.5, 530.5,
        text="₹"+str(price8[0]),
        fill="#000000",
        font=("UrbanistRoman-Regular", int(14.0)))

    bcanvas.create_text(
        749.5, 509,
        text=name8,
        fill="#000000",
        font=("UrbanistRoman-Regular", int(8.0)), width=200, anchor='center')

    bcanvas.create_text(
        500.5, 530.5,
        text="₹"+str(price7[0]),
        fill="#000000",
        font=("UrbanistRoman-Regular", int(14.0)))

    bcanvas.create_text(
        542.5, 509,
        text=name7,
        fill="#000000",
        font=("UrbanistRoman-Regular", int(8.0)), width=200)

    bcanvas.create_text(
        293.5, 530.5,
        text="₹"+str(price6[0]),
        fill="#000000",
        font=("UrbanistRoman-Regular", int(14.0)))

    bcanvas.create_text(
        335.5, 509,
        text=name6,
        fill="#000000",
        font=("UrbanistRoman-Regular", int(8.0)), width=200)

    uiimg8 = PhotoImage(file=f"uiimg8.png")
    b8 = Button(
        image=uiimg8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:redirecttockeckout(cartcount,0),
        relief="flat", activebackground='#AFB0B2')

    b8.place(
        x=845, y=15,
        width=131,
        height=47)

    w = Label(masterwin, text=cartcount, font=("UrbanistRoman-Regular", 11), bg='#AFB0B2')
    w.place(x=825,y=29)

    uiimg9 = PhotoImage(file=f"uiimg9.png")
    b9 = Button(
        image=uiimg9,
        borderwidth=0,
        highlightthickness=0,
        command=selectionmenu,
        relief="flat", activebackground='#0E0E0C')

    b9.place(
        x=10, y=83,
        width=135,
        height=24)
    bcanvas.create_image(
        133, 195,
        image=pht1_img)

    bcanvas.create_image(
        336, 195,
        image=pht2_img)

    bcanvas.create_image(
        548, 195,
        image=pht3_img)

    bcanvas.create_image(
        751, 195,
        image=pht4_img)

    bcanvas.create_image(
        128, 421,
        image=pht5_img)

    bcanvas.create_image(
        336, 421,
        image=pht6_img)

    bcanvas.create_image(
        543, 421,
        image=pht7_img)

    bcanvas.create_image(
        751, 421,
        image=pht8_img)

    blist=[b0,b1,b2,b3,b4,b5,b6,b7]
    mainloop()

def selectionmenu(x=0):
    global masterwin,scanvas,ogp,total,l1,l2,l3,cartcount,total,ogp,customern,plot,xyz
    widget_list = all_children(masterwin)
    try:
        xyz.delete
    except:
        pass
    for item in widget_list:
        item.place_forget()
    if x==1:
        total=ogp
    elif x==2:
        ogp=0
        total=0
        l1.clear()
        l2.clear()
        l3.clear()
        l4.clear()
        l5.clear()
        l6.clear()
        cartcount=0

    scanvas = Canvas(
        masterwin,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    scanvas.place(x=0, y=0)
    smbg_img = PhotoImage(file=f"smbg.png")
    scanvas.create_image(
        500.0, 300.0,
        image=smbg_img)
    smimg0 = PhotoImage(file=f"smimg0.png")
    b0 = Button(
        image=smimg0,
        borderwidth=0,
        highlightthickness=0,
        command=fiction,
        relief="flat")
    b0.place(
        x=447, y=90,
        width=250,
        height=85)
    smimg1 = PhotoImage(file=f"smimg1.png")
    b1 = Button(
        image=smimg1,
        borderwidth=0,
        highlightthickness=0,
        command=comics,
        relief="flat")
    b1.place(
        x=447, y=314,
        width=250,
        height=85)
    smimg2 = PhotoImage(file=f"smimg2.png")
    b2 = Button(
        image=smimg2,
        borderwidth=0,
        highlightthickness=0,
        command=novel,
        relief="flat")
    b2.place(
        x=447, y=202,
        width=250,
        height=85)

    imgbiog = PhotoImage(file=f"biog.png")
    bbiog = Button(
        image=imgbiog,
        borderwidth=0,
        highlightthickness=0,
        command=biography,
        relief="flat")

    bbiog.place(
        x=717, y=90,
        width=250,
        height=85)

    imgir = PhotoImage(file=f"ir.png")
    bir = Button(
        image=imgir,
        borderwidth=0,
        highlightthickness=0,
        command=indianwriting,
        relief="flat")

    bir.place(
        x=717, y=202,
        width=250,
        height=85)

    imgctb = PhotoImage(file=f"ctb.png")
    bctb = Button(
        image=imgctb,
        borderwidth=0,
        highlightthickness=0,
        command=crimethriller,
        relief="flat")

    bctb.place(
        x=717, y=314,
        width=250,
        height=85)

    imgbb = PhotoImage(file=f"bookmarkb.png")
    bbb = Button(
        image=imgbb,
        borderwidth=0,
        highlightthickness=0,
        command=bookmarks,
        relief="flat")

    bbb.place(
        x=537, y=418.5,
        width=346,
        height=79)

    uiimgc = PhotoImage(file=f"scheckout.png")
    bc = Button(
        image=uiimgc,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: redirecttockeckout(cartcount,1),
        relief="ridge", activebackground='#DBDDE9')

    bc.place(
        x=837, y=11,
        width=131,
        height=47)
    lg = PhotoImage(file=f"logoutb.png")
    blg = Button(
        image=lg,
        borderwidth=0,
        highlightthickness=0,
        command=lambda :login(2),
        relief="flat", bd=0, activebackground='#C2C5CE')

    blg.place(
        x=20, y=13,
        width=120,
        height=43)

    imgmo = PhotoImage(file=f"myorders.png")
    bmo = Button(
        image=imgmo,
        borderwidth=0,
        highlightthickness=0,
        command=history,
        relief="flat")

    bmo.place(
        x=25, y=65,
        width=107,
        height=60)
    scanvas.create_text(
        235,245,
        text="Hello "+customern+" 🙂",
        fill="#000000",
        font=("UrbanistRoman-Regular", int(20.0)))

    w = Label(masterwin, text=cartcount, font=("UrbanistRoman-Regular", 11), bg='#C1C1C3')
    w.place(x=970, y=24)
    mainloop()

def history():
    global noofb,framelength,dataa,hhhcanvas,framepic,wrapperh,hcanvas,customern,masterwin
    def deleteuserdata():
        global hhhcanvas,wrapperh
        wrapperh.destroy()
        wrapperh = LabelFrame(masterwin)
        hhhcanvas = Canvas(wrapperh, height=470, width=450, bd=0, highlightthickness=0)
        hhhcanvas.pack(side='left', fill='y')
        scrollbar = ttk.Scrollbar(wrapperh, orient='vertical', command=hhhcanvas.yview)
        scrollbar.pack(side='right', fill='y')
        hhhcanvas.configure(yscrollcommand=scrollbar.set)
        myframe = Frame(hhhcanvas, height=0, width=0, borderwidth=0, highlightthickness=0, relief='flat')
        hhhcanvas.bind('<Configure>', lambda e: hhhcanvas.configure(scrollregion=hhhcanvas.bbox('all')))
        hhhcanvas.create_window((0, 0), window=myframe, anchor='nw')
        wrapperh.place(x=470, y=65)
        eeframe=PhotoImage(file=f"eframe.png")
        hhhcanvas.create_image(0,0,image=eeframe)
        c1.execute(("drop table if exists {};").format(customern))
        mainloop()
    def idkname():
        global noofb,framelength,dataa,hhhcanvas,framepic,masterwin,plot,xyz
        for i in range(noofb):
            hhhcanvas.create_image(
                0, framelength,
                image=framepic)
            framelength += 235

        z1 = 0
        z4 = -15
        z5 = 15
        for i in dataaa:
            hhhcanvas.create_text(-170, z1,
                                  text=i[0],
                                  fill="#000000",
                                  font=("UrbanistRoman-Regular", int(20.0)), width=140)

            hhhcanvas.create_text(-75, z1,
                                  text=i[1],
                                  fill="#000000",
                                  font=("UrbanistRoman-Regular", int(15.0)), width=140)

            hhhcanvas.create_text(40, z1,
                                  text="₹"+str(i[3]),
                                  fill="#000000",
                                  font=("UrbanistRoman-Regular", int(20.0)), width=140)

            hhhcanvas.create_text(140, z4,
                                  text=i[4],
                                  fill="#000000",
                                  font=("UrbanistRoman-Regular", int(15.0)), width=140)
            hhhcanvas.create_text(140, z5,
                                  text=i[5],
                                  fill="#000000",
                                  font=("UrbanistRoman-Regular", int(15.0)), width=140)
            z1 += 235
            z4 += 235
            z5 += 235

    scanvas.delete("all")
    widget_list = all_children(masterwin)
    for item in widget_list:
        item.place_forget()
    hcanvas = Canvas(
        masterwin,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    hcanvas.place(x=0, y=0)

    backgroundhimg = PhotoImage(file=f"hbg.png")
    hcanvas.create_image(
        500.0, 300.0,
        image=backgroundhimg)

    img0h = PhotoImage(file=f"backhb.png")
    b0h = Button(
        image=img0h,
        borderwidth=0,
        highlightthickness=0,
        command=selectionmenu,
        relief="flat")

    b0h.place(
        x=27, y=19,
        width=116,
        height=39)

    imgch = PhotoImage(file=f"clearhistory.png")
    bch = Button(
        image=imgch,
        borderwidth=0,
        highlightthickness=0,
        command=deleteuserdata,
        relief="flat")

    bch.place(
        x=145, y=371,
        width=175,
        height=48)
    
    wrapperh = LabelFrame(masterwin)
    hhhcanvas = Canvas(wrapperh, height=470, width=450, bd=0, highlightthickness=0)
    hhhcanvas.pack(side='left', fill='y')
    scrollbar = ttk.Scrollbar(wrapperh, orient='vertical', command=hhhcanvas.yview)
    scrollbar.pack(side='right', fill='y')
    hhhcanvas.configure(yscrollcommand=scrollbar.set)
    myframe = Frame(hhhcanvas, height=0, width=0, borderwidth=0, highlightthickness=0, relief='flat')
    hhhcanvas.bind('<Configure>', lambda e: hhhcanvas.configure(scrollregion=hhhcanvas.bbox('all')))
    hhhcanvas.create_window((0, 0), window=myframe, anchor='nw')
    wrapperh.place(x=470, y=65)

    framepic = PhotoImage(file=f"frame2.png")
    eframepic = PhotoImage(file=f"eframe.png")

    framelength = 0
    noofb = 0
    c1.execute("show tables;")
    users=c1.fetchall()
    cv=0
    for i in users:
        if i[0]==customern:
            c1.execute(("select * from {};").format(customern))
            dataaa=c1.fetchall()
            for j in dataaa:
                noofb+=1
            idkname()
            cv+=1
            break
    if cv==0:
        hhhcanvas.create_image(
            0, 0,
            image=eframepic)
    mainloop()

def cc():
    global masterwin,customern
    a, b = cn.get(), entry0.get()
    c.execute('select * from credentials;')
    credentials = c.fetchall()
    somevariable=0
    if len(credentials)!=0:
        for i in credentials:
            if str(i[0]) == str(a) and str(i[1]) == str(b):
                customern = a
                selectionmenu()
                break
            else:
                if somevariable==0:
                    ut = canvas.create_text(
                        290.0, 410,
                        text="Username or Password  incorrect",
                        fill="#000000",
                        font=("UrbanistRoman-Light", int(10.0)))
                    masterwin.after(2700, canvas.delete, ut)
                    somevariable+=1
                else:
                    pass
    else:
        ut = canvas.create_text(
            290.0, 410,
            text="Username or Password  incorrect",
            fill="#000000",
            font=("UrbanistRoman-Light", int(10.0)))
        masterwin.after(2700, canvas.delete, ut)

def login(x=1):
    global masterwin,cn,entry0,canvas,ogp,total,cartcount
    if x==0:
        masterwin = Tk()
        masterwin.geometry("1000x600")
        masterwin.configure(bg="#ffffff")
        masterwin.title("LittleTome")

    else:
        widget_list = all_children(masterwin)
        for item in widget_list:
            item.place_forget()

    if x==2:
        ogp = 0
        total = 0
        l1.clear()
        l2.clear()
        l3.clear()
        l4.clear()
        l5.clear()
        l6.clear()
        cartcount = 0

    canvas = Canvas(
        masterwin,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(x=0, y=0)

    loginbg_img = PhotoImage(file=f"loginbg.png")
    canvas.create_image(
        500.0, 300.0,
        image=loginbg_img)

    loginimage0 = PhotoImage(file=f"loginimage0.png")
    b0 = Button(
        image=loginimage0,
        borderwidth=0,
        highlightthickness=0,
        command=cc,
        relief="flat", bd=0, activebackground='#FAFAFA')

    b0.place(
        x=231, y=418,
        width=119,
        height=42)

    imgcab = PhotoImage(file=f"cab.png")
    bcab = Button(
        image=imgcab,
        borderwidth=0,
        highlightthickness=0,
        command=createaccount,
        relief="flat")

    bcab.place(
        x=219, y=527,
        width=137,
        height=28)

    entry0_img = PhotoImage(file=f"loginimg_textBox.png")
    canvas.create_image(
        289.0, 380,
        image=entry0_img)

    entry0 = Entry(
        bd=0,
        bg="#d9d9d9",
        highlightthickness=0,show="*")

    entry0.place(
        x=201.0, y=362,
        width=176.0,
        height=35)

    entry1_img = PhotoImage(file=f"loginimg_textBox.png")
    canvas.create_image(
        289.0, 301,
        image=entry1_img)

    newuser = PhotoImage(file=f"newuser.png")
    canvas.create_image(
        290,510,
        image=newuser)

    cn = Entry(
        bd=0,
        bg="#d9d9d9",
        highlightthickness=0)

    cn.place(
        x=201.0, y=283,
        width=176.0,
        height=35)
    if x == 0:
        masterwin.resizable(False, False)
        masterwin.mainloop()
    else:
        mainloop()

def createaccount():
    global lcanvas,masterwin,entry0l,entry1l
    def createaccount():
        global entry0l,entry1l
        c.execute('select * from credentials;')
        credentials = c.fetchall()
        a,b=entry1l.get(),entry0l.get()
        existingusers=[]
        for i in credentials:
            existingusers.append(i[0])
        if len(a)!=0 and len(b)!=0:
                if a not in existingusers:
                    query = "insert into credentials(username,password) values(%s,%s);"
                    data = (str(a), str(b))
                    c.execute(query, data)
                    db.commit()
                    login()
                else:
                    uut = lcanvas.create_text(
                        290.0, 238,
                        text="Username already exists. Please try a different one",
                        fill="#000000",
                        font=("UrbanistRoman-Light", int(10.0)))
                    masterwin.after(2700, lcanvas.delete, uut)

        else:
            uut = lcanvas.create_text(
                290.0, 412.0,
                text="Please enter your username and password to create an account",
                fill="#000000",
                font=("UrbanistRoman-Light", int(10.0)))
            masterwin.after(2700, lcanvas.delete, uut)


    canvas.delete("all")
    widget_list = all_children(masterwin)
    for item in widget_list:
        item.place_forget()
    lcanvas = Canvas(
        masterwin,
        bg="#ffffff",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    lcanvas.place(x=0, y=0)

    background_img = PhotoImage(file=f"createa.png")
    lcanvas.create_image(
        500.0, 300.0,
        image=background_img)

    imgcb = PhotoImage(file=f"cab.png")
    bcb = Button(
        image=imgcb,
        borderwidth=0,
        highlightthickness=0,
        command=createaccount,
        relief="flat",activebackground="#F9F9F9")

    bcb.place(
        x=219, y=424,
        width=146,
        height=34)

    entry0limg = PhotoImage(file=f"loginimg_textBox.png")
    lcanvas.create_image(
        289.0, 380,
        image=entry0limg)

    entry0l = Entry(
        bd=0,
        bg="#d9d9d9",
        highlightthickness=0)

    entry0l.place(
        x=201.0, y=362,
        width=176.0,
        height=35)

    entry1limg = PhotoImage(file=f"loginimg_textBox.png")
    lcanvas.create_image(
        289.0, 301,
        image=entry1limg)

    entry1l = Entry(
        bd=0,
        bg="#d9d9d9",
        highlightthickness=0)

    entry1l.place(
        x=201.0, y=283,
        width=176.0,
        height=35)

    imglc = PhotoImage(file=f"lcancelb.png")
    blc = Button(
        image=imglc,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:login(1),
        relief="flat",activebackground="#F9F9F9")

    blc.place(
        x=246, y=475,
        width=94,
        height=36)
    mainloop()

login(0)
