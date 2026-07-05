import os
import re
from datetime import datetime


def extract_title_from_markdown(filepath):
    """Extract title from a <!-- title: ... --> comment if present, otherwise use the filename."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            match = re.match(r'<!--\s*title:\s*(.+?)\s*-->', first_line)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error reading title from {filepath}: {e}")
    return os.path.basename(filepath).replace('.md', '').replace('-', ' ').title()


def extract_date_from_markdown(filepath):
    """Extract date from markdown file if present, else fall back to file mtime."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            date_patterns = [
                r'\*([A-Za-z]+ \d{1,2}, \d{4})\*',  # *January 15, 2024*
                r'(\d{4}-\d{2}-\d{2})',              # 2024-01-15
                r'([A-Za-z]+ \d{1,2}, \d{4})',       # January 15, 2024
            ]
            for pattern in date_patterns:
                match = re.search(pattern, content)
                if match:
                    return match.group(1)
    except Exception as e:
        print(f"Error reading date from {filepath}: {e}")

    try:
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).strftime('%B %d, %Y')
    except Exception:
        return "Unknown date"


def date_sort_key(date_str):
    """Parse a date string for chronological sorting instead of comparing it as text."""
    for fmt in ('%B %d, %Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return datetime.min


def generate_posts_html():
    """Generate posts.html by scanning posts/ and inserting a list into the <!-- posts--> marker in html_template.html."""

    # Anchor every path to this script's own location so it can be run from anywhere,
    # not just from the repo root.
    src_dir = os.path.dirname(os.path.abspath(__file__))

    template_path = os.path.join(src_dir, 'html_template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Scan the posts directory for markdown files
    posts_dir = os.path.join(src_dir, 'posts')
    entries = []
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md') and not any(word in filename for word in ('template', 'index')):
            filepath = os.path.join(posts_dir, filename)
            entries.append({
                'name': filename[:-3],
                'title': extract_title_from_markdown(filepath),
                'date': extract_date_from_markdown(filepath),
            })

    # Sort posts by date (newest first) - parsed, not string-compared
    entries.sort(key=lambda e: date_sort_key(e['date']), reverse=True)

    posts_html = '<p class="lead">\n  <ul>\n'
    for entry in entries:
        posts_html += f'    <li><a href="post.html?post={entry["name"]}">{entry["title"]}</a> <small>({entry["date"]})</small></li>\n'
    if not entries:
        posts_html += '    <li>No posts available yet.</li>\n'
    posts_html += '  </ul>\n</p>\n'

    if '<!-- posts-->' not in template:
        raise Exception('Could not find <!-- posts--> marker in html_template.html')

    new_content = template.replace('<!-- posts-->', posts_html)

    output_path = os.path.join(src_dir, 'posts.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Generated posts.html with {len(entries)} posts using html_template.html")


if __name__ == '__main__':
    generate_posts_html()
