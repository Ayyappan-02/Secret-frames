import cv2
import random

from steg.utils import _split_frames, _lsb_encode, _embed_frame, _wrap_up, _lsb_decode

def steg_photo(path1, path2):
	steg_key = "frames="
	path3 = ""
	vidObj = cv2.VideoCapture(path1)
	steg_img = cv2.imread(path2)
	frame_array, size = _split_frames(vidObj)
	steg_img = cv2.resize(steg_img, (size[0]//2, size[1]//2))
	frame_array, frames = _embed_frame(frame_array, steg_img, [])
	for frame in frames:
		steg_key += str(frame) + ","
	#encrypt before using the string directly
	print(steg_key)
	frame_array[0] = _lsb_encode(frame_array[0], steg_key)
	print(_lsb_decode(frame_array[0]))
	path3 = _wrap_up(path1, frame_array, size)
	tmpvid = cv2.VideoCapture(path3)
	frame_array, size = _split_frames(tmpvid)
	print("now")
	print(_lsb_decode(frame_array[0]))
	return path3

def steg_video(path1, path2):
	steg_key = "frames"
	path3 = ""
	vidObj1 = cv2.VideoCapture(path1)
	vidObj2 = cv2.VideoCapture(path2)
	frame_array1, size1 = _split_frames(vidObj1)
	frame_array2, size2 = _split_frames(vidObj2)
	frames = []
	for i in range(len(frame_array2)):
		frame_array2[i] = cv2.resize(frame_array2[i], ( size1[0]//2, size1[1]//2) )
		frame_array1, frames = _embed_frame(frame_array1, frame_array2[i], frames)
	for frame in frames:
		steg_key += str(frame) + ","
	#encrypt before using the string directly
	frame_array1[0] = _lsb_encode(frame_array1[0], steg_key)
	path3 = _wrap_up(path1, frame_array1, size1) 
	return path3

steg_photo("/home/osboxes/secret-frames/video.mp4", "/home/osboxes/secret-frames/Lena.jpg")
