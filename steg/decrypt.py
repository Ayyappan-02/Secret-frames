import cv2

from steg.utils import _split_frames, _extract_frame
from stegano import lsb
import skvideo.io

def steg_photo(path):
	steg_key = ""
	vidObj = cv2.VideoCapture(path)
	frame_array, size = _split_frames(vidObj)
	n = len(frame_array)
	tmp_path = path[:path.rindex("/")+1] + "tmp.png"
	cv2.imwrite(tmp_path, frame_array[n//2])
	steg_key = lsb.reveal(tmp_path)
	steg_key = steg_key[7:-1]
	steg_key = steg_key.split(",")
	final = path[:path.rindex("/")+1] + "data.png"
	for i in range(len(steg_key)):
		steg_key[i] = int(steg_key[i])
	for i in range(1, len(steg_key), 3):
		r_frame = steg_key[i]
		g_frame = steg_key[i+1]
		b_frame = steg_key[i+2]
		img = _extract_frame(frame_array, r_frame, g_frame, b_frame)
		cv2.imwrite(final,img)
	return final

def steg_video(path):
	steg_key = ""
	vidObj = cv2.VideoCapture(path)
	frame_array, size = _split_frames(vidObj)
	n = len(frame_array)
	tmp_path = path[:path.rindex("/")+1] + "tmp.png"
	cv2.imwrite(tmp_path, frame_array[n//2])
	steg_key = lsb.reveal(tmp_path)
	steg_key = steg_key[7:-1]
	steg_key = steg_key.split(",")
	final = path[:path.rindex("/")+1] + "data.png"
	frame_array1 = []
	for i in range(len(steg_key)):
		steg_key[i] = int(steg_key[i])
	#print(steg_key)
	for i in range(1, len(steg_key), 3):
		r_frame = steg_key[i]
		#print(r_frame)
		g_frame = steg_key[i+1]
		b_frame = steg_key[i+2]
		img = _extract_frame(frame_array, r_frame, g_frame, b_frame)
		frame_array1.append(img)
	outputfile = path[:path.rindex("/")+1] + "data.mp4"
	writer = skvideo.io.FFmpegWriter(outputfile, outputdict={
	  '-vcodec': 'libx264rgb',  #use the h.264 codec
	  '-crf': '0',           #set the constant rate factor to 0, which is lossless
	  '-preset':'veryslow'   #the slower the better compression, in princple, try 
	}) 
	for i in range(len(frame_array1)):
	    writer.writeFrame(frame_array1[i][:,:,::-1])
	writer.close()
	print(outputfile)
	return outputfile
