import os
import secrets
import random
import shutil
from flask import current_app
from flask_login import current_user
from PIL import Image


def save_picture(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Путь к нашему приложению
    full_path = os.path.join(current_app.root_path, 'static', 'profile_pics/', current_user.username, 'account_image')
    # Если папка не существуеть то создать 
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    picture_path = os.path.join(full_path, picture_fn)
    # Изменяем размер
    output_size = (360, 360)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

# Обрабатываем картинку
def save_picture_post(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Путь к нашему приложению
    full_path = os.path.join(current_app.root_path, 'static', 'profile_pics/', current_user.username, 'post_images')
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    picture_path = os.path.join(full_path, picture_fn)
    # Изменяем размер
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



def random_avatar(user):
    # создания пути где будет папка с данными пользователя
        full_path = os.path.join(os.getcwd(), 'blog/static', 'profile_pics', user, 'account_image')
        # Если папки нет то зоздать
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        full_path_avatar = os.path.join(os.getcwd(), 'blog/static/profile_pics/Avatars/')
        # список всех  имен элементов файла
        list_avatars = os.listdir(full_path_avatar)
        # получаем одно изображение
        lst = random.choice(list_avatars)
        # путь к изображению
        random_image_fill = os.path.join(full_path_avatar, lst)
        # изображение копируем в папку к пользователю
        shutil.copy(random_image_fill, full_path)
        return lst
        