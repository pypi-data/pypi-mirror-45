from tkinter import *
from .pak import *
import PIL.ImageTk
import PIL.Image
import contextlib
import _thread
import random
import os
with contextlib.redirect_stdout(None):
    from pygame import mixer


class Object():
    def __init__(self, file, **kwargs):
        self.load(file)

    def load(self, file, **kwargs):
        if file == '':
            file = kwargs.get('file')
        try:
            file_content = file
            if file_content == '':
                return

            content = ''
            sections = {}

            for line in file_content:
                line = line.replace(' ', '')
                line = line.replace('\n', '')
                line = line.replace('\r', '')
                content = content + line

            section = ''
            section_name = ''
            in_section = False
            level = 0

            for character in content:
                if in_section:
                    if character == '}':
                        in_section = False
                        level -= 1
                        sections[section_name] = section.split(';')
                        section_name = ''
                        section = ''
                    else:
                        section = section + character
                else:
                    if character == '{':
                        in_section = True
                        level += 1
                    else:
                        section_name = section_name + character

            for section in sections:
                section_name = section
                section = sections[section]
                if section_name.lower() == 'behaviour':
                    pass

                for pair in section:
                    if pair != '':
                        pair = pair.split(':')
                        if pair[0] != '' and pair[1] != '':
                            key, value = pair[0], pair[1]
                            exec('self.%s = %s' % (key, value))

        except Exception as e:
            print('Error while reading Object file: %s' % e)

    def set(self, key, value):
        exec('self.%s = %s' % (key, value))

    def get(self, value):
        return exec('self.%s' % value)


class Player(Object):
    def __init__(self, file):
        Object.__init__(self, file)


class Map():
    def __init__(self, file):
        self.file = file
        self.config = {}
        self.objects = []
        self.pak = None
        self.load()
        self.player = Player(self.pak.read(self.config['player']).decode('utf-8'))

    def load(self, file=''):
        if file == '':
            file = self.file
        try:
            file = open(file, 'r')
            file_content = file.readlines()
            file.close()
            if file_content == '':
                return

            content = ''
            sections = {}

            for line in file_content:
                line = line.replace(' ', '')
                line = line.replace('\n', '')
                content = content + line

            section = ''
            section_name = ''
            in_section = False
            level = 0

            for character in content:
                if in_section:
                    if character == '}':
                        in_section = False
                        level -= 1
                        sections[section_name] = section.split(';')
                        section_name = ''
                        section = ''
                    else:
                        section = section + character
                else:
                    if character == '{':
                        in_section = True
                        level += 1
                    else:
                        section_name = section_name + character

            for section in sections:
                section_name = section
                section = sections[section]
                for pair in section:
                    if pair != '':
                        pair = pair.split(':')
                        if pair != '':
                            key, value = pair[0], pair[1]
                            exec('self.%s[\'%s\'] = %s' % (section_name.lower(), key, value))

            needed_attributes = ['data', 'player']

            for attribute in needed_attributes:
                if self.config.get(attribute):
                    pass
                else:
                    raise Exception('Map file has to have the attribute: %s' % attribute)

            self.pak = Pak(self.config['data'])

        except Exception as e:
            print('Error while reading Map file:\n%s' % e)

    def load_objects(self):
        for object in self.objects:
            print(object)

    def set(self, value, new_value):
        exec('self.%s = \'%s\'' % (value, new_value))

    def get(self, value):
        return exec('self.%s' % value)

    def get_objects(self):
        counter = 0
        for object in self.objects:
            counter +=1
        return counter


