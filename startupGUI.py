from tkinter import *
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
from PIL import ImageTk, Image
from ctypes import windll

import sqlite3
import os

import subprocess
import threading

'''
todo list:
- bind enter key to enter information
- ensure credit page (include license information)
- create shell of the main screen
- create settings screen
- consider what to make configurable in settings
'''

#gaining system information for configuration
userMaxScreenSize = Tk()
maxScreenWidth = userMaxScreenSize.winfo_screenwidth()
maxScreenHeight = userMaxScreenSize.winfo_screenheight()
userMaxScreenSize.destroy()

#setting variables for window
halfScreenWidth = int((maxScreenWidth / 2))
halfScreenHeight = int((maxScreenHeight / 2))

halfScreenWidthAdjusted = int(halfScreenWidth-280)
halfScreenHeightAdjusted = int(halfScreenHeight-100)

setMainWindowGeometrystartup = (f"{halfScreenWidthAdjusted}x{halfScreenHeightAdjusted}+{halfScreenWidth-230}+{halfScreenHeight-200}")

startupImagePath = "img\AS3.png"

#variables related to the database
db_name = "userChatRecords.db"
chat_id = 0
current_chat_id = None

#Debug section
print(maxScreenHeight," and ",maxScreenWidth)

#Settings for the settings screen
userSelectedFont = "MS Sans Serif"
disableSound = False #experimental


#configure welcome window
mainWindow = Tk()
mainWindow.grid()
mainWindow.lift
mainWindow.attributes("-topmost", True)
mainWindow.attributes("-topmost", False)
mainWindow.title("[Insert Name] Chatbox")
mainWindow.configure(bg="#1C1C1C")
mainWindow.geometry(setMainWindowGeometrystartup)
#mainWindow.geometry("1600x900") debug option
mainWindow.resizable(width=False, height=False)

def on_exit():
    if messagebox.askyesno("Experiment Termination","Terminating the program. I'll just add this to your file under \"Premature Conclusions.\""):
        taskbar = windll.user32.FindWindowA(b'Shell_TrayWnd', None)
        windll.user32.ShowWindow(taskbar, 9)
        conn = sqlite3.connect(db_name)
        conn.close()
        mainWindow.destroy()
    else:
        pass


mainWindow.protocol("WM_DELETE_WINDOW", on_exit)

#loading logo (used all the time)
logoImagePath = "img/ASL3.png"
originalLogoImage = Image.open(logoImagePath)
resizedOriginalLogoImage = originalLogoImage.resize((50 ,50))
headerLogoImage = ImageTk.PhotoImage(resizedOriginalLogoImage)

#define switch_window()
'''
def switch_window():
    mainWindow.after(10000, open_main)

def open_main():
    mainWindow.destroy()
    subprocess.run(["python", "mainGUI.py"])
    time.sleep(4)
'''
    
#Code for the Loadbar:
def create_windows7_progress_bar(parent):
    canvas = Canvas(parent, width=383, height=10, bg='#1C1C1C', highlightthickness=0)
    
    # Create 12 segments with 1px spacing
    segments = []
    for i in range(12):
        x1 = i * 31  # 20px width + 1px spacing
        x2 = x1 + 30
        segments.append(canvas.create_rectangle(x1, 0, x2, 10, fill='#0a246a', outline='#0a246a'))
    
    def animate(block_position=0):
        # Reset all segments to dark blue
        for segment in segments:
            canvas.itemconfig(segment, fill='#0a246a', outline='#0a246a')
        
        # Light up 4 consecutive segments
        for i in range(4):
            idx = (block_position + i) % 12
            canvas.itemconfig(segments[idx], fill='#5b9bf8', outline='#5b9bf8')
        
        # Schedule next animation frame
        canvas.after(50, animate, (block_position + 1) % 12)
    
    # Start animation
    animate()
    return canvas

def remove_startupWidgets():
    for widget in mainWindow.winfo_children():
        widget.destroy()
    welcome_screen()

