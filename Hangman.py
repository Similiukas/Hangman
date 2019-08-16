import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
from urllib.request import urlopen as ureq
import random
import sys
import os



class Difficulty(tk.Label):
    def __init__(self):
        self.text = "Welcome to the hangman game\nYour objective is to guess a word\nBy guessing 1 letter at a time\nIf the letter isn't in the word\nA man is getting hanged\nNow choose a difficulty"
        tk.Label.__init__(self, text=self.text, font=("Aerial", 17), bg="SkyBlue")
        self.pack()
        self.button1 = tk.Button(root, text="Easy", font=("Aerial", 20), width=8, command=lambda widget="button1": self.start(widget), bg="Lime")
        self.button1.pack(side="left", expand=True)
        root.geometry("350x300")
        root.resizable(width=False, height=False)
        root.configure(bg="SkyBlue")
        self.button2 = tk.Button(root, text="Hard", font=("Aerial", 20), width=8, command=lambda widget="button2": self.start(widget), bg="Crimson")
        self.button2.pack(side="right", expand=True)

    def start(self, button):
        global hints, life, point
        if button == "button1":
            hints = 1
            life = 1
            point = 5
        else:
            hints = 0
            life = 2
            point = 10
        self.destroy()
        self.button1.destroy()
        self.button2.destroy()
        Main(root)


