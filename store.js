/* store.js — the pages' link to the server.

   Each page owns one document (the dashboard's apps and categories, or the
   passkey tracker's accounts). Pages keep working on an in-memory copy exactly
   as before and call save() after every change; this file turns those calls
   into whole-document PUTs, one at a time, in order.

   Every document carries a revision. A write sent from a stale copy is
   refused by the server with the current document, and onConflict() hands
   that to the page. Nothing is merged and nothing is silently overwritten.

   Notices appear only when something is wrong (Exception-Only Rule); a
   healthy save shows nothing at all. */
(function () {
    'use strict';

    const ENDPOINTS = { dashboard: '/api/dashboard', passkeys: '/api/passkeys' };

    /* ---- the one notice ---- */
    let notice = null;
    let noticeText = null;
    let noticeAction = null;

    function ensureNotice() {
        if (notice) return;
        const style = document.createElement('style');
        style.textContent =
            '.sync-notice{position:fixed;left:20px;bottom:20px;z-index:50;max-width:min(420px,calc(100vw - 40px));' +
            'display:flex;align-items:center;gap:15px;padding:10px 15px;background:var(--surface);color:var(--ink);' +
            'border:1px solid var(--rule);border-radius:8px;font:inherit;font-size:.9rem;line-height:1.5}' +
            '.sync-notice[hidden]{display:none}' +
            '.sync-notice button{flex:none;font:inherit;font-size:.9rem;font-weight:500;padding:5px 10px;cursor:pointer;' +
            'background:var(--surface);color:var(--ink);border:1px solid var(--rule);border-radius:6px}' +
            '.sync-notice button:hover{background:var(--signal-wash);border-color:var(--signal);color:var(--signal)}' +
            '.sync-notice button:focus-visible{outline:2px solid var(--signal);outline-offset:2px}';
        document.head.appendChild(style);

        notice = document.createElement('div');
        notice.className = 'sync-notice';
        notice.setAttribute('role', 'status');
        notice.hidden = true;
        noticeText = document.createElement('span');
        noticeAction = document.createElement('button');
        noticeAction.type = 'button';
        notice.append(noticeText, noticeAction);
        document.body.appendChild(notice);
    }

    function showNotice(message, actionLabel, onAction) {
        ensureNotice();
        noticeText.textContent = message;
        noticeAction.hidden = !actionLabel;
        noticeAction.textContent = actionLabel || '';
        noticeAction.onclick = onAction || null;
        notice.hidden = false;
    }

    function hideNotice() {
        if (notice) notice.hidden = true;
    }

    /* ---- a store ---- */
    function create(name, options) {
        const url = ENDPOINTS[name];
        const delay = (options && options.delay) || 0;
        const onConflict = (options && options.onConflict) || function () {};

        let rev = 0;
        let getter = null;
        let dirty = false;
        let inflight = false;
        let timer = null;
        let retryTimer = null;
        let failures = 0;

        async function load() {
            const res = await fetch(url, { cache: 'no-store' });
            if (!res.ok) throw new Error('HTTP ' + res.status);
            const doc = await res.json();
            rev = doc.rev;
            hideNotice();
            return doc;
        }

        function save(get) {
            getter = get;
            dirty = true;
            clearTimeout(timer);
            clearTimeout(retryTimer);
            timer = setTimeout(flush, delay);
        }

        async function flush() {
            clearTimeout(timer);
            timer = null;
            if (inflight || !dirty) return;
            inflight = true;
            dirty = false;

            const body = JSON.stringify(Object.assign({}, getter(), { baseRev: rev }));
            let retry = false;
            try {
                const res = await fetch(url, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: body,
                    // Lets a save started as the tab closes still complete.
                    // The browser caps keepalive bodies at 64 KB.
                    keepalive: body.length < 60000
                });
                if (res.status === 409) {
                    const latest = await res.json();
                    rev = latest.rev;
                    dirty = false;
                    failures = 0;
                    hideNotice();
                    onConflict(latest);
                } else if (!res.ok) {
                    throw new Error('HTTP ' + res.status);
                } else {
                    rev = (await res.json()).rev;
                    failures = 0;
                    hideNotice();
                }
            } catch (err) {
                dirty = true;
                retry = true;
                failures += 1;
                showNotice('Not saved: can’t reach the server. Retrying…', 'Retry now', flush);
            } finally {
                inflight = false;
            }

            if (retry) {
                clearTimeout(retryTimer);
                retryTimer = setTimeout(flush, Math.min(30000, 2000 * Math.pow(2, failures - 1)));
            } else if (dirty) {
                flush();
            }
        }

        // Returns the server's document if it has moved on since we loaded
        // and we have nothing unsaved; otherwise null. Used when a tab comes
        // back into view, so a change made on another machine appears
        // without a reload.
        async function refresh() {
            if (dirty || inflight || timer) return null;
            try {
                const res = await fetch(url, { cache: 'no-store' });
                if (!res.ok) return null;
                const doc = await res.json();
                if (dirty || inflight || timer || doc.rev === rev) return null;
                rev = doc.rev;
                return doc;
            } catch (err) {
                return null;
            }
        }

        window.addEventListener('pagehide', function () {
            if (dirty) flush();
        });

        return { load: load, save: save, refresh: refresh };
    }

    window.MSKStore = { create: create, showNotice: showNotice, hideNotice: hideNotice };
})();
