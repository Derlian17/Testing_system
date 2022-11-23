from PIL import Image
import tkinter as tk

im = open('image.pdi', 'w')
im.writelines('Pixel In-Depth Image')
file = '''
1 2x4 0,0,0
0 0 255,255,255
0 1 255,255,255
0 2 200,200,200
0 2.1 100,100,100
0 2.2 100,100,100
0 2.3 100,100,100
0 2.4 100,100,100
0 2.5 100,100,100
0 3 200,200,200
1 0 255,255,255
1 1 255,255,255
1 2 200,200,200
1 2.1 100,100,100
1 2.2 100,100,100
1 2.3 100,100,100
1 2.4 100,100,100
1 2.5 100,100,100
1 3 200,200,200
'''
im.write(file)


class ImagePDI:
    def __init__(self, text, size='200x200', name='image.png', bg=(0, 128, 0)):
        w, h = size.split('x')
        w, h = int(w), int(h)
        self.size = size.split('x')
        self.size = (int(size.split('x')[0]), int(size.split('x')[1]))
        self.image = [[list()] * w] * h
        self.item = ''
        self.text = text
        self.name = name
        self.bg = bg

    def __getitem__(self, item):
        self.item = item
        return self.image[item]

    def set_pixel(self, x, y):
        pass

    def paint(self, depth, x, y):
        # x = round(x / 200 * 200 * 10 ** depth)
        # y = round(y / 200 * 200 * 10 ** depth)
        image = Image.open('im.png')
        im1 = image.resize((min(200, self.size[0] * 10 ** depth), min(200, self.size[1] * 10 ** depth)))

        pix = im1.load()
        w, h = im1.size
        im = dict()
        # print(w, h)
        el = (0, 0, 0)
        for line in self.text.strip().split('\n'):
            if round(float(line.split()[0]), depth) >= x / 10 ** depth and \
                    round(float(line.split()[1]), depth) >= y / 10 ** depth:
                im[' '.join(line.split()[:-1])] = line.split()[-1]
        for i in range(x, x + w):
            for j in range(y, y + h):
                n = 0
                # if i >= w or j >= h:
                #     break
                x1, y1 = round(i / 10 ** depth, depth - n), round(j / 10 ** depth, depth - n)
                # if n == depth:
                #     x1, y1 = int(x1), int(y1)
                while f'{x1} {y1}' not in im.keys() and n < depth:
                    # print(x1, y1)
                    n += 1
                    x1, y1 = round(i / (10 ** depth), depth - n), round(j / (10 ** depth), depth - n)
                    # if n == depth:
                    #     x1, y1 = int(x1), int(y1)
                if f'{x1} {y1}' in im.keys():
                    col = tuple(map(int, im[f'{x1} {y1}'].split(',')))
                    # print(x1, y1)
                else:
                    col = self.bg
                # print(i, j, col, x1, y1)
                pix[i - x, j - y] = col

        im1.save(self.name)

    def test1(self):
        print(self.text)


im = open('image3.pdi', 'r')
im.readline()
d, size, bg = im.readline().split()
bg = tuple(map(int, bg.split(',')))
image = ImagePDI(''.join(im.readlines()), size=size)
image.paint(1, 0, 0)
# for line in im.readlines():
#     x, y, color = line.split()
#     x, y = round(float(x)), round(float(y))
#     color = tuple(map(int, color.split(',')))


x_mouse, y_mouse = 0, 0
x_start, y_start = 0, 0
paint = False
pnt = False
colors = [(0, 0, 0), (128, 128, 128), (255, 255, 255)]
col_num = 2
col = colors[col_num]
master = tk.Tk(className='_PDI_editor_')
master.geometry('250x250+100+100')
master.resizable(False, False)

canvas = tk.Canvas(master, width=200, height=200, background='green')

canvas.config(cursor='pencil')
but1 = tk.Button(width=21, height=21, text='💾', font=20)
but1.place_configure(x=205, y=50, width=21, height=21)
but2 = tk.Button(width=21, height=21, text='📁', font=20)
but2.place_configure(x=205, y=75, width=21, height=21)
but3 = tk.Button(width=21, height=21, text='🎨', font=20)
but3.place_configure(x=205, y=100, width=21, height=21)
scale = tk.Scale(width=10, orient='horizontal', bg='red', to=3, from_=0)
scale.place_configure(width=200, height=40, x=5, y=205)
label = tk.Canvas(width=40, height=40, background='green')
label.place_configure(x=205, y=5)
rect = label.create_rectangle(4, 4, 40, 40, width=2, outline='grey')
arrow_left = tk.Button(width=12, height=12, text='←')
arrow_left.place_configure(width=12, height=12, x=205, y=150)
arrow_right = tk.Button(width=12, height=12, text='→')
arrow_right.place_configure(width=12, height=12, x=230, y=150)
arrow_up = tk.Button(width=12, height=12, text='↑')
arrow_up.place_configure(width=12, height=12, x=217, y=137)
arrow_down = tk.Button(width=12, height=12, text='↓')
arrow_down.place_configure(width=12, height=12, x=217, y=162)
lbl = canvas.create_image(0, 0, anchor='nw')
canvas.place_configure(x=0, y=0)
# image_canvas = canvas.create_image(0, 0, 'image.bmp')


