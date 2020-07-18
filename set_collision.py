import notify2
import time
import pyautogui
import pyperclip
import sys
import util
import pytiled_parser

if len(sys.argv)<2:
    print("Maskfile (TMX File in CSV compression) needed")
    exit(1)
maskfile=sys.argv[1]

dx,dy,sx,sy=util.getGrid()

notify2.Notification('','I will start creating the map '+maskfile).show()

tilemap=pytiled_parser.parse_tile_map(maskfile)



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


notify2.Notification('','Everything finished').show()