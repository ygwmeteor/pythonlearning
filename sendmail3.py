import smtplib
 
sendto = 'gaowei.yuan@netbraintech.com'
user= 'gaowei.yuan@netbraintech.com'
password = 'Meteor.1'
smtpsrv = "smtp.office365.com"
smtpserver = smtplib.SMTP(smtpsrv,587)
 
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(user, password)
email_list = [line.strip() for line in open('email.txt')]
for sendto in email_list:
    header = 'To:' + sendto + '\n' + 'From: ' + user + '\n' + 'Subject:testing \n'
   # print(header)
    msgbody = header + '\nHi,\n\nThis is a test Email send using Python \n\n\nGavin Yuan\n\n'
    smtpserver.sendmail(user, sendto, msgbody)
    print('done!')
smtpserver.close()