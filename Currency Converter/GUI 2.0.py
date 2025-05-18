import customtkinter as ctk
from tkinter import *
import requests
from datetime import timedelta, datetime
import requests
import json
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Buat file utama
MainDir= os.path.dirname(os.path.abspath(__file__))
MainFile= os.path.join(MainDir, "history.json")

if os.path.exists(MainFile):
    with open(MainFile, "r") as f:
        history= json.load(f)

else:
    history= {}

dari_jenis= None #variabel simpan jenis mata uang
ke_jenis= None   #variabel simpan tujuan mata uang
jumlah= None     #variabel jumlah mata uang

MainURL = Your API key


def asal_uang(*args):
    global dari_jenis
    dari_jenis = matauang_asal.get()

def tujuan_uang(*args):
    global ke_jenis
    ke_jenis= matauang_tujuan.get()

def amount(*args):
    global jumlah
    jumlah = float(jumlah_uang.get())

def convert():
    url = Your API key
    
    response = requests.get(url)
    data = response.json()
        
    if data["result"] == "success":
        nilai_tukar = data["conversion_rates"][ke_jenis]
        jumlah_yang_dikonversi = jumlah * nilai_tukar
        jumlah_final= f"{jumlah_yang_dikonversi:.2f}"+ " " + f"{ke_jenis}"
        result_display.configure(state= 'normal')
        result_display.delete(0, END)
        result_display.insert(0, jumlah_final)
        result_display.configure(state= 'readonly')
    else:
        print(f"Error: {data['error-type']}")
        return None, None

def close():
    plt.close(fig)
    window.destroy()

# Atur window utama
window = ctk.CTk()
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()

fonts = ctk.CTkFont("Montserrat",20,'bold')
fontsEnt = ctk.CTkFont("Montserrat",18,'bold')
fontsTitle = ctk.CTkFont("Montserrat",35,'bold')

matauang_asal= ctk.StringVar()
matauang_tujuan= ctk.StringVar()
matauang_asal.trace_add('write', asal_uang)
matauang_tujuan.trace_add('write', tujuan_uang)

jumlah_uang= ctk.StringVar()
jumlah_uang.trace_add('write', amount)

cenX = int((screenwidth/2) - (950/2))          
cenY = int((screenheight/2) - (700/2))

window.configure(fg_color ='#dff2ff')

label_title = ctk.CTkLabel(master= window, text= 'CURRENCY\n CONVERTER', text_color='#0e253c', font= fontsTitle)
label_title.place(x = 100, y = 40)

window.geometry(f"950x700+{cenX}+{cenY}")
window.resizable(False, False)

# Buat frame
frame1 = ctk.CTkFrame(master = window, width=330, height=480, corner_radius=20, fg_color= '#f4fcff')
frame1.place(x= 50, y= 150)

frame2 = ctk.CTkFrame(master = window, width=540, height=380, corner_radius=20, fg_color= '#f4fcff')
frame2.place(x= 400, y= 60)

frame3 = ctk.CTkFrame(master = window, width=500, height=210, corner_radius=20, fg_color= '#ffffff')
frame3.place(x= 400, y= 420)

# Komponen frame 1
label_from = ctk.CTkLabel(master = frame1, font=fonts, text="From", text_color="#0e253c") 
label_from.place(x = 57, y=20)

label_to = ctk.CTkLabel(master=frame1, font=fonts, text="To", text_color="#0e253c")
label_to.place(x = 210, y=20)

menu_from = ctk.CTkOptionMenu(master = frame1, values= ['USD', 'IDR', 'EUR', 'SGD', 'JPY'], width=90, height=50, corner_radius=10, variable=matauang_asal)
menu_from.place(x= 50, y= 60)

menu_to = ctk.CTkOptionMenu(master = frame1, values= ['USD', 'IDR', 'EUR', 'SGD', 'JPY'], width=90, height=50, corner_radius=10, variable=matauang_tujuan)
menu_to.place(x= 200, y= 60)

InputUang = ctk.CTkEntry(master= frame1,width=250, height=60, placeholder_text= "Masukkan nilai uang", placeholder_text_color= "#0e253c", fg_color= "white",text_color= "#0e253c",
                          border_color= "#bec8d3", border_width=2,font=fontsEnt, corner_radius=15, textvariable= jumlah_uang)
InputUang.place(x= 45, y= 130)

tombol_conv = ctk.CTkButton(master = frame1, text= 'CONVERT',text_color='white', font=fonts, width=220, height=60, corner_radius=15, fg_color='#87bdec', command=convert)
tombol_conv.place(x= 60, y= 210)

label_result = ctk.CTkLabel(master=frame1, font = fonts, text = 'Hasil', text_color='#0e253c')
label_result.place(x= 60, y= 280)

result_display = ctk.CTkEntry(master= frame1,width=250, height=60, fg_color= "white",text_color= "#0e253c",
                          border_color= "#bec8d3", border_width=2,font=fontsEnt, corner_radius=15)
result_display.configure(state= 'readonly')
result_display.place(x = 45, y = 310)


# Komponen frame 2

# Parsing tanggal agar bisa dibaca
res = requests.get(MainURL)
data= res.json()
tanggal= data["time_last_update_utc"]
tanggalObj= datetime.strptime(tanggal, "%a, %d %b %Y %H:%M:%S %z")
tanggalReal= tanggalObj.date().isoformat()

#Ambil nilai tukar USD IDR
GraphChange= data["conversion_rates"]["IDR"]

# Filtrasi tanggal
MaxTanggal= datetime.strptime(tanggalReal, "%Y-%m-%d").date() - timedelta(days=6)
FilterDate= {}
for d, v in history.items():
    dReal= datetime.strptime(d, "%Y-%m-%d").date()
    if dReal >= MaxTanggal:
        FilterDate[d] = v

FilterDate[tanggalReal] = GraphChange
history = FilterDate

with open(MainFile, "w") as f:
    json.dump(history, f, indent=2)

# Matplotlib
TanggalList= []
NilaiKursList= []

for i in sorted(history.keys()):
    TanggalList.append(datetime.strptime(i, "%Y-%m-%d").date())
    NilaiKursList.append(history[i])

fig, ax = plt.subplots(figsize=(5,3))
ax.plot(TanggalList, NilaiKursList, marker='o', color='black', linestyle='-')
ax.set_title("1 USD to IDR")
ax.set_ylabel('Nilai Tukar')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
fig.autofmt_xdate()
fig.patch.set_color('#f4fcff')

deploy= FigureCanvasTkAgg(fig, master=frame2)
deploy.draw()
deploy.get_tk_widget().pack(pady=10)

# Komponen frame 3

window.protocol("WM_DELETE_WINDOW", close)
window.mainloop()
