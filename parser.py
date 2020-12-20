import requests
import bs4

with open('specialities.txt', encoding='utf8') as f:
    wanted_specialities = f.readlines()
    wanted_specialities_prefixes = [speciality[:6] for speciality in wanted_specialities]

def is_wanted(speciality):
    for prefix in wanted_specialities_prefixes:
        if speciality.startswith(prefix):
            return True
    return False

with open('documents.txt') as f:
    document_urls = f.read().split()

for document_url in document_urls:
    responce = requests.get(document_url)
    
    parser = bs4.BeautifulSoup(responce.text, 'html.parser')
    specialities = [h3.contents[0] for h3 in parser('h3')]
    tables = parser('table')
    students_data = zip(specialities, tables)

    for speciality, table in students_data:
        if not is_wanted(speciality):
            continue

        rows = table('tr')
        good_rows = []
        for row in rows:
            if row.has_attr('class') and row['class'][0] == 'hdr':
                continue
            good_rows.append(row)
        rows = good_rows
        
        names = []
        for row in rows:
            td = row('td')[0] # get first column with name
            last_name, first_name, *_ = td.contents[0].split() # get only first and last names
            name = f'{first_name} {last_name}'
            names.append(name)
        
        with open('names.txt', 'a', encoding='utf-8') as f:
            for name in names:
                print(name, file=f)