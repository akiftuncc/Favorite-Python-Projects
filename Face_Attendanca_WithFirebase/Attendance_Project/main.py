import asyncio
import threading
import cv2
import cvzone
import face_recognition
import mediapipe as mp
import numpy as np
import pickle
import os
from datetime import datetime
import json
from firebase_admin import db, credentials, storage, initialize_app

detect_correctness = 2
detection_rate = 0.9
scale_rate = 0.8
detect_division = 5
comparision_list = []  # len=> kişi sayısı, 6,6  468,468
mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection()  # face success rate .97

mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
async def run_detection_coroutine(img):
    diff_calculated_values = []
    name_arr = []
    first_solution_array = [[],[]] #x,y values
    second_solution_array = [[],[],[]] #x,y,z values
    
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
                

                if width > 0.42*scale_rate and width < 0.50/scale_rate and height > 0.56*scale_rate and height <0.66/scale_rate and x_min > 0.30*scale_rate and x_min < 0.36/scale_rate and y_min > 0.30*scale_rate and y_min < 0.36/scale_rate:
                
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
                                temp_z2_array.append(round(lm.z/(height*width*height*width),detect_correctness))
                            # Z INDEXI BAZEN POZITIF BAZEN NEGATIF (çok inceleme)

                    first_solution_array[0].append(temp_x1_array)
                    first_solution_array[1].append(temp_y1_array) # oluşan liste => [ [ [1. xler],[2. xler] ...],[ [1. yler, 2. yler] ] ]

                    second_solution_array[0].append(temp_x2_array)
                    second_solution_array[1].append(temp_y2_array)
                    second_solution_array[2].append(temp_z2_array) # oluşan liste => [ [ [1. xler], [2. xler] ...],[ [1.yler], [2. yler] ],[ [1. zler], [2. zler] ] ]
                
                    first_solution_x_differences = []
                    first_solution_y_differences = []
                    second_solution_x_differences = []
                    second_solution_y_differences = []
                    second_solution_z_differences = [] 

                    diff_list_appender(first_solution_array[0],first_solution_x_differences)
                    diff_list_appender(first_solution_array[1],first_solution_y_differences)
                    diff_list_appender(second_solution_array[0],second_solution_x_differences)
                    diff_list_appender(second_solution_array[1],second_solution_y_differences)
                    diff_list_appender(second_solution_array[2],second_solution_z_differences)

                    first_solution_x_transposed = transpose(first_solution_x_differences)   # len[[[]]]=6   len[[]]=6 len[]=1
                    first_solution_y_transposed = transpose(first_solution_y_differences)
                    second_solution_x_transposed = transpose(second_solution_x_differences) # len[[[]]]=468 len[[]]=468  len[]=1
                    second_solution_y_transposed = transpose(second_solution_y_differences)
                    second_solution_z_transposed = transpose(second_solution_z_differences)

                    dimension_2_diffs = []
                    dimension_3_diffs = []
                    for index,i in enumerate(first_solution_x_transposed):
                       
                        for index1,i1 in enumerate(i):
                            x = i1
                            y = first_solution_y_transposed[index][index1]
                            dimension_2_diff = (abs(x**2) + abs(y**2))**0.5
                            dimension_2_diffs.append(dimension_2_diff)

                    for index,i in enumerate(second_solution_x_transposed):
                        for index1,i1 in enumerate(i):
                            x = i1
                            y = second_solution_y_transposed[index][index1]
                            z = second_solution_z_transposed[index][index1]
                            dimension_3_diff = (abs(x**2)+abs(y**2)+abs(z**2))**0.5
                            dimension_3_diffs.append(dimension_3_diff)

                    solutions_list = [dimension_2_diffs,dimension_3_diffs]
                    
                    diff_calculated_values = []
                    for i in range(len(comparision_list)): #len = person num
                        diff_values = [0,0] #dim1,dim2
                        for j in range(len(comparision_list[i])-1): #len = 4+1 (+1 name) -1 ile 4 oldu // 2
                            count_value = 0
                            for k in range(len(comparision_list[i][j])): #len = 6,468
                                for index,l in enumerate(solutions_list[j][k]):
                                    solutions_value = l
                                    comparision_value = comparision_list[i][j][k]
                                    count_value+= round(abs(comparision_value-solutions_value),detect_correctness)
                                    
                            if j == 0 or j == 1:
                                # count_value*=10
                                pass
                            diff_values[j] = round(count_value,detect_correctness)
                        
                        diff_calculated_values.append(sum(diff_values))    
                    
                    min_index = diff_calculated_values.index(min(diff_calculated_values))
                    for i in comparision_list:
                        name_arr.append(i[2][0][:-1])
                    name = comparision_list[min_index][2][0][:-1]
        mean_calculated = 0
        if len(diff_calculated_values) != 0:
            mean_calculated = (sum(diff_calculated_values) / len(diff_calculated_values)) +1
        index_values = []
        
        return [name_arr,diff_calculated_values,mean_calculated]
    return "-"
