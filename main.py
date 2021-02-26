from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display

from typing import Iterable, Tuple
import colorsys
import itertools
from fractions import Fraction
from pprint import pprint

text_x = 25
text_y = 150

def getInputs():
    userCode = input("Enter the code, with each subcode comma separated (ex: 'MF,D,001,A'): ")
    userCodes = userCode.split(',')
    inputs = {}
    for i in userCodes:
        inputs[i] = {'description': input("Enter a short description for \'{}\': ".format(i))}

    return inputs

def main():
    # inputs = getInputs()
    # print(inputs)
    inputs = {'AB': {'description': 'first'}, 'DA': {'description': 'q'}, '001': {'description': 'skip'}, 'A': {'description': 'asd'}, 'B': {'description': 'z'}, 'C': {'description': '15615615615611561656'}, 'D': {'description': 'qwe'}}

    with Image(width=2000, height=1000, background=Color('white')) as image:
        with Drawing() as draw:
            draw.fill_color = Color('red')
            draw.stroke_color = Color('red')
            draw.font="DejaVu-Sans-Mono"
            # draw.font_style = 'italic'
            draw.font_size = 128

            input_text = ''.join(inputs.keys())
            # DRAW THE CODE
            draw.text(x=text_x, y=text_y, body=input_text)

            # INPUTS 
            draw.stroke_width = 2.5
            draw.fill_color = Color('black')
            draw.stroke_color = Color('black')
            draw.font="DejaVu-Sans-Mono"
            bracket_text_displace = 12 # where should the two brackets start from
            bracket_force_y = -5 # how far up into the font the two brackets should start from
            bracket_height = 15 # y height of the bracket
            bracket_shorten_x = 3 # half the x gap between two brackets

            # CALCULATED
            skip_count=0
            for value in inputs.values():
                print(value)
                if value['description'] == 'skip':
                    skip_count+=1

            print(skip_count)
            font_width = draw.font_size*.602 # guessed based on DejaVu-Sans-Mono
            bracket_bottom = bracket_text_displace + bracket_height # how far down the bracket bottom line should be drawn

            curpos = 0
            draw.font_size = 64
            # for each subcode

            skips_done = 0
            for i, inp in enumerate(inputs.keys()):
                remaining_keys = len(inputs)-i-1

                if inputs[inp]['description'] == 'skip':
                    char_count = len(inp)
                    curpos = curpos+char_count
                    skips_done+=1
                    continue

                char_count = len(inp)
                # if remaining_keys == 0:
                #     remaining_keys = 1
                nextpos=curpos+char_count

                # draw first vertical lines for a subcode
                draw.line( (text_x+curpos*font_width+bracket_shorten_x, bracket_force_y+text_y+bracket_text_displace),
                    (text_x+curpos*font_width+bracket_shorten_x, text_y+bracket_bottom) )

                if remaining_keys > 0:
                    # draw second vertical line
                    draw.line( (text_x+nextpos*font_width-bracket_shorten_x, bracket_force_y+text_y+bracket_text_displace),
                        (text_x+nextpos*font_width-bracket_shorten_x, text_y+bracket_bottom) )

                    # draw the underline
                    draw.line( (text_x+curpos*font_width+bracket_shorten_x, text_y+bracket_bottom),
                        (text_x+nextpos*font_width-bracket_shorten_x, text_y+bracket_bottom) )

                    midpoint = (text_x+curpos*font_width + text_x+nextpos*font_width+bracket_shorten_x*2)//2
                else:
                    # last element needs no bracket_shorten at the end
                    
                    # draw second vertical line
                    draw.line( (text_x+nextpos*font_width, bracket_force_y+text_y+bracket_text_displace),
                        (text_x+nextpos*font_width, text_y+bracket_bottom) )

                    # draw the underline
                    draw.line( (text_x+curpos*font_width+bracket_shorten_x, text_y+bracket_bottom),
                        (text_x+nextpos*font_width, text_y+bracket_bottom) )

                    midpoint = (text_x+curpos*font_width + text_x+nextpos*font_width+bracket_shorten_x)//2


                # draw the long vertical line
                height = draw.font_size*(remaining_keys-(skip_count-skips_done)+.5)*1.75
                draw.line((midpoint, text_y+bracket_bottom), (midpoint, text_y+bracket_bottom+height))


                # draw the horizontal line precending text
                width = draw.font_size * .85
                draw.line((midpoint, text_y+bracket_bottom+height),(midpoint+width, text_y+bracket_bottom+height))

                # write the description text
                draw.text(x=int(midpoint+width+bracket_text_displace), y=int(text_y+bracket_bottom+height+draw.font_size//2)-10, body=inputs[inp]['description'])




                curpos=nextpos

            draw(image)
            image.format = "png"
            image.save(filename='output.png')
            display(image)


main()








