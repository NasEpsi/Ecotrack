#importing the library we will need
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import schedule
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt, QThread, QTimer
import requests
from bs4 import BeautifulSoup

#Database to store users’ green activities
UserData = pd.DataFrame(columns=['Username', 'WaterConsumption', 'ElectricityConsumption', 'Transport', 'WasteFood', 'MeatConsumption', 'ConsumptionOrganicFood', 'CyclingWalkingDistance', 'CarpoolingPublicTransport', 'Date'])
UserData['Date'] = pd.to_datetime('today').normalize()

#Function to reset the score every day by keeping the data in a database
def ResetDailyScore():
    global UserData

    #Sauvegarder les données actuelles
    UserData.to_csv('current_data.csv', index=False)

    # Back up historical data
    HistoricalData = UserData.copy()
    HistoricalData.to_csv('historical_data.csv', index=False)

    # Reset the DataFrame UserData
    UserData = pd.DataFrame(columns=['Username', 'WaterConsumption', 'ElectricityConsumption', 'Transport', 'WasteFood', 'MeatConsumption', 'ConsumptionOrganicFood', 'CyclingWalkingDistance', 'CarpoolingPublicTransport', 'Date'])
    UserData['Date'] = pd.to_datetime('today').normalize()

#Coefficient for Ecological Footprint Calculation
CoeffWater = 0.012
CoeffElectricity = 0.009
CoeffTransport = 0.009 
CoeffWasteFood = 0.05
CoeffMeatConsumption = 0.03
CoeffOrganicFood = -0.03
CoeffCyclingWalkingDistance = -0.06
CoeffCarpoolingPublicTransport = -0.04

#Function to calculate user’s ecological footprint
def CalculateEcologicFootprint(UserActivities):

    # Filter activities by current date
    UserActivities = UserActivities[UserActivities['Date'] == pd.to_datetime('today').normalize()]
    
    #Calculation based on ecological activities
    WaterImpact = np.sum(UserActivities['WaterConsumption'] * CoeffWater)
    ElectricityImpact = np.sum(UserActivities['ElectricityConsumption'] * CoeffElectricity)
    TransportImpact = np.sum(UserActivities['Transport'] * CoeffTransport)
    MeatConsumptionImpact = np.sum(UserActivities['MeatConsumption'] * CoeffMeatConsumption)
    wasteFoodImpact = np.sum(UserActivities['WasteFood'] * CoeffWasteFood)
    OrganicFoodImpact = np.sum(UserActivities['ConsumptionOrganicFood'] * CoeffOrganicFood)
    CyclingWalkingDistance = np.sum(UserActivities['CyclingWalkingDistance'] * CoeffCyclingWalkingDistance)
    CarpoolingPublicTransport = np.sum(UserActivities['CarpoolingPublicTransport'] * CoeffCarpoolingPublicTransport)

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
    sns.barplot(x='Username', y='ConsumptionOrganicFood', data=UserActivities)
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

# Function to retrieve ecological tips from an API or web scraping
def GetEcoTips():
    # Example of web scraping for tips from a website
    try:
        Url = 'https://example.com/eco-tips'
        Response = requests.get(Url)
        Soup = BeautifulSoup(Response.text, 'html.parser')
        Tips = Soup.find_all('div', class_='eco-tip')
    
        # Retrieve Tips
        EcoTips = [Tip.text for Tip in Tips]
        return EcoTips
    
    except requests.exceptions.RequestException as e:
        QMessageBox.critical("Error when accessing the network:", e)
        return []

# User interface with PyQt
class EcoTipsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ecological Tips')
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel('Click the button for eco-friendly tips.')
        self.layout.addWidget(self.label)
        
        self.button = QPushButton('Tips')
        self.button.clicked.connect(self.ShowEcoTips)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)

        # Function to display eco-friendly tips
    def ShowEcoTips(self):
        eco_tips = GetEcoTips()
        tips_text = '\n'.join(eco_tips)
        self.label.setText(tips_text)

# Class for the dashboard page
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dashboard')
        
        # Add widgets to display charts and user information
        self.layout = QVBoxLayout()
        self.label = QLabel('Dashboard Page')
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

