# Aniarc
A tool that help animator to observe and note the arcs in the animation.

## Repository
https://github.com/leealbert0508-pixel/Aniarc

## Description
This tool will accept image sequence, and allow user to add dot and annotation on the arc, and export as mp4 or gif.


## Features
Can play image sequence, can move frame by frame.
It has a GUI surface.

Can Create a visual timesheet under GUI surface(optional)
    - Work as timeline.
    - Dot will show on the timesheet.
    - In order to saprate different cell.
    - Ex. Cell A use red dot, Cell B use Bule dot...
    - Add it under the output video.

For adding dot, there are few mode(still thinking...
1. Just dot.
    - Dot only stay in each frame.
2. Dot trail
    - Dot between each frame will create a trial for pbservation.
3. Curve mode
    - Dot for previous frame will stay still, and create curve between dot from next frame.
    - user can chose they want curve or straight line between each dot.

About annotation, Aniarc allow user to add their note inside the frame.
    - User can decide how long will the annotation exist.
    - There are two mode for annotation.
        - Default: On the upper left corner, by default 50% opacity.
        - Custon: Click the curser to chose the place for the annotation.

## Challenges
Use knowladge and skill learn from the course.


## Outcomes
Ideal Outcome:
- Achieve all feature a mention in the "Feature".

Minimal Viable Outcome:
- Program can draw dot on the sequence and output the mp4 file.
    - Which I think is possible to just use the knowladge from class to achieve(Pygame).

## Milestones
- Week 1
3hr
    - Finsh the proposol -
    - Create a function that can read the image sepuence.
    - Can play the image sequence, and move frame by frame.
        - Include timeline

- Week 2
5~7hr
    - Debug code from last week.
    - Adding new idea or feature(if possible
    - Create a function to draw dot on each frame.
    - Create a function to change the color of dot.
    - Create a function to let user to select which frame they want to add dot, which do not.
        - dot stay still untill next dot being draw on the frame.

- Week 3
5~7hr
    - Debug code from last week
    - Create a function that use the dot, which user input, to create trail.
    - Create a function to create a curve between each dot.
        - user can chose they want curve or straight line between each dot.

- Week 4
5~7hr
    - Debug
    - Create function for annotation.
    - Clean up the code.
    - Record Video
    - Export Mp4 File