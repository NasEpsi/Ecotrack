#importing the library we will need
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import schedule
import time

#Database to store users’ green activities
UserData = pd.DataFrame(colums=['Username', 'WaterConsumption', 'ElectricityConsumption', 'Transport', 'WasteFood', 'MeatConsumption', 'ConsumptionOrganicFood', 'CyclingWalkingDistance', 'CarpoolingPublicTransport', 'Date'])
UserData['Date'] = pd.to_datetime('today').normalize()

#Function to reset the score every day by keeping the data in a database
def ResetDailyScore():
    global UserData

    # Back up historical data
    HistoricalData = UserData.copy()
    HistoricalData.to_csv('historical_data.csv', index=False)
    
    # Reset the DataFrame UserData
    UserData = pd.DataFrame(columns=['Username', 'WaterConsumption', 'ElectricityConsumption', 'Transport', 'WasteFood', 'MeatConsumption', 'ConsumptionOrganicFood', 'CyclingWalkingDistance', 'CarpoolingPublicTransport', 'Date'])

#Main Dashboard 
def DashBoard(username):
    UserActivities = UserData[UserData['Username'] == username]
    EcologicFootprint = CalculateEcologicFootprint(UserActivities)
    ReportwaterConsumption(UserActivities)
    ReportElectricityConsumption(UserActivities)
    ReportTransport(UserActivities)
    ReportwasteFood(UserActivities)
    ReportMeatConsumption(UserActivities)
    ReportOrganicFood(UserActivities)
    ReportTotalEcologicImpact(UserActivities)
    ReportCyclingWalkingDistance(UserActivities)
    ReportCarpoolingPublicTransport(UserActivities)

#Function to calculate user’s ecological footprint
def CalculateEcologicFootprint(UserActivities):

    # Filter activities by current date
    UserActivities = UserActivities[UserActivities['Date'] == pd.to_datetime('today').normalize()]
    
    #Calculation based on ecological activities
    WaterImpact = np.sum(UserActivities['WaterConsumption'] * CoeffWater)
    ElectricityImpact = np.sum(UserActivities['ElectricityConsumption'] * CoeffElectricity)
    TransportImpact = np.sum(UserActivities['Transport'] * CoeffTransport)
    MeatConsumptionImpact = np.sum(UserActivities['MeatConsumption'] * CoeffMeatConsumtion)
    wasteFoodImpact = np.sum(UserActivities['WasteFood'] * CoeffWasteFood)
    OrganicFoodImpact = np.sum(UserActivities['ConsumptionOrganicFood'] * CoeffOrganicFood)
    CyclingWalkingDistance = np.sum(UserActivities['CyclingWalkingDistance'] * CoeffCyclingWalkingDistance)
    CarpoolingPublicTransport = np.subtract(UserActivities['CarpoolingPublicTransport'] * CoeffCarpoolingPublicTransport)

    TotalEcologicImpact = WaterImpact + ElectricityImpact + TransportImpact + wasteFoodImpact + MeatConsumptionImpact + OrganicFoodImpact + CyclingWalkingDistance + CarpoolingPublicTransport

    #Score and phrase of encouragement
    if TotalEcologicImpact >= 19:
        print("You are not ecological, make more effort for the good of the planet!")
        return TotalEcologicImpact
    
    if 19 > TotalEcologicImpact >= 13:
        print("You\'re trying, keep it up!")
        return TotalEcologicImpact
    
    if 13 > TotalEcologicImpact >= 6: 
        print("You’re almost at the maximum, don’t give up!")
        return TotalEcologicImpact
    
    if TotalEcologicImpact < 6:
        print("You are an example to follow, you must be a guide!")
        return TotalEcologicImpact
    
#Coefficient for Ecological Footprint Calculation
CoeffWater = 0.012
CoeffElectricity = 0.009
CoeffTransport = 0.009 
CoeffWasteFood = 0.05
CoeffMeatConsumtion = 0.03
CoeffOrganicFood = -0.03
CoeffCyclingWalkingDistance = -0.06
CoeffCarpoolingPublicTransport = -0.04

def ReportwaterConsumption(UserActivities): 
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Username', y='WaterConsumption', data=UserActivities)
    plt.title('Water consumption per user')
    plt.xlabel('User')
    plt.ylabel('Water Consumption')
    plt.savefig('static/water_consumption_plot.png')


def ReportElectricityConsumption(UserActivities): 
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Username', y='ElectricityConsumption', data=UserActivities)
    plt.title('Electricity consumption per user')
    plt.xlabel('User')
    plt.ylabel('Electricity consumption')
    plt.savefig('static/electricity_consumption_plot.png')

def ReportTransport(UserActivities): 
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Username', y='Transport', data=UserActivities)
    plt.title('Number of transports per user')
    plt.xlabel('User')
    plt.ylabel('transport')
    plt.savefig('static/transport_plot.png')

def ReportwasteFood(UserActivities): 
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Username', y='WasteFood', data=UserActivities)
    plt.title('Food wasted per user')
    plt.xlabel('User')
    plt.ylabel('Wasted food')
    plt.savefig('static/Waste_Food_plot.png')

def ReportMeatConsumption(UserActivities): 
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Username', y='MeatConsumption', data=UserActivities)
    plt.title('Meat consumption per user')
    plt.xlabel('User')
    plt.ylabel('Meat consumption')
    plt.savefig('static/Meat_Consumption_plot.png')

def ReportOrganicFood(UserActivities): 
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Username', y='OrganicFood', data=UserActivities)
    plt.title('Consumption of organic food per user')
    plt.xlabel('User')
    plt.ylabel('Consumption of organic food')
    plt.savefig('static/Organic_food_plot.png')

def ReportCyclingWalkingDistance(UserActivities): 
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Username', y='CyclingWalkingDistance', data=UserActivities)
    plt.title('CyclingWalkingDistance')
    plt.xlabel('User')
    plt.ylabel('CyclingWalkingDistance')
    plt.savefig('static/Cycling_Walking_Distance_plot.png')

def ReportCarpoolingPublicTransport(UserActivities): 
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Username', y='CarpoolingPublicTransport', data=UserActivities)
    plt.title('CarpoolingPublicTransport')
    plt.xlabel('User')
    plt.ylabel('CarpoolingPublicTransport')
    plt.savefig('static/Carpooling_Public_Transport_plot.png')

def ReportTotalEcologicImpact(UserActivities):
    fig = px.scatter(UserActivities, x='Username', y='TotalEcologicImpact', title='Total Ecologic Impact')
    fig.write_html('static/TotalEcologicImpact.html')

# Schedule daily reset at midnight
schedule.every().day.at("00:00").do(ResetDailyScore)

# Execution loop to monitor scheduled tasks
while True:
    schedule.run_pending()
    # Wait 20 minutes between each check
    time.sleep(1200)  