# Python / Django Live Project Details
# Please view the link in the YTSiteWalkthrough.txt file for a tour of the site! 
Topic: Best Cities in the U.S.
### Introduction
I have completed a 2 week sprint in the Software Development Bootcamp through The Tech Academy. I was assigned to a project where I created a website with a topic of my choice to practice what I have been learning. Along the way I also was presented with some new concepts that I hadn't seen up until that point. Such as Html/JSON parsing. Overall, this proved to be a great learning experience as I was able to implement and build on what I had learned so far.

### Takeaway
One of the biggest takeaways from this project was how comfortable I have grown with the unknown. For me this looks like taking in the problem/objective and beginning to figure out how I want to approach it. Another was how important it was to break my code up in to manageable pieces in order for me to keep things straight in my head. And lastly, spending time in my work led to me getting that much more in tune with where things were and what things did.

### Building the basic application
This was mostly an exercise in creating and setting up a new application within a project in Django.

### Creating/displaying a functioning create page
This story was a continuation of the Django set up. A model was created with the appropriate fields to be tracked based on my topic. I chose to reference a website that provided data on cost of living for states in the U.S. Based on this I added a set of choices that could be chosen to submit how the submitted state compares to the base index which was 100.

AVG_COST_OF_LIVING = [
    ('Above Average','Above Average'),
    ('Average','Average'),
    ('Below Average','Below Average'),
]

class Places(models.Model):
    city = models.CharField(max_length=30, default="", blank=True, null=False)
    state = models.CharField(max_length=2, default="", blank=True, null=False)
    state_cost_index = models.DecimalField(default=0.00, max_digits=1000, decimal_places=1)
    cost_of_living_average = models.CharField(max_length=60, choices=AVG_COST_OF_LIVING)
    description = models.TextField(max_length=300, default="", blank=True, null=False)
Displaying all items from the database
This story was pretty straight forward. The hardest part was getting familiar with Django Template Language and its capabilites. The most challenging part of this was getting the correct item to display based on its id within the database. Places.id was the solution which I found use for later in the project as well.

views.py
def Best_Cities_topcities(request):
    topC = Places.objects.all()
    return render(request, 'BestCities/Best_Cities_topcities.html', {'topC': topC})
html
<table>
        <tr>
            <th>City</th>
            <th>State</th>
        </tr>
        {% for places in topC %}
        <tr>
            <td><a href="{% url 'Best_Cities_details' places.id %}">{{ places.city }}</a></td>
            <td>{{ places.state }}</td>
        </tr>
        {% endfor %}
    </table>
Displaying a single item from the database
This was where the .id was used in order to retrieve specific information. The data was displayed in another table filling in headers and data fields based on the id.

views.py
def Best_Cities_details(request, pk):
    item = get_object_or_404(Places, pk=pk)
    return render(request, 'BestCities/Best_Cities_details.html', {'item': item})
Creating edit/delete functionality
This functionality was added by displaying existing information in a form.

views.py
def Best_Cities_edit(request, pk):
    item = get_object_or_404(Places, pk=pk)
    form = PlacesForm(data=request.POST or None, instance=item)
    if request.method == 'POST':
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.save()
            return redirect('Best_Cities_topcities')
        else:
            print(form.errors)
    else:
        return render(request, 'BestCities/Best_Cities_edit.html', {'form': form, 'item': item})
        
### Connecting to an API / Parsing through JSON
I used a weather API from rapidapi that turned out to be a little different than most APIs students find. This was a good exercise in learning how to discern between options which is not something I am used to doing with code. Searching for an api introduced new variables to consider before deciding to use it. I decided to continue after instructor approval and ended up being challenged throughout its implementation.

An adjustment I would make is to have the search fields take in three separate fields and creating a string with commas between each input and then using that new string as the search critera. The API required a city, state (abbreviated), and country (abbreviated) in order to popualte the rest of the data. Ultimately a great exercise in learning how to navigate and implement an API.

Another challenge from this story, and an opportunity to have some creativity was that I needed to display specific data that a user may want. The solution I came up with was to use checkboxes to then display only certain information about the searched city. In order to do that I found some resources that showed me how to check if a checkbox has been checked. After which I referenced that variable with the bool of each checkbox that then displayed any selected info.

I am most proud of the outcome of this story! It was an awesome example of struggling but overcoming and completing the task. A total confidence booster and motivator.

