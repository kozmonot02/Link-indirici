# gerekli modülleri yükle
# !/usr/bin/python
import subprocess

# installing required modules
subprocess.call(["pip", "install", "wget"])
subprocess.call(["pip", "install", "tk"])

# modülleri içeri aktar
import os
import wget
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class Downloader:
    def __init__(self, master):
        self.master = master
        master.title("Link İndirici")

        self.download_folder = ""

        self.lbl_folder = tk.Label(master, text="Kaydedilecek klasör: ")
        self.lbl_folder.grid(row=0, column=0)

        self.btn_folder = tk.Button(master, text="Klasör Seç", command=self.select_folder)
        self.btn_folder.grid(row=1, column=0)

        self.btn_download = tk.Button(master, text="İndir", command=self.download_links)
        self.btn_download.grid(row=2, column=0)

        self.progress_bar = ttk.Progressbar(master, orient="horizontal", mode="determinate")
        self.progress_bar.grid(row=3, column=0)

        self.progress_label = tk.Label(master, text="")
        self.progress_label.grid(row=4, column=0)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_folder = folder
            self.lbl_folder.config(text=f"Kaydedilecek klasör: {self.download_folder}")

    def download_links(self):
        if not self.download_folder:
            messagebox.showerror("Hata", "Lütfen bir klasör seçin!")
            return

        # linkler.txt dosyasını açıp her satırı bir listeye atıyoruz
        with open("veri.txt", "r", encoding="utf-8") as f:
            links = [line.strip().split("|")[0].strip() for line in f]

        # downloads klasörünü oluşturuyoruz
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        num_links = len(links)
        self.progress_bar.config(maximum=num_links)
        for i, link in enumerate(links):
            try:
                print(f"İndiriliyor {link}:")
                # dosyayı seçilen klasöre kaydediyoruz
                wget.download(link, os.path.join(self.download_folder, os.path.basename(link)), bar=self.progress)
                print("\nİndirme tamamlandı!")
            except Exception as e:
                print(f"Hata oluştu: {e}")

            self.progress_bar.step(1)
            self.progress_label.config(text=f"{i+1}/{num_links} dosya indirildi")

    def progress(self, current, total, width=80):
        progress_width = int(width * current / total)
        progress_str = f"[{'=' * progress_width}{' ' * (width - progress_width)}]"
        percent_str = f"{100 * current / total:.1f}%"
        print(f"{progress_str} {percent_str}", end='\r')

root = tk.Tk()
d = Downloader(root)
root.mainloop()

