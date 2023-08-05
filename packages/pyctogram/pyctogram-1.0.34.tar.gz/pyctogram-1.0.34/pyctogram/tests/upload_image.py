import os
import time

from pyctogram.instagram_client import client
from pyctogram.tests import account

if __name__ == '__main__':
    insta_client = client.InstagramClient('sova_norman', 'heckfy20')
    insta_client.login()
    images = [
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/167.jpg',
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/168.jpg',
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/386.jpg'
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/171.jpg',
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/177.jpg',
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/175.jpg',
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/180.jpg',
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/185.jpg',
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/165.jpg',
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/384.jpg',
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/163.jpg',
        '/Users/ruslangilfanov/pets/insta_project/images/sova_timofei/382.jpg',
    ][::1]
    for image_path in images:
        response = insta_client.upload_photo(image_path)
        print(response)
        time.sleep(10)
