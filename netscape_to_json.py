import os
import json

def netscape_to_json(netscape_cookie_str: str) -> str:

    cookies = []
    lines = netscape_cookie_str.strip().split('\n')
    for line in lines:
        if not line.startswith('#') and line.strip():
            parts = line.split('\t')
            if len(parts) == 7:
                cookie = {
                    "domain": parts[0],
                    "httpOnly": parts[1].upper() == "TRUE",
                    "path": parts[2],
                    "secure": parts[3].upper() == "TRUE",
                    "expires": float(parts[4]),
                    "name": parts[5],
                    "value": parts[6],
                    "sameSite": "Lax"
                }
                cookies.append(cookie)
    return json.dumps(cookies)

def process_folder(folder_path):

  for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    if os.path.isfile(file_path):
      with open(file_path, 'r') as f:
        netscape_cookie_str = f.read()
        json_data = netscape_to_json(netscape_cookie_str)

      with open(file_path, 'w') as f:
        f.write(json_data)

folder_path = input("Enter cookie folder path : ")
process_folder(folder_path)