class Main(tk.Frame):

    def __init__(self, parent):
        global hints
        # Frame for hints and score
        tk.Frame.__init__(self, parent, bg="Khaki")
        self.pack(fill="x")

        # Window size and title
        self.parent = parent
        parent.geometry("610x670")
        parent.title("Hangman")
        parent.protocol("WM_DELETE_WINDOW", self.close)  # If user wants to close the app
        parent.resizable(width=False, height=False)

        # Frame for hidden word and guessed letters
        self.frame = tk.Frame(root, bg="Gold")
        self.frame.pack(fill="both", side="bottom", expand=True)

        # Fonts
        self.fnt_0 = tkFont.Font(family="Aerial", size="14")
        self.fnt_1 = tkFont.Font(family="Aerial", size="17")
        self.fnt_2 = tkFont.Font(family="Aerial", size="25")

        # Label for hint 
        self.hint_label = tk.Label(self, text="Hints left: {}/1".format(hints), font=self.fnt_0, bg="Khaki")
        self.hint_label.pack(fill="both", side="left")

        # Label for score
        self.score = 0
        self.score_label = tk.Label(self, text="Score: 0",font=self.fnt_0, bg="Khaki")
        self.score_label.pack(fill="both", side="right")

        # Image
        self.lives = 6
        self.img = Image.open("Images\spr_hangman_6.png")  # download.jpg
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.label = tk.Label(root, image=self.tkimg, bg="Khaki")
        self.label.pack(fill="x")

        # Label which says about the state of the game
        self.info = tk.Label(self.frame, text="Start guessing the word!", font=self.fnt_1, bg="Orange")  # Change the text----------
        self.info.pack(fill="x")

        # Label where for hidden word
        self.hidden = tk.Label(self.frame, font=self.fnt_2, bg="Gold")
        self.hidden.bind("<Key>", self.game)
        self.hidden.pack(expand=True)
        self.hidden.focus_set()

        # Button for a hint
        self.hint = tk.Button(self.frame, text="Press for a hint", command=self.help, font=self.fnt_0, bg="Pink")
        self.hint.pack()

        # Label which displays guessed letters
        self.letters = tk.Label(self.frame, text="guessed letters:", font=self.fnt_1, bg="Gold")
        self.letters.pack(expand=True)

        # Label for a game version
        self.version = tk.Label(self.frame, text="V1.0", bg="Gold")
        self.version.pack(side="bottom")

        # Making a list of words
        uClient = ureq("http://www.ef.com/english-resources/english-vocabulary/top-1000-words/")
        page_html = uClient.read()
        soup = BeautifulSoup(page_html, "html.parser")
        html = soup.findAll("div", {"class": "field-item even"})
        wordss = str.split(html[0].text)

        self.words = wordss[95:]
        self.word = random.choice(self.words)
        self.hidden_text = ["_" for _ in range(len(self.word))]
        self.hidden["text"] = " ".join(self.hidden_text)

    
    # Main game function. Called then pressed a button on keyboard
    def game(self, event):
        global life, point
        if event.char.lower() in ("abcdefghijklmnopqrstuvwxyz") and event.char.upper() not in self.letters["text"]:
            self.letters["text"] += " " + event.char.upper()

            # If the guess is correct
            if event.char.lower() in self.word:
                self.info["text"] = "Your guess {} is correct!".format(event.char.lower())
                self.score += point
                self.score_label["text"] = "Score: {}".format(self.score)
                for i, item in enumerate(self.word):
                    if item == event.char.lower():
                        self.hidden_text[i] = event.char.lower()

            # If the guess is wrong
            else:
                self.lives -= life
                if not self.lives:
                    self.reset()
                else:
                    self.info["text"] = "Wrong guess, try again"
                    self.img = Image.open("Images\spr_hangman_{}.png".format(self.lives))
                    self.tkimg = ImageTk.PhotoImage(self.img)
                    self.label["image"] = self.tkimg
            
            # If the word is guessed
            if "".join(self.hidden_text) == self.word:
                self.reset()
        else:
            self.info["text"] = "Invalid guess, try again"

        self.hidden["text"] = " ".join(self.hidden_text)
    

    # Function for a hint
    def help(self):
        global hints
        if hints == 1:
            self.hint_label["text"] = "Hints left: 0/1"
            random_letter = random.choice(self.word)

            while random_letter in self.hidden_text:
                random_letter = random.choice(self.word)
            else:
                hints = 0
                self.letters["text"] += " " + random_letter.upper()
                for index, item in enumerate(self.word):
                    if item == random_letter:
                        self.hidden_text[index] = random_letter

            self.hidden["text"] = " ".join(self.hidden_text)
            # If the user uses the hint last and the word is complete
            if "".join(self.hidden_text) == self.word:
                self.reset()

        else:
            self.info["text"] = "No hints left"

    
    # Resets everything when the word is guessed
    def reset(self):
        global hints
        if not self.lives:
            self.info["text"] = "No lives left.The word was [{0}]\nYour score was [{1}]".format(self.word, self.score)
            self.img = Image.open("Images\spr_hangman_0.png")
            self.tkimg = ImageTk.PhotoImage(self.img)
            self.label["image"] = self.tkimg
            #  Can't have spaces between words in path (https://stackoverflow.com/questions/50320438/os-execl-wrong-argument-split)
            if messagebox.askokcancel("You lost!", "Do you want to restart?"):
                print("Does is still run?")
                python = sys.executable
                os.execl(sys.executable, 'python', __file__, *sys.argv[1:])
                # os.execl(python, "python", *sys.argv)
            else:
                root.quit()
        else:
            self.lives = 6
            self.img = Image.open("Images\spr_hangman_6.png")
            self.tkimg = ImageTk.PhotoImage(self.img)
            self.label["image"] = self.tkimg
            self.info["text"] = "Good job, the word was [{}]. Now keep on going!".format(self.word)
            self.score += 20
            self.score_label["text"] = "Score: {}".format(self.score)
            self.word = random.choice(self.words)
            self.hidden_text = ["_" for _ in range(len(self.word))]
            self.letters["text"] = "guessed letters:"
            hints = 1
            self.hint_label["text"] = "Hints left: 1/1"
            self.hidden["text"] = " ".join(self.hidden_text)

    
    # When pressed on X to close the game is if user wants to close the game
    def close(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            root.destroy()




if __name__ == "__main__":
    root = tk.Tk()
    Difficulty()
    root.mainloop()
