import json,sys,base64,re
from PIL import Image
import io
parts=[]
for f in sys.argv[2:]:
    data=json.load(open(f))
    t=data[0]['text'] if isinstance(data,list) else data
    t=t.strip()
    # unwrap JSON string if quoted
    if t.startswith('"'):
        t=json.JSONDecoder().raw_decode(t)[0]
    parts.append(t)
s=''.join(parts)
b64=s.split(',',1)[1]
im=Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGBA')
bbox=im.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox()
im=im.crop(bbox)
im.save(sys.argv[1]); print(sys.argv[1], im.size)
