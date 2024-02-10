from PIL import ImageTk, Image

class Photo():
    def __init__(self, canvas, file_name, x, y, size_x, size_y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image_file = Image.open(file_name)
        self.image_file = self.image_file.resize((size_x, size_y))
        self.canvas_image = ImageTk.PhotoImage(self.image_file)
        self.photo = self.canvas.create_image(self.x, self.y, image=self.canvas_image)

    def hide(self):
        self.canvas.itemconfigure(self.photo, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.photo, state='normal')
