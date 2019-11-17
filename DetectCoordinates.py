# Imports
import psycopg2
import json
import herepy
import authentification

# City Preprocessor - Replaces umlauts from the place name
class CityPreprocessor():
    
    def preprocessor(self, city):

        # Replace umlauts
        city = city.replace("\u00e4", "ae")
        city = city.replace("\u00f6", "oe")
        city = city.replace("\u00fc", "ue")
        city = city.replace("\u00df", "ss")
        city = city.replace("\u00c4","Ae")
        city = city.replace("\u00d6","Oe")
        city = city.replace("\u00dc","Ue")
        return city

# Database Authentification - Connection to the database is established    
class DatabaseAuthenification():
    
    def dbConnection(self):
        # Connect to Database - psycopg2 to execute PostgreSQL command through Python source code
        connection = psycopg2.connect(user = authentification.user,
                                      password = authentification.password,
                                      host = authentification.host,
                                      port = authentification.port,
                                      database = authentification.database)
        return connection

# Database Query - Query of the database whether car license plate exists    
class DatabaseQuery():
    
    def queryDatabase(self, namedEntity):
        postgreSQL_Query = "select district from numberplate where acronym = '" + namedEntity["location"] + "';"
        try: 
            cursor.execute(postgreSQL_Query) 
            numberplate_records = cursor.fetchall() 
    
            recordsArray = numberplate_records[0]
            location["location"] = recordsArray[0]
        except (Exception) as error :
            print("kein Nummernschild")
            
# Location to Json - If location is in Germany, the location with the required information is returned in Json format 
class LocationToJson():
    
    def locToJson(self, response, index):
        # Determine coordinates from response-Json
        responseKey = response.__getattribute__("Response")
        metaInfo = responseKey["MetaInfo"]
        view = responseKey["View"]
        view = view[0]
        result = view["Result"]
        locationArray = result[0]
        location = locationArray["Location"]
        position = location["DisplayPosition"]
        latitude = position["Latitude"]
        longitude = position["Longitude"]
    
        # Determine city from response-Json
        address = location["Address"]
        city = address["Label"]
        country = address["Country"]
        if (country == "DEU"):
            nEntity = json.loads(lines[index])
        
            loc = {
                "text": nEntity["text"],
                "date": nEntity["date"],
                "author": nEntity["author"],
                "location": nEntity["location"],
                "locLabel": city_preprocessor.preprocessor(city),
                "latitude": latitude,
                "longitude" : longitude
                }
            jsonLoc = json.dumps(loc)
            return jsonLoc
        
        return False

# Location Combination - Checks whether two names together describe a place. If this is the case, the location is saved in a file. 
class Locationcombination():

    def combine_locations(self, locations, namedEntity, numLine):   
        i = 0
        while i < len(locations)-1:
            j = i+1
            while j < len(locations):                
                try:    
                    index1 = numLine - len(locations) + i 
                    index2 = numLine - len(locations) + j
                    comLocation = locations[i] + " " + locations[j] 
                    response = geocoderApi.free_form(comLocation)
                    jsonLoc = loc_json.locToJson(response, index1)
                    
                    if jsonLoc != False:
                        # check the city for location content
                        jsonReturn = json.loads(jsonLoc)
                        locLabel = jsonReturn["locLabel"] 
                        if (locLabel.find(locations[i]) != -1) and (locLabel.find(locations[j]) != -1):                                
                            jsonReturn["location"] = comLocation
                            jsonLoc = json.dumps(jsonReturn)
                            #Write in File
                            fileCoordinates.write(jsonLoc + "\n")
                            combinations.append(index1)
                            combinations.append(index2)
                except (Exception) as error :
                    print("kein Ort enthalten")
                j += 1
            i += 1
   
        locations.clear()
        locations.append(namedEntity["location"])
        
        return namedEntity["text"]

# Delete Location - If the location is already used as a combination, it is deleted from the list so that it is not determined twice     
class DeleteLocation():

    def delete_comloc(self, combinations):
        num = 0
        combinations.sort()
        combinations = sorted(set(combinations), key=combinations.index)
        for entry in combinations:
            del lines[entry - num]
            num += 1
        return combinations

# Main-Methode
if __name__ == '__main__':

    try:
        # Create class objects
        city_preprocessor = CityPreprocessor()
        db_auth = DatabaseAuthenification()
        db_query = DatabaseQuery()
        loc_json = LocationToJson()
        loc_combination = Locationcombination()
        delete_loc = DeleteLocation()
                    
        # Save locations in list       
        try:
            fileLocation = open("locations.txt", "r")
            lines = []                    
            for line in fileLocation:
                line = line.replace("\n", "")
                lines.append(line)
        except (Exception) as error :
            print ("File konnte nicht ausgelesen werden: ", error) 
            
        finally:
            fileLocation.close()      

        # Query Database for locations        
        try:
            connectionDB = db_auth.dbConnection()
            cursor = connectionDB.cursor()    
            for line in lines:  
                namedEntity = json.loads(line)
                queryDb = db_query.queryDatabase(namedEntity)
                        
        except (Exception) as error :
            print ("Datenbankabfrage konnte nicht durchgefuehrt werden: ", error)
                 
        finally:
            if(connectionDB):
                cursor.close()
                connectionDB.close()
                                            
        # Query spaCy for locations
        try:
            fileCoordinates = open("coordinates.txt", "w")
            geocoderApi = herepy.GeocoderApi(authentification.appID, authentification.appCode)

            #Combine named Entities
            locations = []
            combinations = []
            numLine = 0 
            tweet = ""                   
            for line in lines:
                namedEntity = json.loads(line)
                if (numLine == 0):            
                    locations.append(namedEntity["location"])
                    tweet = namedEntity["text"]
                elif ((tweet == namedEntity["text"])== True):
                    locations.append(namedEntity["location"])            
                else:
                    tweet = loc_combination.combine_locations(locations,namedEntity,numLine)
                numLine += 1
            comb = loc_combination.combine_locations(locations,namedEntity,numLine)
            
            combinations = delete_loc.delete_comloc(combinations)
            
            # Check single Entities
            numLine = 0
            for line in lines:
                namedEntity = json.loads(line)               
                try: 
                    if ((namedEntity["location"] == "Sued") | (namedEntity["location"] == "West") | (namedEntity["location"] == "Nord") | (namedEntity["location"] == "Ost")| (namedEntity["location"] == "Mitte")) == False:
                        response = geocoderApi.free_form(namedEntity["location"])
                        jsonLoc = loc_json.locToJson(response, numLine)
                        if jsonLoc != False:
                            #Write in File
                            fileCoordinates.write(jsonLoc + "\n")
                except (Exception) as error :
                    print("kein Ort enthalten")
                numLine += 1        
        except (Exception) as error :
            print("Orte konnten nicht ermittelt werden")
                
        finally:  
            fileCoordinates.close()
            
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to or fetching Data", error)