#removes the widgets seen in the welcome screen, and unbinds the key initially used for return
def remove_welcomeScreen():
    for widget in mainWindow.winfo_children():
        widget.destroy()
    lambda:welcome_screen.wsEntry.unbind("<Return>")
    main_screen()

def displayLegal():
    for widget in mainWindow.winfo_children():
        widget.destroy()
    legal_page()

def displaySetting():
    for widget in mainWindow.winfo_children():
        widget.destroy()
    settings_page()

def create_new_chat(user_id, wsEntry):
    wsEGetter = wsEntry.get()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Insert a new chat into the Chats table
    cursor.execute('''
        INSERT INTO Chats (UserID) VALUES (?)
    ''', (user_id,))
    conn.commit()
    
    # Get the last inserted ChatID
    global chat_id
    chat_id = cursor.lastrowid

    # Insert the first message into the Messages table
    cursor.execute('''
        INSERT INTO Messages (ChatID, UserID, MessageContent) VALUES (?, ?, ?)
    ''', (chat_id, user_id, wsEGetter))
    conn.commit()

    # Update the global variable for the currently selected chat ID
    global current_chat_id
    current_chat_id = chat_id  # Set the current chat ID to the newly created chat ID

    # Run the backend script with the new chat details
    wsEGetter = str(wsEGetter)
    chat_id = str(chat_id)
    subprocess.run(['python', 'dependencies/backend.py', wsEGetter, chat_id])

    remove_welcomeScreen()

