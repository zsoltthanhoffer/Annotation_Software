# Spatial Annotation Software

This software serves the purpose of annotating objects in imported videos.

## Details

### 1. Launch

- Only the executable file in the "dist" folder is required.
- After downloading it, run the executable.

### 2. Usage

- Once the program is open, click the "Browse" button to import a video.
- After importing, a new window (using OpenCV) opens with the video, and video playback begins.
- At the top of the video window, you can see the current frame of the video, and there is a slider to navigate to a specific frame.
- You can control the video using buttons on the blue interface or use shortcut keys for faster workflow.
- In the video window, you can draw rectangles with your mouse to annotate objects in the scene.
- Use the "Start Here" button to save the starting frame.
- Use the "End Here" button to save the last frame to be annotated.
- In the field next to the "Label," you can enter a label for the object you want to annotate with the rectangle.
- Use the "Submit" button to add the entry to the table at the top of the blue interface. This table shows the start and end frame numbers, as well as the assigned label.
- By clicking the "Save" button, you can save all entries in the table to an XML file. The file will contain the start frame, end frame, label, and the starting and ending points of the rectangle on the frame.

### 3. Table Management

- You can delete specific rows using the "Delete" button by selecting multiple rows in the table.
- The "Clear All" button deletes all previously added entries from the table.

### 4. Shortcut Keys

- While standing in the video window:
  - Press 'q' to pause the video.
  - Press 'w' to save the starting frame for annotation (Start Here).
  - Press 'e' to save the ending frame for annotation (End Here).
  - Press 's' to save the annotation with the start and end frames to the table.
- Shortcut keys are available even after pressing 'q.'
- If the video is playing, you can close the video player window by pressing 'esc.'

