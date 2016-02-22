# Premier league predictor Search script ~ Author - Zack Akil 2014 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from Tkinter import Tk

#open browser
print("Opening browser...")
driver = webdriver.Firefox()
driver.get("http://www.bbc.com/sport/football/premier-league/table")
assert "Football" in driver.title
print("Found Page")

#find table containing team rankings
leageTable = driver.find_element_by_css_selector('[data-competition-slug="premier-league"]')
while True:
    teams = leageTable.find_elements_by_class_name("team")
    #print out all team names found
    for item in teams:
        print(item.get_attribute("id"))
    #take input for home team
    homeTeamToFind = raw_input("\nWho is the home team?")
    print("Looking for "+homeTeamToFind )
    #find home team stats
    homeTeam = leageTable.find_element_by_id(homeTeamToFind)
    homeTeamPos = homeTeam.find_element_by_class_name("position-number")
    print("Home teams position is "+homeTeamPos.text )
    #calculate home team form based on previous game stats
    homeTeamPreviousGames = homeTeam.find_element_by_class_name("last-10-games").find_elements_by_tag_name('li')
    i = 0
    homeForm = 0
    homeCurrentpos = int(homeTeamPos.text)
    for item in homeTeamPreviousGames:
        i = i + 1
        if i > 8:
            print(item.text)
            if item.text == "Loss":
                homeForm = homeForm - 1
            if item.text == "Win":
                homeForm = homeForm + 1
    print("Home teams form: ")
    print( homeForm )
    #take input for away team
    awayTeamToFind = raw_input("\nWho is the away team?")
    print("Looking for "+awayTeamToFind )
    #find away team stats
    awayTeam = leageTable.find_element_by_id(awayTeamToFind)
    awayTeamPos = awayTeam.find_element_by_class_name("position-number")
    print("Away teams position is "+awayTeamPos.text )
    #calculate home team form based on previous game stats
    awayTeamPreviousGames = awayTeam.find_element_by_class_name("last-10-games").find_elements_by_tag_name('li')
    i = 0
    awayForm = 0
    awayCurrentpos = int(awayTeamPos.text)
    for item in awayTeamPreviousGames:
        i = i + 1
        if i > 8:
            print(item.text)
            if item.text == "Loss":
                awayForm = awayForm - 1
            if item.text == "Win":
                awayForm = awayForm + 1
    print("Away teams form: ")
    print( awayForm )
    #caculate "win index" based on team stats
    homeTeamPosDiff = 0 - (homeCurrentpos - awayCurrentpos)
    print("Home team postion differential: ")
    print(homeTeamPosDiff)

    homeWinIndex = homeTeamPosDiff + (homeForm*10) + 5
    awayWinIndex = -homeTeamPosDiff + (awayForm*10)

    print("Home win index:" + str(homeWinIndex ))
    print("Away win index:" + str(awayWinIndex ))
    #predict 2:1 win to which team has higher win index
    if homeWinIndex - awayWinIndex > 0:
        print(homeTeamToFind + " 2 :"+awayTeamToFind + " 1")
        print(homeTeamToFind + " WIN!")
    else:
        print(homeTeamToFind + " 1 :"+awayTeamToFind + " 2")
        print(awayTeamToFind + " WIN!")
        
    #loop if another prediction wants to be made
    loop = raw_input("\nWould you like to predict another match? (y/n)")
    if loop == "n":
        break

driver.close()