# Class for Green Activity Input Page
class ActivitiesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Enter Activities')
        
        # Add widgets to capture green activities
        self.layout = QVBoxLayout()

        self.water_label = QLabel('Water Consumption:')
        self.water_input = QLineEdit()
        self.layout.addWidget(self.water_label)
        self.layout.addWidget(self.water_input)
        
        self.electricity_label = QLabel('Electricity Consumption:')
        self.electricity_input = QLineEdit()
        self.layout.addWidget(self.electricity_label)
        self.layout.addWidget(self.electricity_input)
        
        self.transport_label = QLabel('Transport:')
        self.transport_input = QLineEdit()
        self.layout.addWidget(self.transport_label)
        self.layout.addWidget(self.transport_input)

        self.wasteFood_label = QLabel('WasteFood:')
        self.wasteFood_input = QLineEdit()
        self.layout.addWidget(self.wasteFood_label)
        self.layout.addWidget(self.wasteFood_input)

        self.meatConsum_label = QLabel('MeatConsumption')
        self.meatConsum_input = QLineEdit()
        self.layout.addWidget(self.meatConsum_label)
        self.layout.addWidget(self.meatConsum_input)

        self.organicFood_label = QLabel('ConsumptionOrganicFood:')
        self.organicFood_input = QLineEdit()
        self.layout.addWidget(self.organicFood_label)
        self.layout.addWidget(self.organicFood_input)

        self.CWD_label = QLabel('CyclingWalkingDistance:')
        self.CWD_input = QLineEdit()
        self.layout.addWidget(self.CWD_label)
        self.layout.addWidget(self.CWD_input)

        self.CPT_label = QLabel('CarpoolingPublicTransport:')
        self.CPT_input = QLineEdit()
        self.layout.addWidget(self.CPT_label)
        self.layout.addWidget(self.CPT_input)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_activities)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def submit_activities(self):
        # Retrieve the values entered by the user
        # Add validation to ensure user entries are valid numbers
        try:
            water_consumption = float(self.water_input.text())
            electricity_consumption = float(self.electricity_input.text())
            transport = float(self.transport_input.text())
            waste_food = float(self.wasteFood_input.text())
            meat_consumption = float(self.meatConsum_input.text())
            organic_food = float(self.organicFood_input.text())
            cycling_walking_distance = float(self.CWD_input.text())
            carpooling_public_transport = float(self.CPT_input.text())
        except ValueError:
            # Handle error if user entry is not a valid number
            QMessageBox.critical(self, 'Error', 'Please enter valid numeric values for activities.')

        # Add activities to UserData database
        global UserData
        UserData = UserData.append({'Username': 'User1',
                                    'WaterConsumption': water_consumption,
                                    'ElectricityConsumption': electricity_consumption,
                                    'Transport': transport,
                                    'WasteFood': waste_food,
                                    'MeatConsumption': meat_consumption,
                                    'ConsumptionOrganicFood': organic_food,
                                    'CyclingWalkingDistance': cycling_walking_distance,
                                    'CarpoolingPublicTransport': carpooling_public_transport,
                                    'Date': pd.to_datetime('today').normalize()})

