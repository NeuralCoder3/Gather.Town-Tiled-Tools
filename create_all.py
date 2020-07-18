import notify2
import time
import pyautogui
import pyperclip
import sys
import util
import pytiled_parser


if len(sys.argv)<2:
    print("File (tmx file in csv compression) needed")
    exit(1)
file=sys.argv[1]

tilemap=pytiled_parser.parse_tile_map(file)

notify2.Notification('','I will start creating the map '+file).show()

dx,dy,sx,sy=util.getGrid()




util.browserCmd("document.getElementsByTagName('button')[1].click();")

mask=None
for layer in tilemap.layers:
    if layer.name=="Collision":
        mask=layer.data
        break

if mask is None:
    print("No collision layer was found")
    exit(1)

yc=0
xc=0
for row in mask:
    xc=0
    for cell in row:
        if cell>0:
            pyautogui.click(sx+dx*xc,sy+dy*yc)
        xc+=1
    yc+=1






notify2.Notification('','Creating objects').show()

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

            util.writeInput('object-popup-distThreshold',radius)
            util.writeInput('object-popup-highlighted',img)
            util.writeInput('object-popup-normal',img)
            util.writeInput('object-popup-previewMessage',name)
            util.writeInput('object-popup-zoomLink',url)

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

            util.writeInput('targetMap',dest)
            util.writeInput('targetMapX',destX)
            util.writeInput('targetMapY',destY)

            util.browserCmd("document.getElementsByTagName('button')[12].click();")
            print(px,py,"=>",dest,destX,destY)


notify2.Notification('','Everything finished').show()