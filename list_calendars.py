# Import knihoven
from cal_setup import get_calendar_service
import datetime
import re

# Funkce na získání nejbližších akcích z google kalendáře
# DEBUG_PRINT_OUTS -> Vypisování informací do console
# from_now -> True => vrátí pouze nadcházející, False => vrátí všechny eventy
def get_calendars(DEBUG_PRINT_OUTS, from_now, calendar_id):
   real_out = []
   service = get_calendar_service()

   # Dnešní datum
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   # Získání eventů z kalendáře
   events_out = None
   if(from_now):
       events_out = service.events().list(calendarId=calendar_id, timeMin=now, # Najde všechny nadcházející eventy a srovná je chronologicky
                                        maxResults=100, singleEvents=True,
                                        orderBy='startTime').execute()
   else:
       events_out = service.events().list(calendarId=calendar_id, # Najde všechny eventy eventy v daném kalendáři a srovná je chronologicky
                                         maxResults=100, singleEvents=True,
                                         orderBy='startTime').execute()

   # Projití všech eventů
   for event in events_out['items']:
       output = []
       #print(event)
       if(DEBUG_PRINT_OUTS):
           print(event['summary'])
       # Připsání názvu eventu
       output.append(event['summary'])


       # -------------------------------------------------------------------------------------------
       # Pokusy o získání popisu eventu
       # Pokud je v eventu napsaný popis
       try:
           text = event['description']
           text = re.sub('<[^<]+?>', ' ', text) # Odstranění HTML tagů
           output.append(text)
           if(DEBUG_PRINT_OUTS):
               print(text)
       # Pokud není popis
       except:
           output.append("Tento event nemá popis.")
           if(DEBUG_PRINT_OUTS):
               print("Tento event nemá popis.")
       # -------------------------------------------------------------------------------------------
       # Pokusy o získání data začátku eventu
       # Pokud je v eventu napsané jenom datum a ne čas
       try:
          format = "%Y-%m-%d"
          intp = event['start']['date']
          dt_object = datetime.datetime.strptime(intp, format)
          if(DEBUG_PRINT_OUTS):
              print(str(dt_object.day) + "." + str(dt_object.month) + "." + str(dt_object.year))
          output.append(str(dt_object.day) + "." + str(dt_object.month) + "." + str(dt_object.year))
       # Pokud je datum i čas
       except:
          format = "%Y-%m-%dT%H:%M:%S%z"
          intp = event['start']['dateTime']
          dt_object = datetime.datetime.strptime(intp, format)
          minutes = str(dt_object.minute)
          if(minutes == "0"):
              minutes = "00"
          if(DEBUG_PRINT_OUTS):
              print(str(dt_object.day) + "." + str(dt_object.month) + "." + str(dt_object.year) + " " + str(dt_object.hour) + ":" + minutes)
          output.append(str(dt_object.day) + "." + str(dt_object.month) + "." + str(dt_object.year) + " " + str(dt_object.hour) + ":" + minutes)

       # -------------------------------------------------------------------------------------------
       # Pokusy o získání data začátku eventu
       # Pokud je v eventu napsané jenom datum a ne čas
       try:
           if(event['start']['date'] != event['end']['date']):
               format = "%Y-%m-%d"
               intp = event['end']['date']
               dt_object = datetime.datetime.strptime(intp, format)
               if(DEBUG_PRINT_OUTS):
                   print(str(dt_object.day) + "." + str(dt_object.month) + "." + str(dt_object.year))
               output.append(str(dt_object.day) + "." + str(dt_object.month) + "." + str(dt_object.year))
       except:
           # Jestliže v eventu není datum, pak tam musí být datum a čas.
           # Pokud, kašlu na to... mě ty kmentáře nebaví, vy to snad pochopíte =)
           try:
               if(event['start']['dateTime'] != event['end']['dateTime']):
                   format = "%Y-%m-%dT%H:%M:%S%z"
                   intp = event['end']['dateTime']
                   dt_object = datetime.datetime.strptime(intp, format)
                   minutes = str(dt_object.minute)
                   if(minutes == "0"):
                       minutes = "00"
                   if(DEBUG_PRINT_OUTS):
                       print(str(dt_object.day) + "." + str(dt_object.month) + "." + str(dt_object.year) + " " + str(dt_object.hour) + ":" + minutes)
                   output.append(str(dt_object.day) + "." + str(dt_object.month) + "." + str(dt_object.year) + " " + str(dt_object.hour) + ":" + minutes)
           except:
               output.append(None)
               if(DEBUG_PRINT_OUTS):
                   print("Do match") # Prostě se datum a čas začátku schodoují s koncem eventu

        # -------------------------------------------------------------------------------------------
       if(DEBUG_PRINT_OUTS):
           print(output)
           print("--------------------")
       # Přidání aktuálně rozpracovaného eventu do pole výsledků
       output.append(event['htmlLink'])
       real_out.append(output)

   if(DEBUG_PRINT_OUTS):
       print(real_out)
   return real_out # Vrácení eventů v použitelnějším formátu

if __name__ == '__main__':
   get_calendars(True, False, 'medvediberoun@skaut.cz')
