# #!/usr/bin/env python3
# # -*- encoding:utf-8 -*-
# TelegramBot_YYG - Douyu Nofification
# Copyright (C) 2018  Patrick Young
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Also add information on how to contact you by electronic and paper mail.

import requests

defaultroomid = '71017'
baseurl = 'http://open.douyucdn.cn/api/RoomApi/room/'
roomurl = 'https://www.douyu.com/'

def douyunty(roomid=defaultroomid):
    query = baseurl + str(roomid)
    req = requests.get(query)
    resp = req.json()
    if req.status_code == 200:
        pass
    else:
        return 'Requests Error!'

    if resp['error'] == 0:
        try:
            status_live = resp['data']['room_status']
            if status_live == '2':
                result = 'Your requested room id: ' + str(roomid) + ' is **NOT LIVING** !'
                return result
            elif status_live == '1':
                result_template = 'Your sweetheart is **now living** ! Click [here]({urldata}) to watch it now.'.format(urldata=roomurl+str(roomid))
                return result_template
        except:
            return 'Error whlie parsing data.'
    else:
        return resp['data']


if __name__ == '__main__':
    roomid = input("Roomid?")
    if roomid == '':
        print(douyunty(defaultroomid))
    else:
        print(douyunty(roomid))