def transpose(array):
    return np.array(array).T

def run_detection_async(img):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(run_detection_coroutine(img))
    loop.close()
    return result

def process_image_async(img):
    result = run_detection_async(img)
    print(result)

def diff_list_appender(main_list, parent_list):
    def difference_with_other_dotes(array):
        difference_list = []
        for i in array:
            difference_list_each = []
            for j in array:
                difference_list_each.append(round(abs(i - j), detect_correctness))
            difference_list.append(difference_list_each)
        return difference_list

    for i in main_list:
        parent_list.append(difference_with_other_dotes(i))

async def create_array_from_txt_coroutine():
    with open("dosya.txt", "r") as dosya:
        for i in dosya:
            if i[0:4] == "Name":
                list_index = 0
                txt_list = [[], [], [i[6:]]]  # name, x1list y1list ...
            j = i[0:-1]
            if j == "-":
                list_index += 1
            else:
                try:
                    converted_list = json.loads(i)
                    txt_list[list_index].append(converted_list)
                except:
                    pass

            if i[0:3] == "end":
                comparision_list.append(txt_list)
modeType = 0
async def main():
    # Firebase'i başlat
    cred = credentials.Certificate("Key.json")
    initialize_app(cred, {
        'databaseURL': "https://faceattendacerealtime-66ada-default-rtdb.firebaseio.com/",
        'storageBucket': "faceattendacerealtime-66ada.appspot.com"
    })

    bucket = storage.bucket()

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    

    imgBackground = cv2.imread('FaceFiles/background.png')

    # Importing the mode images into a list
    folderModePath = 'FaceFiles/ModeParts'
    modePathList = os.listdir(folderModePath)
    modePathList.remove(".DS_Store")
    imgModeList = []
    for path in modePathList:
        imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

    
    # Load the encoding file
    print("Loading Encode File ...")
    file = open('EncodeFile.p', 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, studentIds = encodeListKnownWithIds
    print("Encode File Loaded")

    modeType = 0
    counter = 0
    id = -1
    imgStudent = []

    
    await create_array_from_txt_coroutine()

    already_signed_list = []
    while True:
        success, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)

        if imgS is None or imgS.size == 0:
            print("Error: Resized image is empty.")
            break

        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        imgBackground[162:162 + 480, 55:55 + 640] = img
        print(len(imgModeList))
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if faceCurFrame:
            name_detected = await run_detection_coroutine(img)
            try:
                mean_detected = name_detected[2]
                name_list = []
                for index,i in enumerate(name_detected[1]):
                    if mean_detected > i:
                        name_list.append(name_detected[0][index])
                print(name_list)

                for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex]:
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                        imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                        id = studentIds[matchIndex]
                        if not(id in already_signed_list):
                            if id in name_list:
                                print("------ID-------:", id, name_detected)
                                already_signed_list.append(id)
                                if counter == 0:
                                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                                    cv2.imshow("Face Attendance", imgBackground)
                                    cv2.waitKey(1)
                                    counter = 1
                                    modeType = 1
            except:
                print("2 People")
            if counter != 0:

                if counter == 1:
                    studentInfo = db.reference(f'Students/{id}').get()
                    blob = bucket.get_blob(f'Images/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)
                    if secondsElapsed > 30:
                        ref = db.reference(f'Students/{id}')
                        studentInfo['attendance_count'] += 1
                        ref.child('attendance_count').set(studentInfo['attendance_count'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if modeType != 3:

                    if 10 < counter < 20:
                        modeType = 2

                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 10:
                        cv2.putText(imgBackground, str(studentInfo['attendance_count']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (245, 250, 240), 1)
                        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (245, 250, 240), 1)
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (245, 250, 240), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (95, 95, 95), 1)

                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (48, 50, 52), 1)

                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                    counter += 1

                    if counter >= 20:
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        else:
            modeType = 0
            counter = 0

        await run_detection_coroutine(img)

        cv2.imshow("Face Attendance", imgBackground)
        cv2.waitKey(1)

if __name__ == "__main__":
    asyncio.run(main())