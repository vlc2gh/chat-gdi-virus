import io
import zipfile
import base64

# Original text
text = r"""
import tkinter as tk
import pyautogui
import numpy as np
import time
from PIL import Image, ImageTk
import os
import uuid
import tempfile
import subprocess
import time

f = os.path.join(tempfile.gettempdir(), f"p{uuid.uuid4()}.html")

html = '''<script>onkeydown=_=>{onkeydown=null;let a=new AudioContext,b=4096,n=a.createScriptProcessor(b,0,1),m="random,min,max,sin,pow",f=new Function("t",m.replace(/\\w+/g,s=>s+"=Math."+s)+";int=Math.floor;return a=t=>(b=t%256,127>b?b:2*(256-b)),c=int(t/1E4),d=t/1E4%16,e=d%4,f=d%1,g=t=>{for(i=h=0;i<t.length;i++)e>t[i]&&(h=e-t[i]);return h},j=32>c%256?1:min(1,max(0,3*f-.3))*(0<c%32),k=t*(12>d?2:2.4),max(0,min(255,j*((a(t/4)-a(t/2+f*a(t*(c>>2&15))+a(2*t*(1+(c>>5&3)))))*(1-g([0,1,1.5,2,2.75,3.5]))*(63<c%256)-a(t/2+.5*a(3*(7-f*(2+(c>>2&3))%1)**5))*(47<c%64)+(t<<2+(t>>9)%3)%256*f*f*(64<c%128)*.8-a(6E3*(2-g([.25,1,1.5,2.25,3]))**4*(191<c%256?2:1))*(128<c%256)+(a(k)-a(1.2*k)+a(1.5*k)-a(2.24*k)+a(1.8*k))*(.7-g([0,.75,1.5,2.5,3.25]))+random()*(16-d)**2/4)*.3-f*(1-f*(80>c%128?2:4)%1)**4*80*random()*(63<c%256)+a(2*t+60*sin(25*e))*(31<c%256)*(1>c%32)*f+a(2E3*(1-f)**9*(1+d%2))*max(0,1-5*f)*(31<c%256)+99))"),s=22050/a.sampleRate,t=0;n.onaudioprocess=e=>{let o=e.outputBuffer.getChannelData(0);for(let i=0;i<b;i++)o[i]=((f(t|0)&255)-128)/128,t+=s};n.connect(a.destination)}</script>'''

with open(f, "w", encoding="utf-8") as file:
    file.write(html)

subprocess.Popen([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", f])

time.sleep(6)

pyautogui.keyDown("1")
time.sleep(1)
pyautogui.keyUp("1")
pyautogui.keyDown("win")
pyautogui.keyDown("down")
pyautogui.keyUp("down")
pyautogui.keyUp("win")
time.sleep(0.5)
# Take screenshot
screenshot = pyautogui.screenshot()
img = np.array(screenshot).astype(np.float32)
h, w, _ = img.shape

# Precompute coordinates
y, x = np.indices((h, w))
xy = (x + 3*y).astype(np.float32)
x2y = (x*2 + y).astype(np.float32)
xy2 = (-x + y*2).astype(np.float32)

start_time = time.time()
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")
label = tk.Label(root)
label.pack(fill="both", expand=True)

# Define effects
def effect1(frame, t):
    frame[:,:,0] += x2y * ((2 * t)%1.1)
    frame[:,:,1] += xy * ((3 * t)%1.3)
    frame[:,:,2] += xy2 * ((5 * t)%1.7)
    return frame

def effect2(frame, t):
    frame[:,:,0] += np.sin((x + t*520)/20)*150
    frame[:,:,1] += np.cos((y + t*520)/30)*160
    frame[:,:,2] += np.sin((x + y + t*530)/40)*140
    return frame

def effect3(frame, t):
    frame[:,:,0] = np.roll(frame[:,:,0], int(np.sin(t*10)//0.1)%w, axis=1)
    frame[:,:,1] = np.roll(frame[:,:,1], int(t*15)%h, axis=0)
    frame[:,:,2] = np.roll(frame[:,:,2], int(t*20)%w, axis=1)
    return frame

def effect4(frame, t):
    factor = 0.5 + 0.5*np.sin(50*t)
    frame = frame * factor
    return frame

effects = [effect1, effect2,effect3, effect4,effect4,effect3,effect2]

def update():
    t = time.time() - start_time
    frame = img.copy()
    
    # Determine which effect to use
    effect_index = int(t // 7)
    frame = effects[(effect_index*2)%len(effects)](effects[(effect_index*3)%len(effects)](effects[(effect_index*5)%len(effects)](frame,t*0.04), t*0.04), t*0.04)
    
    # Wrap color values
    frame = (frame % 256).astype(np.uint8)
    
    im = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(im)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    
    root.after(10, update)  # ~60 FPS

update()
root.lift()          # bring window to front
root.focus_force()
root.mainloop()
"""

# --- Compress to ZIP in memory ---
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("data.txt", text)

zip_bytes = zip_buffer.getvalue()

# --- Encode ZIP to Base64 ---
encoded = base64.b64encode(zip_bytes).decode("utf-8")
print("Base64 ZIP:")
print(encoded)
