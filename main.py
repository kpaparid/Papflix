"""This module does blah blah."""
import os
import os.path
import subprocess
import sys
import sqlite3

import pymysql as mdb
from PySide2.QtCore import QObject, Signal, Slot, QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
# from imdb import IMDb
from imdb import Cinemagoer
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint

from sqlalchemy import true
from custom_models import PersonModel
from movie import Movie

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL = PersonModel()
SUGGESTIONS = PersonModel()
# ia = IMDb()

ia = Cinemagoer()


def db_query(sql):
    """Query DB"""
    # database = mdb.connect(host='localhost', user='root',
    #                        passwd='marmi', port=3306, database="papflix")
    database = sqlite3.connect('movies.db')

    cursor = database.cursor()
    cursor.execute(sql)
    database.close()


def db_read(query):
    """Read Movies from DB"""
    try:
        # database = mdb.connect(host='localhost', user='root',
        #                        passwd='marmi', port=3306, database="papflix")
        database = sqlite3.connect('movies.db')
        cursor = database.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        database.close()
        return results

    except mdb.Error as err:
        print("Error reading data from MySQL table", err)
        return 'Error'


def db_insert(val):
    """Insert val in DB """
    # database = mdb.connect(host='localhost', user='root',
    #                        passwd='marmi', port=3306, database="papflix")
    database = sqlite3.connect('movies.db')
    sql = "INSERT INTO `movie`(`ID`,\
    `title`,\
    `year`,\
    `overview`,\
    `genres`,\
    `runtime`,\
    `popularity`,\
    `vote`,\
    `vote_imdb`,\
    `imdb_id`,\
    `stars`,\
    `stars_poster`,\
    `char_name`,\
    `poster`,\
    `backdrop_path`,\
    `trailer`,\
    `file_name`,\
    `folder`,\
    `path`,\
    `similarity`) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
    ON DUPLICATE KEY UPDATE \
    ID=VALUES(ID), title=VALUES(title), year=VALUES(year), overview=VALUES(overview), genres=VALUES(genres), runtime=VALUES(runtime), popularity=VALUES(popularity),\
    vote=VALUES(vote), vote_imdb=VALUES(voteImdb), imdb_id=VALUES(imdbID), stars=VALUES(stars), stars_poster=VALUES(stars_poster),\
    char_name=VALUES(char_name), poster=VALUES(poster), backdrop_path=VALUES(backdrop_path), trailer=VALUES(trailer),\
    file_name=VALUES(file_name), folder=VALUES(folder), path=VALUES(path), similarity=VALUES(similarity)"

    cursor = database.cursor()
    try:
        # Execute the SQL command
        cursor.execute(sql, val)
        # Commit your changes in the database
        # print('commit')
        database.commit()
    except mdb.Error as err:
        # Rollback in case there is any error
        print('Error Inserting in DB')
        database.rollback()
        print(err)

    # disconnect from server
    database.close()


def db_connection():
    """Connect to DB"""
    try:
        # database = mdb.connect(host='localhost', user='root', passwd='marmi', port=3306, database="papflix")
        # print('Connection', 'Database Connected Successfully')
        # cursor = database.cursor()
        # cursor.execute("SELECT VERSION()")
        # data = cursor.fetchone()
        # print("Database version : %s " % data)
        # database.close()

        # print("Database version")
        # CONNECTION_STRING = "mongodb+srv://kpaparid:Paparidis1993@cluster0.8gzcu.mongodb.net/canteenDatabase"
        # from pymongo import MongoClient
        # client = MongoClient(CONNECTION_STRING)
        # c = client['canteenDatabase']
        # item_details = c["meals"].find_one()
        # print(item_details)
        database = sqlite3.connect('movies.db')

    except mdb.Error as err:
        print('Connection', 'Failed To Connect Database')
        print(err)
        sys.exit(1)


