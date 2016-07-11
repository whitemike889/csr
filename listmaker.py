import os, csv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MENU_DIR = os.path.join(ROOT_DIR, 'images')

csvFile = os.path.join(ROOT_DIR, 'imagelist.csv')

with open(csvFile,'w') as f:
    writer = csv.writer(f, csv.excel)
    for item in os.listdir(MENU_DIR):
        if ".png" in item:
            writer.writerow([item])

