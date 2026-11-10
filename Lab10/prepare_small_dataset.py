"""Підготовка обмеженого набору даних Dogs vs. Cats для лабораторної роботи 10.

З 25 000 зображень train.zip з Kaggle формується невеликий набір: по 2000 зображень кожного класу
для навчання, по 500 для перевірки і по 500 для тестування. Усі зображення в наборах різні.
"""
import os
import shutil

# Каталог з набором даних (розпакований train.zip з Kaggle)
data_dir = '/content/dogs-vs-cats/train'
# Каталог з даними для навчання
train_dir = 'train'
# Каталог з даними для перевірки
val_dir = 'val'
# Каталог з даними для тестування
test_dir = 'test'
# Кількість зображень одного класу в кожному наборі
nb_train, nb_val, nb_test = 2000, 500, 500


def create_directory(dir_name):
    """Створює каталог dir_name з підкаталогами cats і dogs (старий каталог видаляється)."""
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(os.path.join(dir_name, "cats"))
    os.makedirs(os.path.join(dir_name, "dogs"))


def copy_images(start_index, end_index, source_dir, dest_dir):
    """Копіює зображення котів і собак з номерами від start_index до end_index у підкаталоги cats і dogs."""
    for i in range(start_index, end_index):
        shutil.copy2(os.path.join(source_dir, "cat." + str(i) + ".jpg"), os.path.join(dest_dir, "cats"))
        shutil.copy2(os.path.join(source_dir, "dog." + str(i) + ".jpg"), os.path.join(dest_dir, "dogs"))


for d in (train_dir, val_dir, test_dir):
    create_directory(d)

# 0-1999 - навчання, 2000-2499 - перевірка, 2500-2999 - тестування
copy_images(0, nb_train, data_dir, train_dir)
copy_images(nb_train, nb_train + nb_val, data_dir, val_dir)
copy_images(nb_train + nb_val, nb_train + nb_val + nb_test, data_dir, test_dir)

for d in (train_dir, val_dir, test_dir):
    print(d, ': cats -', len(os.listdir(os.path.join(d, "cats"))), ', dogs -', len(os.listdir(os.path.join(d, "dogs"))))
