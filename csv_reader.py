import csv
import os.path

TALL_HEADER = "description,code|1,code|1|type,code|2,code|2|type,setting,standard_charge|gross,standard_charge|discounted_cash,payer_name,plan_name,modifiers,standard_charge|negotiated_dollar,standard_charge|negotiated_percentage,standard_charge|negotiated_algorithm,estimated_amount,standard_charge|min,standard_charge|max,standard_charge|methodology,additional_generic_notes" 
ATTRIBUTES = TALL_HEADER.split(',')
HOSPITALS = ['nj_Clara-Maass-Medical-Center', 'nj_morristown-medical-center', 'nj_jefferson-cherry-hill-hospital']

cpt_codes = ['59840', '59841',                  # abortion 
             '77063', '77065', '77066', '77067' # mammogram
            ]

output_file = "trimmed.csv"

if not os.path.exists(output_file):
    with open(output_file, 'w', newline='') as outfile:
        outfile.write( "hospital," + TALL_HEADER)    

with open(output_file, 'a', newline='') as outfile:
    csv_writer = csv.writer(outfile, delimiter=',')
    
    for hospital in HOSPITALS:
        with open('prices/' + hospital + '_standardcharges.csv', newline='') as csvfile:

            for i in range(2):
                next(csvfile)
            # trim header fieldnames
            header = [h.strip() for h in next(csvfile).split(',')]
            header = [a.replace(' | ', '|') for a in header]
            header = [a.lower() for a in header]
            header = [a.strip('"') for a in header]
            csv_reader = csv.DictReader(csvfile, delimiter=',', quotechar='|', fieldnames=header)

            if 'payer_name' not in csv_reader.fieldnames:
                print("Price transparancy file is not in tall format for hospital " + hospital + ".")
                print(row)
                # continue with next hospital
                continue
            
            for a in ATTRIBUTES:
                if a not in csv_reader.fieldnames:
                    print("Attribute " + a + " is missing in file for hospital " + hospital + ".")
                    print(TALL_HEADER)
                    print("==="*10)
                    print(csv_reader.fieldnames)
                    # continue with next hospital
                    continue

            i = 3
            for row in csv_reader:
                # trim quotes
                for key, value in row.items():
                    if isinstance(value, str):
                        row[key] = value.strip('"')
                if row['code|1|type'] == 'CPT' and row['code|1'] in cpt_codes:
                    line = [hospital]
                    for a in ATTRIBUTES:
                        line.append(row[a])
                    csv_writer.writerow(line)