def populate_suggestions():
    """Populates Suggestions in main page"""
    SUGGESTIONS.clearAll()
    limit = "20"

    movies = db_read(
        "SELECT * FROM movie WHERE backdrop_path NOT LIKE 'null' ORDER BY RAND() LIMIT " + limit)
    count = 0
    for row in movies:
        if count < 20:
            count += 1
            #                                   1   2       3       13      7       5       4       10      11          12          15           14
            #                addPerson(self, title, year, overview, poster, vote, runtime, genre, stars, starsPoster, characters, trailer, backdrop_path)
            SUGGESTIONS.addPerson(row[1], row[2], row[3], row[13], row[7], row[5], row[4], row[10], row[11],
                                  row[12], row[15], row[14], row[18])


def populate_movies(limit):
    """Gets movies in random order"""
    MODEL.clearAll()
    query = ''

    # self.clearMovies.emit()
    if limit == 0:
        query = "SELECT * FROM movie ORDER BY RAND()"
    else:
        query = "SELECT * FROM movie ORDER BY RAND() LIMIT " + str(limit)
    movies = db_read(query)
    for row in movies:
        MODEL.addPerson(row[1], row[2], row[3], row[13], row[7], row[5], row[4], row[10], row[11], row[12], row[15],
                        row[14], row[18])


def background_worker():
    print('background')
    mov = db_read('SELECT IMDBID FROM `movie` WHERE vote_imdb = ""')
    print('background2')
    for m in mov:
        imdb_id = m[0].replace('tt', '')
        rating = ia.get_movie(imdb_id).get('rating')
        sql = "UPDATE movie SET vote_imdb = '" + \
            str(rating) + "' WHERE vote_imdb = ''"
        # print(sql)
        print('BACKGROUND RATING ' + str(rating))
        print('BACKGROUND id ' + str(imdb_id))
        db_read(sql)


