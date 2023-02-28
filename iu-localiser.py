#!/usr/bin/env python
# coding: utf-8


# This file will be used to cluseter the 10 nearest locations to a GPA coordinate
import pandas as pd
import numpy as np
from tqdm import tqdm
import PySimpleGUI as sg


def find_closest_locations(user_gps, df, n=None):

       user_lat, user_lng = user_gps

       # For each value in W3W column
       for index, row in tqdm(df.iterrows(), total=df.shape[0]):

              try:
                     # Read GPS
                     gps = row['GPS']
                     lat, lng = gps.split(', ')
                     lat, lng = float(lat), float(lng)

                     # Calculate dmanhattan istance between user and W3W
                     distance = np.sqrt((user_lat - lat)**2 + (user_lng - lng)**2)

                     # Save the distance to the dataframe
                     df.at[index, 'Distance'] = distance
              except Exception as e:
                    raise ValueError(f'Error at index {index}\n {e}')


       # Sort DF by distance and save
       df = df.sort_values(by=['Distance'], ascending=True)

       # Only use columns Item id, Name, GPS, Distance Номер телефону, Контактні засоби, Скільки вікон у вас розбито?, Яка ваша адреса?
       df = df[['Name', 'GPS', 'Номер телефону', 'Контактні засоби', 'Скільки вікон у вас розбито?', 'Яка ваша адреса?']]
       df['Номер телефону'] = [f"\'+{int(tel_i)}" for tel_i in df['Номер телефону']]

       df.to_csv(f'~/Downloads/Sorted_{user_lat}_{user_lng}.csv')
       print(f'File saved to ~/Downloads/Sorted_{user_lat}_{user_lng}.csv')




sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.InputText("Enter your latitude here", key='lat')],
            [sg.InputText("Enter your longitude here", key='lng')],
            # Allow use to select a file
            [sg.Text('Select a file'), sg.Input(key='file'), sg.FileBrowse(key='file')],
            [sg.Button('Ok'), sg.Button('Cancel')] ]



import sys
if __name__ == '__main__':

       # Add test argument to run with test data
       if sys.argv[1] == 'test':
              # Run file with test data
              df = pd.read_excel('~/Downloads/Customer_Tracker_Payment_Due_1677569125.xlsx', header=2, index_col=12)
              # Remove rows where GPS is NaN
              df = df[df['GPS'].notna()]
              user_gps = (15, 15)

              find_closest_locations(user_gps, df)

       else:
              # Create the Window
              window = sg.Window('Window Title', layout)
              # Event Loop to process "events" and get the "values" of the inputs
              while True:
                     event, values = window.read()
                     if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                            break
                     print(f'You entered {values}')

                     # Read in the file
                     df = pd.read_excel(values['file'], header=2, index_col=12)

                     # Remove rows where GPS is NaN
                     df = df[df['GPS'].notna()]
                     user_gps = (float(values['lat']), float(values['lng']))

                     find_closest_locations(user_gps, df)

                     # Change window to loading screen

              window.close()

       
