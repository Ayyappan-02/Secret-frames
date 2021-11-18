import cv2

from steg.utils import _split_frames, _lsb_decode

def steg_photo(path):
	steg_key = ""
	vidObj = cv2.VideoCapture(path)
	frame_array, size = _split_frames(vidObj)
	steg_key = _lsb_decode(frame_array[0])
	print(steg_key)
	return path

def steg_video(path):
	pass

steg_photo("/home/osboxes/secret-frames/tmpvideo.mp4")
