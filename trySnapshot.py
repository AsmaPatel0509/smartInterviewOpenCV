import cv2
import time
import boto3
import pymysql
from flask import Flask,request

app = Flask(__name__)

@app.route("/")
def fn1():
    client = boto3.client('rekognition')
    bucket = 'aws-bucket-name'
    connection = pymysql.connect(
            host = 'mydb.chsifs6arhem.us-east-1.rds.amazonaws.com',
            user = 'username',
            password = 'password',
            db = 'dbname'
        )
    cursor1 = connection.cursor()

    folder = input("Enter email-id:")
    session = boto3.session.Session(region_name='region-name')
    s3 = boto3.client('s3')
    S3 = session.client('s3')
    bucket = 'aws-bucket-name'

    client = boto3.client('rekognition')
    cap = cv2.VideoCapture(0)
    print("capturing")
    img_counter = 0

    userId = request.args.get("userId")
    print("userId=",userId)
    while(True):
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            if k % 256 == 27:
                # Esc pressed
                print("Quitting...")
                break

            img_name = "frame{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))

            #Upload to S3
            s3.upload_file("C:/path/to/image/directory/" +img_name, bucket, folder +"/" +img_name, ExtraArgs={'ACL':'public-read'})
            print("Snapshot uploaded to S3.")

            #NEEDS FIX!!!
            #Link generation
            link = "https://" + bucket + ".s3.amazonaws.com/" + folder + "/" + img_name
            print("Link: ", link)

            time.sleep(10)

            #Expression Analysis
            print("Analysing expressions")

            response = client.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': folder +'/frame0.png'}}, Attributes=["ALL"])
            print('Detected faces for ' + img_name)
            for faceDetail in response['FaceDetails']:
                # print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
                #       + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
                print('Here are the emotions:')
                exp = faceDetail['Emotions']
                print(exp)
                for i in exp:
                    cursor1.execute(
                        "INSERT into userExpression(id, expression, confidence, imageName, imagePath) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                            userId, str(i['Type']), str(i['Confidence']), img_name, link)
                    )
                    print("Inserted in RDS")
                    connection.commit()

            img_counter += 1

    cap.release()
    cv2.destroyAllWindows()

app.run()
