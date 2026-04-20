from urllib.request import urlopen
from bs4 import BeautifulSoup

ENERGY_MAP = {
    "Grass": "[G]",
    "Fighting": "[F]",
    "Metal": "[M]",
    "Psychic": "[P]",
    "Water": "[W]",
    "Fire": "[R]",
    "Dark": "[D]",
    "Lightning": "[L]",
}

def findCard(s):
    #f replaces {s[x]} with the element from the (s) 
    url = f"https://limitlesstcg.com/cards/{s[0]}/{s[1]}"
    print("url = " + url)
    html = urlopen(url).read()

    soup = BeautifulSoup(html, "html.parser")

    attackContainer = soup.find_all(class_="card-text-attack-info")
    abilityContainer = soup.find_all("p", class_="card-text-ability-info")

    results = []

    # --- CARD NAME ---
    for tag in soup.select(".card-text-name a"):
            name = tag.get_text(strip=True)

            if (name.startswith(("Grass", "Fighting", "Metal", "Psychich", "Water", "Fire", "Dark", "Lightning"))) and (name.endswith("Energy")):
                results.append(name)

            elif ("Grass" in name):
                results.append(name.replace("Grass", "[G]"))

            elif ("Fighting" in name):
                results.append(name.replace("Fighting", "[F]"))

            elif ("Metal" in name):
                results.append(name.replace("Metal", "[M]"))

            elif ("Psychic" in name):
                results.append(name.replace("Psychic", "[P]"))

            elif ("Water" in name):
                results.append(name.replace("Water", "[W]"))

            elif ("Fire" in name):
                results.append(name.replace("Fire", "[R]"))

            elif ("Dark" in name):
                results.append(name.replace("Dark", "[D]"))

            elif ("Lightning" in name) :
                results.append(name.replace("Lightning", "[L]"))  

            else:
                results.append(name)

    # --- FIND ABILITYS NAME ---
    for abi in abilityContainer:
        abiText = abi.get_text(strip=True)
        abiArray = abiText.split()
        if len(abiText) < 2:
            results.append(abiText[1])
        else:
            abiArray.pop(0)
            final = " ".join(abiArray)
            results.append(final)

    # --- FIND ATTACK NAMES ---
    #Remove attack's damage number
    def num_there(s):
        return any(i.isdigit() for i in s)

    for attack in attackContainer:
        #Removes energy symbol
        span = attack.find("span")
        if span:
            span.decompose()
        
        #Adds attacks name
        text = attack.get_text(strip=True)

        #If there is number in the end of attacks name
        if (num_there(text)):
            text2 = " ".join(text.split()[:-1])
            results.append(text2)

        #If there isn't number at the end of attacks name
        else:
            results.append(text)

    final = " ".join(results)
    return(final)

#Copy-paste list and it end when list reach line with "end"
#Turns the paste to array
loop = True
lines = []
try:
    while loop == True:
        newLine = input()
        if newLine == 'end':
            loop = False
        else:  
            lines.append(newLine)
except EOFError:
    pass
lines = "\n".join(lines)
lastLines = lines.split()

#Goes through each card one by one
x = 0
finalList = []
while x < len(lastLines):
    combinedString = []
    amountOfCards = lastLines[x]
    #Check if the next element is 3 letter word with all caps, if not goes to next element
    while len(combinedString) < 1:
        if len(lastLines[x]) != 3:
            x += 1
        elif lastLines[x].isupper():
            combinedString.append(lastLines[x])
            x +=1
        else:
            x += 1

    #Check if the next element in array is (card) number
    combinedString.append(lastLines[x])
    #Add amount of cards as a first element then add the rest that finalList returns
    finalList.append(amountOfCards + " " + findCard(combinedString))
    x += 1

result = '\n'.join(str(item) for item in finalList)
print(result)