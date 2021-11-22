import requests

def createImg():

    resp = requests.get('https://aws.random.cat/meow')
    data = resp.json()
    p = data['file']
    f = requests.get(p)
    name = str(p).split('/')[-1]
    name2 = name.split('.')[0]
    out = open('.\img\\' + name2 + '.jpg', "wb")
    out.write(f.content)
    out.close()

if __name__ == '__main__':
    n = int(input())
    for i in range(n):
        createImg()
