# Imports
import de_core_news_sm #spacy
import json

# Housenumber - Checks if house number exists in Tweet and adds it to the street
class Housenumber():

    def add_housenumber(self, location, text):
        positionLoc = text.find(location)
        positionNum = positionLoc + len(location) + 1
        number = ""
        location = location + " "
        for x in range(4):
            if text[positionNum + x].isnumeric():
                number = text[positionNum + x]
                location = location + number
            else:
                return location

        return location

# Main-Methode
if __name__ == '__main__':
    
    try:        
        #house_number = Housenumber()
        
        # Read tweets from fileLocation
        fileTweets = open("tweets.txt", "r")
        fileLocation = open("locations.txt", "w")
        nlp = de_core_news_sm.load()
        for line in fileTweets:
            tweet = json.loads(line)
            tweetText = tweet["text"]    
        
            # Entity Detection          
            nlpTweet= nlp(tweetText)        
            entities=[(i, i.label_, i.label) for i in nlpTweet.ents]   
            
            # write result in json format to file
            for obj in entities:
                #try:
                #    location = house_number.add_housenumber(str(obj[0]), tweet["text"])
                #except (Exception) as error :
                location = str(obj[0])

                loc = {
                    "text": tweet["text"],
                    "date": tweet["date"],
                    "author": tweet["author"],
                    "location": location.strip(),
                    "label": str(obj[1])
                    }
    
                jsonLoc = json.dumps(loc)
                fileLocation.write(jsonLoc + "\n")
                       
    except (Exception) as error :
        print("NamedEntities konnten nicht ermittelt werden.",error)
        
    finally:
        fileLocation.close()
        fileTweets.close()