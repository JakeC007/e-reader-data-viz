"""
Jan 25, 2020
Jake Chanenson
Quick script to clean the kindle data so that JSON parsers can parse.
"""

def main():
  fileName = input("Please enter the full file name of the kindle data without the extension: ")
  #fileName = 'jan2021_kindle_data'
  data = readKindleData(fileName)
  writeCleanedData(fileName, data)
  
  numLines = sum(1 for line in open(fileName+'_CLEANED.json'))
  print(f"Your data is cleaned! The file is titled {fileName}_CLEANED.json\nThere are {numLines-2} entries in your file.")
  
def readKindleData(fileName):
  """
  Reads in the kindle data and processes it.
  @param: fileName - takes the file name before the extension
  @returns: data - cleaned json data
  """
  
  with open(fileName+'.json', "r") as f:
    foo = []
    for line in f:
      foo.append(line.split("=")[1].strip('\n')) # grab the json str after the '='
      data = ',\n'.join(foo) # need to put commas between top level json for array creation

  return data

def writeCleanedData(fileName, data):
  """
  Writes the new file of cleaned json data.
  @param: 
      fileName - takes the file name before the extension
      data - cleaned data
  @returns: None
  """
  
  with open (fileName+'_CLEANED.json', "w") as nf:
    nf.write('[\n')
    nf.write(data)
    nf.write('\n]\n')

main()
