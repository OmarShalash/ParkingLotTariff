import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

event = ctrl.Antecedent(np.arange(0, 11, 1), 'event')
weather = ctrl.Antecedent(np.arange(0, 11, 1), 'weather')
keyword = ctrl.Antecedent(np.arange(0, 11, 1), 'keyword')
percentage_tarrif = ctrl.Consequent(np.arange(0, 201, 1), 'percentage_tarrif')

weather.automf(5)
keyword.automf(5)
# event.automf(3)

percentage_tarrif['low'] = fuzz.trimf(percentage_tarrif.universe, [0, 25, 50])
percentage_tarrif['L/M'] = fuzz.trimf(percentage_tarrif.universe, [25, 50, 100 ])
percentage_tarrif['medium'] = fuzz.trimf(percentage_tarrif.universe, [75, 100, 125])
percentage_tarrif['M/H'] = fuzz.trimf(percentage_tarrif.universe, [100, 130, 160])
percentage_tarrif['high'] = fuzz.trimf(percentage_tarrif.universe, [120, 160, 200])


event['no'] = fuzz.trimf(weather.universe, [0, 3, 5 ])
event['yes'] = fuzz.trimf(weather.universe, [2, 5, 10])

# weather['Rain'] = fuzz.trimf(weather.universe, [0, 2, 3 ])  //poor
# weather['HugeRain'] = fuzz.trimf(weather.universe, [2, 4, 6])  //mediocre 
# weather['Snow'] = fuzz.trimf(weather.universe, [3, 6, 8])      // average
# weather['Fog'] = fuzz.trimf(weather.universe, [6, 8, 9 ])     //decent
# weather['Tornado'] = fuzz.trimf(weather.universe, [7, 9, 10])  //good


# keyword['Hotel'] = fuzz.trimf(keyword.universe, [0, 2, 3])    //poor
# keyword['Supermarket'] = fuzz.trimf(keyword.universe, [1, 3, 5])   //mediocre 
# keyword['Hospital'] = fuzz.trimf(weather.universe, [3, 5, 6])    // average
# keyword['Cinema'] = fuzz.trimf(keyword.universe, [4, 6, 8])   //decent
# keyword['Bar'] = fuzz.trimf(keyword.universe, [6, 8, 10])   //good


# percentage_tarrif['low'].view()




# rule1= ctrl.Rule(weather['Rain']  & event['yes']  & keyword['Hotel'], percentage_tarrif['low'])
# rule2= ctrl.Rule(weather['Snow']  & event['yes']  & keyword['Supermarket'], percentage_tarrif['L/M'])
# rule3= ctrl.Rule(weather['HugeRain']  & event['no']  & keyword['Hospital'], percentage_tarrif['high'])
# rule4= ctrl.Rule(weather['Tornado']  & event['no']  & keyword['Hotel'], percentage_tarrif['M/H'])
# rule5= ctrl.Rule(weather['HugeRain']  & event['yes']  & keyword['Cinema'], percentage_tarrif['medium'])
# rule6= ctrl.Rule(weather['Rain']  & event['yes']  & keyword['Bar'], percentage_tarrif['high'])
# rule4= ctrl.Rule(weather['Tornado']  & event['no']  & keyword['Supermarket'], percentage_tarrif['low'])
# rule5= ctrl.Rule(weather['HugeRain']  & event['yes']  & keyword['Cinema'], percentage_tarrif['M/H'])
# rule6= ctrl.Rule(weather['Rain']  & event['yes']  & keyword['Bar'], percentage_tarrif['L/M'])

rule1= ctrl.Rule(weather['poor']  & event['yes']  & keyword['poor'], percentage_tarrif['low'])
rule2= ctrl.Rule(weather['average']  & event['yes']  & keyword['mediocre'], percentage_tarrif['L/M'])
rule3= ctrl.Rule(weather['mediocre']  & event['no']  & keyword['average'], percentage_tarrif['high'])
rule4= ctrl.Rule(weather['good']  & event['no']  & keyword['poor'], percentage_tarrif['M/H'])
rule5= ctrl.Rule(weather['mediocre']  & event['yes']  & keyword['decent'], percentage_tarrif['medium'])
rule6= ctrl.Rule(weather['poor']  & event['yes']  & keyword['good'], percentage_tarrif['high'])
rule4= ctrl.Rule(weather['good']  & event['no']  & keyword['mediocre'], percentage_tarrif['low'])
rule5= ctrl.Rule(weather['mediocre']  & event['yes']  & keyword['decent'], percentage_tarrif['M/H'])
rule6= ctrl.Rule(weather['poor']  & event['yes']  & keyword['good'], percentage_tarrif['L/M'])

# rule1= ctrl.Rule(weather['Rain']   & keyword['Hotel'], percentage_tarrif['low'])
# rule2= ctrl.Rule(weather['Snow']   & keyword['Supermarket'], percentage_tarrif['L/M'])
# rule3= ctrl.Rule(weather['Fog']   & keyword['Hospital'], percentage_tarrif['high'])
# rule4= ctrl.Rule(weather['Tornado']   & keyword['Hotel'], percentage_tarrif['M/H'])
# rule5= ctrl.Rule(weather['HugeRain']   & keyword['Cinema'], percentage_tarrif['medium'])
# rule6= ctrl.Rule(weather['Rain']   & keyword['Bar'], percentage_tarrif['high'])

percentage_tarrif_ctrl=ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6])
percentage=ctrl.ControlSystemSimulation(percentage_tarrif_ctrl)

percentage.input['weather']=3
percentage.input['keyword']=6
percentage.input['event']=1
percentage.compute()

print(percentage.output['percentage_tarrif']/100)

percentage_tarrif.view(sim=percentage)

# rule1.view
# rule1.view()

event.view()
weather.view()
keyword.view()
percentage_tarrif.view()

input()