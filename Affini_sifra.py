import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from math import gcd

# Dvě abecedy pro pomoc s mapováním šifry(jaké číslo má dané písmeno a napoak)
L2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",range(26)))
I2L = dict(zip(range(26),"ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

#Pro výpočet inverzního prvku a
def inv_a(a):
    if gcd (a,26) != 1:
        return messagebox.showerror ("Error","'a' nemá inverzní hodnotu , zvol jinou hodnotu pro 'a'")
    else:
        je = False
        for i in range (0,26):
            if (i * a % 26) == 1:
                je = True
                break
        return i

#Ošetření klíče pro diakritiku
def OsetriKlic(klic,czen):
    diakritika = {"Á":"A","Č":"C","É":"E","Ě":"E","Ď":"D","Í":"I","Ň":"N","Ó":"O","Ř":"R","Š":"S","Ť":"T","Ů":"U",
                  "Ú":"U","Ý":"Y","Ž":"Z","0":" NULA ","1":" JEDNA ","2":" DVA ","3":" TRI ","4":" CTYRI ","5":" PET ","6":" SEST ","7":" SEDM "
                  ,"8":" OSM ","9":" DEVET "," ":" "}
    osetrenyKlic = ""
    klic1 = re.sub ('[!,*)@#%(&$_?.^]','',klic)
    klic1 = klic1.upper ()
    if czen == 1:  # pro češtinu
        validniAbeceda = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","X",
                          "Y","Z"]
        klic1.replace ("W","V")
    else:
        validniAbeceda = ["A","B","C","D","E","F","G","H","I","K","L","M","N","O","P","Q","R","S","T","U","V","W","X",
                          "Y","Z"]
        klic1.replace ("J","I")
    for i in klic1:

        if validniAbeceda.count (i) > 0:
            osetrenyKlic += i
        else:
            try:
                aaa = diakritika[i]
                osetrenyKlic += aaa
            except:
                pass
    return osetrenyKlic

def BKEY(klic):
    lookp_dict = {"NULA":"0","JEDNA":"1","DVA":"2","TRI":"3","CTYRI":"4","PET":"5","SEST":"6","SEDM":"7","OSM":"8","DEVET":"9"}
    temp = klic.split ()
    res = []
    for wrd in temp:
        res.append (lookp_dict.get (wrd,wrd))

    res = ' '.join (res)
    return res

def sifrovani(text, a, b):
    sifratext = ""
    for c in text.upper():
        if c.isalpha(): sifratext += I2L[ (L2I[c] * a + b)%26 ]
        else: sifratext += c
    return sifratext

def desifrovani(sifratext, a, b):
    text = ""
    for c in sifratext.upper():
        if c.isalpha(): text += I2L[ (inv_a(a) * (L2I[c] - b) )%26 ]
        else: text += c
    return text


class Affinisifra:

    def __init__(self, root):

        self.plain_text = tk.StringVar(root, value="")
        self.cipher_text = tk.StringVar(root, value="")
        self.a = tk.IntVar(root)
        self.b = tk.IntVar(root)

        root.title("Affiní šifra")

        style = ttk.Style()
        style.configure("TLabel",
                        font = "Serif 15",
                        padding=10)
        style.configure("TButton",
                         font="Serif 15",
                         padding=10)
        style.configure("TEntry",
                        font="Serif 18",
                        padding=10)

        self.plain_label = tk.Label(root, text="Text  =>", fg="darkgreen").grid(row=0, column=1)
        self.plain_entry = ttk.Entry(root,textvariable=self.plain_text, width=50)
        self.plain_entry.grid(row=0, column=2, rowspan=4 , columnspan=4)

        self.plain_clear = tk.Button(root, text="Smazat", command=lambda: self.clear('plain')).grid(row=2, column=1)

        self.a_label = tk.Label(root, text="a").grid(row=4, column=0)

        self.a_entry = tk.Entry(root, textvariable=self.a).grid(row=4, column=1)

        self.b_label = tk.Label(root, text="b").grid(row=5, column=0)

        self.b_entry = tk.Entry(root, textvariable=self.b).grid(row=5, column=1)

        self.encipher_button = ttk.Button(root, text="Zašifrovat",command=lambda: self.encipher_press()).grid(row=4, column=3)

        self.decipher_button = ttk.Button(root, text="Dešifrovat",command=lambda: self.decipher_press()).grid(row=4, column=4)

        self.cipher_label = tk.Label(root, text="Affiní šifra  =>", fg="red").grid(row=7, column=1)

        self.cipher_entry = ttk.Entry(root,textvariable=self.cipher_text, width=50)
        self.cipher_entry.grid(row=6, column=2, rowspan=4 , columnspan=4)

        self.cipher_clear = tk.Button(root, text="Smazat",command=lambda: self.clear('cipher')).grid(row=8, column=1)



    def clear(self, str_val):
        if str_val == 'cipher':
            self.cipher_entry.delete(0, 'end')
        else:
            self.plain_entry.delete(0, 'end')

    def get_key(self):
        a_val = self.a.get()
        inv_a(a_val)
        b_val = self.b.get()
        return a_val, b_val

    def encipher_press(self):
        a, b = self.get_key()
        cipher_text = sifrovani(OsetriKlic(self.plain_entry.get(),1), a, b)
        self.cipher_entry.delete(0, "end")
        self.cipher_entry.insert(0, cipher_text)

    def decipher_press(self):
        a, b = self.get_key()
        plain_text = desifrovani(self.cipher_entry.get(), a, b)
        plain_text1=BKEY(plain_text)
        self.plain_entry.delete(0, "end")
        self.plain_entry.insert(0, plain_text1)


root = tk.Tk()

caesar = Affinisifra(root)

root.mainloop()
