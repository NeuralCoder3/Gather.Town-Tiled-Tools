
import notify2
import time
import pyautogui
import pyperclip
import sys
import util
import pytiled_parser

def writeInput(field,text):
    util.browserCmd("document.getElementById('"+field+"').focus();")
    time.sleep(0.5)
    pyautogui.hotkey('ctrl','a')
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl','v')

if len(sys.argv)<2:
    print("Portalfile (tmx file in csv compression) needed")
    exit(1)
file=sys.argv[1]


tilemap=pytiled_parser.parse_tile_map(file)

dx,dy,sx,sy=util.getGrid()

for layer in tilemap.layers:
    if not isinstance(layer, pytiled_parser.objects.ObjectLayer):
        continue
    if layer.name=="Link":
        util.browserCmd("document.getElementsByTagName('button')[5].click();")
        for link in layer.tiled_objects:
            px=int(link.location.x//32)
            py=int(link.location.y//32)

            radius=link.properties["r"]
            img=link.properties["img"]
            url=link.properties["url"]
            name='Press x to enter '+link.properties["name"]

            pyautogui.click(sx+dx*px,sy+dy*py)
            time.sleep(1)
            util.browserCmd("document.querySelectorAll('.mm-tooltip-container')[5].click()")

            writeInput('object-popup-distThreshold',radius)
            writeInput('object-popup-highlighted',img)
            writeInput('object-popup-normal',img)
            writeInput('object-popup-previewMessage',name)
            writeInput('object-popup-zoomLink',url)

            util.browserCmd("document.getElementsByTagName('button')[12].click();")

    elif layer.name=="Portal":
        util.browserCmd("document.getElementsByTagName('button')[3].click();")
        for portal in layer.tiled_objects:
            px=int(portal.location.x//32)
            py=int(portal.location.y//32)

            dest=portal.properties["to"]
            destX=portal.properties["x"]
            destY=portal.properties["y"]

            pyautogui.click(sx+dx*px,sy+dy*py)
            time.sleep(1)

            writeInput('targetMap',dest)
            writeInput('targetMapX',destX)
            writeInput('targetMapY',destY)

            util.browserCmd("document.getElementsByTagName('button')[12].click();")
            print(px,py,"=>",dest,destX,destY)