from bs4 import BeautifulSoup 
import requests
import re
import io
import csv
def request_github_trending(url):
    response = requests.get(url) #the requests module allows to send HTTP requests using Python 
    return response.content #show content (html code) from the url

# print(request_github_trending("https://github.com/trending"))

def extract(page):
    soup = BeautifulSoup(page, "html.parser") #BeautifulSoup library was used for pulling data out of HTML file by using html parser
    html_repos = soup.find_all("article", class_ = "Box-row") #with help of Inspect was found class of all html repositories  
    return html_repos

def transform(html_repos):
    array = []
    for article in html_repos:
        rep_name = article.find("h1", class_ = "h3 lh-condensed").find('a') 
        description = article.find("p", class_ = "col-9 color-text-secondary my-1 pr-4")
        prog_lang = article.find("span", class_ = "d-inline-block ml-0 mr-3")
        nbr_stars = article.find("a", class_ = "Link--muted d-inline-block mr-3")
        nbr_forks = article.find("a", class_ = "Link--muted d-inline-block mr-3", href=re.compile("members")) #nbr_stars and nbr_forks have the same class but different href.re.compile helped to find nbr_forks where hrefs contain word "member"
        developer = article.find_all("img", class_ = "avatar mb-1 avatar-user", alt = True)
        repository = {'developer': None, 'repository_name': None, 'nbr_stars': None, "nbr_forks":None, "description":None, "programming language":None } #create an array of hash
        developers = "" #create a string that will contain all names of developers parced from images
        if rep_name:
            repository["repository_name"] = rep_name.text.replace("\n", "").replace(" ", "") #transform html code to text and delete unnecessary spaces and "\n" between words
        if description:
            repository["description"] = description.text.replace("\n", "").replace("      ", "").replace("    ", "")
        if prog_lang:
            repository["prog_lang"] = prog_lang.text.replace("\n", "")
        if nbr_stars:
            repository["nbr_stars"] = nbr_stars.text.replace("\n", "").replace("        ", "")
        if nbr_forks:
            repository["nbr_forks"] = nbr_forks.text.replace("\n", "").replace("        ", "")
        for img in developer:
            developers = developers + img["alt"].replace("\n", "") #parce all names from images
        developers = developers.split("@")[1:] #split names of developers by @ and start from the first index to avoid empty array with index
        developers = ", ".join(developers) #join comma delimited
        repository["developer"] = developers 
        array.append(repository) #add all data from repository (array of hash) to empty array
    return array

def format(array):
    header = ['Developer', 'Repository Name', 'Number of Stars'] #name 3 columns
    output = io.StringIO()  #this module implements a file-like class, StringIO, that reads and writes a string buffer (also known as memory files)
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC) #return a writer object responsible for converting the user’s data into delimited strings on the given file-like object
    writer.writerow(header) #write the row parameter to the writer’s file object
    for i in array:
        writer.writerow([i["developer"], i["repository_name"], i["nbr_stars"]]) #go through the array with objects and get values and write them to the array from string
    return output.getvalue() #getvalue() returns the entire contents of the stream regardless of current position

page = request_github_trending("https://github.com/trending")
html_repos = extract(page)
repositories_data = transform(html_repos)
csv = format(repositories_data)
# print(csv)
