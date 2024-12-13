import json

SECRET_KEY = "ksu_team_1"

# import ngrok
# import time
#
# # Establish connectivity
# listener = ngrok.forward(addr="localhost:8080", authtoken="1t43yy8gVlVvgdaKvobTQVH4UTS_4upRsHn8mjohW1WnBDVw5",     proto="tcp")
# # Output ngrok url to console
# print(f"Ingress established at {listener.url()}")
#
# # Keep the listener alive
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Closing listener")
#
#
# import os
# a = os.popen('dir аниме_готово_кинул')
# result = a.read()
# a.close()
# print(type(result))
# from data.__all_models import *
# from data import db_session
# db_session.global_init("db/database.db")
# for img_name in list(filter(lambda x: ".png" in x,result.split())):
#     img = Img()
#     img.style = 1
#     img.path = "img/anime/" + img_name
#     print(img.path)
#     db = db_session.create_session()
#     db.add(img)
#     db.commit()

# import math
# a = int(input())
# len_num = int(math.log(a, 10)) + 1
# answer = True
# for i in range(int(len_num // 2)):
#     right = a // 10 ** (len_num - 1)
#     left = a % 10
#     if(right == left):
#         a = a % 10 ** (len_num - 1)
#         a = a // 10
#         len_num -= 2
#
#     else:
#         answer = False
#         break
#
# if(answer):
#     print("да")
# else:
#     print("нет")


import os

path_with_tilde = r'~/documents/document.txt'
expanded_path = os.path.expanduser(path_with_tilde)
print(expanded_path)  # Output: /home/user/documents/document.txt