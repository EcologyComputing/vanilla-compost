const fs = require('fs');
const path = require('path');

function extractTitleFromMarkdown(filepath) {
    try {
        const content = fs.readFileSync(filepath, 'utf8');
        const firstLine = content.split('\n')[0].trim();
        const match = firstLine.match(/<!--\s*title:\s*(.+?)\s*-->/);
        if (match) {
            return match[1];
        }
    } catch (e) {
        console.error(`Error reading title from ${filepath}:`, e);
    }
    const basename = path.basename(filepath, '.md');
    return basename.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

function formatDate(date) {
    const day = String(date.getDate()).padStart(2, '0');
    return `${MONTHS[date.getMonth()]} ${day}, ${date.getFullYear()}`;
}

function extractDateFromMarkdown(filepath) {
    try {
        const content = fs.readFileSync(filepath, 'utf8');
        const datePatterns = [
            /\*([A-Za-z]+ \d{1,2}, \d{4})\*/, // *January 15, 2024*
            /(\d{4}-\d{2}-\d{2})/,             // 2024-01-15
            /([A-Za-z]+ \d{1,2}, \d{4})/        // January 15, 2024
        ];
        for (const pattern of datePatterns) {
            const match = content.match(pattern);
            if (match) {
                return match[1];
            }
        }
    } catch (e) {
        console.error(`Error reading date from ${filepath}:`, e);
    }

    try {
        const stats = fs.statSync(filepath);
        return formatDate(stats.mtime);
    } catch (e) {
        return "Unknown date";
    }
}

function dateSortKey(dateStr) {
    // Parse against the two specific formats this file actually writes/reads,
    // rather than the more permissive Date.parse - which would also "succeed"
    // on date-like strings that aren't really one of these two formats.
    const monthMatch = dateStr.match(/^([A-Za-z]+) (\d{1,2}), (\d{4})$/);
    if (monthMatch) {
        const monthIndex = MONTHS.indexOf(monthMatch[1]);
        if (monthIndex !== -1) {
            return new Date(Number(monthMatch[3]), monthIndex, Number(monthMatch[2])).getTime();
        }
    }

    const isoMatch = dateStr.match(/^(\d{4})-(\d{2})-(\d{2})$/);
    if (isoMatch) {
        return new Date(Number(isoMatch[1]), Number(isoMatch[2]) - 1, Number(isoMatch[3])).getTime();
    }

    return 0; // unparseable - treat as oldest, matching the Python version's datetime.min fallback
}

function generatePostsHtml() {
    const srcDir = __dirname;
    const templatePath = path.join(srcDir, 'html_template.html');
    if (!fs.existsSync(templatePath)) {
        console.error(`Could not find template at ${templatePath}`);
        process.exit(1);
    }
    const template = fs.readFileSync(templatePath, 'utf8');

    const postsDir = path.join(srcDir, 'posts');
    if (!fs.existsSync(postsDir)) {
        console.error(`Could not find posts directory at ${postsDir}`);
        process.exit(1);
    }

    const files = fs.readdirSync(postsDir);
    const entries = [];

    for (const filename of files) {
        if (filename.endsWith('.md') && !filename.includes('template') && !filename.includes('index')) {
            const filepath = path.join(postsDir, filename);
            entries.push({
                name: filename.slice(0, -3),
                title: extractTitleFromMarkdown(filepath),
                date: extractDateFromMarkdown(filepath)
            });
        }
    }

    entries.sort((a, b) => dateSortKey(b.date) - dateSortKey(a.date));

    let postsHtml = '<p class="lead">\n  <ul>\n';
    for (const entry of entries) {
        postsHtml += `    <li><a href="post.html?post=${entry.name}">${entry.title}</a> <small>(${entry.date})</small></li>\n`;
    }
    if (entries.length === 0) {
        postsHtml += '    <li>No posts available yet.</li>\n';
    }
    postsHtml += '  </ul>\n</p>\n';

    if (!template.includes('<!-- posts-->')) {
        throw new Error('Could not find <!-- posts--> marker in html_template.html');
    }

    const newContent = template.replace('<!-- posts-->', postsHtml);
    const outputPath = path.join(srcDir, 'posts.html');
    fs.writeFileSync(outputPath, newContent, 'utf8');

    console.log(`Generated posts.html with ${entries.length} posts using html_template.html`);
}

generatePostsHtml();
