'Gx 包下的图片处理'

def read_img(filename):
	import cv2
	import np as np
	global cv2
	global np
	'使用 imdecode方法能够访问到包含中文字符的图片'
	arr = cv2.imdecode(np.fromfile(filename, dtype= np.uint8), -1)
	return np.array(arr)
	pass

def _main():
	arr = read_img("./image.jpg")
	print(arr.shape)
	pass
if __name__ == '__main__':
	_main()

