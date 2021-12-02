{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "748b77f6-88e4-4165-b210-f3c190aec521",
   "metadata": {},
   "outputs": [],
   "source": [
    "zipcode = [] #empty array to store all zip_codes\n",
    "post_C = soup.find_all(\"tag\", {\"k\": \"addr:postcode\"})\n",
    "\n",
    "for code in post_C:\n",
    "    zipcode.append(code)\n",
    "#using beautiful soup to find tags with incorrect zipcodes\n",
    "\n",
    "#print(zipcode) #printed the zipcodes to ensure they all printed from the entire dataset.\n",
    "\n",
    "#removing all unwanted zipcodes from our data:\n",
    "unwanted_codes = soup.find_all(\"tag\", {\"k\": \"addr:postcode\"} and {\"v\": \"89434\"})\n",
    "for x in unwanted_codes:\n",
    "    zipcode.remove(x)\n",
    "\n",
    "    next_code = soup.find_all(\"tag\", {\"k\": \"addr:postcode\"} and {\"v\":\"89431\"})   \n",
    "for a in next_code:\n",
    "    zipcode.remove(a)\n",
    "    \n",
    "bad_zip = soup.find_all(\"tag\", {\"k\": \"addr:postcode\"}and {\"v\":\"89432\"})\n",
    "for b in bad_zip:\n",
    "    zipcode.remove(b)\n",
    "\n",
    "sp_zip = soup.find_all(\"tag\", {\"k\": \"addr:postcode\"}and {\"v\":\"89435\"})\n",
    "for c in sp_zip:\n",
    "    zipcode.remove(c)\n",
    "    \n",
    "sp_zip2 = soup.find_all(\"tag\", {\"k\": \"addr:postcode\"}and {\"v\":\"89436\"})\n",
    "for d in sp_zip2:\n",
    "    zipcode.remove(d)\n",
    "\n",
    "unknown_zip = soup.find_all(\"tag\", {\"k\": \"addr:postcode\"}and {\"v\":\"96118\"})\n",
    "for u in unknown_zip:\n",
    "    zipcode.remove(u)\n",
    "\n",
    "#for x in zipcode:\n",
    "#    print(x) # Zipcode now only holds the correct zip codes. Another print to ensure all unwated zipcodes were gone."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
