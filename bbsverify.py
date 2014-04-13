#!usr/bin/evn python
#! -*- coding:utf8 -*-
'''
Copyright (c) 2014, lcyang/ChongYang Liu
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''


import Image
import requests
import os

class BBSVerify(object):
    def __init__(self, imgUrl):
        '''init the instance
            every password in the number stand for a number , '=' ,'?','+' or '-',
            when you got a list like:
            ['13182762641040803421706', '9464204649063203301004', '4040404000314404040', '40508730416290558610', '808080808080808080808080', '978342314996744364506']
            it is meaning '83+7=?'
        '''
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
        # Uncomment the im.show line to show img
        # im.show()
        #convert im,·L (8-bit, 0-255 pixels, black and white)
        iml = im.convert("L")
        #append every x_line(img.size[0]) data to list x_line whitch data not eq 255
        data = iml.load()
        matrix_line = {}
        x_line = []
        for i in range(im.size[0]):
            matrix_line[i] = []
            for j in range(im.size[1]):
                if data[i,j] != 255:
                    matrix_line[i].append(data[i,j])
        #join every x_line(im.size[0]) to a string, means a pasword
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
            #number ['908320242872802241362', '734548110228600216', '404040404040', '18417810880660', '244782452402402362572912', '808080808080808080808080', '978342314996744364506']
            #every password in the number stand for a number , '=' ,'?','+' or '-'
            exps = ""
            for num in number:
                if self.password[num] != "=" and self.password[num] != "?":
                    exps += self.password[num]
            return eval(exps)
        except:
            #failed 
            return False

    def download_img(self):
        '''download img from imgurl
        '''
        local_filename = "./codes/" + self.imgUrl.split('=')[-1]
        r = self.req.get(self.imgUrl, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: 
                    f.write(chunk)
                    f.flush()
            f.close()
        return local_filename


if __name__ == '__main__':
    verify = BBSVerify("http://bbs.swust.edu.cn/ckquestion.php?q=-1&t=1397372353790")
    print verify.exp()