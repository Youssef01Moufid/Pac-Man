import json

try:
    with open("/home/ymoufid/Desktop/pacman/config_file.json") as f:
        content = f.read()

    data = json.loads(content)

    print(data)

except Exception as e:
    print(e)
