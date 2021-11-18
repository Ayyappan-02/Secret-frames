import cv2, pywt
import random
import numpy as np
import moviepy.editor as mp
import skvideo.io
from subprocess import call, STDOUT
import os


def _split_frames(vidObj):
	count = 0
	frame_array = []
	sucess = 1
	
	while sucess:
		sucess, img = vidObj.read()
		if img is None:
			break
		if count == 0:
			height, width, layers = img.shape
			size = (width, height)
		frame_array.append(img)
		count += 1
	return frame_array, size

def _frame_numbers(frame_array, frames):
	while True:
		frame = random.randint(1, len(frame_array)-1)
		if frame not in frames:
			return frame

def _embed_data(img, steg_channel):
	(B, G, R) = cv2.split(img)
	coeffs = pywt.dwt2(R, 'haar', mode='periodization')
	LL, (LH, HL, HH) = coeffs
	for i in range(len(HH)):
		for j in range(len(HH[i])):
			HH[i][j] = steg_channel[i][j].astype(np.float)
	coeffs = LL, (LH, HL ,HH)
	new_r = pywt.idwt2(coeffs, 'haar', mode='periodization')
	new_r = np.uint8(new_r)
	merged = cv2.merge([B, G, new_r])
	return merged

def _embed_frame(frame_array, steg_img, frames):
	r_frame = _frame_numbers(frame_array, frames)
	frames.append(r_frame)
	g_frame = _frame_numbers(frame_array, frames)
	frames.append(g_frame)
	b_frame = _frame_numbers(frame_array, frames)
	frames.append(b_frame)
	(B, G, R) = cv2.split(steg_img)
	frame_array[r_frame] = _embed_data(frame_array[r_frame], R)
	frame_array[g_frame] = _embed_data(frame_array[g_frame], G)
	frame_array[b_frame] = _embed_data(frame_array[b_frame], B)
	return frame_array, frames

def _wrap_up(path, frame_array, size):
	tmp = path[:path.rindex("/")+1] + "tmp" + path[path.rindex("/")+1:]
	outputfile = tmp   #our output filename
	writer = skvideo.io.FFmpegWriter(outputfile, outputdict={
	  '-vcodec': 'libx264rgb',  #use the h.264 codec
	  '-crf': '0',           #set the constant rate factor to 0, which is lossless
	  '-preset':'veryslow'   #the slower the better compression, in princple, try 
	}) 
	for i in range(len(frame_array)):
	    writer.writeFrame(frame_array[i][:,:,::-1])
	writer.close()
	myclip = mp.VideoFileClip(path)
	audio_tmp = path[:path.rindex("/")+1] + "audio_tmp.mp3"
	myclip.audio.write_audiofile(audio_tmp)
	cover_path = path[:path.rindex("/")+1] + "cover.mp4"
	call(["ffmpeg", "-i", tmp, "-i", audio_tmp, "-codec", "copy", cover_path, "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
	return cover_path

def _extract_channel(img):
	(B,G,R) = cv2.split(img)
	coeff = pywt.dwt2(R, 'haar', mode='periodization')
	LL, (LH, HL, HH) = coeff
	channel = np.uint8(HH)
	return channel

def _extract_frame(frame_array, r, g, b):
	r_steg = _extract_channel(frame_array[r])
	g_steg = _extract_channel(frame_array[g])
	b_steg = _extract_channel(frame_array[b])
	steg = cv2.merge([b_steg, g_steg, r_steg])
	return steg 
