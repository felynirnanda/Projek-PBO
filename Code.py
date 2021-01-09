import sqlite3
from abc import ABC, abstractmethod

class Pengguna(ABC):
    @abstractmethod
    def showInfo(self):
        pass

    @abstractmethod
    def umur(self):
        pass

class Pelanggan(Pengguna):
    jumlahPelanggan = 0
    def __init__(self, nomerID, nama, alamat, noHP, tahunLahir):
        # private variabel
        self.__nama = nama
        self.__alamat = alamat
        self.__noHP = noHP
        self.tahunLahir = tahunLahir
        Pelanggan.jumlahPelanggan += 1
        self.__nomer_id = nomerID

    def showInfo(self):
        print("Nama\t\t: {}\nAlamat\t\t: {}\nNomer HP\t: {}".format(self.nama, self.alamat, self.noHP))

    def umur(self):
        usiaSaatIni = 2020 - self.__tahunLahir
        return usiaSaatIni

    @property
    def nomer_id(self):
        return self.__nomer_id       
    
    @property
    def nama(self):
        pass

    @nama.getter
    def nama(self):
        return self.__nama

    @nama.setter
    def nama(self, inputNama):
        self.__nama = inputNama

    @nama.deleter
    def nama(self):
        print("deleted name")
        self.__nama = None

    @property
    def alamat(self):
        pass

    @alamat.getter
    def alamat(self):
        return self.__alamat

    @alamat.setter
    def alamat(self, inputAlamat):
        self.__alamat = inputAlamat

    @alamat.deleter
    def alamat(self):
        print("deleted addres")
        self.__alamat = None

    @property
    def noHP(self):
        pass

    @noHP.getter
    def noHP(self):
        return self.__noHP

    @noHP.setter
    def noHP(self, inputNoHP):
        self.__noHP = inputNoHP

    @noHP.deleter
    def noHP(self):
        print("deleted number phone")
        self.__noHP = None

class Karyawan(Pelanggan):
    def __init__(self, noID, nama, alamat, noHP, noKtp, tahunLahir):
        super().__init__(noID, nama, alamat, noHP, tahunLahir)
        self.noKtp = noKtp

    def showInfo(self):
        print("Nama\t\t: {}\nNomer KTP\t: {}\nAlamat\t\t: {}\nNomer HP\t: {}".format(self.nama, self.noKtp, self.alamat, self.noHP))

class SaldoPelanggan:
    def __init__(self, nomorid, nama, alamat, noHP):
        self.__nomorid = nomorid
        self.__nama = nama
        self.__alamat = alamat
        self.__noHP = noHP
        self.__jumlahSaldo = self.jumlahSaldo()
        self.__jumlahHutang = self.apdetHutang()

    def jumlahSaldo(self):
        conn = sqlite3.connect('project.sqlite')
        cursor = conn.cursor()
        hasil = cursor.execute("select jumlahUang from SaldoPelanggan where noID = ?", (str(self.__nomorid),)).fetchone()[0]
        conn.close()
        return hasil

    def showSaldo(self):
        print(self.__jumlahSaldo)

    # waktu transaksi pada masing-masing method untuk mengetahui kapan transaksi saat itu dilakukan, pakai datetime database auto sabi
    def saldoTabungan(self):
        uangMasuk = int(input("Masukan jumlah uang yang ingin Anda tabung: "))
        jumlahSaldoTabungan = self.__jumlahSaldo + uangMasuk
        self.__jumlahSaldo = jumlahSaldoTabungan
        conn = sqlite3.connect('project.sqlite')
        cursor = conn.cursor()
        cursor.execute("update SaldoPelanggan set jumlahUang = ? where noID = ? ", (jumlahSaldoTabungan, self.__nomorid,))
        conn.commit()
        conn.close()

    def saldoTarik(self):
        uangTarik = int(input("masukan jumlah uang yang ingin Anda ambil"))
        if self.__jumlahSaldo < uangTarik:
            print("Maaf saldo anda tidak mencukupi")
        else:
            jumlahSaldoTarik = self.__jumlahSaldo - uangTarik
            self.__jumlahSaldo = jumlahSaldoTarik
            conn = sqlite3.connect('project.sqlite')
            cursor = conn.cursor()
            cursor.execute("update SaldoPelanggan set jumlahUang = ? where noID = ? ", (self.__jumlahSaldo, self.__nomorid,))
            conn.commit()
            conn.close()

    def utang(self):
        uangPinjam = int(input("Masukan jumlah uang yang ingin Anda pinjam"))
        bunga = self.bunga(uangPinjam)
        piutang = uangPinjam + bunga
        self.__jumlahHutang += piutang
        jumlahSaldo = self.__jumlahSaldo + uangPinjam 
        self.__jumlahSaldo = jumlahSaldo
        conn = sqlite3.connect('project.sqlite')
        cursor = conn.cursor()
        cursor.execute("update SaldoPelanggan set jumlahHutang = ? ,jumlahUang = ? where noID = ? ", (self.__jumlahHutang, self.__jumlahSaldo, self.__nomorid,))
        conn.commit()
        conn.close()

    def bunga(self, uangPinjam):
        hari = int(input("masukan total hari terhitung hari ini dan hari dimana Anda mengembalikan"))
        bulan = hari / 30
        bungaPinjam = bulan / 12 * 5 / 100 * uangPinjam
        return bungaPinjam

    def bayarHutang(self):
        piutang = self.jumlahHutang
        if self.__jumlahSaldo < piutang:
            print("maaf saldo Anda kurang untuk membayar utang")
        else:
            jumlahSaldo = self.__jumlahSaldo - piutang 
            self.__jumlahSaldo = jumlahSaldo
            conn = sqlite3.connect('project.sqlite')
            cursor = conn.cursor()
            cursor.execute("update SaldoPelanggan set jumlahHutang = 0 ,jumlahUang = ? where noID = ? ", (self.__jumlahSaldo, self.__nomorid,))
            conn.commit()
            conn.close()

    def apdetHutang(self):
        conn = sqlite3.connect('project.sqlite')
        cursor = conn.cursor()
        hasil = cursor.execute("select jumlahHutang from SaldoPelanggan where noID = ?", (str(self.__nomorid),)).fetchone()[0]
        conn.close()
        return hasil

