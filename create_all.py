import notify2
import time
import pyautogui
import pyperclip
import sys
import util
import pytiled_parser
import optparse

class OptionParser (optparse.OptionParser):

    def check_required (self, opt):
      option = self.get_option(opt)

      # Assumes the option's 'default' is set to None!
      if getattr(self.values, option.dest) is None:
          self.error("%s option not supplied" % option)

parser=OptionParser()
parser.add_option("-f","--file",dest="filename",help="tmx file in csv compression for masks",metavar="FILE")
parser.add_option("-c","--collision",dest="collision",action="store_true",help="create collision mask",default=False)
parser.add_option("-o","--objects",dest="objects",action="store_true",help="create object mask",default=False)
# if len(sys.argv)<2:
#     print("File (tmx file in csv compression) needed")
#     exit(1)
# file=sys.argv[1]
(options,args)=parser.parse_args()
parser.check_required("-f")

# if 'filename' not in options.__dict__:
#     parser.error("filename required")
#     exit(1)
# print(options)
file=options.filename

if not options.collision and not options.objects:
    util.notify('Done')
    exit(0)

tilemap=pytiled_parser.parse_tile_map(file)

util.notify('I will start creating the map '+file)

dx,dy,sx,sy=util.getGrid()


if options.collision:

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



if options.objects:

    util.notify('Creating objects')

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


util.notify('Everything finished')
