from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
from TwitterAPI import TwitterAPI
import json
import sqlite3





consumer_key = 'WuBTMDuY2VXhNfzFTzYkO8MaD'
consumer_secret = 'OMCOixy34vTVC85Z4pY4cczPJfpIzu5HDyAtdlGcmKU1WMgxzd'
access_token_key = '1331210683-uFKt1d125UZY2fboH6OA6ehYqUItwoFFJx1lX7B'
access_token_secret = 'qHeKEWqyqWWEVBFPtpyXLaNdFJmtFrFH3SNU3daeKrt6C'
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)


app = Flask(__name__)
 
@app.route("/")
def index():
    return "Index!"
 
@app.route("/hello")
def hello():
    return "Hello World!"
 
@app.route("/members")
def members():
    return "Members"
 
@app.route("/members/<string:name>/")
def getMember(name):
	

	r = api.request('search/tweets', {'q':'#odoo', 'filter':'images'})

	url_list = []
	retweet_count_list = []
	url_retweet_dict = {}


	for item in r:
		


	  	line = str(item)
	  	pos = line.find('media_url_https')
	  	
	  	t = line[pos + 21:].find('\'')
	  	if(pos >= 0):
	  		url = line[pos + 20:pos + 21 + t]
	  		url_list.append(str(url))

	  	retweet_pos = line.find('retweet_count')
	  	t = line[retweet_pos:].find(',')
	  	if(retweet_pos >= 0):
	  		count = line[retweet_pos + 16:retweet_pos+ t]
	  		retweet_count_list.append(int(count))
	size = len(url_list)
	for i in range(0,size):
		url_retweet_dict[url_list[i]] = retweet_count_list[i]
	#print(url_list)
	usr=str(url_list[0])
	print(usr)
	user_image="http://www.naturalprogramming.com/images/smilingpython.gif"
	return render_template('test.html',name=name,user_image=usr)

	# 
	# 	url_retweet_dict[url_list[i]] = retweet_count_list[i]

	# url_list_in_database = Album.objects.all().filter(user = request.user).values('image_url')

	# temp = []
	# for url in url_list_in_database:
	# 	temp.append(str(url['image_url']))

	# url_list_in_database = temp

	# new_urls = list(set(url_list) - set(url_list_in_database))

	# for url in new_urls:
	# 	album = Album(image_url = url, user = request.user, retweet_count = url_retweet_dict[url])
	# 	album.save()

	# temp = Album.objects.all().filter(user = request.user).values('image_url', 'time_added', 'retweet_count')	

	# url_list = {}

	# for entry in temp:
	# 	dt = str(entry['time_added'])[0:10]
	# 	dt = calendar.month_name[int(dt[5:7])] + " " + dt[8:10] + ", " + dt[0:4]
	# 	url_list[str(entry['image_url'])] = (dt, str(entry['retweet_count']))

	# # print url_list

	# total_entries_in_database = len(url_list)

	# return render(request, 'assignment/feed.html', {'url_list': url_list})

@app.route("/init")
def initialize():
	conn=sqlite3.connect('data_file.db')
	c=conn.cursor()
	c.execute('''CREATE TABLE stud(user text,password text)''')
	return redirect(('http://127.0.0.1:5000/login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' or request.form['password'] == 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
        	connn=sqlite3.connect('data_file.db')
        	cc=connn.cursor()
        	users=request.form['username']
        	passwords=request.form['password']
        #	cc.executemany('INSERT INTO stud VALUES (?,?)',[(users,passwords,)])
        #	connn.commit()
        	login=cc.execute('SELECT * from stud WHERE user="%s" AND password="%s"' % (users, passwords))
        	if login.fetchone() is not None:
        		return redirect(('http://127.0.0.1:5000/members/hello/'))
        	else:
        		return render_template('login.html', error=error)
        		


    return render_template('login.html', error=error)   	



        	

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)