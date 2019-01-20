# JobBot
In an attempt to make applying to jobs more productive and less soul-sucking I decided it would be cool if I tried to automate the process.
The JobBot application consists of multiple parts:
1. ApplicationBuilder: 
    1. This class will generate a custom message and resume (Not implemented) based on the job description given
2. Bot:       
    `Bot` is an abstract class that implements a bunch of methods that are common between all the Bot classes.    
    Currently there are 2 bot classes:
      1. `AngelBot`: Manually crawls through job listings using Selenium and applies to them
      2. `LinkedInBot`: Manually visit recruiter's profiles in the hope that they visit my profile and give me a job
### Thoughts
- `AngelBot` was actually super easy to implement and effective since all you needed to apply to a job was to click a button.
    - I really believe that adding an additional note to each job based on my template and keywords ironically differentiated me from crowd of people mindlessly applying to jobs
    - I got my job at Ravelin through an application by `AngelBot`!
## Required Files:
You need these files for the application to work properly:
* "blurbs.json" - This file contains the keywords and text that are used to generate a custom message      
    * The way it works is you specify keywords or tags that will trigger a blurb to be inserted into your custom message, if they are in the job description.
