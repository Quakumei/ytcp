# ytcp
- utility and similarly named site to create typical youtube playlist videos

# Roadmap

+ [ ] mvp 1: write script 
 ```
 ytcp \
 --music-list list.txt \ 
 --background-image bg.png \
 --foreground-image fg.png \
 --resolution=1280x720 \
 -o "laying in patches of sunlight.mp4"
 ``` 
+ [ ] mvp 2: write backend and return video via API
+ [ ] mvp 3: write frontend and make a running service on vercel
+ [ ] mvp 4: make a sustainable server and deploy service there

# Stack

- Java
It will be a somewhat highload backend application, therefore 
java as a backend seams like a reasonable choice. Plus, I want
to practice it. 

- But for now Python
I don't have that much experience in Java and it seems to be rather
complex to do that right off the bat. Let's say it's only a beginning.

# Features...

+ [ ] mvp 1
+ [ ] write not the links, but the link to the playlist with speial tag --playlist-url and link
+ [ ] render playlist titles list on the side if --show-playlist or something
+ [ ] --specify-titles option to change list format and specify for every song ask whether to leave its title or not 
+ [ ] Add explicit proxy support
+ [ ] Add custom kbps choice (currently default 320kbps)
    
# Thanks to
- youtube-dl
