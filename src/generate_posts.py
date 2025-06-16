import os
from dominate.util import include
from dominate.tags import *

def generate_posts_html():
    # import html template
    template = include('src/html_template.html')
    template_split = template.text.split('<!-- posts-->')
    posts = p(cls='lead')
    
    # Add content
    with posts:
        with ul():
            # Scan the posts directory for HTML files
            posts_dir = 'src/posts'
            for filename in os.listdir(posts_dir):
                if filename.endswith('.md') and not any(file in filename for file in ('template','index')):
                    # Get the title from the filename (remove .html and replace - with spaces)
                    title = filename[:-3].replace('-', ' ').title()
                    with li():
                        a(title, href=f'post.html?post={filename[:-3]}')

    posts_txt = posts.render()    
    final_txt = f"{template_split[0]}{posts_txt}{template_split[1]}"    
    # Save the document
    with open('src/posts.html', 'w') as f:
        f.write(final_txt)

if __name__ == '__main__':
    generate_posts_html() 