A simple static blog template based on [markdown](https://www.markdownguide.org/getting-started/).  
[BS](https://en.wikipedia.org/wiki/Bullshit_(disambiguation)) not included 🐄💩

### Live Demo
https://vanilla-compost.netlify.app/
### Quickstart
1. Clone [this repo](https://github.com/EcologyComputing/vanilla-compost) locally.
2. Run it locally from /src with either:
    - With python: ``python -m http.server 8080``
    - or in an [nginx](https://nginx.org/) container (this line works on windows 11)  :  ``docker run -d --rm -p 8080:80 -v "$(pwd):/usr/share/nginx/html" nginx:stable-alpine3.21``  
3. View the default template at http://localhost:8080/  
4. Update for your content accordingly.
5. Add the project to you're own separate github repo.
6. Host it for free on [Netlify](https://docs.netlify.com/welcome/add-new-project/#import-from-an-existing-repository).
7. Add posts & updates via pull requests to your github repo.
## Definitions
***
### [vanilla](https://www.merriam-webster.com/dictionary/vanilla) (adjective)
 lacking distinction : plain, ordinary, conventional.

### [compost](https://www.merriam-webster.com/dictionary/compost) (noun)
 A mixture or compound.
 
 ## Motivation
 After running most of my personal websites on a VPS for over a decade, I decided it was time to migrate them to a more modern platform. Unfortunately, the options available on the market all felt bloated and over-engineered while somehow still lacking the user experience I was hoping for, so I started designing an alternative from [first principles](https://en.wikipedia.org/wiki/First_principle), like [this](https://justfuckingusehtml.com/). Vanilla compost sprouted from this exercise in design.
 
 ## The components  
 ***
 #### Vanilla HTML & CSS
 Static content should be static. HTML is simple enough. While CSS can get complex, the default version of this project only contains 15 lines of custom CSS.

 #### [Marked](https://github.com/markedjs/marked) for parsing Markdown
If HTML is too thick for you, then maybe markdown is more your speed. It was created in 2004 to make formatting text easier than vanilla HTML & CSS, and has since become an established standard for readme files (like the one you're reading), static site generators, and other documentation platforms.

Marked parses markdown to HTML and can be included in an HTML page with a single line of code. 

#### [Bootstrap](https://getbootstrap.com/) for UI
Bootstrap is a frontend toolkit that provides a lot of UI examples that only need 2 lines added to an HTML file to work. The Navigation for the default vanilla compost template (and all of my personal sites) is slimmed down version of [this navbar](https://getbootstrap.com/docs/5.3/components/navbar/).

#### [JQuery](https://jquery.com/) for browser glue
Jquery is a JS library that's fast, small, and feature rich. Vanilla compost uses jquery to parse the name and content of the mardown file for a post and hand it to Marked to display in the browser. A lot of static site generators do this in either a build step or on the backend, which starts to take forever as a site grows larger. Pushing this compute step to the end user's browser just in time for them to view the post their looking for saves a lot of time and energy.

#### [Dominate](https://github.com/Knio/dominate) & python for pipelines
Parsing and generating the full list of available posts would eventually be more than Jquery could handle in the browser. Instead, I shifted this compute step left on our value stream towards the build step. generate_posts.py uses Dominate to parse the available mardown files for each post then generates the posts.html page based off a template file. This can be executed locally while testing or run as part of a pipeline during your deployment process.