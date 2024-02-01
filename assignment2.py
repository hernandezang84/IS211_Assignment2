import urllib2
import csv
import datetime
import logging
import argparse

def downloadData(url):
    response = urllib2.urlopen(url)
    data = response.read()
    return data

def processData(file_contents):
    data = csv.reader(file_contents.splitlines())
    result = {}
    logger = logging.getLogger('assignment2')

    for i, row in enumerate(data):
        try:
            id, name, birthday_str = row
            birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y')
            result[id] = (name, birthday)
        except Exception as e:
            logger.error(f"Error processing line #{i+1} for ID #{id}")

    return result
    
def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y %m %d')}")
    else:
        print("No user found with that id")

def setup_logger():
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('errors.log')
    logger.addHandler(handler)
    return logger

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL of the CSV file")
    args = parser.parse_args()

    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"Error downloading data from {args.url}: {str(e)}")
        return
    
    logger = setup_logger()

    personData = processData(csvData)

    while True:
        id = int(input("Enter an ID to lookup: "))
        if id <= 0:
            break
        displayPerson(id, personData)

    if __name__ == "__main__":
        main()