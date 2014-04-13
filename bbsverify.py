#!usr/bin/evn python
#! -*- coding:utf8 -*-
import Image
import requests
import os

class BBSVerify(object):
    def __init__(self, imgUrl):
        self.password = {
            "754200418396642621058": "0",
            "18417810880660": "1",
            "244782452402402362572912": "2",
            "782452402402362572912": "2",
            "9464204649063203301004": "3",
            "734548110228600216": "4",
            "908320242872802241362": "5",
            "8082042806102182741098": "6",
            "40508730416290558610": "7",
            "13182762641040803421706": "8",
            "992246238128662284880": "9",
            "404040404040": "-",
            "4040404000314404040": "+",
            "808080808080808080808080": "=",
            "978342314996744364506": "?"
        }
        self.imgUrl = imgUrl
        self.req = requests.Session()

    def convert(self):
        filename = self.download_img()
        im = Image.open(filename)
        im.show()
        iml = im.convert("L")
        data = iml.load()
        matrix_line = {}
        x_line = []
        for i in range(im.size[0]):
            matrix_line[i] = []
            for j in range(im.size[1]):
                if data[i,j] != 255:
                    matrix_line[i].append(data[i,j])

        for line in matrix_line:
            if matrix_line[line]:
                x_line.append(reduce(lambda x,y:x+y, matrix_line[line]))
            else:
                x_line.append("s")

        number = map(lambda x:str(x), x_line)
        number =  "".join(number).split("s")
        number = filter(lambda x: x!="", number)    
        return number

    def exp(self):
        try:
            number = self.convert()
            exps = ""
            for num in number:
                if self.password[num] != "=" and self.password[num] != "?":
                    exps += self.password[num]
            return eval(exps)
        except:
            return False

    def download_img(self):
        local_filename = "./codes/" + self.imgUrl.split('=')[-1]
        r = self.req.get(self.imgUrl, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: 
                    f.write(chunk)
                    f.flush()
            f.close()
        return local_filename
