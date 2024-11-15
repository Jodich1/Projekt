import argparse # importerar argparse modulen
from cryptography.fernet import Fernet, InvalidToken # importerar cryptography med Fernet samt InvalidToken
import os # Importerar OS-modulen
import pyfiglet

# ----------------------- skapande av nyckel funktionen ---------------------- #

def generera_nyckel():
    key = Fernet.generate_key() #Generar en slumpmässig nyckel för kryptering och dekryptering
    with open("nyckel.key", "wb") as key_file: #Sparar nyckeln i en fil kallad för nyckel.key
        key_file.write(key) #Skriver innehållet av nyckeln till den nyckel.key filen
    print(f"Nyckeln har blivit sparad som: nyckel.key")
    
    return key #För att kunna använda sig av key variabeln utanför funktionerna


# ---------------- kryptera funktionen ------------------ #


def kryptera_fil(filnamn, key): #skapande av funktionen kryptera för fil och nyckel.
    cipher_suite = Fernet(key) #Initierar Fernet-krypteringsobjektet med nyckeln
    with open(filnamn, "rb") as file: # Laddar filen som ska krypteras
        file_data = file.read()

    cipher_text = cipher_suite.encrypt(file_data) #Gör om innehållet i filen till krypterad

    with open(f"{filnamn}.enc", "wb") as krypterad_fil: #Skapar en ny fil där det krypterade innehållet ska i.
        krypterad_fil.write(cipher_text) #Skriver över de krypterade innehållet till den nya filen som avslutas på .enc

    print(f"Filen {filnamn} har krypterats och sparats som {filnamn}.enc") #Bekräftelse för användaren att filen har blivit krypterad


# ---------------- dekryptera funktionen ---------------------- #

def dekryptera_fil(filnamn, key): #Funktionen för att dekryptera en fil
    cipher_suite = Fernet(key) #Laddar in nyckeln
    with open(filnamn, "rb") as encrypted_file: #Läser in den krypterade filen
        encrypted_text = encrypted_file.read() #
    print(f"Krypterad fil: {filnamn} har laddats") #Bekräftar för användaren att den krypterade filen har laddats in

    try: #En try-sats för att hantera potentiella fel vid dekryptering
        dekrypterad_data = cipher_suite.decrypt(encrypted_text) #
        with open(f"{filnamn}.dec", "wb") as decrypted_file: #Öppnar den tidigare krypterade filen i en ny fil som avslutas på .dec
            decrypted_file.write(dekrypterad_data) #Skriver över den krypterade datan i denna fil
        print(f"Filen har dekrypterats och sparats som {filnamn}.dec") # Bekräftelse för användaren att den krypterade filen har blivit dekrypterad
    except InvalidToken: # Try-satsen används här med en except för att indikera till användaren att de försöker dekryptera en fil som inte är krypterad för att undvika krash
        print(f"Error: Filen är inte krypterad") #Bekräftelse till användaren att den filen de försöker dekryptera inte är krypterad



# --------------------------- Huvud funktionen -------------------------------------#


def main(): #Huvud menyn funktion för användandet av argparse
    cool_text = pyfiglet.figlet_format("Mitt\n" "krypterings\nverktyg", font="slant")
    # En tydlig beskrivining av hur du använder dig av programmet.
    parser = argparse.ArgumentParser( 
    description=(
        f"{cool_text}.\n\n"
        "Metoder:\n\n"
        "  - generera-nyckel: Genererar en ny krypteringsnyckel och sparar den i en fil kallad 'nyckel.key'.\n"
        "  - kryptera: Krypterar angiven fil med hjälp av den genererade nyckeln.\n"
        "  - dekryptera: Dekrypterar en tidigare krypterad fil.\n\n"
        "  - OBS!: Det går inte att dekryptera en fil som inte redan är krypterad! \n\n"
        "Exempel för metoder:\n\n"
        "  python projektarbete.py generera-nyckel\n"
        "  python projektarbete.py 'filnamn' kryptera\n"
        "  python projektarbete.py 'filnamn' dekryptera\n\n"
        "Notera: Det är antingen 'python' eller 'python3' baserat på vilket OS-system du använder dig av.\n\n"
    ),
    formatter_class=argparse.RawTextHelpFormatter # Formaterar texten så inta allting blir i en enda sträng
)
    parser.add_argument("filnamn", type=str, nargs="?", help="Ange namn på filen") #Första argparse argumentet där användaren får skriva in vilken fil de vill kryptera eller dekryptera
    parser.add_argument("metod", type=str, choices=["generera-nyckel", "kryptera", "dekryptera"], help="Vill du generera en nyckel, kryptera eller dekryptera") # Andra argumentet för själva metoden
    args = parser.parse_args()
# Värt att nämna är att jag har lagt in nargs i den första argumentet för att "generera-nyckel" funktionen inte ska behövas skrivas med en fil då detta är onödigt
    if args.metod == "generera-nyckel": #Om användaren vill skapa en nyckel så sker det här då vi kallar på funktionen
        if os.path.exists("nyckel.key"): # Kontroll för att se om en nyckel existerar redan eller inte
            print("Nyckel existerar redan") # Felmeddelande tillbaka till användaren
        else:
            generera_nyckel() 
    
    
    try: #En try excepts-sats för att kontrollera om en nyckel existerar eller ej för att undvika krash.
        with open("nyckel.key", "rb") as nyckel:
            key = nyckel.read()
    except FileNotFoundError:
        key = None

        

    if args.metod == "kryptera": # Om användaren vill kryptera
        if key is None: #Kontroll för att se om nyckel saknas eller ej
            print("Nyckel saknas, skapa gärna en nyckel först") # Bekräftelse till användaren att nyckeln saknas och går därför ej att kryptera
        elif not os.path.exists(args.filnamn): # En kontroll för att se om filen inte existerar
            print(f"{args.filnamn} existerar ej") # En bekräftelse till användaren för visa att filen som de vill kryptera inte existerar
        else:
            kryptera_fil(args.filnamn, key) # kallar på funktionen för att kryptera den angivna filen
    elif args.metod == "dekryptera": # Om användaren väljer att dekryptera
        if key is None: # Kontroll ifall att nyckeln inte existerar
            print("Nyckel saknas, skapa gärna en nyckel först") # Skickar tillbaka till användaren att nyckel inte finns
        elif not os.path.exists(args.filnamn): # En kontroll för att se om filen existerar eller ej
            print(f"{args.filnamn} existerar ej") # Skickar tillbaka till användaren att filen inte existerar
        else: #Ifall filen existerar så kör den dekryptera funktionen
            dekryptera_fil(args.filnamn, key)





main() # Kallar på huvud funktionen.