from tkinter import *
import PIL.Image, PIL.ImageTk
import _thread
import zipfile
import random
import os


class Object():
    def __init__(self, file='', **kwargs):
        self.load(file)

    def load(self, file='', **kwargs):
        if file == '':
            file = kwargs.get('file')
        try:
            file = open(file, 'r')
            file_content = file.readlines()
            file.close()
            if file_content == '':
                return

            content = ""
            sections = {}

            for line in file_content:
                line = line.replace(" ", "")
                line = line.replace("\n", "")
                content = content + line

            section = ""
            section_name = ""
            in_section = False
            level = 0

            for character in content:
                if in_section == True:
                    if character == "}":
                        in_section = False
                        level -= 1
                        sections[section_name] = section.split(";")
                        section_name = ""
                        section = ""
                    else:
                        section = section + character
                else:
                    if character == "{":
                        in_section = True
                        level += 1
                    else:
                        section_name = section_name + character

            for section in sections:
                section_name = section
                section = sections[section]
                # exec("self.%s = {}" % (section_name.lower()))
                if section_name.lower() == "behaviour":
                    pass
                for pair in section:
                    if pair != "":
                        pair = pair.split(":")
                        if pair != '':
                            key, value = pair[0], pair[1]
                            exec("self.%s = %s" % (key, value))

        except Exception as e:
            print("Error while reading Object file:\n%s" % e)

    def set(self, key, value):
        exec("self.%s = %s" % (key, value))

    def get(self, value):
        return exec("self.%s" % value)


class Player(Object):
    def __init__(self, file):
        Object.__init__(self, file)


class Map():
    def __init__(self, file):
        self.file = file
        self.config = {}
        self.objects = []
        self.load()
        self.player = Player(self.config["player"])

    def load(self, file="", **kwargs):
        if file == "":
            file = self.file
        try:
            file = open(file, "r")
            file_content = file.readlines()
            file.close()
            if file_content == "":
                return

            content = ""
            sections = {}

            for line in file_content:
                line = line.replace(" ", "")
                line = line.replace("\n", "")
                content = content + line

            section = ""
            section_name = ""
            in_section = False
            level = 0

            for character in content:
                if in_section:
                    if character == "}":
                        in_section = False
                        level -= 1
                        sections[section_name] = section.split(";")
                        section_name = ""
                        section = ""
                    else:
                        section = section + character
                else:
                    if character == "{":
                        in_section = True
                        level += 1
                    else:
                        section_name = section_name + character

            for section in sections:
                section_name = section
                section = sections[section]
                for pair in section:
                    if pair != "":
                        pair = pair.split(":")
                        if pair != '':
                            key, value = pair[0], pair[1]
                            exec("self.%s[\"%s\"] = %s" % (section_name.lower(), key, value))

        except Exception as e:
            print("Error while reading Map file:\n%s" % (e))

    def load_objects(self):
        for object in self.objects:
            print(object)

    def set(self, value, new_value):
        exec("self.%s = \"%s\"" % (value, new_value))

    def get(self, value):
        return exec("self.%s" % (value))

    def get_objects(self):
        counter = 0
        for object in self.objects:
            counter +=1
        return counter


class Screen(Tk):
    def __init__(self, vres, res, icon, title, music_dir, **kwargs):
        Tk.__init__(self)

        self.vwidth = vres[0]
        self.vheight = vres[1]
        self.width = res[0]  # self.winfo_screenwidth()
        self.height = res[1]  # self.winfo_screenheight()

        self.title(title)
        self.iconbitmap(icon)
        # self.geometry("%dx%d" % (self.width, self.height))
        self.state('zoomed')
        self.resizable(0, 0)

        self.width, self.height = self.winfo_width(), self.winfo_height()
        self.conversion_factor = self.vwidth / self.width

    def convert(self, values):
        try:
            x_new = values[0] / self.conversion_factor
            y_new = values[1] / self.conversion_factor
            return [int(round(x_new)), int(round(y_new))]
        except Exception as e:
            print(e)

    def put_canvas(self):
        try:
            self.canvas = Canvas(self, width=self.width, height=self.height)
            self.canvas.place(relx=0, rely=0)
        except Exception as e:
            print(e)

    def put(self, object, position):
        put_here = self.convert(position)
        self.canvas.create_image(put_here, image=object)
        self.update()

    def load(self, map):
        self.map = map
        self.put_canvas()

        self.read_pak(['self.map.background', 'self.map.player.skin'])

        map.background = PIL.Image.open(map.config["background"]).resize((self.width, self.height), PIL.Image.ANTIALIAS)
        map.background = PIL.ImageTk.PhotoImage(map.background)
        map.background_id = self.canvas.create_image(0, 0, anchor=CENTER, image=map.background)

        if os.path.isfile(map.config["music"]) == True:
            self.music(map.config["music"])

        if 0 in self.map.player.size:
            map.player.skin = PIL.ImageTk.PhotoImage(PIL.Image.open(map.player.skin))
        else:
            map.player.skin = PIL.ImageTk.PhotoImage(
                PIL.Image.open(map.player.skin).resize((map.player.size), PIL.Image.ANTIALIAS))
        self.put(map.player.skin, map.player.position)
        _thread.start_new_thread(self.loop, ())

    def loop(self):
        while True:
            print('Hello!')

    def message(self, message, font, size):
        pass

    def music(self, song):
        if song == "random":
            self.music_list = []
            counter = 0
            for song in os.listdir(self.music_dir):
                self.music_list.append(song)
                counter += 1
            song = self.music_list[random.randint(0, counter - 1)]
        mixer.init(48000, -16, 1, 1024)
        mixer.music.load(os.path.join(self.music_dir, song))
        mixer.music.play(-1)

    def move(self, object, position, speed="", **kwargs):
        if speed == "":
            speed = object.speed

        if position[0] > object.position[0]:
            diff_x = position[0] - object.position[0]
            update_x = 1 * speed
        elif position[0] < object.position[0]:
            diff_x = object.position[0] - position[0]
            update_x = -1 * speed
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

    def read_pak(self, requested_files, file=''):
        resources = 'resources'
        image = os.path.join(resources, 'image')
        sound = os.path.join(resources, 'sound')

        if file == '':
            file = self.map.config['data']
        self.map.pak = zipfile.ZipFile(file, 'r')
        for f in requested_files:
            if f in self.map.pak.namelist():
                exec('%s = io.BytesIO(self.map.pak.read(%s)' % (f, f))
