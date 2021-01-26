"""
Jan 25, 2020
Jake Chanenson
Quick script that converts kindle json data (cleaned) to a csv file. 
The data is stored in a list of dicts as an intermediary step so you may be able to do other cool things with it.
"""
import json
import csv
import dateutil.parser
from dateutil import tz

def main():
  #read in and then close json file
  with open('kindle_data.json') as json_file: 
    data = json.load(json_file) 

  dataDict, uniqueTitles = parseData(data)
   
  writeCSV(dataDict)

  #print summary of output
  print(f"I have written {len(dataDict)} entries the csv file which represents {len(uniqueTitles)} books")
  
  #the datetime obj is an ISO Standard in UTC
  #lets get EST
  EST = tz.gettz('EST')
 
  #UTC can be converted to any format via strftime, though f strings just need a ":"
  #see https://strftime.org/ for formatting
  print(f"The earliest book was at {dataDict[0]['time'].replace(tzinfo=EST):%x %-I:%M %p}")
  print(f"The most recent book was at {dataDict[-1]['time'].replace(tzinfo=EST):%x %-I:%M %p}")


def parseData(data):
  """
  Creates a dict for each json object. It extracts: title, position, time (UTC), ASIN, and the event type (LastPositionRead, Highlight, etc)
  @param: data - json import
  @returns: 
    retLst - list of dicts. Each dict is the relevent json bits
    uniqueTitles -  list of unique titles
  """
  #set up accums
  retLst = []
  uniqueTitles = set()
  
  #extract data from json
  for i in data:
    foo = {}
    foo['title'] = i['contentReference']['guid'].split(":")[0]
    foo['pos'] = i['position']['pos']
    #GMT (UTC) times regardless of whether a "Z" 
    foo['time'] = dateutil.parser.isoparse(i['modificationDate'])
    foo['asin'] = i['contentReference']['asin'] #Amazon Standard Identification Number 
    foo['evntType'] = i['type']
    retLst.append(foo)

    # generate a list of books
    uniqueTitles.add(foo['title'])

  return retLst, uniqueTitles

def writeCSV(data):
  """
  Writes the extracted json data to a CSV file
  @param: data - list of dicts. each dict has book data
  """
  #set up for csv writing
  csvFile = open('kindle_data.csv', 'w')
  csvWriter = csv.writer(csvFile) 

  #write the header
  header = ['time', 'title', 'pos', 'asin', 'event_type']
  csvWriter.writerow(header)

  #write the data
  for d in data:
    csvWriter.writerow([d['time'], d['title'], d['pos'], d['asin'], d['evntType']])
    
  csvFile.close()


main()