class Menu:
    # menu utama untuk semua pengguna
    def menuUtama(self):
        while True:
            print("""Selamat Datang^_^
            1. Daftar Pelanggan
            2. Login Pelanggan
            3. Login Karyawan
            4. Keluar""")
            pilihan = int(input("masukkan nomor yang anda pilih"))
            if pilihan == 1:
                nama = input("masukkan nama anda ")
                alamat = input("masukkan alamat anda ")
                nomorhp = input("masukkan nomor hp anda ")
                tahunLahir = input("masukkan tahun lahir")
                conn = sqlite3.connect('project.sqlite')
                cursor = conn.cursor()
                query = "INSERT INTO Pelanggan(Nama,Alamat,NomorHp, tahunLahir) VALUES (?,?,?,?)"
                cursor.execute(query, (nama, alamat, nomorhp, tahunLahir))
                query = "INSERT INTO SaldoPelanggan(jumlahUang, jumlahHutang) VALUES (0, 0)"
                cursor.execute(query)
                conn.commit()
                conn.close()
                print("Selamat Anda berhasil mendaftar")
            elif pilihan == 2:
                conn = sqlite3.connect('project.sqlite')
                cursor = conn.cursor()
                nama = input("masukkan nama ")
                hasil = cursor.execute("select * from Pelanggan where Nama = ?", (nama,)).fetchone()
                conn.close()
                if len(hasil) > 0:
                    if nama == hasil[1]:
                        pelanggan = Pelanggan(hasil[0],hasil[1], hasil[2], hasil[3], hasil[4])
                        self.menuPelanggan(pelanggan)
                else:
                    print("maaf nama tidak ditemukan")
            elif pilihan == 3:
                conn = sqlite3.connect('project.sqlite')
                cursor = conn.cursor()
                nama = input("masukkan nama ")
                hasil = cursor.execute("select * from Karyawan where Nama = ?", (nama,)).fetchone()
                conn.close()
                print(hasil)
                if len(hasil) > 0:
                    if nama == hasil[1]:
                        karyawan = Karyawan(hasil[0],hasil[1], hasil[2], hasil[3], hasil[4], hasil[5])
                        self.menuKaryawan(karyawan)
                else:
                    print("maaf nama tidak ditemukan")
            elif pilihan == 4:
                break
            else:
                print ("pilihan tidak tersedia")
        

    def menuPelanggan(self, pelanggan):
        while True:
            saldo = SaldoPelanggan(pelanggan.nomer_id, pelanggan.nama, pelanggan.alamat, pelanggan.noHP)
            print("""Selamat Datang di anu
            Silahkan pilih fitur :
            1. Lihat profil
            2. Tambah tabungan
            3. Bayar Hutang
            4. Pinjam
            5. Tarik uang
            6. Lihat saldo
            7. Keluar """)
            pilih = input("masukkan fitur yang anda mau")
            if pilih == "1":
                pelanggan.showinfo()
            elif pilih == "2":
                saldo.saldoTabungan()
            elif pilih == "3":
                saldo.bayarHutang()
            elif pilih == "4":
                saldo.utang()
            elif pilih == "5":
                saldo.saldoTarik()
            elif pilih == "6":
                saldo.showSaldo()
            elif pilih == "7":
                break


    def menuKaryawan(self, karyawan):
        while True:
            print("""Selamat Datang di anu
            silahkan pilih fitur :
            1. Lihat Pelanggan
            2. Lihat Profil
            """)
            pilih = input("pilih fitur yang ingin dipilih")
            if pilih == "1":
                conn = sqlite3.connect('project.sqlite')
                cursor = conn.cursor()
                hasil = cursor.execute("select * from Pelanggan").fetchall()
                conn.close()
                print(f"{'NO':<3}{'NAMA':<10}{'Alamat':<15}{'No Telpn':<10}")
                for baris in hasil:
                    print(f"{baris[0]:<3}{baris[1]:<10}{baris[2]:<15}{baris[3]:<10}")
            elif pilih == "2":
                karyawan.showinfo()   
        
objMenu = Menu()
objMenu.menuUtama()
