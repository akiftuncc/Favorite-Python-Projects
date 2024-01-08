import EncodeGenerator
import AddDataToDatabase
import main
import asyncio

"""
---- BURAYI OKU
Bunu sana örnek olması için oluşturdum.
fonksiyonları bu şekilde çekeceksin ve buton-label'lara gerektiği şekilde yerleştireceksin.
inputa girdiğin değerler  aslında oluşturduğun ekranları temsil ediyor: 
input = 1 data oluşturma ekranına denk geliyor. ekrandaki işlevleri de sen yorum satırlarından anlarsın
input = 2 encode butonuna denk geliyor
input = 3 kamera açma butonuna denk geliyor
Burayı iyice inceledikten sonra kodu entegre etme kısmını rahatça yaparsın. yukarıdaki importları ekleyeceksin fonksiyonları çağırmadan önce unutma.
Son olarak ilk 4 fonksiyona senin ihtiyacın yok sende label dan gelen değerleri student_name,student_number,student_major,student_year değerlerine yazdıracaksın.
"""

###### KİŞİ EKLEME
def name_text_label():
    return AddDataToDatabase.create_name()

def major_text_label():
    return AddDataToDatabase.create_major()

def year_text_label():
    return AddDataToDatabase.create_year()

def student_number_text_label():
    return AddDataToDatabase.create_student_number()

def take_pic_button_click(student_number):
    AddDataToDatabase.take_pic(student_number)

def face_recorder_button_click(student_number):
    AddDataToDatabase.face_recorder(student_number)

def data_creator_button_click(student_name,student_number,student_major,student_year):
    AddDataToDatabase.data_creator(student_name,student_number,student_major,student_year)
########
    
##### ENCODE
def encode_button_click():
    EncodeGenerator.encode_event()
######
    
##### Run Cam
def run_camera():
    asyncio.run(main.main())
######
    
#######################

input_value = int(input("\nKişi ekleme ekranı için 1'e, encode için 2'ye, camera açmak için 3'e bas"))

###### KİŞİ EKLEME KISMI
if input_value == 1:
    student_name = name_text_label() #label'a name girilecek
    student_major = major_text_label() #label'a major girilecek
    student_year = year_text_label() #l3abel'a year girilecek
    student_number = student_number_text_label() #label'a number girilecek
    print(student_name,student_major,student_year,student_number)
    take_pic_button_click(student_number) #Button'a basılınca bu fonksiyon çağırılacak
    face_recorder_button_click(student_number) #button'a basılınca bu fonksiyon çalışacak
    data_creator_button_click(student_name, student_number, student_major, student_year ) 
    #button'a basılınca yukarıdaki fonksiyonun parametrelerine label'da yazılanlar gelecek ve daha sonra fonksiyon çalışacak
######

###### ENCODE
if input_value == 2:
    encode_button_click() #button'a basınca çalışacak
######

###### OPEN CAMERA
if input_value == 3:
    run_camera() #button'a basınca çalışacak
######

