import pymongo, openpyxl, os, dotenv
dotenv.load_dotenv('../.env')

DB_URL = os.environ.get('DB_URL')
DB_NAME = os.environ.get('DB_NAME')

print("Adding data to : ", DB_URL, "/", DB_NAME)

def read_excel_file( file, sheet):
        workbook = openpyxl.load_workbook(file)
        sheet = workbook[sheet]

        rows = []
        for row in sheet.iter_rows(values_only=True):
            row_dict = [cell_value for header,cell_value in zip(sheet[1], row)]
            rows.append(row_dict)
        workbook.close()

        return rows

client = pymongo.MongoClient(DB_URL)

db = client[DB_NAME]
collection = db["states"]
states = read_excel_file('constituency.xlsx', 'States')
state_data = []

print(f"Adding {len(states[1:])} states to database.")

for row in states[1:]:
    id = row[0]
    code = row[1]
    name = row[2]
    no_of_districts = row[3]
    no_of_constituencies = row[4]
    state_data.append({
         "id":id,
         "code": code,
         "name": name, 
         "no_of_districts": no_of_districts, 
         "no_of_constituencies": no_of_constituencies
    })

collection.insert_many(state_data)

district_data = []
collection = db["districts"]
districts = read_excel_file('constituency.xlsx', 'Districts')

print(f"Adding {len(districts[1:])} districts to database.")

for row in districts[1:]:
    id = row[0]
    code = row[1]
    state_code = row[2]
    name = row[3]
    link = row[4]
    no_of_constituencies = row[4]
    description = row[5]
    image = row[6]
    
    link = link if link != 'none' else None
    description = description if description != 'none' else None
    image = image if image != 'none' else None

    district_data.append({
         "id":id,
         "code": code, 
         "state": db["states"].find_one({"code": state_code})["_id"], 
         "name": name, 
         "link": link, 
        "description": description,
        "image": image,
         "no_of_constituencies": no_of_constituencies
    })

collection.insert_many(district_data)


constituency_data = []
collection = db["constituencies"]
constituencies = read_excel_file('constituency.xlsx', 'Constituencies')

print(f"Adding {len(constituencies[1:])} constituencies to database.")

for row in constituencies[1:]:
    id = row[0]
    code = row[1]
    district_code = row[2]
    name = row[3]
    link = row[4]
    description = row[5]
    image = row[6]
    
    link = link if link != 'none' else None
    description = description if description != 'none' else None
    image = image if image != 'none' else None

    constituency_data.append({
         "id":id,
         "code": code, 
         "district": db["districts"].find_one({"code": district_code})["_id"], 
         "name": name, 
         "link": link,
        "description": description,
        "image": image
    })

collection.insert_many(constituency_data)