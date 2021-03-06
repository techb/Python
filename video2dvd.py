# requires ffmpeg, dvdauthor, genisoimage (a part of cdrkit)
# used on Arch Linux, any *nix distro should work
# feel free to add to extensions list, these are the ones I use

import sys
import os
import shutil
import time


frmat = "ntsc"
extensions = ("avi", "mkv", "mp4")
choice = []

if len(sys.argv) == 1:
    for f in os.listdir(os.getcwd()):
        if f[-3:] in extensions:
            choice.append(f)
    if len(choice) == 0:
        print("no videos found")
        sys.exit()
    count = 0
    for i in choice:
        print("%d) %s" % (count, i))
        count += 1
    c = input("Which one: ")
    try:
        chosen = choice[int(c)]
    except:
        print("try again")
        sys.exit()

else:
    # If there is space in the name, wrap in " "
    chosen = sys.argv[1]

print("[+] Creating mpg")
if os.path.isfile(chosen):
    print("Converting %s to mpg" % chosen[-3:])
    x = os.system("""ffmpeg -i "%s" -y -target %s-dvd -aspect 16:9 "%s.mpg" """ % (chosen,frmat, chosen[:-4]))
    if x != 0:
        print("Error, exiting")
        sys.exit()

# This isn't working, dvd just plays, no menu's. Idk. Script still works though.
print("[+] Creating xml")
xml = """
<dvdauthor>
    <vmgm />
    <titleset>
        <titles>
            <pgc><vob file="%s"/></pgc>
        </titles>
    </titleset>
</dvdauthor>
""" % (chosen[:-3]+"mpg")
print(xml)

with open("dvd.xml", "w") as f:
    f.write(xml)

print("Creating dvd")
os.environ['VIDEO_FORMAT'] = frmat
x = os.system("dvdauthor -o dvd -x dvd.xml")
if x != 0:
    print("Error, exiting")
    sys.exit()


print("[+] Creating Iso")
x = os.system("genisoimage -dvd-video -o dvd.iso dvd/")
if x != 0:
    print("Error, exiting")
    sys.exit()


os.system("eject")
input("[!] Insert DVD and press any enter to continue")
print("[+] Burning DVD")
# Give the drive time to spin up
time.sleep(25)

x = os.system("growisofs -dvd-compat -Z /dev/sr0=dvd.iso")
if x != 0:
    print("Error, exiting")
    sys.exit()

# This isn't good, need better clean up.
print("[+] Cleanup")
os.remove(chosen[:-3]+"mpg")
os.remove("dvd.xml")
os.remove("dvd.iso")
shutil.rmtree("dvd")
