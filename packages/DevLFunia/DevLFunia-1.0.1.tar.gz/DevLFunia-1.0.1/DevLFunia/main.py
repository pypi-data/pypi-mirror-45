'''MIT License

Copyright (c) 2019 {Zero Cool} & Aditya Nugraha Kalimantan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''


from . import Config,PhotofuniaException

class Photofunia(Config):
    """docstring for Photofunia"""
    def __init__(self):
        super(Photofunia, self).__init__()

    def info(self, name):
        name = name.replace(' ', '-')
        name = name.replace('_', '-')
        url = self.urlEncode(self.host,name.lower(),self.params)
        response = self.getContent(url)
        return self.response(data=response)

    def easter_greetings(self, path, text=' '):
        url = self.urlEncode(self.host, self.path.easter_greetings, self.params)
        data = {'text': text}
        files = {'image': open(path, 'rb')}
        return self.response(url, data=data, files=files)

    def neon_writing(self, text= ' ' , text2= ' '):
        url = self.urlEncode(self.host, self.path.neon_writing, self.params)
        data = {'text': text, 'text2': text2}
        return self.response(url,data=data)

    def brussels_museum(self,path,checkbox='no'):
        if checkbox.lower() not in ['no','yes']:
            raise PhotofuniaException('Invalid checkbox value')
        url = self.urlEncode(self.host, self.path.brussels_museum, self.params)
        data = {'painting': checkbox}
        files = {'image': open(path, 'rb')}
        return self.response(url, data=data, files=files)

    def watercolour_text(self, text, text2=None, color=1, font='segoeprb', splashes=True):
        if color.lower() not in [1, 2, 3, 4]:
            raise PhotofuniaException('Invalid color value')
        if font.lower() not in ['segoeprb', 'lobster']:
            raise PhotofuniaException('Invalid font value')
        url = self.urlEncode(self.host, self.path.watercolour_text, self.params)
        data = {'text': text, 'text2': text2, 'color': color, 'font': font, 'splashes': self.bool_dict[splashes][0]}
        return self.response(url, data=data)

    def vintage_scooter(self,path):
        url = self.urlEncode(self.host, self.path.vintage_scooter, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def card_with_flowers(self,path):
        url = self.urlEncode(self.host, self.path.card_with_flowers, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def denim_emdroidery(self,text=' ',colour='orange'):
        if colour.lower() not in ['red','orange','green','yellow','blue','purple','white']:
            raise PhotofuniaException('Invalid colour value')
        url = self.urlEncode(self.host, self.path.denim_emdroidery, self.params)
        data = {'text': text, 'colour': colour}
        return self.response(url, data=data)

    def giant_artwork(self,path):
        url = self.urlEncode(self.host, self.path.giant_artwork, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def glass_bauble(self, text= ' ' , text2= ' ',colour='gold',font='scriptbl'):
        if colour.lower() not in ['white','gold']:
            raise PhotofuniaException('Invalid colour value')
        if font.lower() not in ['scriptbl','pacifico','berkshireswash','lobster']:
            raise PhotofuniaException('Invalid font value')
        url = self.urlEncode(self.host, self.path.glass_bauble, self.params)
        data = {'text1': text, 'text2': text2}
        return self.response(url, data=data)

    def christmas_present(self,path,snow=True,checkbox='no'):
        if checkbox.lower() not in ['no','yes']:
            raise PhotofuniaException('Invalid checkbox value')
        url = self.urlEncode(self.host, self.path.christmas_present, self.params)
        data = {'snow': bool(snow), 'cap': checkbox}
        files = {'image': open(path, 'rb')}
        return self.response(url,data=data, files=files)

    def christmas_diary(self,path,text=' '):
        url = self.urlEncode(self.host, self.path.christmas_diary, self.params)
        files = {'image': open(path, 'rb')}
        data = {'text':text}
        return self.response(url,data=data, files=files)

    def posters_on_the_wall(self,path,path1=None,path2=None,checkbox='no'):
        if checkbox.lower() not in ['no','yes']:
            raise PhotofuniaException('Invalid checkbox value')
        url = self.urlEncode(self.host, self.path.posters_on_the_wall, self.params)
        files = {'image': open(path, 'rb')}
        if path1:
            files.update({'image2': open(path1, 'rb')})
        if path2:
            files.update({'image3': open(path2, 'rb')})
        data = {'bw':checkbox}
        return self.response(url,data=data, files=files)

    def festive_days(self,path,path1=None):
        url = self.urlEncode(self.host, self.path.festive_days, self.params)
        files = {'image': open(path, 'rb')}
        if path1:
            files.update({'image2': open(path1, 'rb')})
        return self.response(url,data=data, files=files)

    def explorer_drawing(self,path):
        url = self.urlEncode(self.host, self.path.explorer_drawing, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def at_the_beach(self,path):
        url = self.urlEncode(self.host, self.path.at_the_beach, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def in_the_woods(self,path):
        url = self.urlEncode(self.host, self.path.in_the_woods, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url,files=files)

    def haunted_hotel(self,text=' ',checkbox='no'):
        if checkbox.lower() not in ['no','yes']:
            raise PhotofuniaException('Invalid checkbox value')
        url = self.urlEncode(self.host, self.path.haunted_hotel, self.params)
        data = {'text': text, 'hotel': checkbox}
        return self.response(url,data=data)

    def calendar(self, path, type='Year', year='2019'):
        url = self.urlEncode(self.host, self.path.calendar, self.params)
        data = {'type': type, 'year': year}
        files = {'image': open(path, 'rb')}
        return self.response(url, data=data, files=files)

    def banksy_shredder(self, path,animation='animated',checkbox='no'):
        if checkbox.lower() not in ['no','yes']:
            raise PhotofuniaException('Invalid checkbox value')
        if animation.lower() not in ['animated','still']:
            raise PhotofuniaException('Invalid animation value')
        url = self.urlEncode(self.host, self.path.banksy_shredder, self.params)
        data = {'animation': animation, 'stencil': checkbox}
        files = {'image': open(path, 'rb')}
        return self.response(url, data=data, files=files)

    def cinema_ticket(self, text= ' ' , text2= ' '):
        url = self.urlEncode(self.host, self.path.cinema_ticket, self.params)
        data = {'text1': text, 'text2': text2}
        return self.response(url, data=data)

    def golden_coin(self, path, text=' ', text2=' '):
        url = self.urlEncode(self.host, self.path.golden_coin, self.params)
        data = {'text': text, 'text2': text2}
        files = {'image': open(path, 'rb')}
        return self.response(url, data=data, files=files)

    def arrow_signs(self, text= ' ' , text2= ' '):
        url = self.urlEncode(self.host, self.path.arrow_signs, self.params)
        data = {'text1': text, 'text2': text2}
        return self.response(url, data=data)

    def autumn_leaf(self,path,text=' ',colour='yes'):
        if colour.lower() not in ['no','yes']:
            raise PhotofuniaException('Invalid checkbox value')
        url = self.urlEncode(self.host, self.path.autumn_leaf, self.params)
        data = {'text': text, 'colour': colour}
        files = {'image': open(path, 'rb')}
        return self.response(url, data=data, files=files)

    def interior_picture(self,path,colour='yellow',checkbox='no'):
        if checkbox.lower() not in ['no','yes']:
            raise PhotofuniaException('Invalid checkbox value')
        if colour.lower() not in ['red','pink','violet','green','yellow','blue','grey']:
            raise PhotofuniaException('Invalid colour value')
        url = self.urlEncode(self.host, self.path.interior_picture, self.params)
        data = {'colour': colour, 'pencil': checkbox}
        files = {'image': open(path, 'rb')}
        return self.response(url, data=data, files=files)

    def shopping_arcade(self, path):
        url = self.urlEncode(self.host, self.path.shopping_arcade, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def daily_newspaper(self, path, text= ' ' , text2= ' '):
        url = self.urlEncode(self.host, self.path.daily_newspaper, self.params)
        files = {'image': open(path, 'rb')}
        data = {'text1': text, 'text2': text2}
        return self.response(url, data=data, files=files)

    def yacht(self,text=' '):
        url = self.urlEncode(self.host, self.path.yacht, self.params)
        data = {'text': text}
        return self.response(url, data=data)

    def poster_wall(self, path,col1= 'white' ,path1=None, col2= ''):
        if col1.lower() not in ['white','yellow','red','green','blue']:
            raise PhotofuniaException('Invalid col1 value')
        if path1 and col2.lower() not in ['white','yellow','red','green','blue']:
            raise PhotofuniaException('Invalid col2 value')
        elif not path1 and col2:
            raise PhotofuniaException('Invalid path1 value')
        url = self.urlEncode(self.host, self.path.poster_wall, self.params)
        files = {'image': open(path, 'rb')}
        data = {'col1': col1}
        if path1:
            files.update({'image2': open(path1, 'rb')})
            data.update({'col2':col2})
        return self.response(url, data=data, files=files)

    def magic_card(self,path,type='king',type1='heart'):
        if type.lower() not in ['king','queen']:
            raise PhotofuniaException('Invalid type value')
        if type1 and col2.lower() not in ['heart','spade','diamond','club']:
            raise PhotofuniaException('Invalid type1 value')
        url = self.urlEncode(self.host, self.path.magic_card, self.params)
        files = {'image': open(path, 'rb')}
        data = {'type': type,'type1':type1}
        return self.response(url, data=data, files=files)

    def art_admirer(self,path):
        url = self.urlEncode(self.host, self.path.art_admirer, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def sketch_practicing(self,path):
        url = self.urlEncode(self.host, self.path.sketch_practicing, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def passage(self,path):
        url = self.urlEncode(self.host, self.path.passage, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def cloudy_filter(self,path,type='2'):
        if type(type) != int:
            raise PhotofuniaException('Invalid type value')
        elif type(type) == int and int(type) > 6:
            raise PhotofuniaException('Invalid type value')
        url = self.urlEncode(self.host, self.path.cloudy_filter, self.params)
        files = {'image': open(path, 'rb')}
        data= {'type':type}
        return self.response(url,data=data, files=files)

    def water_writing(self, text= ' '):
        url = self.urlEncode(self.host, self.path.water_writing, self.params)
        data = {'text': text}
        return self.response(url, data=data)

    def postage_stamp(self,path,colour='violet'):
        if colour.lower() not in ['violet','pink','red','green','marine','blue']:
            raise PhotofuniaException('Invalid colour value')
        url = self.urlEncode(self.host, self.path.postage_stamp, self.params)
        files = {'image': open(path, 'rb')}
        data= {'colour':colour}
        return self.response(url,data=data, files=files)

    def activists(self,path,text=' '):
        url = self.urlEncode(self.host, self.path.activists, self.params)
        files = {'image': open(path, 'rb')}
        data= {'text':text}
        return self.response(url,data=data, files=files)

    def travellers_sketch(self,path):
        url = self.urlEncode(self.host, self.path.travellers_sketch, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def mirror(self,path):
        url = self.urlEncode(self.host, self.path.mirror, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def ink_portrait(self,path):
        url = self.urlEncode(self.host, self.path.ink_portrait, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def old_tram(self,path,path1):
        url = self.urlEncode(self.host, self.path.old_tram, self.params)
        files = {'image': open(path, 'rb'),'image2': open(path1, 'rb')}
        return self.response(url, files=files)

    def truck_advert(self,path):
        url = self.urlEncode(self.host, self.path.truck_advert, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def gallery_visitors(self,path,colour='col',checkbox='no'):
        if colour.lower() not in ['bw','col']:
            raise PhotofuniaException('Invalid colour value')
        if checkbox.lower() not in ['no','yes']:
            raise PhotofuniaException('Invalid checkbox value')
        url = self.urlEncode(self.host, self.path.gallery_visitors, self.params)
        files = {'image': open(path, 'rb')}
        data = {'posterize':checkbox}
        return self.response(url, data=data, files=files)

    def bracelet(self, text= ' ' ):
        url = self.urlEncode(self.host, self.path.bracelet, self.params)
        data = {'text': text}
        return self.response(url, data=data)

    def girl_with_bicycle(self,path):
        url = self.urlEncode(self.host, self.path.girl_with_bicycle, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def easter_flowers(self,path):
        url = self.urlEncode(self.host, self.path.easter_flowers, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def easter_frame(self,path):
        url = self.urlEncode(self.host, self.path.easter_frame, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def painting_snap(self,path,checkbox='no'):
        if checkbox.lower() not in ['no','yes']:
            raise PhotofuniaException('Invalid checkbox value')
        url = self.urlEncode(self.host, self.path.painting_snap, self.params)
        files = {'image': open(path, 'rb')}
        data = {'texture':checkbox}
        return self.response(url, data=data, files=files)

    def coffee_and_tulips(self,path,text=' '):
        url = self.urlEncode(self.host, self.path.coffee_and_tulips, self.params)
        files = {'image': open(path, 'rb')}
        data = {'text':text}
        return self.response(url, data=data, files=files)

    def night_street(self,path,text=' '):
        url = self.urlEncode(self.host, self.path.night_street, self.params)
        files = {'image': open(path, 'rb')}
        data = {'text':text}
        return self.response(url, data=data, files=files)

    def red_wall(self,path,type='poster'):
        if type.lower() not in ['poster','photo']:
            raise PhotofuniaException('Invalid type value')
        url = self.urlEncode(self.host, self.path.red_wall, self.params)
        files = {'image': open(path, 'rb')}
        data = {'type':type}
        return self.response(url, data=data, files=files)

    def puppy_with_frame(self,path):
        url = self.urlEncode(self.host, self.path.puppy_with_frame, self.params)
        files = {'image': open(path, 'rb')}
        return self.response(url, files=files)

    def rose_vine(self,path,text=' ',text2=' '):
        url = self.urlEncode(self.host, self.path.rose_vine, self.params)
        files = {'image': open(path, 'rb')}
        data = {'text':text,'text2':text2}
        return self.response(url, data=data, files=files)

    def neon(self, text= ' ' , text2= ' '):
        url = self.urlEncode(self.host, self.path.neon, self.params)
        data = {'text1': text, 'text2': text2}
        return self.response(url, data=data)