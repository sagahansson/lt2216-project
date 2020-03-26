from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
import random

OOO_list = [("Cheese, milk, butter, yoghurt.", 
             "milk", 
             "All the others are made FROM milk.", 
             "Think about how the items are produced."),
           ("Airplane, raven, ostrich, hot air balloon.", 
            "ostrich", 
            "Ostrich is the only one that doesn't fly.", 
            "Think about the means of transportation."),
           ("Socks, boots, mittens, slippers", 
            "mittens", 
            "Mittens are worn on your hands, while all the others are worn on your feet.", 
            "Think about what they make warm."),
           ("Optician, police station, post office, pharmacy", 
            "police station", 
            "Police stations don't sell things, while the other places do.", 
            "Think about what you'd do in the different places."),
           ("Bus, lorry, bicycle, car", 
            "bicycle", 
            "A bicycle is moved by foot pedals, all the others are motorised.", 
            "Think about what makes them move."),
           ("Now, low, cow, vow", 
            "low", 
            "In 'low', -ow is pronounced differently from how it's pronouned in the rest.", 
            "Say them out loud."),
           ("Tough, puff, dough, enough", 
            "dough", 
            "Dough is the only one with the /oʊ/ sound, all the others have a /ʌf/ sound.", 
            "Try pronouncing them.")]


class ActionGameStart(Action):

    def name(self) -> Text:
        
        return "action_game_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        former_rand = tracker.get_slot("rand") 
        former_ooo = tracker.get_slot("whatooo")
        
        if type(former_ooo) == list:
            if tuple(former_ooo) in OOO_list:
                OOO_list.remove(tuple(former_ooo))
        if len(OOO_list) == 0:
            dispatcher.utter_message(text="Unfortunately I've run out of questions. Goodbye!")
            return []
        else:

            setup_q = "Which one is the odd one out? "
            rand = random.choice(range(len(OOO_list)))
            whatooo = OOO_list[rand]
            
            dispatcher.utter_message(text=setup_q + (whatooo[0]))
            
            return [SlotSet("rand", rand), SlotSet("whatooo", whatooo)]

class ActionEvaluate(Action):

    def name(self) -> Text:
        return "action_evaluate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #usermessageanswer = (tracker.latest_message['text']).lower()
        user_intent = tracker.latest_message['intent']['name']
        whatooo = tuple(tracker.get_slot("whatooo")) 
        
        print(tracker.latest_message['text'])
        #print("latest message: ",tracker.latest_message)
        print(tracker.latest_message['intent']['name'])
        
        if user_intent == whatooo[1]:
            
            dispatcher.utter_message(text="Correct! " + whatooo[2] + " Wanna go again?")
            return []
        else:
            dispatcher.utter_message(text="Nope, try again!")
        
            return []
        

        
class ActionRepeat(Action):

    def name(self) -> Text:
        return "action_repeat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        whatooo = tuple(tracker.get_slot("whatooo")) 
        setup_q = "Which one is the odd one out? "
        
        dispatcher.utter_message(text=setup_q + whatooo[0])

        return []

        
class ActionHint(Action):

    def name(self) -> Text:
        return "action_hint"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        whatooo = tuple(tracker.get_slot("whatooo")) 
        dispatcher.utter_message(text=whatooo[3])

        return []

    

class ActionExplain(Action):

    def name(self) -> Text:
        return "action_explain"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        whatooo = tuple(tracker.get_slot("whatooo")) 
        setup_s = "The answer is "
        another_q = "Do you want to have a go at another one?"
        
        dispatcher.utter_message(text=setup_s + whatooo[1] + ". " + whatooo[2] + "\n" + another_q)

        return []