def re_col():
    global col_num, col, but3
    col_num += 1
    col_num %= len(colors)
    col = colors[col_num]
    col_h = f'#{hex(col[0])[2:]}{hex(col[1])[2:]}{hex(col[2])[2:]}'
    but3.config(bg=col_h)


but3.config(command=re_col)

file = '''0 0 -1,0,0\n'''


def paint_true(event):
    global x_mouse, y_mouse, paint
    paint = True


def paint_false(event, f=False):
    global x_mouse, y_mouse, paint, pnt
    pnt = False
    paint = paint and f


def mouse_x_y(event):
    global x_mouse, y_mouse, file, col, pnt
    x_mouse, y_mouse = event.x, event.y
    x1, y1 = canvas.winfo_pointerxy()
    xs, ys = canvas.winfo_rootx(), canvas.winfo_rooty()
    if paint and 0 + xs <= x1 <= 200 + xs and 0 + ys <= y1 <= 200 + ys:
        x, y, col1 = file.split('\n')[-2].split()
        x, y = int((float(x) - x_start) * 10 ** scale.get()), int((float(y) - y_start) * 10 ** scale.get())
        if pnt:
            col_h = f'#{hex(col[0])[2:]}{hex(col[1])[2:]}{hex(col[2])[2:]}'
            canvas.create_line(x, y, x_mouse, y_mouse, fill=col_h, tags='line')
        else:
            pnt = True
        file += f'{x_start + x_mouse / 10 ** scale.get()} ' \
                f'{y_start + y_mouse / 10 ** scale.get()} {str(col).replace(" ", "").strip("()")}\n'
    if x1 < 0 + xs or x1 > 200 + xs or y1 < 0 + ys or y1 > 200 + ys:
        paint_false(event, True)


pdi_im = ImagePDI('', name='test.png', bg=(0, 128, 0))


def move(x, y):
    global x_start, y_start, image1
    x_start += x * 100
    y_start += y * 100
    x_start, y_start = int(max(min(x_start, 200 * 10 ** scale.get() - 200), 0)), \
                       int(max(min(y_start, 200 * 10 ** scale.get() - 200), 0))
    x_l, y_l = label.coords(rect)[:2]
    x_l += x / 10 ** scale.get() * (40 - 40 / 2 ** scale.get()) / 2
    y_l += y / 10 ** scale.get() * (40 - 40 / 2 ** scale.get()) / 2
    x_l = max(min(x_l, 40 - 40 / 2 ** scale.get()), 4)
    y_l = max(min(y_l, 40 - 40 / 2 ** scale.get()), 4)
    label.coords(rect, x_l, y_l, x_l + 40 / 2 ** scale.get(), y_l + 40 / 2 ** scale.get())
    pdi_im.text = '\n'.join(file.split('\n')[1:])
    # print(pdi_im.text)
    if pdi_im.text.count('\n') > 0:
        pdi_im.paint(scale.get(), x_start, y_start)
    canvas.delete('line')
    image1 = tk.PhotoImage(master=master, file='test.png')
    canvas.itemconfig(lbl, image=image1)


arrow_left.configure(command=lambda: move(-1, 0))
arrow_right.configure(command=lambda: move(1, 0))
arrow_up.configure(command=lambda: move(0, -1))
arrow_down.configure(command=lambda: move(0, 1))
scale.configure(command=lambda event: move(0, 0))


''''🞅🞄-🖉'''
master.bind('<Motion>', mouse_x_y)
master.bind('<ButtonPress 1>', paint_true)
master.bind('<ButtonRelease 1>', paint_false)
master.bind('<Left>', lambda event: [move(-1, 0), paint_false(event)])  # [v, ?]
master.bind('<Up>', lambda event: [move(0, -1), paint_false(event)])
master.bind('<Right>', lambda event: [move(1, 0), paint_false(event)])
master.bind('<Down>', lambda event: [move(0, 1), paint_false(event)])
master.mainloop()
file = '\n'.join(file.split('\n')[1:])
print(file)