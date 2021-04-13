#!/bin/bash 

# This script record your desktop. It calculates your screen resoltion and saves
# the video in ~/Video/output.mkv file. 
# dilawar@ee.iitb.ac.in
#rm -f ~/Video/output.mkv
Xaxis=$(xrandr -q | grep '*' | uniq | awk '{print $1}' |  cut -d 'x' -f1)
Yaxis=$(xrandr -q | grep '*' | uniq | awk '{print $1}' |  cut -d 'x' -f2)
ffmpeg -video_size $(($Xaxis))x$(($Yaxis)) -r 60 -f x11grab -i :0.0 \
       -f alsa -ac 2 -i default \
       -c:v libx264 -qp 0 -preset ultrafast \
       "$HOME/Rec-$(date '+%Y-%m-%d_%H.%M.%S').mp4"
