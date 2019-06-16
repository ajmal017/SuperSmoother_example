# Based on initial question from here.
# https://www.reddit.com/r/algotrading/comments/c0o4b8/can_someone_help_me_with_this/
# Code modified from here
# https://nbviewer.jupyter.org/github/jakevdp/supersmoother/blob/master/examples/Supersmoother.ipynb

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
# NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
# DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
# WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Dont forget to tip your server!
# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

import seaborn
from supersmoother import SuperSmoother, LinearSmoother
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import json
import requests
from random import randint
from time import sleep

# Use seaborn for plotting defaults.
# This can be safely commented-out if seaborn is not installed
seaborn.set()

# Install the package
# source at http://github.com/jakevdp/supersmoother
# or use ``pip install supersmoother``

#CREDS###################################################################
LIVE_API_KEY = ''
LIVE_USERNAME = ""
LIVE_PASSWORD = ""
LIVE_ACC_ID = ""
##########################################################################
DEMO_API_KEY = ''
DEMO_USERNAME = ""
DEMO_PASSWORD = ""
DEMO_ACC_ID = ""
###########################################################################

b_REAL = False

if b_REAL:
    REAL_OR_NO_REAL = 'https://api.ig.com/gateway/deal'
    API_ENDPOINT = "https://api.ig.com/gateway/deal/session"
    API_KEY = LIVE_API_KEY
    data = {"identifier": LIVE_USERNAME, "password": LIVE_PASSWORD}
else:
    REAL_OR_NO_REAL = 'https://demo-api.ig.com/gateway/deal'
    API_ENDPOINT = "https://demo-api.ig.com/gateway/deal/session"
    API_KEY = DEMO_API_KEY
    data = {"identifier": DEMO_USERNAME, "password": DEMO_PASSWORD}

headers = {'Content-Type': 'application/json; charset=utf-8',
           'Accept': 'application/json; charset=utf-8',
           'X-IG-API-KEY': API_KEY,
           'Version': '2'
           }

r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=headers)

headers_json = dict(r.headers)
CST_token = headers_json["CST"]
print(R"CST : " + CST_token)
x_sec_token = headers_json["X-SECURITY-TOKEN"]
print(R"X-SECURITY-TOKEN : " + x_sec_token)

# GET ACCOUNTS
base_url = REAL_OR_NO_REAL + '/accounts'
authenticated_headers = {'Content-Type': 'application/json; charset=utf-8',
                         'Accept': 'application/json; charset=utf-8',
                         'X-IG-API-KEY': API_KEY,
                         'CST': CST_token,
                         'X-SECURITY-TOKEN': x_sec_token}

auth_r = requests.get(base_url, headers=authenticated_headers)
d = json.loads(auth_r.text)

base_url = REAL_OR_NO_REAL + '/session'

if b_REAL:
    data = {
        "accountId": LIVE_ACC_ID,
        "defaultAccount": "True"}  # Main Live acc
else:
    data = {
        "accountId": DEMO_ACC_ID,
        "defaultAccount": "True"}  # Main Demo acc

auth_r = requests.put(
    base_url,
    data=json.dumps(data),
    headers=authenticated_headers)

# print("-----------------DEBUG-----------------")
# print("#################DEBUG#################")
# print(auth_r.status_code)
# print(auth_r.reason)
# print(auth_r.text)
# print("-----------------DEBUG-----------------")
# print("#################DEBUG#################")


##########################################################################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################END OF LOGIN CODE###############################
##########################################################################



def dataset_from_broker():
    # Axes are the horizontal and vertical lines used to frame a graph or chart:
    # x axis is the horizontal axis, In our case (time)
    # y axis is the vertical axis, In our case (price)
    # dy is the actual price
    # rate limit (IG Index)
    sleep(randint(1, 3))

    # Bitcoin, purely for testing. Change this to your own thing.
    epic_id = "CS.D.BITCOIN.TODAY.IP"

    base_url = REAL_OR_NO_REAL + '/markets/' + epic_id
    auth_r = requests.get(
        base_url, headers=authenticated_headers)
    d = json.loads(auth_r.text)

    base_url = REAL_OR_NO_REAL + "/prices/" + epic_id + "/DAY/365"
    # Price resolution (MINUTE, MINUTE_2, MINUTE_3, MINUTE_5,
    # MINUTE_10, MINUTE_15, MINUTE_30, HOUR, HOUR_2, HOUR_3,
    # HOUR_4, DAY, WEEK, MONTH)
    auth_r = requests.get(base_url, headers=authenticated_headers)
    d = json.loads(auth_r.text)

    # print("-----------------DEBUG-----------------")
    # print("#################DEBUG#################")
    # print(auth_r.status_code)
    # print(auth_r.reason)
    # print(auth_r.text)
    # print("-----------------DEBUG-----------------")
    # print("#################DEBUG#################")

    x = []
    y = []
    dy = []

    for i in d['prices']:

        if i['lowPrice']['bid'] is not None:
            lowPrice = i['lowPrice']['bid']
            x.append(lowPrice)
        ########################################
        if i['highPrice']['bid'] is not None:
            highPrice = i['highPrice']['bid']
            y.append(highPrice)
        # ########################################
        # if i['closePrice']['bid'] is not None:
            # closePrice = i['closePrice']['bid']
            # dy.append(closePrice)
        # ########################################

    # print(x)
    # print(y)
    # print(dy)
    dy = x
    return x, y, dy


# Generate and visualize the data
t, y, dy = dataset_from_broker()
plt.errorbar(t, y, dy, fmt='o', alpha=0.3)
plt.show()
plt.clf()

# fit the supersmoother model
model = SuperSmoother()
model.fit(t, y, dy)

# find the smoothed fit to the data
tfit = np.linspace(np.amin(t), np.amax(t), len(t))
yfit = model.predict(tfit)
# Show the smoothed model of the data
plt.errorbar(t, y, dy, fmt='o', alpha=0.3)
plt.plot(tfit, yfit, '-k')
plt.show()
plt.clf()

plt.errorbar(t, y, dy, fmt='o', alpha=0.3)
for smooth in model.primary_smooths:
    plt.plot(tfit, smooth.predict(tfit),
             label='span = {0:.2f}'.format(smooth.span))
plt.legend()
plt.show()
plt.clf()
t = np.linspace(np.amin(t), np.amax(t), len(t))
plt.plot(t, model.span(t))
plt.xlabel('t')
plt.ylabel('smoothed span value')

plt.show()
plt.clf()

N = 1000
span = span2 = 0

tfit = np.linspace(np.amin(t), np.amax(t), len(t))
t, y, dy = dataset_from_broker()

for rseed in np.arange(N):
    model = SuperSmoother().fit(t, y, dy)
    span += model.span(tfit)
    span2 += model.span(tfit) ** 2

mean = span / N
std = np.sqrt(span2 / N - mean ** 2)
plt.plot(tfit, mean)
plt.fill_between(tfit, mean - std, mean + std, alpha=0.3)
plt.xlabel('t')
plt.ylabel('resulting span')
plt.show()
plt.clf()

t, y, dy = dataset_from_broker()
plt.errorbar(t, y, dy, fmt='o', alpha=0.3)

# for alpha in range(0,10):
for alpha in [0, 8, 10]:
    smoother = SuperSmoother(alpha=alpha)
    smoother.fit(t, y, dy)
    print ("[+]debug, " + str(smoother.predict(tfit)))
    plt.plot(tfit, smoother.predict(tfit),
             label='alpha = {0}'.format(alpha))
plt.legend(loc=2)
plt.show()
plt.clf()
