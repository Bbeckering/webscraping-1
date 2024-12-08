from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url_list = [
    'https://cfbstats.com/2016/team/51/index.html',
    'https://cfbstats.com/2017/team/51/index.html',
    'https://cfbstats.com/2018/team/51/index.html',
    'https://cfbstats.com/2019/team/51/index.html',
    'https://cfbstats.com/2020/team/51/index.html',
    'https://cfbstats.com/2021/team/51/index.html',
    'https://cfbstats.com/2022/team/51/index.html',
    'https://cfbstats.com/2023/team/51/index.html',
    'https://cfbstats.com/2024/team/51/index.html'
        ]

points_per_game_list = []
passing_yards_list = []
third_down_conv_list = []
field_goal_list = []

rival_game_attendance = {'Texas': 0,
                         'Texas Tech': 0,
                         'Oklahoma': 0,
                         'Oklahoma St.': 0,
                         'Iowa St.': 0,
                            }

for url in url_list:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req  = Request(url, headers = headers)


    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, 'html.parser')
    stats = soup.findAll('td')
    
    
    points_per_game_list.append(stats[1].text)
    passing_yards_list.append(stats[22].text)
    third_down_conv_list.append(stats[64].text)
    field_goal_list.append(stats[82].text)


    table_rows  = soup.findAll('tr')
   
    
    
    for row in table_rows:
        stats = row.find_all('td')
        if len(stats) > 1:
            team = stats[1].text.replace("+","").replace("@","").strip()
            cleaned_team = ''.join([char for char in team if not char.isdigit()]).rstrip().lstrip()
            if cleaned_team in rival_game_attendance.keys():
                current_attendance = rival_game_attendance[cleaned_team]
                new_attendance = int(stats[4].text.replace(",",""))
                rival_game_attendance[cleaned_team] = current_attendance + new_attendance

    



print("2016-2024 Baylor Statistical Highpoints:")
print(f"Stat \t\t\t\tYear: Measure")
print(f"Points Per Game  \t\t{2016 + int(points_per_game_list.index(max(points_per_game_list)))}: {max(points_per_game_list)} points per game.")
print(f"Passing Yards  \t\t\t{2016 + int(passing_yards_list.index(max(passing_yards_list)))}: {max(passing_yards_list)} passing yards.")
print(f"Third Down Conversion %  \t{2016 + int(third_down_conv_list.index(max(third_down_conv_list)))}: {max(third_down_conv_list)}.")
print(f"Field Goal %  \t\t\t{2016 + int(field_goal_list.index(max(field_goal_list)))}: {max(field_goal_list)}.")



sorted_rival_game_attendance = dict(sorted(rival_game_attendance.items(), key=lambda item: item[1], reverse=True))

teams, attendance = [], []

for k, v in sorted_rival_game_attendance.items():
    teams.append(k)
    attendance.append(v)

from plotly.graph_objs import Bar
from plotly import offline

data = [
      {
            "type":"bar",
            "x":teams,
            "y":attendance,
            "marker": {
                  'color': "rgb(21, 71, 52)",
            },
            "opacity": .8
      }

]

mylayout = {
      "title": "Biggest Rivalry based on Attendance",
      "xaxis": {"title": "Teams"},
      "yaxis": {"title": "Attendance"},
      "plot_bgcolor": "rgb(255, 184, 28)",
}     


fig = {"data": data, "layout": mylayout}

offline.plot(fig, filename = "python_repos.html")