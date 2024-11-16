import tkinter as tk
import csv
import os
from tkinter import messagebox, ttk
from datetime import datetime

# Fungsi untuk menyimpan data karyawan ke file CSV
def simpan_karyawan(nama, karyawan_id):
    if not nama or not karyawan_id:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
        return
    file_exists = os.path.isfile("data_karyawan.csv")
    with open("data_karyawan.csv", "a", newline="") as file:
        writer = csv.writer(file)

        # Jika file belum ada, tambahkan header
        if not file_exists:
            writer.writerow(["ID Karyawan", "Nama Karyawan"]) # tambahkan header

        
        writer.writerow([karyawan_id, nama])

        messagebox.showinfo("Berhasil", "Data karyawan berhasil disimpan!")
        entry_nama.delete(0, tk.END)
        entry_id.delete(0, tk.END)

# Fungsi untuk menyimpan data absensi ke file CSV
def simpan_absensi(karyawan_id, nama_karyawan):
    if not nama_karyawan or not karyawan_id:
        messagebox.showwarning("Peringatan", "Pilih karyawan untuk mencatat absensi!")
        return
    
    # Menyimpan data absensi ke file CSV
    file_exists = os.path.isfile("data_absensi.csv")
    with open("data_absensi.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["ID Karyawan", "Nama Karyawan", "Waktu"])

        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([karyawan_id, nama_karyawan, waktu])
        messagebox.showinfo("Berhasil", f"Absensi untuk {nama_karyawan} berhasil dicatat!")
        window_absensi.destroy()

# Fungsi untuk setiap tombol
def input_karyawan():
    window = tk.Toplevel(root)
    window.title("Input Karyawan")
    window.geometry("300x200")

    # Label dan Entry untuk Nama Karyawan
    tk.Label(window, text="ID Karyawan:", font=('Arial', 10)).pack(pady=5)
    global entry_id
    entry_id = tk.Entry(window, width=30)
    entry_id.pack(pady=5)

    tk.Label(window, text="Nama Karyawan:", font=('Arial', 10)).pack(pady=5)
    global entry_nama
    entry_nama = tk.Entry(window, width=30)
    entry_nama.pack(pady=5)

    btn_simpan = tk.Button(window, text="Simpan", command=lambda: simpan_karyawan(entry_nama.get(), entry_id.get()))
    btn_simpan.pack(pady=10)

def absensi_karyawan():
    global window_absensi
    window_absensi = tk.Toplevel(root)
    window_absensi.title("Absensi Karyawan")

    window_absensi.geometry("400x300")

    # Membaca data karyawan dari file CSV
    data_karyawan = []
    try:
        with open("data_karyawan.csv", "r") as file:
            reader = csv.reader(file)
            next(reader) #lewati header
            data_karyawan = list(reader)
    except FileNotFoundError:
        messagebox.showwarning("Peringatan", "Data karyawan belum tersedia. Tambahkan karyawan terlebih dahulu.")
        window_absensi.destroy()
        return
    
    # Label Judul
    tk.Label(window_absensi, text="Pilih Karyawan untuk absensi", font=("Arial", 12, "bold")).pack(pady=10)

    # Dropdown untuk memilih karyawan
    tk.Label(window_absensi, text="Nama Karyawan:").pack(pady=5)
    global selected_karyawan
    selected_karyawan = tk.StringVar(window_absensi)
    karyawan_nama_list = [f"{row[0]} - {row[1]}" for row in data_karyawan] # Format: "ID - Nama"
    selected_karyawan.set(karyawan_nama_list[0]) # Set default value

    dropdown = tk.OptionMenu(window_absensi, selected_karyawan, *karyawan_nama_list)
    dropdown.pack(pady=5)

    # Tombol simpan absensi
    btn_absen = tk.Button(window_absensi, text="Catat Absensi", command=lambda: simpan_absensi(*selected_karyawan.get().split(" - ")))
    btn_absen.pack(pady=20)

def rekap_absensi():
    global window_rekap
    window_rekap = tk.Toplevel(root)
    window_rekap.title("Rekap Absensi")
    window_rekap.geometry("600x400")

    # Label Judul
    tk.Label(window_rekap, text="Rekap Absensi karyawan", font=('Arial', 12, 'bold')).pack(pady=10)

    # Tabel menggunakan Treeview
    columns = ("ID Karyawan", "Nama Karyawan", "Waktu")
    tree = ttk.Treeview(window_rekap, columns=columns, show="headings")
    tree.heading("ID Karyawan", text="ID Karyawan")
    tree.heading("Nama Karyawan", text="Nama Karyawan")
    tree.heading("Waktu", text="Waktu")
    tree.pack(fill=tk.BOTH, expand=True)

    # Membaca data absensi dari file CSV
    try:
        with open("data_absensi.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", tk.END, values=row)
    except FileNotFoundError:
        messagebox.showwarning("Peringantan", "Belum ada data absensi.")

# Membuat tampilan utama
root = tk.Tk()
root.title("Aplikasi Absensi Karyawan")
root.geometry("300x200") # ukuran

# Label Judul
label = tk.Label(root, text="Aplikasi Absensi Karyawan", font=("Arial:", 14, "bold"))
label.pack(pady=10)

# Tombol Menu
btn_input = tk.Button(root, text="Input Karyawan", width=20, command=input_karyawan)
btn_input.pack(pady=5)

btn_absensi = tk.Button(root, text="Absensi", width=20, command=absensi_karyawan)
btn_absensi.pack(pady=5)

btn_rekap = tk.Button(root, text="Rekap Absensi", width=20, command=rekap_absensi)
btn_rekap.pack(pady=5)

# Menjalankan aplikasi
root.mainloop()