def draw_StartupLoad(db_name):
    #create startup slogan font
    startupFontItal = font.Font(family=userSelectedFont, size=15, slant="italic")

    #preventing the cells from collapsing when empty
    gRow = 13
    gColumn = 8

    for num in range(gRow):
        mainWindow.grid_rowconfigure(num, minsize=20, weight=1 )

    for num in range(gColumn):
        mainWindow.grid_columnconfigure(num, minsize=5, weight=1)

    #draw welcome screen
    originalStartupImage = Image.open(startupImagePath)
    resizedOriginalStartupImage = originalStartupImage.resize((400 ,120))
    tk_imagestartup = ImageTk.PhotoImage(resizedOriginalStartupImage)

    startupImageLabel = Label(mainWindow, image=tk_imagestartup, bg="#1C1C1C")
    startupImageLabel.image = tk_imagestartup
    startupImageLabel.grid()
    startupImageLabel.grid_configure(column=3, row=4, columnspan=1, rowspan=2, sticky=NSEW)

    startupsloganLabel = Label(mainWindow, text="\"A Trusted Friend in Science\"", font=(startupFontItal), bg="#1C1C1C", fg="#D3D3D3")
    startupsloganLabel.grid()
    startupsloganLabel.grid_configure(row=6, column=3, columnspan=1, rowspan=1, sticky=NSEW)

    win7StylePB = create_windows7_progress_bar(mainWindow)
    win7StylePB.grid(row=10, column=3, columnspan=1, rowspan=1)

    #executing the 10 second wait till next window
    mainWindow.after(10000, lambda:remove_startupWidgets())

    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        print("Succesful creation of '{db_name}' database")
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Chats (
            ChatID INTEGER PRIMARY KEY,
            UserID INTEGER,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Messages (
            MessageID INTEGER PRIMARY KEY AUTOINCREMENT,
            ChatID INTEGER,
            UserID INTEGER,
            MessageContent TEXT,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ChatID) REFERENCES Chats(ChatID)
                       )
        ''')
        conn.commit()
    elif os.path.exists(db_name):
        print("Database already exists")

    else:
        print("FAILURE! Error: 5CF")

def legal_page():
    setMainWindowGeometrystartup = (f"{halfScreenWidth}x{maxScreenHeight}+{halfScreenWidth}+0")
    mainWindow.geometry(setMainWindowGeometrystartup)

    #preventing the cells from collapsing when empty
    gRow = 45
    gColumn = 20

    for num in range(gRow):
        mainWindow.grid_rowconfigure(num, minsize=20, weight=1 )

    for num in range(gColumn):
        mainWindow.grid_columnconfigure(num, minsize=5, weight=1)

    #Buttons arranged on the left side of the screen
    goWelcomeButton = Button(mainWindow, text="Go to Welcome Screen", font=(userSelectedFont, 10), bg="#333333", fg="#FFFFFF", command=remove_startupWidgets)
    goMainButton = Button(mainWindow, text="Go to Main Screen", font=(userSelectedFont, 10), bg="#333333", fg="#FFFFFF", command=remove_welcomeScreen)
    goQuit = Button(mainWindow, text="Quit", font=(userSelectedFont, 10), bg="#333333", fg="#FFFFFF", command=on_exit)

    goWelcomeButton.grid_configure(row=3, column=1, rowspan=1, columnspan=4, sticky=NSEW)
    goMainButton.grid_configure(row=5, column=1, rowspan=1, columnspan=4, sticky=NSEW)
    goQuit.grid_configure(row=7, column=1, rowspan=1, columnspan=4, sticky=NSEW)

    #All text that is from the middle to end of the screen
    #Copyright Notice is displayed
    copyrightNotice=Text(mainWindow, font=(userSelectedFont, 11), bg="#1C1C1C", fg="#FFFFFF", wrap=WORD)
    copyrightNotice.grid_configure(row=3, column=6, rowspan=4, columnspan=14)
    copyrightNotice.insert(END,"Copyright Notice: All symbols, logos, slogans, images, and other related materials are the property of Valve Corporation and are protected by copyright and other intellectual property laws. Unauthorized use, reproduction, or distribution of these materials is prohibited without prior written permission from Valve Corporation.")
    copyrightNotice.tag_add("color", "1.0", "1.17")
    copyrightNotice.tag_config("color", foreground="red")

    #License Statement is displayed
    licenseStatement=Text(mainWindow, font=(userSelectedFont, 11), bg="#1C1C1C", fg="#FFFFFF", wrap=WORD)
    licenseStatement.grid_configure(row=8, column=6, rowspan=5, columnspan=14)
    licenseStatement.insert(END, "License Statement: All works are used in accordance with Section D, License to Use Valve Game Content in Fan Art, as outlined in the Valve Subscriber Agreement (https://store.steampowered.com/subscriber_agreement).Unauthorized use, reproduction, or distribution of these materials is prohibited without prior written permission from Valve Corporation.")
    licenseStatement.tag_add("color", "1.0", "1.18")
    licenseStatement.tag_config("color", foreground="red")

    #Disclaimer Statement is displayed
    disclaimerStatement=Text(mainWindow, font=(userSelectedFont, 11), bg="#1C1C1C", fg="#FFFFFF", wrap=WORD)
    disclaimerStatement.grid_configure(row=14, column=6, rowspan=4, columnspan=14)
    disclaimerStatement.insert(END, "Disclaimer: We, [Group Name], claim no affiliation with Valve Corporation or any individuals associated with Valve Corporation. Any references to Valve Corporation are for informational purposes only and do not imply any endorsement or partnership.")
    disclaimerStatement.tag_add("color", "1.0", "1.11")
    disclaimerStatement.tag_config("color", foreground="cyan")

    #Legal Statement is displayed
    legalStatement=Text(mainWindow, font=(userSelectedFont, 11), bg="#1C1C1C", fg="#FFFFFF", wrap=WORD)
    legalStatement.grid_configure(row=19, column=6, rowspan=4, columnspan=14)
    legalStatement.insert(END,"Legal Notice: This project is for non-commercial use only. All donations or payments are to be directed to Valve Corporation for the game Portal, which inspired this chatbot. Any contributions made will not benefit [Group Name] and are intended solely for Valve Corporation.")
    legalStatement.tag_add("color", "1.0", "1.13")
    legalStatement.tag_config("color", foreground="red")

    #Purchase Information is displayed
    purchaseInformation=Text(mainWindow, font=(userSelectedFont, 11), bg="#1C1C1C", fg="#FFFFFF", wrap=WORD)
    purchaseInformation.grid_configure(row=24, column=6, rowspan=4, columnspan=14)
    purchaseInformation.insert(END, "Purchase Information: Portal is available for purchase at the following website: https://store.steampowered.com/app/400/Portal/. \n \n")
    purchaseInformation.tag_add("color","1.0", "1.21")
    purchaseInformation.tag_add("color","1.80", "1.127")
    purchaseInformation.tag_config("color", foreground="cyan")

    accountInformation=Text(mainWindow, font=(userSelectedFont, 11), bg="#1C1C1C", fg="#FFFFFF", wrap=WORD)
    accountInformation.grid_configure(row=29, column=6, rowspan=4, columnspan=14)
    accountInformation.insert(END, "Account Requirement: To purchase and access the game, you are required to have a valid Steam account. You can create an account by visiting https://store.steampowered.com/join/.")
    accountInformation.tag_add("color","1.0","1.19")
    accountInformation.tag_add("color","1.139","1.176")
    accountInformation.tag_config("color", foreground="cyan")

def settings_page():
    setMainWindowGeometrystartup = (f"{halfScreenWidth}x{maxScreenHeight}+{halfScreenWidth}+0")
    mainWindow.geometry(setMainWindowGeometrystartup)

    #preventing the cells from collapsing when empty
    gRow = 45
    gColumn = 20

    for num in range(gRow):
        mainWindow.grid_rowconfigure(num, minsize=20, weight=1 )

    for num in range(gColumn):
        mainWindow.grid_columnconfigure(num, minsize=5, weight=1)

    #Buttons arranged on the left side of the screen
    goWelcomeButton = Button(mainWindow, text="Go to Welcome Screen", font=(userSelectedFont, 10), bg="#333333", fg="#FFFFFF", command=remove_startupWidgets)
    goMainButton = Button(mainWindow, text="Go to Main Screen", font=(userSelectedFont, 10), bg="#333333", fg="#FFFFFF", command=remove_welcomeScreen)
    goQuit = Button(mainWindow, text="Quit", font=(userSelectedFont, 10), bg="#333333", fg="#FFFFFF", command=on_exit)

    goWelcomeButton.grid_configure(row=3, column=1, rowspan=1, columnspan=4, sticky=NSEW)
    goMainButton.grid_configure(row=5, column=1, rowspan=1, columnspan=4, sticky=NSEW)
    goQuit.grid_configure(row=7, column=1, rowspan=1, columnspan=4, sticky=NSEW)

def welcome_screen():
    taskbar = windll.user32.FindWindowA(b'Shell_TrayWnd', None)
    windll.user32.ShowWindow(taskbar, 0)

    setMainWindowGeometrystartup = (f"{halfScreenWidth}x{maxScreenHeight}+{halfScreenWidth}+0")
    mainWindow.geometry(setMainWindowGeometrystartup)

    #preventing the cells from collapsing when empty
    gRow = 45
    gColumn = 20

    for num in range(gRow):
        mainWindow.grid_rowconfigure(num, minsize=15, weight=1 )

    for num in range(gColumn):
        mainWindow.grid_columnconfigure(num, minsize=10, weight=1)

    wsMainLogoAndTextFrame = Frame(mainWindow, bg="#1C1C1C")
    wsMainLogoAndTextFrame.grid_configure(row=16, column=5, columnspan=6, rowspan=2)

    wsLogoLabel = Label(wsMainLogoAndTextFrame, image=headerLogoImage, bg="#1C1C1C")
    wsLogoLabel.image = headerLogoImage
    wsMainText = Label(wsMainLogoAndTextFrame, text="Aperture Science", font=(userSelectedFont, 30), bg="#1C1C1C", fg="#FFFFFF")

    wsSubtextFont = font.Font(family=userSelectedFont, size=10, slant="italic")
    wsSubText = Label(mainWindow, text="\"Not Never But NOW\"", font=(wsSubtextFont), bg="#1C1C1C", fg="#FFFFFF")
    wsModelText = Label (mainWindow, text="AS Model: GLaDOS", font=(userSelectedFont, 5), bg="#1C1C1C", fg="#FFFFFF")
    wsButtonEntryEnter = Button(mainWindow, text="\u21B5", font=(userSelectedFont, 10), bg="#2A2A2A", fg="#FFFFFF", command=lambda:create_new_chat(1,wsEntry))
    wsButtonSetting = Button(mainWindow, text="Settings", font=(userSelectedFont, 10), bg="#333333", fg="#FFFFFF", command=displaySetting)
    wsEntry = Entry(mainWindow, width=60, justify=LEFT, cursor="xterm", font=(userSelectedFont, 10), bg="#2A2A2A", fg="#FFFFFF")
    wsEntry.bind("<Return>", lambda *args:create_new_chat(1,wsEntry))
    wsButtonLegal = Button(mainWindow, text="Legal", font=(userSelectedFont, 10), bg="#333333", fg="#FFFFFF", command=displayLegal)

    wsMainText.grid_configure(row=0, column=2, rowspan=1, columnspan=4)
    wsLogoLabel.grid_configure(row=0, column=0, columnspan=2, rowspan=2, padx=20)
    wsSubText.grid_configure(row=18, column=5, sticky=NSEW, columnspan=7)
    wsModelText.grid_configure(row=22, column=3, columnspan=2, sticky=W)
    wsButtonEntryEnter.grid_configure(row=20, column=15, columnspan=2, sticky=NSEW)
    wsButtonSetting.grid_configure(row=0, column=0, columnspan=3, sticky=NSEW)
    wsEntry.grid_configure(row=20, column=3, columnspan=12, sticky=NSEW)
    wsButtonLegal.grid_configure(row=1, column=0, columnspan=3, sticky=NSEW)

def chat_select_filler():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT c.ChatID, MIN(m.Timestamp) AS FirstMessageTime, 
               (SELECT m.MessageContent FROM Messages m WHERE m.ChatID = c.ChatID ORDER BY m.Timestamp LIMIT 1) AS FirstMessageContent
        FROM Chats c
        LEFT JOIN Messages m ON c.ChatID = m.ChatID
        GROUP BY c.ChatID
        ORDER BY FirstMessageTime
    ''')

    chats = cursor.fetchall()
    conn.close()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for chat in chats:
        chat_id = chat[0]
        first_message_content = chat[2] if chat[2] else ""
        first_word = first_message_content.split()[0] if first_message_content else "No Message"

        button = Button(scrollable_frame, text=f"ChatID: {chat_id} - {first_word}",
                        command=lambda chat_id=chat_id: switch_chat(chat_id))
        button.pack(pady=5)

