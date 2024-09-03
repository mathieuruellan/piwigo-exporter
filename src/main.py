import argparse
import pymysql
import pathlib
import os
from contextlib import closing
import shutil

import sys
print(sys.argv)

def export_album(connection, album_row, src_path,dst_root_path):
    dst_album_path = pathlib.PurePath(dst_root_path, album_row['name']) 
    if not os.path.exists(dst_album_path):
        os.makedirs(dst_album_path)

    # copy all images
    with closing(connection.cursor()) as image_cursor:
        image_cursor.execute('SELECT i.path as path FROM piwigo_image_category as ic RIGHT JOIN piwigo_images as i  ON ic.image_id = i.id WHERE ic.category_id=%s', album_row['id'])
        for image_row in image_cursor:
            src_image_file = pathlib.PurePath(src_path, image_row['path'])
            if not os.path.isfile(src_image_file):
                raise Exception('file {0} not found'.format(src_image_file))
            shutil.copy(src_image_file,dst_album_path)
        
    # child albums
    with closing(connection.cursor()) as child_albums_cursor:
        child_albums_cursor.execute('SELECT * FROM piwigo_categories WHERE id_uppercat=%s',album_row['id'])
        for child_album_row in child_albums_cursor:
            export_album(connection, child_album_row, src_path, dst_album_path)
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbpassword", help="dbpassword") 
    parser.add_argument("--dbuser", help="dbuser")
    parser.add_argument("--dbhost", help="dbhost")
    parser.add_argument("--dbname", help="dbname")
    parser.add_argument("--src_path", help="source path to get original image")
    args = parser.parse_args()
    

    # Connect to the database
    connection = pymysql.connect(host=args.dbhost,
                                 user=args.dbuser,
                                 password=args.dbpassword,
                                 database=args.dbname,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    with closing(connection.cursor()) as cursor:
        cursor.execute('SELECT * FROM piwigo_categories WHERE id_uppercat is NULL')
        for album_row in cursor:
            export_album(connection, album_row, args.src_path, 'data')
            pass


            
