import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image


def create_name():
    return input("name:")

def create_major():
    return input("major:")

def create_year():
    return int(input("starting year:"))

def create_student_number():
    return input("Student Number: ")

def take_pic(student_number):
    print(student_number)
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Webcam")
    def crop_image(img_path,frame):
        def crop_center(image, target_height, target_width):
            height, width, _ = image.shape

            start_y = (height - target_height) // 2
            end_y = start_y + target_height
            start_x = (width - target_width) // 2
            end_x = start_x + target_width

            cropped_image = image[start_y:end_y, start_x:end_x]

            return cropped_image

        # Crop the image to 216x216 and center it along the x-axis
        cropped_frame = crop_center(frame, 216, 216)

        # Save the cropped image
        output_path = img_path
        cv2.imwrite(output_path, cropped_frame)

    while True:
        ret,frame= cam.read()

        if not ret:
            print("Error")
            break

        frame = cv2.resize(frame, (384, 216))

        cv2.imshow("test",frame)

        k=cv2.waitKey(1)

        if k%256 == 27:
            print("App closing")
            break

        elif k%256 ==32:
            img_name = "images/"+student_number+".png"   
            crop_image(img_name,frame)
            break
    
    

    return student_number

def face_recorder(student_number):

    detect_correctness = 2 #ondalık kısım
    record_frames = 50
    detection_rate = 0.9 #between 0-1  (detection_score)
    scale_rate = 0.82 # between 0-1
    detect_division = 20  # detect_division daha sonra text dosyasına yazılacak ve facecheck bu yazılan değere göre detect_division değerini alacak

    def write_to_file(mean_list):
        for i in mean_list:
            dosya.write(str(i)+"\n")
        dosya.write("-\n")

    def transpose(array):
        return np.array(array).T

    def diff_list_appender(main_list,parent_list):
        def difference_with_other_dotes(array):
            difference_list = []
            for i in array:
                difference_list_each = []
                for j in array:
                    difference_list_each.append(round(abs(i-j),detect_correctness))
                difference_list.append(difference_list_each)
            return difference_list
        # for i in first_solution_array[0]:
        #   first_solution_x_differences.append(difference_with_other_dotes(j))
        for i in main_list:
            parent_list.append(difference_with_other_dotes(i))

    def mean_list_appender(transposed_list,mean_list):
        for i in range(len(transposed_list)):
            temp_arr = []
            for j in transposed_list[i]:
                mean = sum(j)/len(j)
                temp_arr.append(round(mean,detect_correctness))
            mean_list.append(temp_arr)

    cap = cv2.VideoCapture(0)
    mpDraw = mp.solutions.drawing_utils
    drawSpec=mpDraw.DrawingSpec(thickness=1,circle_radius=1)

    mpFaceDetection = mp.solutions.face_detection
    faceDetection = mpFaceDetection.FaceDetection() #face success rate .97

    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)

    first_solution_array = [[],[]] #x,y values
    second_solution_array = [[],[],[]] #x,y,z values
    frame_count = 0
    while frame_count<record_frames:
        
        succes,img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results_faceDetection=faceDetection.process(imgRGB)
        results_faceMesh = faceMesh.process(imgRGB)
        
        if results_faceDetection.detections and results_faceMesh.multi_face_landmarks and len(results_faceDetection.detections)==1:
            for id,detection in enumerate(results_faceDetection.detections):
                if detection.score[0]>detection_rate:
                    
                    y_min=detection.location_data.relative_bounding_box.ymin #y_min yüksekken düşük min veriyor
                    x_min=detection.location_data.relative_bounding_box.xmin
                    width = detection.location_data.relative_bounding_box.width
                    height = detection.location_data.relative_bounding_box.height

                    
                    if width > 0.29*scale_rate and width < 0.36/scale_rate and height > 0.53*scale_rate and height <0.61/scale_rate and x_min > 0.33*scale_rate and x_min < 0.39/scale_rate and y_min > 0.22*scale_rate and y_min < 0.28/scale_rate:
                        frame_count += 1
                    
                        # print(detection.location_data.relative_keypoints[0])
                        temp_x1_array = []
                        temp_y1_array = []
                        for i in detection.location_data.relative_keypoints:
                            temp_x1_array.append(round(abs((abs(i.x))/width),detect_correctness))
                            temp_y1_array.append(round(abs((abs(i.y))/height),detect_correctness))

                        #ih,iw,ic=img.shape
                        
                        for faceLms in results_faceMesh.multi_face_landmarks:
                            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_TESSELATION,drawSpec,drawSpec)

                            temp_x2_array = []
                            temp_y2_array = []
                            temp_z2_array = []
                            for id,lm in enumerate(faceLms.landmark):
                                if id % detect_division == 0:
                                    temp_x2_array.append(round(abs((lm.x)/width),detect_correctness))
                                    temp_y2_array.append(round(abs((lm.y)/height),detect_correctness))
                                    temp_z2_array.append(round(abs((lm.z)/(height*width*height*width)),detect_correctness))
                                # Z INDEXI BAZEN POZITIF BAZEN NEGATIF (çok inceleme)
                            print(round(sum(temp_z2_array),1),round(sum(temp_x2_array),1),round(sum(temp_y2_array),1))

                        first_solution_array[0].append(temp_x1_array)
                        first_solution_array[1].append(temp_y1_array) # oluşan liste => [ [ [1. xler],[2. xler] ...],[ [1. yler, 2. yler] ] ]

                        second_solution_array[0].append(temp_x2_array)
                        second_solution_array[1].append(temp_y2_array)
                        second_solution_array[2].append(temp_z2_array) # oluşan liste => [ [ [1. xler], [2. xler] ...],[ [1.yler], [2. yler] ],[ [1. zler], [2. zler] ] ]
                    else:
                        print("hatalı konumlanla")
                mpDraw.draw_detection(img,detection)
                detection_score_string = f"{detection.score}"
                cv2.putText(img,f"Face detection rate: {int(detection.score[0]*100)}%     Frames left: {record_frames-frame_count}",(20,70),cv2.FONT_HERSHEY_PLAIN,3,(0,40,40),2)
        cv2.imshow("Image",img)
        cv2.waitKey(1)

    first_solution_x_differences = []
    first_solution_y_differences = []
    second_solution_x_differences = []
    second_solution_y_differences = []
    second_solution_z_differences = [] # şimdilik boş kalacak

    diff_list_appender(first_solution_array[0],first_solution_x_differences)
    diff_list_appender(first_solution_array[1],first_solution_y_differences)
    diff_list_appender(second_solution_array[0],second_solution_x_differences)
    diff_list_appender(second_solution_array[1],second_solution_y_differences)
    diff_list_appender(second_solution_array[2],second_solution_z_differences)

    first_solution_x_transposed = transpose(first_solution_x_differences)
    first_solution_y_transposed = transpose(first_solution_y_differences)
    second_solution_x_transposed = transpose(second_solution_x_differences)
    second_solution_y_transposed = transpose(second_solution_y_differences)
    second_solution_z_transposed = transpose(second_solution_z_differences)

    first_solution_x_mean = [] # x1 in x1,x2,x3,x4,x5,x6  sonra x2'nin olaran devam ediyor ve bu farkların ortalamasını alıyor
    first_solution_y_mean = [] #
    second_solution_x_mean = []
    second_solution_y_mean = []
    second_solution_z_mean = []

    mean_list_appender(first_solution_x_transposed,first_solution_x_mean)
    mean_list_appender(first_solution_y_transposed,first_solution_y_mean)
    mean_list_appender(second_solution_x_transposed,second_solution_x_mean)
    mean_list_appender(second_solution_y_transposed,second_solution_y_mean)
    mean_list_appender(second_solution_z_transposed,second_solution_z_mean)

    ###### YENI ALGORITMA BASLANGIC

    dimension_2_diffs = []
    dimension_3_diffs = []
    for index,i in enumerate(first_solution_x_mean):
        print("x:", i)
        for index1,i1 in enumerate(i):
            x = i1
            y = first_solution_y_mean[index][index1]
            dimension_2_diff = (abs(x**2) + abs(y**2))**0.5
            dimension_2_diffs.append(round(dimension_2_diff,detect_correctness))

    for index,i in enumerate(second_solution_x_mean):
        for index1,i1 in enumerate(i):
            x = i1
            y = second_solution_y_mean[index][index1]
            z = second_solution_z_mean[index][index1]
            dimension_3_diff = (abs(x**2)+abs(y**2)+abs(z**2))**0.5
            dimension_3_diffs.append(round(dimension_3_diff,detect_correctness))
    ##### YENI ALGORITMA BITIS

    with open("dosya.txt", "a") as dosya:
        dosya.write(f"Name: {student_number}\n")
        write_to_file(dimension_2_diffs)
        write_to_file(dimension_3_diffs)
        dosya.write("end "+student_number+"\n")


def data_creator(data_name, student_number, data_major, data_year):
    
    cred = credentials.Certificate("Key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://faceattendacerealtime-66ada-default-rtdb.firebaseio.com/"
    })
    ref = db.reference('Students')

    data = {
        student_number:
            {
                "name": data_name,
                "major": data_major,
                "starting_year": data_year,
                "last_attendance_time": "2011-11-11 11:11:11",
                "attendance_count":0,
                "attendance_list":[],
            },
    }
    for key, value in data.items():
        ref.child(key).set(value)
    
    face_recorder(student_number)


# student_number = create_student_number()

# data_name = create_name()
# data_major=create_major()
# data_year = create_year()
# take_pic(student_number)
# face_recorder(student_number)
# data_creator(student_number)


