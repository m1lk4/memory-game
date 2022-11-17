import os
from PIL import Image, ImageTk
import tkinter
import time
import random


CANVAS_WIDTH = 1100
CANVAS_HEIGHT = 550
TITLE_WIDTH = 450
TITLE_HEIGHT = 30
TIMER_WIDTH = 900
TIMER_HEIGHT = 200
IMAGE_WIDTH = 160
IMAGE_HEIGHT = 110
MARGING = 10
TEXT_FONT = 20
CANT_PAIRS = 6

def main():
    # create canvas
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Memory Game')
    canvas.create_text(
        TITLE_WIDTH,
        TITLE_HEIGHT,
        text='GUESS PAIRS     AND      HAVE FUN!',
        font=('verdana', TEXT_FONT, 'bold')
    )
    # create and update timer
    timer = canvas.create_text(
        TIMER_WIDTH,
        TIMER_HEIGHT,
        text='cronómetro',
        tag='cron',
        font=('verdana', TEXT_FONT, 'bold')
    )
    update_clock(0, timer, canvas)
    # choose images to play. Save the images in a list
    list_cards = choose_image()
    # show images in canvas with a rectangle above
    images_and_rects = create_board(list_cards, canvas)
    # when user press the rectangles run function 'find_pairs'
    canvas.tag_bind('rect', '<ButtonPress-1>', find_pairs)
    canvas.prev_images_tags = {}    # save tag's image when user sees it
    canvas.counter = 0              # count pairs's match
    # show text when user wins
    image_winner(canvas)
    canvas.mainloop()


def update_clock(t, timer, canvas):
    """
    Timer count unless you win. When you win, appears an image.
    So while image disappear, timer run.
    """
    if canvas.itemcget('you_won', 'state') != 'normal':
        canvas.itemconfig(timer, text='BEAT YOUR TIME \n\n    ' + str(t) + ' seconds')
        canvas.after(1000, update_clock, t + 1, timer, canvas)
    else:
        canvas.itemconfig(timer, state='disabled')


def choose_image():
    # get images from file and then mix them
    list_cards1 = os.listdir('pycards')
    random.shuffle(list_cards1)
    # duplicate images to obtain pairs and mix
    list_cards = list_cards1[:CANT_PAIRS] * 2
    random.shuffle(list_cards)
    return list_cards


def create_board(list_cards, canvas):
    # save images and rects in lists for reference
    cards = []
    rects = []
    i = 0   # reference the index of the list for saving images and rects
    # create images and rects and locate them in five columns and two rows
    for col in range(4):
        for row in range(3):
            x = 50 + col * (IMAGE_WIDTH + MARGING)
            y = 100 + row * (IMAGE_HEIGHT + MARGING)
            image = Image.open('pycards/' + list_cards[i])
            image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
            cards.append(ImageTk.PhotoImage(image))
            canvas.create_image(x, y, anchor='nw', image=cards[i], tags=list_cards[i])
            rectangle = canvas.create_rectangle(
                x,
                y,
                x + IMAGE_WIDTH,
                y + IMAGE_HEIGHT,
                fill='#556511',
                tags='rect',
                activefill='#B4D627',
                activewidth=2,
                outline='#B4D627',
                width=3
            )
            rects.append(rectangle)
            i += 1
    return cards


def find_pairs(event):
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    current_rect = canvas.find_closest(x, y)   # find rectangle closest to click
    # if user starts seeing the first image. So hidden closest rect and save the image's tag and the rect's tag.
    if not canvas.prev_images_tags:
        canvas.itemconfig(current_rect, state='hidden')
        first_image = canvas.find_closest(x, y)
        canvas.prev_images_tags['image'] = canvas.gettags(first_image)
        canvas.prev_images_tags['rect'] = current_rect
    else:  # see second image, hide rect and save current image's tag
        canvas.itemconfig(current_rect, state='hidden')
        second_image = canvas.find_closest(x, y)
        current_images_tags = canvas.gettags(second_image)
        if current_images_tags == canvas.prev_images_tags['image']: # that means images are the same
            canvas.counter += 1   # count pairs match
            canvas.prev_images_tags = {}
            check_win(canvas)
        else:    # the two images doesn't match
            cover_images(canvas, current_rect)

def check_win(canvas):
    if canvas.counter == CANT_PAIRS:  # means all pairs are match, so user win
        canvas.itemconfig('you_won', state='normal')


def cover_images(canvas, current_rect):
    canvas.update()
    time.sleep(1)
    canvas.itemconfig(current_rect, state='normal')
    canvas.itemconfig(canvas.prev_images_tags['rect'], state='normal')
    canvas.prev_images_tags = {}


def image_winner(canvas):

    canvas.create_text(
        350,
        260,
        text='YOU WIN!!!! :)',
        state='hidden',
        tag='you_won',
        font=('verdana', 40, 'bold'),
        fill='#CC10E1')


def make_canvas(width, height, title):
    """
    Creates and returns a drawing canvas
    of the given int size.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


if __name__ == '__main__':
    main()