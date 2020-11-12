import time
import random
import hashlib
from jieba.analyse import textrank
import yagmail
from yagmail.error import YagInvalidEmailAddress, YagConnectionClosed, YagAddressError

from .models import KeyWord

sender_email = "1456437967@qq.com"
sender_code = "zvopussnugrtbabh"
host = 'smtp.qq.com'
subject = [" WoooHooo.News 验证码"]
base_contents = '''
<table style="width: 99.8%; height: 95%;">
    <tbody>
        <tr>
            <td id="QQMAILSTATIONERY" style="background:url(https://rescdn.qqmail.com/bizmail/zh_CN/htmledition/images/xinzhi/bg/a_02.jpg) no-repeat #fffaf6; min-height:550px; padding:100px 55px 200px 100px; ">
            <div style="text-align: center;"><font>{},您好！&nbsp;</font></div>
            <div style="text-align: center;"><font><br>
                </font>
            </div>
            <div style="text-align: center;"><font>您的 WoooHooo.News 验证码/临时登录密码 为&nbsp;</font></div>
            <div style="text-align: center;"><font><br>
                </font>
            </div>
            <div style="text-align: center;"><font color="#ff0000"><b><u>{}</u></b></font></div>
            <div style="text-align: center;"><font><br>
                </font>
            </div>
            <div style="text-align: center;"><font>如非您本人操作无需理会。&nbsp;</font></div>
            <div style="text-align: center;"><font><br>
                </font>
            </div>
            <div style="text-align: center;"><font>感谢支持。</font></div>
            </td>
        </tr>
    </tbody>
</table>
<div><includetail><!--<![endif]--></includetail></div>
''' #使用 ''' 嵌入HTML代码，使用 format 嵌入称呼(ss)与验证码(key)

def md5(number):
    obj = hashlib.md5() # 加盐hash
    obj.update(str(number).encode('utf-8'))
    hash_key = obj.hexdigest()
    return hash_key

def send_validation_email(username, email_addr):
    key = random.randint(100000, 999999)
    contents = [base_contents.format(username, key)]
    try:
        yag = yagmail.SMTP(user=sender_email, password=sender_code, host=host) # 链接邮箱服务器发信
        yag.send(email_addr, subject, contents)
    except (YagInvalidEmailAddress, YagConnectionClosed, YagAddressError) as e:
        print("error: ", e)
        return "-1"
    hash_key = md5(key)
    return hash_key


def extract_keywords(content, user, topk=5):
    keywords = textrank(content, topK=topk, withWeight=True, allowPOS=('n', 'nt', 'nr', 'vn'))
    print(keywords)
    keyword_list = []
    for keyword, _ in keywords:
        keyw = KeyWord.objects.create(keyword=keyword)
        keyw.user.set([user])
        keyword_list.append(keyw)
    return keyword_list
