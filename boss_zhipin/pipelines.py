# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import pymysql

class BossZhipinPipeline:
    def open_spider(self, spider):
        self.file = open('jobs_new.csv', 'a', newline='', encoding='utf_8_sig')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['company', 'name', 'location', 'salary', 'edu', 'experience', 'skills', 'demand'])

    def process_item(self, item, spider):
        self.writer.writerow(
            [item.get('company'), item.get('name'), item.get('location'), item.get('salary'), item.get('edu'),
             item.get('experience'), item.get('skills'), item.get('demand')])
        return item

    def close_spider(self, spider):
        self.file.close()

# class BossZhipinSQLPipeline:
#     def open_spider(self, spider):
#         self.connection = pymysql.connect(
#             host='localhost',
#             user='root',
#             password='12345678',
#             database='jobs_db'
#         )
#         self.cursor = self.connection.cursor()
#
#
#     def process_item(self, item, spider):
#         self.cursor.execute(
#             '''
#             INSERT INTO jobs (company, name, location, salary, edu, experience, skills, demand)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             ''',
#             (item.get('company'), item.get('name'), item.get('location'), item.get('salary'), item.get('edu'),
#              item.get('experience'), item.get('skills'), item.get('demand'))
#         )
#         self.connection.commit()
#         return item
#
#     def close_spider(self, spider):
#         self.cursor.close()
#         self.connection.close()


