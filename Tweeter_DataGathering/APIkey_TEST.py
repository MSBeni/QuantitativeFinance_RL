filepath = "/home/i-sip_iot/s_vv/TweeterAPI.txt"
keys_list = []
# keys = open(filepath, 'r').read()
# print(keys.strip())
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       # print("Line {}: {}".format(cnt, line.strip()))
       keys_list.append(line.strip())
       line = fp.readline()
       cnt += 1

consumer_key, consumer_secret, access_key, access_secret = [el for el in keys_list]
print(consumer_key)
