# Agent work

reqire python 3.6.x [3.6.9]

## If you are not in python 3.6 , do following command
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.6
sudo apt install python3-pip
python3 -m pip install --user --upgrade pip



# Require enviroment

gst-launch-1.0 and plugin: rtspsrc, rtph264depay, mpegtsmux, hlssink

gst-launch-1.0 rtspsrc location="rtsp://link is-live=true ! rtph264depay ! mpegtsmux ! hlssink max-files=5 playlist-length=3 playlist-location=superindex.m3u8 playlist-root=\"/get-file-hls/camid" target-duration=15 --gst-debug=3 >loggst.txt 2>&1


pip3 install requests