def switch_chat(chat_id):
    global current_chat_id
    current_chat_id = chat_id
    print(f"Switching to ChatID: {current_chat_id}")
    threading.Thread(target=display_chat, args=(current_chat_id,)).start()

def chat_select_creater():
    canvas = Canvas(mainWindow, bg="#333333", width=135, height=400)
    global scrollable_frame
    scrollable_frame = Frame(canvas, bg="#414141")

    # Create a scrollbar
    scrollbar = Scrollbar(mainWindow, orient="vertical", command=canvas.yview, bg="#414141")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Grid the scrollbar and canvas
    scrollbar.grid(row=4, column=3, rowspan=34, sticky=NS)
    canvas.grid(row=4, column=0, columnspan=3, rowspan=34, sticky=NSEW)

    # Create a window in the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Update the scroll region
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scroll_region)

    # Ensure the scrollable frame expands properly
    scrollable_frame.pack(fill='both', expand=True)

    # Call the function to fill the chat select area
    chat_select_filler()

def message_read_creator():
    #creating the chat scrollable area
    #c
    canvas = Canvas(mainWindow, bg="#333333", width=400, height=420)
    scrollable_frame = Frame(canvas, bg="#414141", highlightbackground="#888888", highlightcolor="#888888", highlightthickness=2)

    # Create a scrollbar
    scrollbar = Scrollbar(mainWindow, orient="vertical", command=canvas.yview, bg="#414141")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Grid the scrollbar and canvas
    scrollbar.grid(row=4, column=45, rowspan=38, sticky=NS)
    canvas.grid(row=4, column=5, columnspan=39, rowspan=38, sticky=NSEW)

    # Create a window in the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Update the scroll region
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scroll_region)

    scrollable_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

