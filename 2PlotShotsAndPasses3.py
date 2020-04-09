#Make a shot map and a pass map using Statsbomb data
#Set match id in match_id_required.

#Function to draw the pitch
import matplotlib.pyplot as plt
import numpy as np

#Size of the pitch in yards (!!!)
pitchLengthX=120
pitchWidthY=80

#ID for England vs Sweden Womens World Cup
match_id_required = 69301
home_team_required ="England Women's"
away_team_required ="Sweden Women's"
player_required = "Sara Caroline Seger"

# Load in the data
# I took this from https://znstrider.github.io/2018-11-11-Getting-Started-with-StatsBomb-Data/
file_name=str(match_id_required)+'.json'

#Load in all match events 
import json
with open('Statsbomb/data/events/'+file_name) as data_file:
    #print (mypath+'events/'+file)
    data = json.load(data_file)

#get the nested structure into a dataframe 
#store the dataframe in a dictionary with the match id as key (remove '.json' from string)
from pandas.io.json import json_normalize
df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])

#A dataframe of shots
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')

#Draw the pitch
from FCPython import createPitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')

#Exercise: 
#1, Create a dataframe of passes which contains all the passes in the match
#2, Plot the start point of every Sweden pass. Attacking left to right.
#3, Plot only passes made by Caroline Seger (she is Sara Caroline Seger in the database)
#4, Plot arrows to show where the passes we

#1  dataframe of passes
passes = df.loc[df['type_name'] == 'Pass'].set_index('id')

#3 plot passes made by Caroline
#3 plot arrows to show where the passes
for i,passing in passes.iterrows():
    x = passing['location'][0]
    y = passing['location'][1]
    end_x = passing['pass_end_location'][0]
    end_y = passing['pass_end_location'][1]

    team_name=passing['team_name']
    player=passing['player_name']

    circleSize=1
    if(player==player_required):
        passCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="yellow")
        passArrow=plt.Arrow(x,pitchWidthY-y,end_x - x, end_y - y)
        ax.add_patch(passCircle)
        ax.add_patch(passArrow)

plt.text(5,75,player_required + ' passes') 
fig.set_size_inches(10, 7)
fig.savefig('Output/passesSeger.pdf', dpi=100) 
plt.show()

