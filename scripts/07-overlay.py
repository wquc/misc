import os
from PIL import Image

### Need to tweak to find best location
coeffs = (0.3, 0.5) # position for foreground image wrt background
wcode  = 255        # RGB code (wcode, wcode, wcode) for white color

def overlay_images(name_fg, name_bg, coeffs):
	x_coeff, y_coeff = coeffs
	### 1. Read foreground image and delete white color for transparency
	img_fg = Image.open(name_fg).convert("RGBA")
	new_pixels = []
	for each_pixel in img_fg.getdata():
		if sum(each_pixel[:3]) == wcode*3:
			new_pixels.append((0, 0, 0, 0))
		else:
			new_pixels.append((each_pixel[0], each_pixel[1], each_pixel[2], 255))
	img_fg.putdata(new_pixels)
	### 2. Read back image and overlay with foreground image
	img_bg = Image.open(name_bg).convert("RGBA")
	position = (int((img_bg.width-img_fg.width)*x_coeff), int((img_bg.height-img_fg.height)*y_coeff))
	img_bg.paste(img_fg, position, mask=img_fg)
	return img_bg

for i in range(40):
	print i
	name1 = 'snapshots/demo.%05d.ppm'%i
	name2 = 'data/demo-frame%03d.png'%i
	overlay_images(name1, name2, coeffs).save('movies/demo-%03d.png'%(i+1), 'PNG')

print "Converting images to GIF movie.."
os.system("convert -delay 10 -loop 0 movies/demo-*.png movies/demo.gif")
print "Done."