def display_chat(chat_id, word_limit=13):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT MessageID, UserID, MessageContent 
        FROM Messages 
        WHERE ChatID = ? 
        ORDER BY MessageID
    ''', (chat_id,))
    
    messages = cursor.fetchall()
    conn.close()

    if scrollable_frame.winfo_exists():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

    for message in messages:
        message_id, user_id, message_content = message
        
        # Limit the display of user ID to a maximum of 5 characters
        limited_user_id = str(user_id)[:5]  # Adjust the number as needed

        # Split the message into words and format it according to the word limit
        words = message_content.split()
        formatted_message = ""
        for i in range(0, len(words), word_limit):
            line = ' '.join(words[i:i + word_limit])
            formatted_message += line + "\n"  # Add a newline for each line

        # Create the label with the formatted message
        if user_id == 1:  # Human
            label = Label(scrollable_frame, text=f"User {limited_user_id}: {formatted_message.strip()}", bg="#414141", fg="white", anchor='e', justify='right')
            label.pack(fill='x', padx=10, pady=5)
        elif user_id == -1:  # AI
            label = Label(scrollable_frame, text=f"AI {limited_user_id}: {formatted_message.strip()}", bg="#414141", fg="white", anchor='w', justify='left')
            label.pack(fill='x', padx=10, pady=5)

    # Schedule the next refresh
    mainWindow.after(5000, refresh_chat)

def refresh_chat():
    if current_chat_id is not None:
        threading.Thread(target=display_chat, args=(current_chat_id,)).start()

def message_read_creator():
    global scrollable_frame  # Make scrollable_frame global to access it in display_chat
    canvas = Canvas(mainWindow, bg="#333333", highlightbackground="#888888", highlightcolor="#888888", highlightthickness=2)
    scrollable_frame = Frame(canvas, bg="#414141", highlightbackground="#888888", highlightcolor="#888888", highlightthickness=2)

    scrollbar = Scrollbar(mainWindow, orient="vertical", command=canvas.yview, bg="#414141", troughcolor="#B40000", highlightbackground="#1C9B86")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.grid(row=4, column=45, rowspan=38, sticky=NS)
    canvas.grid(row=4, column=5, columnspan=39, rowspan=38, sticky=NSEW)

    mainWindow.grid_rowconfigure(0, weight=1)
    mainWindow.grid_columnconfigure(0, weight=1)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scroll_region)
    scrollable_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

def main_screen():
    setMainWindowGeometrystartup = (f"{halfScreenWidth}x{maxScreenHeight}+{halfScreenWidth-9}+0")
    mainWindow.geometry(setMainWindowGeometrystartup)

    #preventing the cells from collapsing when empty for the main window
    gRow = 45
    gColumn = 20

    for num in range(gRow):
        mainWindow.grid_rowconfigure(num, minsize=15, weight=1 )

    for num in range(gColumn):
        mainWindow.grid_columnconfigure(num, minsize=10, weight=1)

    mainWindow.grid_columnconfigure(4, minsize=5, weight=0)
    mainWindow.grid_columnconfigure(3, minsize=5, weight=0)
    mainWindow.grid_rowconfigure(38, minsize=5, weight=0)
    mainWindow.grid_rowconfigure(3, minsize=5, weight=0)
    mainWindow.grid_rowconfigure(42, minsize=5, weight=0)

    #Creation of the header frame, housing logo, title and configurational buttons
    #Firstly, initializing the header fram and opening the image
    msHeaderFrame = Frame(mainWindow, bg="#1C1C1C")
    msHeaderFrame.grid_configure(row=0, column=0, columnspan=20, rowspan=2, padx=7, pady=7, sticky=NSEW)
    msLogoLabel = Label(msHeaderFrame, image=headerLogoImage, bg="#1C1C1C")
    msLogoLabel.image = headerLogoImage

    #preventing the cells from collapsing when empty for the header frame
    hRow = 2
    hColumn = 21

    for num in range(hRow):
        msHeaderFrame.grid_rowconfigure(num, minsize=15, weight=1 )

    for num in range(hColumn):
        msHeaderFrame.grid_columnconfigure(num, minsize=30, weight=1)

    #creating and drawing all things into the header of the main screen
    msHeaderTitle = Label(msHeaderFrame, text="Aperture Science", font=(userSelectedFont, 30), bg="#1C1C1C", fg="#FFFFFF")
    msHeaderSeperator = ttk.Separator(master=mainWindow, orient=HORIZONTAL)
    
    msHeaderSeperator.grid_configure(row=3, column=0, columnspan=21,rowspan=1, sticky=NSEW)
    msHeaderTitle.grid_configure(row=0, column=9, columnspan=7, rowspan=2)
    msLogoLabel.grid_configure(row=0, column=0, columnspan=2, rowspan=2, sticky=W)

    #creating and drawing the chat selection area
    #Identifying the zone to place this
    chatSelectIdent = ttk.Separator(master=mainWindow, orient=VERTICAL)
    chatSelectIdent.grid_configure(row=4, column=4, rowspan=46, columnspan=1, sticky=NSEW, pady=0)

    #doesn't meet the chatSelectIdent, nor can center align for a good look. Refer to Win95 Design
    settingsSelectIndent = ttk.Separator(master=mainWindow, orient=HORIZONTAL)
    settingsSelectIndent.grid_configure(row=38, column=0, rowspan=1, columnspan=4, sticky=NSEW, padx=0)

    #textbox and message display border
    textboxSelectIndent = ttk.Separator(master=mainWindow, orient=HORIZONTAL)
    textboxSelectIndent.grid_configure(row=42, column=5, rowspan=1, columnspan=15, sticky=NSEW, padx=0)

    #Creating User Buttons
    msLegal=Button(mainWindow, text="Legal", font=(userSelectedFont, 10), bg="#333333", fg="#FFFFFF", command=displayLegal)
    msSetting=Button(mainWindow, text="Settings", font=(userSelectedFont, 10), bg="#333333", fg="#FFFFFF", command=displaySetting)

    msLegal.grid_configure(row=43, column=1, rowspan=1, columnspan=2, sticky=NSEW)
    msSetting.grid_configure(row=41, column=1, rowspan=1, columnspan=2, sticky=NSEW)

    #Creating text entry
    msEntry = Entry(mainWindow, width=60, justify=LEFT, cursor="xterm", font=(userSelectedFont, 10), bg="#2A2A2A", fg="#FFFFFF")
    msEntry.grid_configure(row=43, column=5, rowspan=1, columnspan=15, sticky=NSEW)

    chat_select_creater()
    message_read_creator()

    '''
    -use of tk.messages would see use for the responses and query
    -dynamically moving text boxes up on the canvas as a new message gets created is the next issue
    -same problem arises for the new chats section, although there we may see use of labels.
    '''

'''
    settingsArea = Label(mainWindow, bg="#8aaac2")
    settingsArea.grid_configure(row=38, column=0, rowspan=6, columnspan=4, sticky=NSEW)

    https://discuss.python.org/t/hide-show-windows-taskbar/9688
'''

draw_StartupLoad(db_name)
mainWindow.mainloop()
