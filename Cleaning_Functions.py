from bs4 import BeautifulSoup as bs

data = []
# Read the XML file
with open("sample2.osm", "r", encoding="utf8") as file:
    # Read each line in the file, readlines() returns a list of lines
    data = file.readlines()
    # Combine the lines in the list into a string
    data = "".join(data)
    soup = bs(data, "lxml")


#soup = bs(data, "lxml")
zipcode = [] #empty array to store all zip_codes
post_C = soup.find_all("tag", {"k": "addr:postcode"})

for code in post_C:
    zipcode.append(code)
#using beautiful soup to find tags with incorrect zipcodes

#print(zipcode) #printed the zipcodes to ensure they all printed from the entire dataset.

#removing all unwanted zipcodes from our data:
unwanted_codes = soup.find_all("tag", {"k": "addr:postcode"} and {"v": "89434"})
for x in unwanted_codes:
    zipcode.remove(x)

    next_code = soup.find_all("tag", {"k": "addr:postcode"} and {"v":"89431"})   
for a in next_code:
    zipcode.remove(a)
    
bad_zip = soup.find_all("tag", {"k": "addr:postcode"}and {"v":"89432"})
for b in bad_zip:
    zipcode.remove(b)

sp_zip = soup.find_all("tag", {"k": "addr:postcode"}and {"v":"89435"})
for c in sp_zip:
    zipcode.remove(c)
    
sp_zip2 = soup.find_all("tag", {"k": "addr:postcode"}and {"v":"89436"})
for d in sp_zip2:
    zipcode.remove(d)

unknown_zip = soup.find_all("tag", {"k": "addr:postcode"}and {"v":"96118"})
for u in unknown_zip:
    zipcode.remove(u)

#for x in zipcode:
#    print(x) # Zipcode now only holds the correct zip codes. Another print to ensure all unwated zipcodes were gone.
