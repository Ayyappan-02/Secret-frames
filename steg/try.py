import cv2

from utils import _split_frames, _lsb_encode, _lsb_decode

path = "/home/osboxes/secret-frames/video.mp4"

vidObj = cv2.VideoCapture(path)

frame_array, size = _split_frames(vidObj)
steg_key ="as"
frame_array[0] = _lsb_encode(frame_array[0], steg_key)
print(_lsb_decode(frame_array[0]))

path = "/home/osboxes/secret-frames/tryvideo.mp4"
fps = 25
out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
for i in range(len(frame_array)):
	out.write(frame_array[i])
out.release()

vidObj = cv2.VideoCapture(path)
frame_array1, size1 = _split_frames(vidObj)
print(_lsb_decode(frame_array1[0]))
