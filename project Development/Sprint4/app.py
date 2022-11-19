# import libraries
from flask import Flask, render_template, request,redirect,url_for
from newsapi.newsapi_client import NewsApiClient
import ibm_db

# init flask app
app = Flask(__name__)
print("Connection to database...................")
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PROTOCOLO=TCPIP;PORT=30756;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pbp31273;PWD=0mhmHAwaShMBEWZw","","")

print("connected")

# Init news api
newsapi = NewsApiClient(api_key='4cdb334889e44d18a39525dbca66376d')

# helper function
def get_sources_and_domains():
	all_sources = newsapi.get_sources()['sources']
	sources = []
	domains = []
	for e in all_sources:
		id = e['id']
		domain = e['url'].replace("http://", "")
		domain = domain.replace("https://", "")
		domain = domain.replace("www.", "")
		slash = domain.find('/')
		if slash != -1:
			domain = domain[:slash]
		sources.append(id)
		domains.append(domain)
	sources = ", ".join(sources)
	domains = ", ".join(domains)
	return sources, domains

@app.route("/", methods=['GET', 'POST'])
def home():
	if request.method == "POST":
		sources, domains = get_sources_and_domains()
		keyword = request.form["keyword"]
		related_news = newsapi.get_everything(q=keyword,
									sources=sources,
									domains=domains,
									language='en',
									sort_by='relevancy')
		no_of_articles = related_news['totalResults']
		if no_of_articles > 100:
			no_of_articles = 100
		all_articles = newsapi.get_everything(q=keyword,
									sources=sources,
									domains=domains,
									language='en',
									sort_by='relevancy',
									page_size = no_of_articles)['articles']
		return render_template("home.html", all_articles = all_articles,
							keyword=keyword)
	else:
		top_headlines = newsapi.get_top_headlines(country="in", language="en")
		total_results = top_headlines['totalResults']
		if total_results > 100:
			total_results = 100
		all_headlines = newsapi.get_top_headlines(country="in",
													language="en",
													page_size=total_results)['articles']
		return render_template("home.html", all_headlines = all_headlines)
	return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
# def login():
# 	return render_template("login.html")
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        # print(user_name,password)
        query = ibm_db.exec_immediate(conn,"SELECT UNAME,PASSWORD FROM USERS WHERE UNAME='"+user_name+"'")
        results = ibm_db.fetch_both(query)
        print("results", results)
        if results:
            print(password,results['PASSWORD'])
            if results["PASSWORD"].strip() == password:
                print(password, user_name)
                return redirect(url_for('home', msg="Welcome {0}".format(user_name)))    
        return redirect(url_for('login'))
		
@app.route("/Registration", methods=["GET", "POST"])
def Registration():
	if request.method == "GET":
		return render_template('registration.html')
	if request.method == 'POST':
		# print("Data")
		user_name = request.form.get('username')
		password = request.form.get('password')
		email = request.form.get('email_id')
        # print(user_name,password,email)
		query = ibm_db.exec_immediate(conn, "INSERT INTO USERS VALUES ('"+ user_name+"','"+password+"','"+email+"')")
		return redirect(url_for('login'))
	# return render_template("Registration.html")

if __name__ == "__main__":
	app.run(debug = True)
