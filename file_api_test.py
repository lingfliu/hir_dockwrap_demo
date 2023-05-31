from api import FileApi

fapi = FileApi('http://192.168.0.209:7394')

# res = fapi.upload('test_image.jpg')
# print(res)
# fid = res['msg']['data']['new_name']
# print(fid)
fid = 'a0382a321bf9447ea99c6cb7a7f836da.jpg'
res = fapi.download(fid, 'test_image_2.jpg')