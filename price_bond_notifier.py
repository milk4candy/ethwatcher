import requests
import smtplib
from email.mime.text import MIMEText

sold_bond = 320
buy_bond = 235
notify = True
debug = False
msg = ''

gm_user = 'user'
gm_passwd = 'passwd'

try:
    ret = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey=HJMV5ZABTGQB3PTT35WF49FDIQS5Z9E1EM').json()

    if ret['status'] == '1' and ret['message'] == 'OK':
        price = float(ret['result']['ethusd'])
        if price >= sold_bond:
            msg = 'ETH price is over $ '+ str(sold_bond) + ' USD now. You should SOLD ETH ASAP!'
        elif price <= buy_bond:
            msg = 'ETH price is under $ '+ str(buy_bond) + ' USD now. You should BUY ETH ASAP!'
        else:
            notify = False
            msg = 'ETH price is ' + str(price) + 'USD. Do NOT make any move!'
    else:
        msg = 'Oops! Looks something goes wrong on Etherscan API!'

except Exception as e:
    msg = 'Oops! Looks something goes wrong on price_bond_notifier!'


try:
    if notify:
        mail = MIMEText(msg)
        mail['Subject'] = 'ETH Price Bond Notification'
        mail['From'] = gm_user
        mail['To'] = gm_user

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gm_user, gm_passwd)
        server.sendmail(gm_user, gm_user, mail.as_string())
        server.close()
except Exception as e:
    print(e)

exit()
