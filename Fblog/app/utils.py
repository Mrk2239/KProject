from app.extentions import mail


def sendmail(app,msg):
    with app.app_context() as context:
        mail.send(msg)
        print('邮件已发送')