def get_length(filename):
    # result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
    #                         "format=duration", "-of",
    #                         "default=noprint_wrappers=1:nokey=1", '"'+filename+'"'],
    # stdout=subprocess.PIPE,
    # stderr=subprocess.STDOUT)
    result = subprocess.run(['cmd.exe', '/c', 'ffprobe', '-v', 'error',
                             '-show_entries', 'format=duration', '-of',
                             'default=noprint_wrappers=1:nokey=1', '-sexagesimal',
                             filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    duration = str(result.stdout.decode("utf-8")).split(':')
    dur = int(duration[0]) * 60 + int(duration[1])
    print(str(dur) + ' min')
    return dur


def folder_name(path, number):
    """This module does blah blah."""

    return path.split('\\')[-number]


class MyApp(QObject):
    Title = 'Joker'
    movie = Signal(str)
    poster = Signal(str)
    clearMovies = Signal()
    closeFilter = Signal(str)
    movies = []
    scrap = ''

    @Slot(str)
    def submit_filter(self, query):
        """Filter database with the provided query"""

        query = query.split('|')
        text = query[2].replace(' OR', ',').replace(' AND', ',') + ':'
        if text == ':':
            text = "Random Movies:"
        query[0] = query[0].replace('Year', '`year`')
        query[1] = query[1].replace('Rating', '`vote_imdb`')
        query[3] = query[3].replace('Sort By:', 'ORDER BY').replace(
            'Name', '`title` ASC').replace('Year', '`year` DESC').replace('Vote', '`vote` DESC')
        query[2] = query[2].replace('Action', "`genres` LIKE '%Action%'") \
            .replace('Animation', "`genres` LIKE '%Animation%'") \
            .replace('Adventure', "`genres` LIKE '%Adventure%'") \
            .replace('Comedy', "`genres` LIKE '%Comedy%'") \
            .replace('Crime', "`genres` LIKE '%Crime%'") \
            .replace('Documentary', "`genres` LIKE '%Documentary%'") \
            .replace('Drama', "`genres` LIKE '%Drama%'") \
            .replace('Family', "`genres` LIKE '%Family%'") \
            .replace('Fantasy', "`genres` LIKE '%Fantasy%'") \
            .replace('History', "`genres` LIKE '%History%'") \
            .replace('Horror', "`genres` LIKE '%Horror%'") \
            .replace('Music', "`genres` LIKE '%Music%'") \
            .replace('Mystery', "`genres` LIKE '%Mystery%'") \
            .replace('Romance', "`genres` LIKE '%Romance%'") \
            .replace('Science Fiction', "`genres` LIKE '%Science Fiction%'") \
            .replace('TV Movie', "`genres` LIKE '%TV Movie%'") \
            .replace('Thriller', "`genres` LIKE '%Thriller%'") \
            .replace('War', "`genres` LIKE '%War%'") \
            .replace('Western', "`genres` LIKE '%Western%'")

        print('REFORM')
        parameters = ''
        for param in query:
            if len(param) >= 1:
                parameters += '( ' + param + ') AND '
        base_query = 'SELECT * FROM `movie` WHERE '
        query = base_query + parameters[:-5].replace('AND ( ORDER', 'ORDER') \
            .replace(' ASC)', ' ASC') \
            .replace(' DESC)', ' DESC')
        print(query)
        mov = db_read(query)
        MODEL.clearAll()
        self.closeFilter.emit(text)
        for row in mov:
            MODEL.addPerson(row[1], row[2], row[3], row[13], row[7], row[5], row[4], row[10], row[11], row[12], row[15],
                            row[14], row[18])

    @Slot(str)
    def onSearch(self, search):
        """Searches database for @search"""
        print('Searching for ' + search)
        query = ''
        query = "SELECT * FROM movie WHERE `title` LIKE '%" + search + \
            "%' OR `stars` LIKE '%" + search + "%' ORDER BY title "
        print(query)
        movies = db_read(query)
        MODEL.clearAll()
        for row in movies:
            MODEL.addPerson(row[1], row[2], row[3], row[13], row[7], row[5], row[4], row[10], row[11], row[12], row[15],
                            row[14], row[18])

    @Slot(str)
    def onClick(self):
        print('click')

    @Slot(str)
    def watch(self, path):
        """Starts movie from path"""
        print(path)
        #        p = 'cmd /c "start "" '+path+'"""'

        p = 'cmd /c "start "" "' + path
        p += '"'

        print(p)
        os.system(p)

    @Slot(str)
    def onComp(self, str):
        """Main GUI init"""

        if str == 'Home':
            populate_suggestions()
            populate_movies(21)
        elif str == 'Main':
            populate_movies(0)

    def db_init(self, path):
        """Init DB"""

        count = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                if (file.endswith(".VOB") or file.endswith(".avi") or
                        file.endswith(".mp4") or file.endswith(".mkv")):
                    path = os.path.join(root, file)
                    if file.endswith(".VOB"):
                        # 3 .vob #2 all
                        folder = folder_name(path, 3)
                        filename = folder
                    else:
                        folder = folder_name(path, 2)
                        filename = file
                    if count <= 1000000:
                        print('------')
                        path = os.path.join(root, file)

                        print('p: ' + path)
                        if 'CD2' not in filename and 'cd2' not in filename:
                            tainia = Movie(True, (filename, folder, path))
                            if tainia.scrap != '' and tainia.scrap:
                                ts = tainia.scrap.split(', ')
                                for scrapi in ts:
                                    if scrapi not in self.scrap.split(', '):
                                        self.scrap += tainia.scrap

                                # print('scrap:'+self.scrap)
                            print(str(count))

                            entry = tainia.get_db_entry()
                            # print(entry)
                            db_insert(entry)
                            self.movies.append(tainia)

                    count += 1

    @Slot()
    def exit(self):
        sys.exit(-1)

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        db_connection()
        path = 'H:movies'
        # self.background_worker()

        # self.initDB(path)

        flag = True
        if flag:
            self.db_init(path)
        else:
            mov = db_read('SELECT * FROM `movie`')
            for row in mov:
                self.movies.append(Movie(flag, row))


if __name__ == '__main__':

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    main = MyApp()
    engine.rootContext().setContextProperty('myListModel', MODEL)
    engine.rootContext().setContextProperty('SuggestionsModel', SUGGESTIONS)
    engine.rootContext().setContextProperty("MyApp", main)
    engine.load(QUrl.fromLocalFile(
        os.path.join(CURRENT_DIR, 'mainWindow.qml')))
    if not engine.rootObjects():
        sys.exit(-1)
    print('exit')
    sys.exit(app.exec_())
