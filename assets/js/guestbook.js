/* Public guestbook: read labelled GitHub issues; visitors post on GitHub. */
(() => {
  'use strict';
  const guestbook = document.querySelector('.guestbook');
  if (!guestbook) return;
  const { repository, label } = guestbook.dataset;
  if (!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repository) || !/^[A-Za-z0-9_-]+$/.test(label)) return;
  const status = guestbook.querySelector('.guestbook-status');
  const list = guestbook.querySelector('.guestbook-messages');
  const refresh = guestbook.querySelector('.guestbook-refresh');
  const repositoryUrl = `https://github.com/${repository}`;
  const endpoint = `https://api.github.com/repos/${repository}/issues?labels=${encodeURIComponent(label)}&state=open&sort=created&direction=desc&per_page=5`;
  const dateFormat = new Intl.DateTimeFormat('en', { day: 'numeric', month: 'short', year: 'numeric' });
  let loading = false;

  const renderMessage = (issue) => {
    const entry = document.createElement('li');
    entry.className = 'guestbook-message';
    const heading = document.createElement('h4');
    const link = document.createElement('a');
    link.href = `${repositoryUrl}/issues/${issue.number}`;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = issue.title.replace(/^\[Guestbook\]\s*/i, '').trim() || 'Guestbook message';
    heading.append(link);
    const excerpt = document.createElement('p');
    const body = (issue.body || '').replace(/^### Message\s*\n+/i, '').trim();
    excerpt.textContent = body.length > 400 ? `${body.slice(0, 400).trimEnd()}…` : body;
    const meta = document.createElement('div');
    meta.className = 'guestbook-message-meta';
    const author = document.createElement('span');
    author.textContent = issue.user?.login ? `@${issue.user.login}` : 'GitHub visitor';
    meta.append(author);
    const date = new Date(issue.created_at);
    if (!Number.isNaN(date.getTime())) {
      const time = document.createElement('time');
      time.dateTime = date.toISOString();
      time.textContent = dateFormat.format(date);
      meta.append(time);
    }
    const replies = document.createElement('span');
    replies.textContent = `${issue.comments || 0} ${issue.comments === 1 ? 'reply' : 'replies'}`;
    meta.append(replies);
    entry.append(heading, excerpt, meta);
    return entry;
  };

  const loadMessages = async () => {
    if (loading) return;
    loading = true;
    refresh.disabled = true;
    guestbook.setAttribute('aria-busy', 'true');
    status.textContent = 'Loading recent messages…';
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 12000);
    try {
      const response = await fetch(endpoint, {
        headers: { Accept: 'application/vnd.github+json' },
        credentials: 'omit',
        signal: controller.signal,
      });
      if (!response.ok) throw new Error('Guestbook unavailable');
      const issues = await response.json();
      if (!Array.isArray(issues)) throw new Error('Invalid guestbook response');
      const messages = issues.filter(issue => !issue.pull_request && Number.isSafeInteger(issue.number) && issue.number > 0 && typeof issue.title === 'string');
      list.replaceChildren(...messages.map(renderMessage));
      status.textContent = messages.length ? 'Recent public messages' : 'No messages yet. Be the first to leave one.';
    } catch (_) {
      status.textContent = list.children.length
        ? 'Could not refresh messages. You can read the latest messages on GitHub.'
        : 'Recent messages could not be loaded. You can read or leave a message on GitHub.';
    } finally {
      window.clearTimeout(timeout);
      loading = false;
      refresh.disabled = false;
      refresh.hidden = false;
      guestbook.setAttribute('aria-busy', 'false');
    }
  };
  refresh.addEventListener('click', loadMessages);
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        observer.disconnect();
        loadMessages();
      }
    }, { rootMargin: '300px' });
    observer.observe(guestbook);
  } else {
    loadMessages();
  }
})();
