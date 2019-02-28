# 3D-Cloud-Renderer
Simulating a 3D cloud renderer using Flask, AWS S3 and 3ds Max

Cloud Rendering Demo - 
<br/>
[![Cloud Rendering Demo](https://img.youtube.com/vi/iWvDo0O_G0s/0.jpg "Cloud Rendering Demo")](https://youtu.be/iWvDo0O_G0s)

__Front-end:__ Flask | __Storage:__ AWS S3 Cloud | __Back-end:__ 3ds Max(running in local)

__Rendering Pipeline:__ (Checkout DEMO 3d_Cloud_renderer.mp4)

_Front-end:_
1. Use the UI to upload 3ds Max scene files(only .max extensions) to AWS S3.
2. Use the fetch models option to receive a list of all the available Max files from S3 Bucket.
3. Select rendering settings: resolution(width and height) and pixel offset.
4. Click render.(what happens in back-end explained below)
5. The final render image will be downloaded from S3 Bucket and displayed in UI.

_Back-end:_
1. Once you click render, respective Max file will be pulled to local.
2. Using the local copy of 3ds Max and specified render settings, 3ds Max command line rendering will be called.
3. The rendered image will then be uploaded to S3 Bucket from your local.
4. This rendered image is then pulled from S3 and displayed in browser(above).
