from mySQLTemplate import *

data = connectSQL()

def template(name):
    companyName = 'NTU MSBA Enterprise' 
    reportHeader = f'{companyName}'
    title = "Certificate of Completion"
    body1 = "This is to certify that the following employee"
    body2 = "Has completed the traineship programme"
    signature = "Signature"
    date = "Date"
    line = "_"*10
   
    for person in data:
        name = person[0]+' '+person[1]
        print('='*100)
        print(f"{reportHeader:<30}")
        print(f"{title:^100}")
        print(f"{body1:^100}")
        print(f"\n{name:^100}\n")
        print(f"{body2:^100}")
        print(f"\n{line:<20}{line:>80}")
        print(f"{signature:<20}{date:>77}\n")
        print("="*100)

if __name__ == "__main__":
    template(data)
