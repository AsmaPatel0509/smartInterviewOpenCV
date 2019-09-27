# Candidate must enter email id equivalent to userId for facial recognition.

import boto3
import cv2

BUCKET_NAME = 'aws-bucket-name'

s3 = boto3.resource('s3')
S3 = boto3.client('s3')
folder = input("Enter email id:")
filename = input("Enter uploaded photo filename:")

s3.meta.client.download_file(BUCKET_NAME, folder +"/"+ filename, filename)
print("Image downloaded from S3")

cap = cv2.VideoCapture(0)

returnValue = False

while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # Esc pressed
            print("Quitting...")
            break
        elif k % 256 == 32:
            #Space pressed, takes snapshot
            img_name = "image{}.png".format("compare")
            #Save snapshot
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))

            #Recognition
            print("Recognizing")
            img = cv2.imread(filename, 1)
            # img = imresize(img, (800, 450))
            # cv2.imshow('asma4', img)
            # print("Show")

            client = boto3.client('rekognition')
            # with open("imgname.png", "rb") as image:
            SourceFile = filename
            TargetFile = img_name

            imageSource = open(SourceFile, 'rb')
            imageTarget = open(TargetFile, 'rb')

            response = client.compare_faces(SimilarityThreshold=70,
                                            SourceImage={'Bytes': imageSource.read()},
                                            TargetImage={'Bytes': imageTarget.read()})

            for faceMatch in response['FaceMatches']:

                position = faceMatch['Face']["BoundingBox"]
                confidence = str(faceMatch['Face']['Confidence'])
                print('Verified!')
                imageSource.close()
                imageTarget.close()
                if (faceMatch['Face']['Confidence'] > 70):
                    returnValue = True
                else:
                    returnValue = False
            print("return value: ")
            cv2.destroyAllWindows()

            print("Compare value boolean: ", returnValue)
            # recognize(s3image, "frame0.png")
            if (returnValue == True):
                print("User verified, continue")
                S3.upload_file("C:/path/to/image/imagename.jpg", BUCKET_NAME, folder +"/imagecompare.png")
                print("Uploaded to S3")
                break
            else:
                print("User not verified")
