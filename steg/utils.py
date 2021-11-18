import cv2, pywt
import random
import numpy as np
import moviepy.editor as mp


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
	fps = 25
	tmp = path[:path.rindex("/")+1] + "tmp" + path[path.rindex("/")+1:]
	print(tmp)
	out = cv2.VideoWriter(tmp, cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
	for i in range(len(frame_array)):
		out.write(frame_array[i])
	out.release()
	"""
	myclip = mp.VideoFileClip(path)
	audio_tmp = path[:path.rindex(".")] + "audio.mp3"
	myclip.audio.write_audiofile(audio_tmp)
	clip = mp.VideoFileClip(tmp)
	audioClip = mp.AudioFileClip(audio_tmp)
	cover_video = clip.set_audio(audioClip)
	cover_path = path[:path.rindex("/")+1] + "cover_" + path[path.rindex("/")+1:]
	cover_video.write_videofile(cover_path)
	"""
	return tmp
