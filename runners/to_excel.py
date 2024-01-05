import json, openpyxl, random, string
from uuid import uuid4

def generate_unique_code(length=4):
  used_codes = set()
  while True:
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    if code not in used_codes:
      used_codes.add(code)
      return code

def run():
    with open('constituency.json', 'r') as f:
        data = json.load(f)
        workbook = openpyxl.Workbook()
        state_sheet = workbook.active
        state_sheet.title = "States"
        state_sheet.append(['id','code', 'name', 'no_of_districts', 'no_of_constituencies'])
        state_sheet['A1'].font = openpyxl.styles.Font(bold=True)
        state_sheet['B1'].font = openpyxl.styles.Font(bold=True)
        state_sheet['C1'].font = openpyxl.styles.Font(bold=True)
        state_sheet['D1'].font = openpyxl.styles.Font(bold=True)

        district_sheet = workbook.create_sheet("Districts")
        district_sheet.append(['id','code','state_code', 'name','link', 'no_of_constituencies', 'description', 'image'])

        constituency_sheet = workbook.create_sheet("Constituencies")
        constituency_sheet.append(['id','code','district_code', 'name','link', 'description', 'image'])
        for _, state_data in data.items():
            state_code = generate_unique_code()
            districts = state_data['districts']
            constituency_count = 0
            for _, district_data in districts.items():
               district_code = generate_unique_code()
               
               district_link = district_data.get('link', 'none')  or 'none'
               district_link = district_link if len(district_link) > 0 else 'none'
               district_description = district_data.get('description', 'none') or 'none'
               district_description = district_description if len(district_description) > 0 else 'none'
               district_image = district_data.get('image', 'none') or 'none'
               district_image = district_image if len(district_image) > 0 else 'none'
               
               constituencies = district_data['constituency']
               constituency_count += len(constituencies.items())
               district_sheet.append([str(uuid4()),district_code,state_code, district_data['name'], district_link, len(constituencies.items()), district_description, district_image])
               for _, constituency_data in constituencies.items():
                    constituency_link = constituency_data.get('link', 'none') or 'none'
                    constituency_link = constituency_link if len(constituency_link) > 0 else 'none'
                    constituency_description = constituency_data.get('description', 'none') or 'none'
                    constituency_description = constituency_description if len(constituency_description) > 0 else 'none'
                    constituency_image = constituency_data.get('image') or 'none'
                    constituency_image = constituency_image if len(constituency_image) > 0 else 'none'

                    constituency_sheet.append([str(uuid4()),generate_unique_code(), district_code, constituency_data['name'], constituency_link, constituency_description, constituency_image])
            state_sheet.append([str(uuid4()),state_code, state_data['name'], len(districts.items()), constituency_count])
                
        workbook.save('constituency.xlsx')


run()