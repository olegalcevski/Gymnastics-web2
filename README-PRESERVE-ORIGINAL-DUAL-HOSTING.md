# ФГСМ original-preserve dual hosting patch

This kit is for the original repo:

`https://github.com/olegalcevski/Gymnastics-web`

It does **not redesign or replace the public website**. It preserves the existing `index.html`, assets, CSS, layout, animations, routes, and content structure. It only adds a data adapter and replaces the old Decap/Netlify Identity admin with a portable admin.

## What changes

- Keeps original public design.
- Adds `app-config.js`.
- Adds `assets/js/content-adapter.js` to redirect original `fetch('content/*.json')` calls.
- Replaces `admin/index.html` with a custom admin panel.
- Adds Netlify Functions backend for Netlify.
- Adds PHP + MySQL backend for Zemi/cPanel.
- Adds `database/schema.sql`.

## Netlify mode

Backend:

- `/.netlify/functions/auth`
- `/.netlify/functions/content`
- `/.netlify/functions/upload`

Storage:

- GitHub JSON files in `content/*.json`
- Uploads committed to `assets/uploads/`

Required Netlify env variables:

```env
ADMIN_PASSWORD=your-admin-password
SESSION_SECRET=long-random-secret
GITHUB_TOKEN=github-fine-grained-token
GITHUB_OWNER=olegalcevski
GITHUB_REPO=Gymnastics-web
GITHUB_BRANCH=main
```

GitHub token permission:

- Fine-grained token
- Repository: `Gymnastics-web`
- Repository permissions: `Contents` → `Read and write`

Netlify deploy settings:

```txt
Build command: empty
Publish directory: .
Functions directory: netlify/functions
```

## Zemi mode

Before uploading to Zemi/cPanel:

1. Copy `app-config.zemi.js` over `app-config.js`.
2. Upload all website files to `public_html`.
3. In cPanel create a MySQL database and user.
4. Import `database/schema.sql` through phpMyAdmin.
5. Copy `config/config.example.php` to `config/config.php`.
6. Fill DB credentials and admin password.
7. Login at `/admin`.
8. Visit `/api/install.php` once while logged in to import existing `content/*.json` into MySQL.

After that:

`/admin` → PHP session → MySQL → original website updates from `/api/content.php`.

## Apply patch

From your cloned original repo root:

```powershell
py fgsm-original-preserve-dual-kit/tools/apply_preserve_original_patch.py
```

or:

```powershell
python fgsm-original-preserve-dual-kit/tools/apply_preserve_original_patch.py
```

Then commit and push.

## Important

Do not use the previous “complete project” ZIP if you want to preserve the original website. Use this original-preserve kit only.