class Screen(Tk):
    def __init__(self, title, icon):
        Tk.__init__(self)

        self.conversion_factor = None
        self.canvas = None
        self.vres = None
        self.map = None

        self.title(title)
        self.iconbitmap(icon)
        # self.geometry('%dx%d' % (self.res[0, self.res[1))
        self.state('zoomed')
        self.resizable(0, 0)

        self.res = [self.winfo_width(), self.winfo_height()]

    def convert(self, values):
        try:
            x_new = values[0] / self.conversion_factor
            y_new = values[1] / self.conversion_factor
            return [int(round(x_new)), int(round(y_new))]
        except Exception as e:
            print('An error occurred while converting values: %s' % e)

    def put_canvas(self):
        try:
            self.canvas = Canvas(self, width=self.res[0], height=self.res[1])
            self.canvas.place(relx=0, rely=0)
        except Exception as e:
            print('An error occurred while initialising canvas: %s' % e)

    def put(self, object, position):
        put_here = self.convert(position)
        self.canvas.create_image(put_here, image=object)
        self.update()

    def load(self, map):
        self.map = map
        self.put_canvas()

        self.map.background = self.map.pak.read_file(self.map.config['background'])
        self.map.player.skin = self.map.pak.read_file(self.map.player.skin)

        self.vres = self.map.config['vres']
        self.conversion_factor = self.res[0] / self.vres[0]

        self.map.background = PIL.Image.open(self.map.background).resize((self.res[0], self.res[1]), PIL.Image.ANTIALIAS)
        self.map.background = PIL.ImageTk.PhotoImage(self.map.background)
        self.map.background_id = self.canvas.create_image(self.res[0] / 2, self.res[1] / 2, anchor=CENTER, image=self.map.background)

        if os.path.isfile(map.config['music']):
            self.music(map.config['music'])

        if self.map.player.size[0] == 0 or self.map.player.size[1] == 0:
            self.map.player.skin = PIL.ImageTk.PhotoImage(PIL.Image.open(self.map.player.skin))
        else:
            self.map.player.skin = PIL.ImageTk.PhotoImage(
                PIL.Image.open(self.map.player.skin).resize(map.player.size, PIL.Image.ANTIALIAS))
        self.put(self.map.player.skin, self.map.player.position)
        _thread.start_new_thread(self.loop, ())

    def loop(self):
        while True:
            print('Hello World!')

    def message(self, message, font, size):
        pass

    def music(self, song):
        if song == 'random':
            music_list = []
            counter = 0
            for song in os.listdir(self.music_dir):
                music_list.append(song)
                counter += 1
            song = self.music_list[random.randint(0, counter - 1)]
        mixer.init(48000, -16, 1, 1024)
        mixer.music.load(os.path.join(self.music_dir, song))
        mixer.music.play(-1)

    def move(self, object, position):
        if position[0] > object.position[0]:
            diff_x = position[0] - object.position[0]
            update_x = 1 * self.speed
        elif position[0] < object.position[0]:
            diff_x = object.position[0] - position[0]
            update_x = -1 * self.speed
        else:
            diff_x = 0
            update_x = 0

        if position[1] > object.position[1]:
            diff_y = position[1] - object.position[1]
            update_y = 1 * object.speed
        elif position[1] < object.position[1]:
            diff_y = object.position[1] - position[1]
            update_y = -1 * object.speed
        else:
            diff_y = 0
            update_y = 0

        if diff_x == 0 and diff_y == 0:
            return
        elif diff_x == diff_y:
            diff = diff_x
            x_bigger = 'Same'
            relation = 1 * object.speed
        elif diff_x == 0 and diff_y > 0:
            diff = diff_y
            relation = 1 * update_y
            x_bigger = False
        elif diff_y == 0 and diff_x > 0:
            diff = diff_x
            relation = 1 * update_x
            x_bigger = True
        elif diff_x > diff_y:
            relation = diff_x / diff_y * object.speed
            diff = diff_x
            x_bigger = True
        elif diff_x < diff_y:
            relation = diff_y / diff_x * object.speed
            diff = diff_y
            x_bigger = False

        for pixel in range(diff):
            if update_x < 0:
                if object.position[0] <= position[0]:
                    update_x = 0
            else:
                if object.position[0] >= position[0]:
                    update_x = 0
            if object.position[1] >= position[1]:
                update_y = 0
            if x_bigger:
                object.position[0] += relation
                object.position[1] += update_y

            elif not x_bigger:
                object.position[0] += update_x
                object.position[1] += relation
            elif x_bigger == 'Same':
                object.position[0] += update_x
                object.position[1] += update_y

            object.position[0], object.position[1] = int(round(object.position[0])), int(round(object.position[1]))
            self.put(self.map.background, [0, 0])
            self.put(object.skin, object.position)