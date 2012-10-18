  1 '''Class for Teamspeak3 ServerQuery access'''
  2 import telnetlib
  3 import time
  4 import datetime
  5
  6
  7 def query_decorator(method):
  8     '''Decorator used for changing spaces to '\s' inside
  9     strings, requred by ServerQuery'''
 10     def wrapper(self, *args, **kw):
 11         new = []
 12         for arg in args:
 13             new.append(str(arg).replace(' ', '\s'))
 14         return(method(self, *new, **kw))
 15     return(wrapper)
 16
 17 def parse_list(sq_string):
 18     '''Function which is parsing raw lists generated by
 19     ServerQuery. It's returning list of dictionaries'''
 20     records = sq_string.split('|')
 21     end_list = []
 22     for record in records:
 23         parameters = record.split(' ')
 24         record_parsed = {}
 25         for parameter in parameters:
 26             try:
 27                 param, value = parameter.split('=', 1)
 28             except ValueError:
 29                 pass
 30             record_parsed[param] = value
 31         end_list.append(record_parsed)
 32     return(end_list)
 33
 34 class ServerQuery():
 35     '''ServerQuery class'''
 36
 37     client_list = []
 38     channel_list = []
 39     ban_list = []
 40     group_list = []
 41
 42     def __init__(self):
 43         self.tel = telnetlib.Telnet('localhost', '10011')
 44
 45     def sender(self, message, expected='error id=0 msg=ok\n\r'):
 46         '''Most important method. It's sending messages to telnet
 47         and recieving expected value, also returning everything with
 48         the expected value. If fails - returning empty string
 49         '''
 50         self.tel.write(''.join([message, '\n']).encode())
 51         response = self.tel.read_until(expected, 1)
 52         if expected in response:
 53             return(response)
 54         else:
 55             return ''
 56
 57     @query_decorator
 58     def login(self, client_login_name='SA', client_login_password='8JPwQQwM'):
 59         self.sender('login client_login_name=' + client_login_name + ' client_login_password=' + client_login_password, 'specific_command')
 60
 61     def set_server(self, sid='1'):
 62         self.sender('use sid='+ sid)
 63
 64     @query_decorator
 65     def changename(self, clid, newname):
 66         self.sender('clientupdate clid=' + clid + ' client_nickname=' + newname)
 67
 68     @query_decorator
 69     def get_from_client_list(self, parameter, value, what):
 70         for user in self.client_list:
 71             if user[parameter] == value:
 72                 return(user[what])
 73
 74     @query_decorator
 75     def get_from_channel_list(self, parameter, value, what):
 76         for channel in self.channel_list:
 77             if channel[parameter] == value:
 78                 return(channel[what])
 79
 80     def update_clientlist(self):
 81         sq_string = self.sender('clientlist')
 82         self.client_list = parse_list(sq_string)
83         return(self.client_list)
 84
 85     def update_banlist(self):
 86         sq_string = self.sender('banlist')
 87         self.ban_list = parse_list(sq_string)
 88         return(self.ban_list)
 89
 90     def update_channellist(self):
 91         sq_string = self.sender('channellist')
 92         self.channel_list = parse_list(sq_string)
 93         return(self.channel_list)
 94
 95     def update_grouplist(self):
 96         sq_string = self.sender('servergrouplist')
 97         self.group_list = parse_list(sq_string)
 98         return(self.group_list)
 99
100     @query_decorator
101     def poke(self, clid, MSG):
102         self.sender('clientpoke msg='+ MSG + ' clid=' + clid)
103
104     @query_decorator
105     def ban(self, clid, seconds, MSG):
106         self.sender('banclient clid=' + clid + ' time' + seconds + ' banreason='+ MSG)
107
108     @query_decorator
109     def clientmove(self, clid, cid):
110         self.sender('clientmove cid=' + cid + ' clid=' + clid)
111
112     @query_decorator
113     def clientkick(self, clid, reasonid, msg):
114         self.sender('clientkick clid=' + ID + ' reasonid=' + reasonid + ' reasonmsg=' + msg)
115
116     @query_decorator
117     def banner(self, bannerlink):
118         self.sender('serveredit virtualserver_hostbanner_gfx_url=' + bannerlink)
119
120     @query_decorator
121     def sendtextmessage(self, clid, msg):
122         self.sender('sendtextmessage targetmode=1  target=' + clid + ' msg=' + msg)
123
124     @query_decorator
125     def welcomemessage(self, msg):
126         self.sender('serveredit virtualserver_welcomemessage=' + msg)
127
128     @query_decorator
129     def changechannelname(self, cid, newname):
130         self.sender('channeledit cid=' + cid + ' channel_name=' + newname)
131
132     @query_decorator
133     def gmmessage(self, cluid, subject, message):
134         self.sender('message add cluid=' + cluid + ' subject=' + subject + ' message=' + message)
135
136     @query_decorator
137     def gmmessage(self, message):
138         self.sender('gm msg=' + message)
139
140     def addusertogroup(self, cldbid, sgid):
141         self.sender('servergroupaddclient sgid=' + sgid + ' cldbid=' + cldbid)
 83         return(self.client_list)
 84
 85     def update_banlist(self):
 86         sq_string = self.sender('banlist')
 87         self.ban_list = parse_list(sq_string)
 88         return(self.ban_list)
 89
 90     def update_channellist(self):
 91         sq_string = self.sender('channellist')
 92         self.channel_list = parse_list(sq_string)
 93         return(self.channel_list)
 94
 95     def update_grouplist(self):
 96         sq_string = self.sender('servergrouplist')
 97         self.group_list = parse_list(sq_string)
 98         return(self.group_list)
 99
100     @query_decorator
101     def poke(self, clid, MSG):
102         self.sender('clientpoke msg='+ MSG + ' clid=' + clid)
103
104     @query_decorator
105     def ban(self, clid, seconds, MSG):
106         self.sender('banclient clid=' + clid + ' time' + seconds + ' banreason='+ MSG)
107
108     @query_decorator
109     def clientmove(self, clid, cid):
110         self.sender('clientmove cid=' + cid + ' clid=' + clid)
111
112     @query_decorator
113     def clientkick(self, clid, reasonid, msg):
114         self.sender('clientkick clid=' + ID + ' reasonid=' + reasonid + ' reasonmsg=' + msg)
115
116     @query_decorator
117     def banner(self, bannerlink):
118         self.sender('serveredit virtualserver_hostbanner_gfx_url=' + bannerlink)
119
120     @query_decorator
121     def sendtextmessage(self, clid, msg):
122         self.sender('sendtextmessage targetmode=1  target=' + clid + ' msg=' + msg)
123
124     @query_decorator
125     def welcomemessage(self, msg):
126         self.sender('serveredit virtualserver_welcomemessage=' + msg)
127
128     @query_decorator
129     def changechannelname(self, cid, newname):
130         self.sender('channeledit cid=' + cid + ' channel_name=' + newname)
131
132     @query_decorator
133     def gmmessage(self, cluid, subject, message):
134         self.sender('message add cluid=' + cluid + ' subject=' + subject + ' message=' + message)
135
136     @query_decorator
137     def gmmessage(self, message):
138         self.sender('gm msg=' + message)
139
140     def addusertogroup(self, cldbid, sgid):
141         self.sender('servergroupaddclient sgid=' + sgid + ' cldbid=' + cldbid)
142
143     def removeuserfromgroup(self, cldbid, sgid):
144         self.sender('servergroupdelclient sgid=' + sgid + ' cldbid=' + cldbid)
145
146     def serverreconnect(self):
147         self.login()
148         self.set_server()
149
150     def quit(self):
151         self.sender('quit')
