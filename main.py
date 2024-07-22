from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os

font_palette = ["black", "white", "red", "blue", "brown", "yellow", "green", "grey", "pink"]
color = ""


def open_picture():
    global picture
    file_path = filedialog.askopenfilename(title="Open Image File",
                                           filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
    if file_path:
        file_entry.insert(index=0, string=file_path)
        with Image.open(f"{file_path}").convert("RGBA") as picture:
            x_size = picture.size[0]
            y_size = picture.size[1]
            x_position_button.configure(from_=0, to=x_size)
            y_position_button.configure(from_=0, to=y_size)
    else:
        messagebox.showinfo(title="Warning", message="No file selected")


# Image.open(f"{file_path}").convert("RGBA") as
def converter():
    global color, result, picture
    with picture:
        template = Image.new("RGBA", picture.size,
                             (255, 255, 255, 0))  # making transparent colored same sized template for drawing
        text_font = font_button.get()
        if text_font == 0:
            messagebox.showinfo(title="Warning", message="Text Font must be bigger then zero")
        fnt = ImageFont.truetype("TimesNewBastard-ItalicWeb.ttf", text_font)  # font
        draw_text = ImageDraw.Draw(template)  # get a drawing context
        opa_val = opacity_button.get()
        user_text = text_entry.get()
        if user_text == "":
            messagebox.showinfo(title="Warning", message="Please enter watermark text")
        if color == "":
            messagebox.showinfo(title="Warning", message="Please select watermark color")
        fill_color = color + (opa_val,)
        x_position = x_position_button.get()
        y_position = y_position_button.get()
        position = (x_position, y_position)

        draw_text.text(position, text=user_text, font=fnt, fill=fill_color)  # opacity(0,255)
        result = Image.alpha_composite(picture, template)
        result.show()


def select_color(but_id):
    global color
    color = ImageColor.getrgb(font_palette[but_id - 1])


def save_file():
    global result
    file = filedialog.asksaveasfile(mode='w', defaultextension=".png",
                                    filetypes=(("PNG file", "*.png"), ("All Files", "*.*")))
    if file:
        abs_path = os.path.abspath(file.name)
        result.save(abs_path)


window = Tk()
window.title("Apply Watermark")
window.config(padx=20, pady=20, bg="white")
# window.geometry("600x600")
i = PhotoImage(width=1, height=1)

font_palette_frame = Frame(window)
font_palette_frame.pack(anchor="center")
font_color_label = Label(font_palette_frame, text="Font Palette")
font_color_label.pack(side="top")

font_border_frame = Frame(window)
font_border_frame.pack(anchor="center")
button_count = 1
for index in range(9):
    button_id = button_count
    button = Button(font_border_frame,
                    bd=0,
                    relief="flat",
                    borderwidth=0,
                    bg=f"{font_palette[button_count - 1]}",
                    activebackground=f"{font_palette[button_count - 1]}",
                    font=('arial', 80, 'bold'),
                    compound='bottom',
                    anchor="center",
                    width=20,
                    height=20,
                    image=i,

                    )
    button.pack(side="left", padx=1, pady=1)
    button.config(command=lambda b=button, b_id=int(button_id): select_color(b_id))
    button_count += 1

entry_frame = Frame(window)
entry_frame.pack(side="top", fill="x", pady=10)

watermark_text_label = Label(entry_frame, text="Watermark Text")
watermark_text_label.pack(side="left", padx=5)
text_entry = Entry(entry_frame, width=35)
text_entry.pack(side="left", padx=5)
file_open_label = Label(entry_frame, text="File Path:")
file_open_label.pack(side="left", padx=5)
file_entry = Entry(entry_frame, width=35)
file_entry.pack(side="left", padx=5)
open_file_button = Button(entry_frame, width=14, text="Select Picture", command=open_picture)
open_file_button.pack(side="left", padx=5)

button_frame = Frame(window)
button_frame.pack(side="bottom", fill="x", pady=10)

save_button = Button(button_frame, width=33, text="Save", command=save_file)
save_button.pack(side="right", padx=5)
converter_button = Button(button_frame, width=33, text="Convert", command=converter)
converter_button.pack(side="right", padx=5)

slider_frame = Frame(window)
slider_frame.pack(side="bottom", fill="x", pady=10)

opacity_label = Label(slider_frame, text="Opacity")
opacity_label.pack(side="left", padx=5)
opacity_button = Scale(slider_frame, width=20, length=100, orient="horizontal", from_=0, to=255)
opacity_button.pack(side="left", padx=5)

font_label = Label(slider_frame, text="Font")
font_label.pack(side="left", padx=5)
font_button = Scale(slider_frame, width=20, length=100, orient="horizontal", from_=0, to=255)
font_button.pack(side="left", padx=5)

x_position_button_label = Label(slider_frame, text="X Pos.")
x_position_button_label.pack(side="left", padx=5)
x_position_button = Scale(slider_frame, width=20, length=100, orient="horizontal", from_=0, to=255)
x_position_button.pack(side="left", padx=5)

y_position_button_label = Label(slider_frame, text="Y Pos.")
y_position_button_label.pack(side="left", padx=5)
y_position_button = Scale(slider_frame, width=20, length=100, orient="horizontal", from_=0, to=255)
y_position_button.pack(side="left", padx=5)

window.mainloop()
