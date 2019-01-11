#!/usr/bin/env python3
import subprocess,argparse
XRANDR_NAME="xrandr"
def try_decode(s):
    try:return s.decode()
    except:return s
def extract_digits(s,default="0"):
    res="".join(c for c in s if c.isdigit())
    if len(res)==0:return default
    else:return res
def get_monitor_list():
    o=try_decode(subprocess.check_output([XRANDR_NAME,"--listactivemonitors"]))
    lines=[f.strip() for f in o.split("\n")]
    lines=[f for f in lines if len(f)>0]
    llen=len(lines)
    mnames=[]
    #minimal error handling lmao
    if llen>0:
        if "monitors" in lines[0].lower():
            monitor_count=int(extract_digits(lines[0]))
            if llen>=monitor_count+1:
                for i in range(monitor_count):
                    mnames.append(lines[1+i].split()[-1])
    return mnames

def set_brightness(monitor,brightness):return subprocess.check_call([XRANDR_NAME,"--output",monitor,"--brightness",str(brightness)])

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-l","--list",help="List monitors found",action="store_true")
    parser.add_argument("-v","--verbose",help="Hit me with that verbosity (hint: it actually don't do aught yet lmao)",action="store_true")
    parser.add_argument("-b","--brightness",help="Specify brightness",action="store",type=float)
    args=parser.parse_args()
    if args.list:
        monitors=get_monitor_list()
        print("Monitors: {0}\n{1}".format(len(monitors),"\n".join(monitors)))
    if args.brightness:
        monitors=get_monitor_list()
        for m in monitors:
            set_brightness(m,args.brightness)
            print("Set brightness on {0} to {1}".format(m,args.brightness))