# Class for Reports page
class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Reports')
        
        # Add widgets to view reports and charts
        self.layout = QVBoxLayout()

        self.buttonWater = QPushButton('Generate Water Consumption Report')
        self.buttonWater.clicked.connect(self.generate_water_consumption_report)
        self.layout.addWidget(self.buttonWater)

        self.buttonElectricity = QPushButton('Generate Electricity Consumption Report')
        self.buttonElectricity.clicked.connect(self.generate_electricity_consumption_report)
        self.layout.addWidget(self.buttonElectricity)

        self.buttonTransport = QPushButton('Generate Transport Report')
        self.buttonTransport.clicked.connect(self.generate_transport_report)
        self.layout.addWidget(self.buttonTransport)

        self.buttonWasteFood = QPushButton('Generate waste Food Report')
        self.buttonWasteFood.clicked.connect(self.generate_waste_food_report)
        self.layout.addWidget(self.buttonWasteFood)

        self.buttonMeatConsumption = QPushButton('Generate Meat Consumption Report')
        self.buttonMeatConsumption.clicked.connect(self.generate_meat_consumption_report)
        self.layout.addWidget(self.buttonMeatConsumption)

        self.buttonOrganicFood = QPushButton('Generate Organic Food consumption Report')
        self.buttonOrganicFood.clicked.connect(self.generate_organic_food_consumption_report)
        self.layout.addWidget(self.buttonOrganicFood)

        self.buttonCWD = QPushButton('Generate Cycling and Walking Distance Report')
        self.buttonCWD.clicked.connect(self.generate_cycling_and_walking_distance_report)
        self.layout.addWidget(self.buttonCWD)

        self.buttonCPT = QPushButton('Generate Carpooling Public Transport Report')
        self.buttonCPT.clicked.connect(self.generate_carpooling_public_transport_report)
        self.layout.addWidget(self.buttonCPT)

        self.buttonTotal = QPushButton('Generate Total Ecologic Impact Report')
        self.buttonTotal.clicked.connect(self.generate_total_impact_report)
        self.layout.addWidget(self.buttonTotal)

        self.setLayout(self.layout)

    
    def generate_water_consumption_report(self):
        ReportwaterConsumption(UserData)

    def generate_electricity_consumption_report(self):
        ReportElectricityConsumption(UserData)

    def generate_transport_report(self):
        ReportTransport(UserData)

    def generate_waste_food_report(self):
        ReportwasteFood(UserData)

    def generate_meat_consumption_report(self):
        ReportMeatConsumption(UserData)

    def generate_organic_food_consumption_report(self):
        ReportOrganicFood(UserData)

    def generate_cycling_and_walking_distance_report(self):
        ReportCyclingWalkingDistance(UserData)

    def generate_carpooling_public_transport_report(self):
        ReportCarpoolingPublicTransport(UserData)

    def generate_total_impact_report(self):
        ReportTotalEcologicImpact(UserData)

# Main class to manage pages with QStackedWidget
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        
        self.stacked_widget = QStackedWidget()
        
        self.dashboard_page = DashboardPage()
        self.activities_page = ActivitiesPage()
        self.reports_page = ReportsPage()
        self.eco_tips_page = EcoTipsWindow()
        
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.activities_page)
        self.stacked_widget.addWidget(self.reports_page)
        self.stacked_widget.addWidget(self.eco_tips_page)

        self.layout = QVBoxLayout()

        # Add buttons to switch between pages
        self.button_dashboard = QPushButton('Dashboard')
        self.button_dashboard.clicked.connect(self.show_dashboard)
        self.layout.addWidget(self.button_dashboard)
        
        self.button_activities = QPushButton('Activities')
        self.button_activities.clicked.connect(self.show_activities)
        self.layout.addWidget(self.button_activities)
        
        self.button_reports = QPushButton('Reports')
        self.button_reports.clicked.connect(self.show_reports)
        self.layout.addWidget(self.button_reports)

        self.button_eco_tips = QPushButton('Eco Tips')  # Bouton pour accéder à la page des conseils
        self.button_eco_tips.clicked.connect(self.show_eco_tips)  # Connectez le bouton à la méthode show_eco_tips
        self.layout.addWidget(self.button_eco_tips)
        
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

    def show_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_page)
        
    def show_activities(self):
        self.stacked_widget.setCurrentWidget(self.activities_page)
        
    def show_reports(self):
        self.stacked_widget.setCurrentWidget(self.reports_page)

    def show_eco_tips(self):
        self.stacked_widget.setCurrentWidget(self.eco_tips_page)

# Class to run the queue loop in a separate thread
class ScheduleThread(QThread):
    def run(self):
        # Execution loop to monitor scheduled tasks
        while True:
            schedule.run_pending()
            # Wait 20 minutes between each check
            time.sleep(1200)

# Main function to run the PyQt application
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Create and start the thread for task scheduling
    schedule_thread = ScheduleThread()
    schedule_thread.start()

    sys.exit(app.exec_())

# Schedule daily reset at midnight
schedule.every().day.at("00:00").do(ResetDailyScore)
  

# PyQt application launch
if __name__ == '__main__':
    main()