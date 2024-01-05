import json, openpyxl, random, string
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
        state_sheet.append(['code', 'name', 'no_of_districts', 'no_of_constituencies'])
        state_sheet['A1'].font = openpyxl.styles.Font(bold=True)
        state_sheet['B1'].font = openpyxl.styles.Font(bold=True)
        state_sheet['C1'].font = openpyxl.styles.Font(bold=True)
        state_sheet['D1'].font = openpyxl.styles.Font(bold=True)

        district_sheet = workbook.create_sheet("Districts")
        district_sheet.append(['code','state_code', 'name','link', 'no_of_constituencies'])

        constituency_sheet = workbook.create_sheet("Constituencies")
        constituency_sheet.append(['code','district_code', 'name','link'])
        for _, state_data in data.items():
            state_code = generate_unique_code()
            districts = state_data['districts']
            constituency_count = 0
            for _, district_data in districts.items():
               district_code = generate_unique_code()
               constituencies = district_data['constituency']
               constituency_count += len(constituencies.items())
               district_sheet.append([district_code,state_code, district_data['name'], district_data['link'], len(constituencies.items())])
               for _, constituency_data in constituencies.items():
                    constituency_sheet.append([generate_unique_code(), district_code, constituency_data['name'], constituency_data['link']])
            state_sheet.append([state_code, state_data['name'], len(districts.items()), constituency_count])
                
        workbook.save('constituency.xlsx')


run()