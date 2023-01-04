# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import logging
import pymongo
import sqlite3
from dotenv import load_dotenv
import os


class MongodbPipeline:
    load_dotenv()
    collection_name = 'Transcripts'

    def open_spider(self, spider):
        mongodb_id = os.environ.get('MONGODB_USERNAME')
        mongodb_pass = os.environ.get('MONGODB_PASSWORD')
        self.client = pymongo.MongoClient(f'mongodb+srv://{mongodb_id}:{mongodb_pass}@cluster0.vewo0my.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client['Transcripts_DB']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item


class SQLitePipeline:
    collection_name = 'Transcripts'

    def open_spider(self, spider):
        self.connection = sqlite3.connect('Transcripts_DB')
        self.c = self.connection.cursor()

        try:
            self.c.execute('''
                CREATE TABLE Transcripts (
                    Title TEXT,
                    Plot TEXT,
                    Transcript TEXT,
                    URL TEXT
                )
            ''')
        except sqlite3.OperationalError:
            pass

        self.connection.commit()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO Transcripts (Title, Plot, Transcript, URL) VALUES (?, ?, ?, ?)
        ''', (
            item.get('Title'),
            item.get('Plot'),
            item.get('Transcript'),
            item.get('URL'),
        ))
        self.connection.commit()
        return item
