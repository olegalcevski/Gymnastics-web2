from pathlib import Path
import shutil

ROOT = Path.cwd()
KIT = Path(__file__).resolve().parents[1]
required = [ROOT/'index.html', ROOT/'content']
missing = [str(p) for p in required if not p.exists()]
if missing:
    raise SystemExit('Run this from the original Gymnastics-web repo root. Missing: ' + ', '.join(missing))

def copytree(src, dst):
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src, dst)

def copyfile(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

# Add backend/admin files. This replaces only admin/index.html, not public design.
copytree(KIT/'netlify', ROOT/'netlify')
copytree(KIT/'api', ROOT/'api')
copytree(KIT/'config', ROOT/'config')
copytree(KIT/'database', ROOT/'database')
(ROOT/'assets/js').mkdir(parents=True, exist_ok=True)
copyfile(KIT/'assets/js/content-adapter.js', ROOT/'assets/js/content-adapter.js')
copyfile(KIT/'admin/index.html', ROOT/'admin/index.html')
copyfile(KIT/'app-config.netlify.js', ROOT/'app-config.js')
copyfile(KIT/'app-config.netlify.js', ROOT/'app-config.netlify.js')
copyfile(KIT/'app-config.zemi.phpmode.js', ROOT/'app-config.zemi.js')
copyfile(KIT/'README-PRESERVE-ORIGINAL-DUAL-HOSTING.md', ROOT/'README-PRESERVE-ORIGINAL-DUAL-HOSTING.md')

# Inject the data adapter into the original index without changing design/content.
index = ROOT/'index.html'
text = index.read_text(encoding='utf-8')
if 'assets/js/content-adapter.js' not in text:
    injection = '<script src="app-config.js"></script>\n<script src="assets/js/content-adapter.js"></script>\n'
    if '</head>' in text:
        text = text.replace('</head>', injection + '</head>', 1)
    else:
        text = injection + text
    index.write_text(text, encoding='utf-8')

# Ensure Netlify knows where functions live.
netlify = ROOT/'netlify.toml'
existing = netlify.read_text(encoding='utf-8') if netlify.exists() else ''
if 'functions = "netlify/functions"' not in existing:
    block = '\n[build]\n  publish = "."\n  functions = "netlify/functions"\n'
    netlify.write_text(existing.rstrip() + block + '\n', encoding='utf-8')

# Add a simple .gitignore entry for real Zemi config.
gitignore = ROOT/'.gitignore'
gi = gitignore.read_text(encoding='utf-8') if gitignore.exists() else ''
for line in ['config/config.php']:
    if line not in gi:
        gi += ('\n' if gi and not gi.endswith('\n') else '') + line + '\n'
gitignore.write_text(gi, encoding='utf-8')

print('DONE: Original public website preserved. Added Netlify Functions, PHP/MySQL backend, admin replacement, and data adapter.')
print('Default mode is Netlify. For Zemi, copy app-config.zemi.js over app-config.js before uploading to public_html.')
