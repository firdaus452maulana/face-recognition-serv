import faceOption

selectOption = 0
selectOption = int(input("Pilih Opsi : "))

if selectOption == 1:
    input_name = input("Masukkan Nama Yang Didaftarkan : ")
    faceOption.register(input_name)
elif selectOption == 2:
    faceOption.login()
