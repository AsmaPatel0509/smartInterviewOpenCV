import boto3
import cv2
from scipy.misc import imresize
import time
BUCKET_NAME = 'aws-rekognition-bucket' # replace with your bucket name
KEY = 'asmaa1.JPEG' # replace with your object key

s3 = boto3.resource('s3')
img2 = ""
frame = ""
img_name = ""
compare = False
rec = 911108
# if __name__ == "__main__":
#     main()

def main():
    print("Main")
    #s3ImageDownload()
    print("Image downloaded from S3")

    cap = cv2.VideoCapture(0)
    print("capturing")
    startTime = time.time()
    print("start time: ", startTime)
    while(True):
        #time.sleep(5)
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow('frame', frame)
        img_counter = 0
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # Esc pressed
            print("Quitting...")
            break
        elif k % 256 == 32:
            #Space pressed, takes snapshot
            img_name = "frame{}.png".format(rec)
            #Save snapshot
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
            compare = recognize("asmaa1.JPEG", 'frame0.png')
            print("Compare value boolean: ", compare)
            # recognize(s3image, "frame0.png")
            if (compare == True):
                print("User verified, continue")
                break
            else:
                print("User not verified")
        # else:
        #     img_name = "frame{}.png".format(img_counter)
        #     cv2.imwrite(img_name, frame)
        #     print("{} written!".format(img_name))
        #     img_counter += 1
        #         #time.sleep(5)

    expressions()
    cap.release()
    cv2.destroyAllWindows()

def s3ImageDownload():
    s3.meta.client.download_file('aws-rekognition-bucket', 'asmaa1.JPEG', 'asmaa1.JPEG')
    print("S3")
    #return "asmaa1.JPEG"

def recognize(SourceFile, TargetFile):
    returnValue = False
    print("Recognize")
    img = cv2.imread('asmaa1.JPEG', 1)
    img = imresize(img, (800, 450))
    #cv2.imshow('asma4', img)
    #print("Show")

    client = boto3.client('rekognition')
    # with open("asma1.png", "rb") as image:

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
        if(faceMatch['Face']['Confidence'] > 70):
            returnValue = True
        else:
            returnValue = False
    print("return value: ", returnValue)
    cv2.destroyAllWindows()
    return returnValue

def expressions():
    print("Expressions")
    photo = 'asmaa1.JPEG'
    client=boto3.client('rekognition')

    response = client.detect_faces(Image={'S3Object':{'Bucket':BUCKET_NAME,'Name':photo}},Attributes=["ALL"])
    print('Detected faces for ' + photo)
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
                + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        print('Here are the emotions:')
        print(str(faceDetail['Emotions']))
        #print(json.dumps(faceDetail, indent=4, sort_keys=True))

main()