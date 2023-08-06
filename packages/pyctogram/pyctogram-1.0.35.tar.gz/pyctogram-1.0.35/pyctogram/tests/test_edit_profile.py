from pyctogram.instagram_client import client

if __name__ == '__main__':
    insta_client = client.InstagramClient('svetlanavlasova927', 'LS2eh06u')
    insta_client.login()
    insta_client.send_sms_code('+4917694916200')


