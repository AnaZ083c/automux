#!/bin/sh

# Set Session Name
SESSION="MySession"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

# Only create tmux session if it doesn't already exist
if [ "$SESSIONEXISTS" = "" ]
then
    # Start New Session with our name
    tmux new-session -d -s $SESSION

    tmux rename-window -t 0 'first_window'
    tmux send-keys -t $SESSION:'first_window' 'echo "First window!"' C-m

    tmux new-window -t $SESSION:1 -n 'second_window'
    tmux send-keys -t $SESSION:'second_window' 'echo "Second window!"' C-m
fi

# Attach Session, on the Main window
tmux attach-session -t $SESSION:0
