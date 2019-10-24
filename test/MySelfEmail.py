import poplib
import base64,time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

def LoginEmail(username,password,pop3_add = 'pop.163.com'):
    # 设置pop3服务器地址
    # pop3_add = 'pop.163.com'
    # 链接到服务器
    server = poplib.POP3(pop3_add)
    # 调试信息 1为打开
    # server.set_debuglevel(1)
    # 欢迎信息
    welcome = server.getwelcome().decode('utf8')
    # print(welcome)
    # 开始身份验证
    try:
        server.user(username)
        server.pass_(password)
    except Exception as e:
        print(str(e))
    else:
        # 返回邮件总数目和占用服务器的空间大小（字节数）， 通过stat()方法即可
        email_num, email_size = server.stat()
        # print("消息的数量: {0}, 消息的总大小: {1}".format(email_num, email_size))
        # 使用list()返回所有邮件的编号，默认为字节类型的串
        rsp, msg_list, rsp_siz = server.list()
        # print("服务器的响应: {0},\n消息列表： {1},\n返回消息的大小： {2}".format(rsp, msg_list, rsp_siz))
        # print('邮件总数： {}'.format(len(msg_list)))

        # 下面单纯获取最新的一封邮件
        total_mail_numbers = len(msg_list)
        rsp, msglines, msgsiz = server.retr(total_mail_numbers)
        # print("服务器的响应: {0},\n原始邮件内容： {1},\n该封邮件所占字节大小： {2}".format(rsp, msglines, msgsiz))
        msg_content = b'\r\n'.join(msglines).decode('utf-8')
        msg = Parser().parsestr(text=msg_content)
    finally:
        return msg


# 解析标题栏的文本解码
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def LoadEmail(msg):
    # 获取信息
    subject = None
    fm = None
    to = None
    date = None
    file_name = None
    # 获取头部信息
    for header in ['From', 'To', 'Subject','Date']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                subject = decode_str(value)
            elif header == 'From':
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                fm = u'%s<%s>' % (name, addr)
            elif header == 'To':
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                to = u'%s<%s>' % (name, addr)
            else:
                # print(value)
                # hdr, addr = parseaddr(value)
                # name = decode_str(hdr)
                # date = u'%s<%s>' % (name, addr)
                date = value

    for texts in msg.walk():
        contentType = texts.get_content_type()
        mycode = texts.get_content_charset()
        text=None
        # 下载附件
        file = texts.get_filename()
        if file:
            file_name=file
            data = texts.get_payload(decode=True)
            att_file = open(file,'wb')
            att_file.write(data)
            att_file.close()
        # 获取正文内容
        elif contentType == 'text/plain':
            data = texts.get_payload(decode=True)
            text = data.decode(mycode)
            # print(text)

        elif contentType == 'text/html':
            """
                    若正文格式为html，则将正文内容写入html文件中，文件名为subject+'.html'
            """
            data = texts.get_payload(decode=True)
            text = data.decode(mycode)
            with open('{}.html'.format(subject), 'w', encoding='utf-8') as f:
                f.write(text)
            text = None
    # print('接收人：{}\n发件人：{}\n主题：{}\n附件名：{}\n接收时间：{}\n邮件正文：\n{}'.format(to, fm, subject, file_name, date, text))
if __name__ == '__main__':
    username = 'mamingnuo@163.com'
    password = 'mms5211314HH'
    pop3_server = 'pop.163.com'
    msg = LoginEmail(username, password, pop3_server)
    if msg:
        LoadEmail(msg)