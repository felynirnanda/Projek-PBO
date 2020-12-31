import sqlite3

class Pelanggan:
    jumlahPelanggan = 0
    def __init__(self, nomerID, nama, alamat, noHP, tahunLahir):
        # private variabel
        self.__nama = nama
        self.__alamat = alamat
        self.__noHP = noHP
        self.tahunLahir = tahunLahir
        Pelanggan.jumlahPelanggan += 1
        self.__nomer_id = nomerID

    def status(self):
        nomerId = self.__nomer_id
        if nomerId[0] == "P":
            status = "Pelanggan"
        else:
            status = "Karyawan"
        print("Status pengguna ialah ", status)

    def showinfo(self):
        print("Nama\t\t: {}\nAlamat\t\t: {}\nNomer HP\t: {}".format(self.nama, self.alamat, self.noHP))

    def umur(self):
        pass
    
    # membuat method untuk menentukan no id pelanggan yang mendaftar
    # def nomerID(self):
    #     nomer_id = "P" + str(Pelanggan.jumlahPelanggan)
    #     return nomer_id

    @property
    def nomer_id(self):
        return self.__nomer_id       


    # membuat method nomerID seolah olah menjadi bagian dari atribut suatu kelas
    # @property
    # def noID(self):
    #     pass
    
    # yang mana, nama atribut dari method nomerID() ialah noID
    # @noID.getter
    # def noID(self):
    #     return self.nomerID()
    
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


# fira = Pelanggan("fira", "Banyuwangi", "085231796284")
# putri = Pelanggan("putri", "Banyuwangi", "085231796284")
# print(fira.noID)
# fira.showinfo()
# print(fira.nomer_id)
# print(putri.nomer_id)

# class Saldo(Pelanggan):
#     def __init__(self, nama, alamat, noHP):
#         super().__init__(nama, alamat, noHP)
#         self.saldo = 0

    # def inputSaldo(self, inputsaldo):
    #     self.saldo = inputsaldo

class Karyawan(Pelanggan):
    def __init__(self, noID, nama, alamat, noHP, noKtp, tahunLahir):
        super().__init__(noID, nama, alamat, noHP, tahunLahir)
        self.noKtp = noKtp

    def showinfo(self):
        print("Nama\t\t: {}\nNomer KTP\t: {}\nAlamat\t\t: {}\nNomer HP\t: {}".format(self.nama, self.noKtp, self.alamat, self.noHP))

    def umur(self):
        usiaSaatIni = 2020 - self.tahunLahir
        return usiaSaatIni

class SaldoPelanggan:
    def __init__(self, nomorid, nama, alamat, noHP):
        self.nomorid = nomorid
        self.nama = nama
        self.alamat = alamat
        self.noHP = noHP
        self.__jumlahSaldo = self.jumlahSaldo()
        self.jumlahHutang = self.apdetHutang()

    def jumlahSaldo(self):
        conn = sqlite3.connect('project.sqlite')
        cursor = conn.cursor()
        hasil = cursor.execute("select jumlahUang from SaldoPelanggan where noID = ?", (str(self.nomorid),)).fetchone()[0]
        conn.close()
        return hasil

    


    def showSaldo(self):
        print(self.__jumlahSaldo)
    

    def inputSaldo(self, inputsaldo):
        self.saldo = inputsaldo


    # def __init__(self, jumlahSaldo):
    #     self.__jumlahSaldo = jumlahSaldo
    #     self.saldoHutang = 0

    # waktu transaksi pada masing-masing method untuk mengetahui kapan transaksi saat itu dilakukan, pakai datetime database auto sabi
    def saldoTabungan(self):
        uangMasuk = int(input("Masukan jumlah uang yang ingin Anda tabung: "))
        jumlahSaldoTabungan = self.__jumlahSaldo + uangMasuk
        self.__jumlahSaldo = jumlahSaldoTabungan
        conn = sqlite3.connect('project.sqlite')
        cursor = conn.cursor()
        cursor.execute("update SaldoPelanggan set jumlahUang = ? where noID = ? ", (jumlahSaldoTabungan, self.nomorid,))
        conn.commit()
        conn.close()
        # return self.__jumlahSaldo

    def saldoTarik(self, waktuTransaksi):
        uangTarik = int(input("masukan jumlah uang yang ingin Anda ambil"))
        if self.__jumlahSaldo < uangTarik:
            print("Maaf saldo anda tidak mencukupi")
        else:
            jumlahSaldoTarik = self.__jumlahSaldo - uangTarik
            self.__jumlahSaldo = jumlahSaldoTarik
        return self.__jumlahSaldo

    def utang(self, waktuTransaksi):
        uangPinjam = int(input("Masukan jumlah uang yang ingin Anda pinjam"))
        bunga = self.bunga() * uangPinjam
        piutang = uangPinjam + bunga
        self.jumlahHutang = piutang

    def bunga(self):
        hari = int(input("masukan total hari terhitung hari ini dan hari dimana Anda mengembalikan"))
        bulan = hari % 30
        bungaPinjam = bulan // 12 * 5 / 100
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
            cursor.execute("update SaldoPelanggan set jumlahHutang = 0 ,jumlahUang = ? where noID = ? ", (self.__jumlahSaldo, self.nomorid,))
            conn.commit()
            conn.close()
        # return self.__jumlahSaldo

    def apdetHutang(self):
        conn = sqlite3.connect('project.sqlite')
        cursor = conn.cursor()
        hasil = cursor.execute("select jumlahHutang from SaldoPelanggan where noID = ?", (str(self.nomorid),)).fetchone()[0]
        conn.close()
        return hasil

class Menu:
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
                conn = sqlite3.connect('project.sqlite')
                cursor = conn.cursor()
                query = "INSERT INTO Pelanggan(Nama,Alamat,'Nomor Hp') VALUES (?,?,?)"
                cursor.execute(query, (nama, alamat, nomorhp))
                conn.commit()
                conn.close()
                print("Selamat Anda berhasil mendaftar")
            elif pilihan == 2:
                conn = sqlite3.connect('project.sqlite')
                cursor = conn.cursor()
                nama = input("masukkan nama ")
                hasil = cursor.execute("select * from Pelanggan where Nama = ?", (nama,)).fetchone()
                conn.close()
                print(hasil)
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
                pelanggan.bayarHutang()
            elif pilih == "5":
                pelanggan.saldoTarik()
            elif pilih == "6":
                pelanggan.showSaldo()





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
