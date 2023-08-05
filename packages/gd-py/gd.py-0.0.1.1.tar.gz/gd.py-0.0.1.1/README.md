# gd.py
gd.py Is A Geometry Dash API Wrapper For Python.
* Simple example:
```python
import gd #importing gd module
client = gd.client #library is based on gd.client
song = client.get_song(1) #fetches song with id '1'
print(song.name, song.dl_link) #prints song name and it's download link
```

