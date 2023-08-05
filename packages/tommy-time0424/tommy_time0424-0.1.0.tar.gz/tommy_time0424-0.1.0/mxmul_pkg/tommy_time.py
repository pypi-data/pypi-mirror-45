print('哈喽，这是Tommy制作的Python第三方库')
import time
year = time.localtime()[0]
month = time.localtime()[1]
day = time.localtime()[2]
hour = time.localtime()[3]
minite = time.localtime()[4]
second = time.localtime()[5]
print('现在是{}年{}月{}日{}时{}分{}秒'.format(year,month,day,hour,minite,second))
