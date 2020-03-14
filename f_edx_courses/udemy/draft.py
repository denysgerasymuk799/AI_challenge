from pyudemy import Udemy
import json


CLIENT_ID = 'XGwKUxLDixGf4mD9UHJNCPLXD9vzVfM6NA9YKufa'
CLIENT_SECRET = 'gYeTjrLot8ndRDdGyBwe1dx3SEVzrwVmAzOpxieZWZOqPYXwGpt6dWmd5xWZ1L7Rxazec5o25' \
                'LANhkgByzsm3J0XtQJxPFpMHJRpzMUb7fFAXidW2hYygnebyO67X83L'
UDEMY = Udemy(CLIENT_ID, CLIENT_SECRET)
ID = 362328


if __name__ == '__main__':
    detail = UDEMY.course_detail()
    print(type(detail))
    with open("draft.json", 'w', encoding='utf-8', errors='ignore') as res_file:
        res_file.write(json.dumps(detail, indent=3))

