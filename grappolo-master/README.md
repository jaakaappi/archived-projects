# grappolo
Online pomodoro timer with friends

* Set your nickname (saved in local storage)
* Start a pomodoro session
* Set your work, short break and long break period lengths (saved in local storage)
* Select the number of periods before a long break (saved in local storage)
* Invite your friends with a direct link
* Chat
* (Make a ready check)
* Start your session for everyone and hide the chat until the work period ends
* Get a sound effect and a notification when the work period ends and a break starts
* Different sound effect for the longer break
* Auto loop?

* Front: React TS, CloudFront -> S3
* Back: NestJs TS, Fargate ECS
* DB: DynamoDB

* Check if the session is valid -> generate a new one if not
* Chat and ready check sound effects