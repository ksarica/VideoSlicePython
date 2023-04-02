import sys
import numpy as np
import cv2 as cv
import os

#######################################################################################################################################################

###################################################  ALL FUNCTIONS ###################################################  

#######################################################################################################################################################

def GetVideoCapture(path):
    capture = cv.VideoCapture(path)

    if not capture.isOpened():
        print("Cannot open file ! Exiting ...")
        exit()
    return capture

def SetVideoSettings(capture):
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    frame_rate = int(capture.get(5))
    frame_count_of_video = int(capture.get(7))
    return frame_width, frame_height, frame_rate, frame_count_of_video

def SetSlicedVideoSettings(outputName, frame_width, frame_height, frame_rate):
    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc('D','I','V','X')
    slicedOutput = cv.VideoWriter(outputName,fourcc, frame_rate,(frame_width,frame_height))
    return slicedOutput

def CheckFrameRange(startFrame, endFrame, frame_count_of_video):
    print(f"Frame count of the video: {frame_count_of_video}")
    print(f"Start and end frames are defined as {startFrame}:{endFrame}")
    if startFrame not in range(0,frame_count_of_video) or endFrame not in range(0,frame_count_of_video) or startFrame >= endFrame:
        print('Starting or Ending Frames is not valid ! Exiting...')
        print(f'Frames must be in range of 0 and {frame_count_of_video - 1}')
        exit()

def WriteSlicedFrames(startFrame, endFrame, capturedVideo, frame_rate, slicedOutput):
    index = 0
    while capturedVideo.isOpened():
        returned, frame = capturedVideo.read()
        if not returned:
                print("Can't receive frame (stream end?). Exiting ...")
                break

        if index in range(startFrame,endFrame + 1):
            print(f"Frame no: {index} now in range ! Video is being written ...")
            slicedOutput.write(frame)

            # uncomment to see video on opencv window
            # cv.imshow('frame', frame) 
            # if cv.waitKey(frame_rate) == ord('q'):
                # break
        else:
            print(f"Frame no: {index} not in range ! Passing...")

        if index >= endFrame:
            print('Finished the process. Releasing...') 
            break

        index = index + 1

def ReleaseWorkingProcesses(capturedVideo, slicedOutput):
    capturedVideo.release()
    slicedOutput.release()
    cv.destroyAllWindows()

def SliceVideo(path, outputName, startFrame, endFrame):
    capturedVideo = GetVideoCapture(path)
    frame_width, frame_height, frame_rate, frame_count_of_video = SetVideoSettings(capturedVideo)
    slicedOutput = SetSlicedVideoSettings(outputName, frame_width, frame_height, frame_rate)
    CheckFrameRange(startFrame, endFrame, frame_count_of_video)
    WriteSlicedFrames(startFrame, endFrame, capturedVideo, frame_rate, slicedOutput) 
    ReleaseWorkingProcesses(capturedVideo, slicedOutput)

def ChangeFileExtension(outputName, currentExtension, desiredExtension, outputNameFinal):
    if not os.path.exists(outputNameFinal):
        os.rename(outputName,outputNameFinal)
        print(f"File extension succesfully changed from {currentExtension} to {desiredExtension}")
    else:
        print(f"File named {outputNameFinal} is already exists !")

#######################################################################################################################################################

###################################################  MAIN ###################################################  

#######################################################################################################################################################

videoPath = sys.argv[1]
outputName = sys.argv[2]
startFrame = int(sys.argv[4])
endFrame = int(sys.argv[5])
SliceVideo(videoPath,outputName,startFrame,endFrame)

# OpenCV does not support .mp4 read
currentExtension = '.' + videoPath.split('.')[-1]
desiredExtension = sys.argv[3]
outputNameFinal = outputName.split('.')[0] + desiredExtension
ChangeFileExtension(outputName, currentExtension, desiredExtension, outputNameFinal)