views.py
def Best_Cities_weather(request):
    info = []

    if request.method == 'POST':
        url = "https://community-open-weather-map.p.rapidapi.com/weather"

        querystring = {"q": request.POST['searchTerm'], "units": "imperial", "mode": "JSON"}

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "be30be0618mshf5d1c84d0650830p17fd71jsn7b66e52ac477"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        weather = json.loads(response.text)

        name = weather['name']
        info.append(name)
        main_info = weather['main']
        temperature = main_info['temp']
        info.append(temperature)
        feelsT = main_info['feels_like']
        info.append(feelsT)
        TH = main_info['temp_max']
        info.append(TH)
        TL = main_info['temp_min']
        info.append(TL)
        Wind = weather['wind']['speed']
        info.append(Wind)
        THumid = main_info['humidity']
        info.append(THumid)

    CTemp = request.POST.get('CurrentTemp', '') == 'on' #these check if a checkbox is selected
    FT = request.POST.get('feelsTemp', '') == 'on'
    TH = request.POST.get('THigh', '') == 'on'
    TL = request.POST.get('TLow', '') == 'on'
    WindSpeed = request.POST.get('Wind', '') == 'on'
    THumid = request.POST.get('Hum', '') == 'on'

    context = {
        'info': info, 'CTemp': CTemp, 'FT': FT, 'TH': TH, 'TL': TL,
        'WindSpeed': WindSpeed, 'THumid': THumid
    }


    return render(request, 'BestCities/Best_Cities_weather.html', context)
html
<div>
    <form method="POST">
        {% csrf_token %}
        <input type="search"
               class="search-field"
               name="searchTerm"
               placeholder="Chattanooga,tn,us"
               required /><hr width="600" color="black">

        <input type="checkbox" id="CurrentTemp" name="CurrentTemp"/>Current Temperature
        <input type="checkbox" id="feelsTemp" name="feelsTemp"/>Feels Like
        <input type="checkbox" id="THigh" name="THigh"/>Today's High
        <br>
        <input type="checkbox" id="TLow" name="TLow"/>Today's Low
        <input type="checkbox" id="Wind" name="Wind"/>Wind Speed
        <input type="checkbox" id="Hum" name="Hum"/>Humidity
        <hr width="600" color="black">
        <input class="btn" type="submit" value="Search"/>
        <hr width="600" color="black">
        <table border="1">
            <tr>
                {% if CTemp or FT or TH or TL or WindSpeed or THumid %}
                    <h3>Weather for {{info.0}}</h3>
                {% endif %}
            </tr>
            <tr>
                {% if CTemp %}
                    <th>Current Temperature (F)</th>
                {% endif %}
                {% if FT %}
                    <th>Feels Like (F)</th>
                {% endif %}
                {% if TH %}
                    <th>Today's High (F)</th>
                {% endif %}
                {% if TL %}
                    <th>Today's Low (F)</th>
                {% endif %}
                {% if THumid %}
                    <th>Humidity (%)</th>
                {% endif %}
                {% if WindSpeed %}
                    <th>Wind Speed</th>
                {% endif %}

            </tr>
            <tr>
                {% if CTemp %}
                   <td>{{info.1}}</td>
                {% endif %}
                {% if FT %}
                    <td>{{info.2}}</td>
                {% endif %}
                {% if TH %}
                    <td>{{info.3}}</td>
                {% endif %}
                {% if TL %}
                    <td>{{info.4}}</td>
                {% endif %}
                {% if THumid %}
                    <td>{{info.6}}</td>
                {% endif %}
                {% if WindSpeed %}
                    <td>{{info.5}}</td>
                {% endif %}
            </tr>
        </table>
    </form>
</div>

### Using Beautiful Soup to Web Scrape / Parsing Through HTML
This set of stories was the setup and use of Beautiful soup to scrape info from a website. The challenge here was to get the requests right in order to distill the info down to what I needed to display. With some instructor assistance, I was able to sucessfully display a page with every state and their average temperatures.

views.py
page = requests.get("https://www.currentresults.com/Weather/US/average-annual-state-temperatures.php")
    soup = BeautifulSoup(page.content, 'html.parser')
    general = soup.find('div', class_='clearboth')
    generalTables = general.find_all('table')


    tempList = []
    for data in generalTables:
        temp = data.find_all('td')
        for x in temp:
            temperature = x.get_text()
            tempList.append(temperature)


    stateList = []
    counter = 0
    while counter < len(tempList):
        stateList.append(tempList[counter])
        counter += 4

    tempHighList = []
    counter = 1
    while counter < len(tempList):
        tempHighList.append(tempList[counter])
        counter += 4


    context = {
        'stateList': stateList, 'tempHighList': tempHighList
    }


    return render(request, 'BestCities/Best_Cities_scrape.html', context)
html
<table>
    <tr>
        <th>State</th>
        <th>Average Temperature (°F)</th>
    </tr>
    {% for item in stateList %}{% for thing in tempHighList %}
        {% if forloop.counter == forloop.parentloop.counter %}
        <tr>
            <td>{{ item }}</td>
            <td>{{ thing }}</td>
        </tr>
        {% endif %}
     {% endfor %}{% endfor %}
</table>

### Front End Improvements
Throughout the project as well as during this story I added various front end improvements. There are various others I would like to add such as the body of the html not getting covered by the footer and styling the navbar.
