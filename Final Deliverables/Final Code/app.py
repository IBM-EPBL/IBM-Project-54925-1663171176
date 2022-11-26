# import libraries
from flask import Flask, render_template, request,redirect,url_for
import jinja2
from newsapi.newsapi_client import NewsApiClient
import ibm_db
import pycountry

# init flask app
app = Flask(__name__)

print(".........................Connecting to database..........................")

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PROTOCOLO=TCPIP;PORT=30756;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pbp31273;PWD=0mhmHAwaShMBEWZw","","")

print("_______________________________connected__________________________________")

# Init news api
newsapi = NewsApiClient(api_key='0ba9ccf85f044894877b98fcf7bb669c')

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
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        sources, domains = get_sources_and_domains()
        keyword = request.form["keyword"]
        related_news = newsapi.get_everything(q=keyword,sources=sources,domains=domains,language='en',sort_by='relevancy')
        no_of_articles = related_news['totalResults']
        if no_of_articles > 100:
            no_of_articles = 100
        all_articles = newsapi.get_everything(q=keyword,sources=sources,domains=domains,language='en',sort_by='relevancy',page_size = no_of_articles)['articles']
        return render_template("home.html", all_articles = all_articles,keyword=keyword)
    else:
        top_headlines = newsapi.get_top_headlines(country="in", language="en")
        total_results = top_headlines['totalResults']
        if total_results > 100:
            total_results = 100
        all_headlines = newsapi.get_top_headlines(country="in",language="en",page_size=total_results)['articles']
        return render_template("home.html", all_headlines = all_headlines)
    return render_template("home.html")


@app.route("/user", methods=['GET', 'POST'])
def user():
    if request.method == "POST":
        sources, domains = get_sources_and_domains()
        keyword = request.form["keyword"]
        related_news = newsapi.get_everything(q=keyword,sources=sources,domains=domains,language='en',sort_by='relevancy')
        no_of_articles = related_news['totalResults']
        if no_of_articles > 100:
            no_of_articles = 100
        all_articles = newsapi.get_everything(q=keyword,sources=sources,domains=domains,language='en',sort_by='relevancy',page_size = no_of_articles)['articles']
        return render_template("home.html", all_articles = all_articles,keyword=keyword)
    else:
        c1 = request.args.get('c1')
        c2 = request.args.get('c2')
        c3 = request.args.get('c3')
        c4 = request.args.get('c4')
        c5 = request.args.get('c5')
        options = [c1, c2, c3, c4, c5]
        option = []
        all_headlines = []
        for ele in options:
            if ele != 'NULL':
                option.append(ele)
        print("USERS CHOICES : ", option)
        input_country = "India"
        input_countries = [f'{input_country.strip()}']
        countries = {}
        for country in pycountry.countries:
            countries[country.name] = country.alpha_2
            codes = [countries.get(country.title(), 'Unknown code') for country in input_countries]
        for ele in option:
            top_headlines = newsapi.get_top_headlines(category=f'{ele.lower()}', language='en', country=f'{codes[0].lower()}')
            for val in top_headlines['articles']:
                all_headlines.append(val)
        return render_template("user.html", all_headlines = all_headlines)
    return render_template("user.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        query = ibm_db.exec_immediate(conn,"SELECT UNAME,PASSWORD,C1,C2,C3,C4,C5 FROM USERS WHERE UNAME='"+user_name+"'")
        res = ibm_db.fetch_both(query)

        r = {}
        i = 0
        for ele in res:
            if i % 2 == 0:
                r[ele] = res[ele].strip('+ ')
            i += 1
        print("results", r)
        if res:
            if res["PASSWORD"].strip() == password:
                print(password, user_name)
                return redirect(url_for('user', c1 = r['C1'], c2 = r['C2'], c3 = r['C3'], c4 = r['C4'], c5 = r['C5']))
        return redirect(url_for('login'))
		
@app.route("/Registration", methods=["GET", "POST"])
def Registration():
    if request.method == "GET":
        return render_template('registration.html')
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email_id')
        print(request.form)
        choice_list = [request.form.get('C1'), request.form.get('C2'), request.form.get('C3'), request.form.get('C4'), request.form.get('C5')]
        for i in range(len(choice_list)):
            if choice_list[i] == None:
                choice_list[i] = 'NULL'
        print(choice_list)
        ibm_db.exec_immediate(conn, "INSERT INTO USERS VALUES ('"+user_name+"','"+password+"','"+email+"', '"+str(choice_list[0])+"', '"+str(choice_list[1])+"', '"+str(choice_list[2])+"', '"+str(choice_list[3])+"', '"+str(choice_list[4])+"')")
        return redirect(url_for('login'))

if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0')
