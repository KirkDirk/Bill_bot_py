# считываем и перезаписываем файл с результатами

def read_db():
    with open("db.txt", "r", encoding = "UTF-8") as db:
        data_play = [int(el) for el in (db.read().split())] 
    return data_play

def write_db(data_play):
    with open("db.txt", "w", encoding = "UTF-8") as db:
        for el in data_play: 
            db.write(str(el)+" ")