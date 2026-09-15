(() => {
  const root = document.documentElement;
  const languageButton = document.querySelector('[data-action="language"]');
  const themeButton = document.querySelector('[data-action="theme"]');
  const savedTheme = localStorage.getItem('academic-theme');
  const savedLanguage = localStorage.getItem('academic-language') || 'zh';

  function applyTheme(theme) {
    root.dataset.theme = theme;
    localStorage.setItem('academic-theme', theme);
    if (themeButton) {
      themeButton.textContent = theme === 'dark' ? (root.lang === 'en' ? 'Light' : '浅色') : (root.lang === 'en' ? 'Dark' : '深色');
      themeButton.setAttribute('aria-pressed', String(theme === 'dark'));
    }
  }

  function applyLanguage(language) {
    root.lang = language === 'en' ? 'en' : 'zh-CN';
    document.querySelectorAll('[data-zh][data-en]').forEach((element) => {
      element.textContent = language === 'en' ? element.dataset.en : element.dataset.zh;
    });
    if (languageButton) languageButton.textContent = language === 'en' ? '中文' : 'EN';
    const filter = document.querySelector('[data-course-filter]');
    if (filter) filter.placeholder = language === 'en' ? 'Date, topic or lecture' : '输入日期、主题或讲次';
    localStorage.setItem('academic-language', language);
    applyTheme(root.dataset.theme || 'light');
  }

  const preferredTheme = savedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  applyTheme(preferredTheme);
  applyLanguage(savedLanguage);

  languageButton?.addEventListener('click', () => applyLanguage(root.lang === 'en' ? 'zh' : 'en'));
  themeButton?.addEventListener('click', () => applyTheme(root.dataset.theme === 'dark' ? 'light' : 'dark'));
  document.querySelector('[data-action="print"]')?.addEventListener('click', () => window.print());

  const topButton = document.querySelector('[data-action="top"]');
  const updateTopButton = () => topButton?.classList.toggle('visible', window.scrollY > 360);
  window.addEventListener('scroll', updateTopButton, { passive: true });
  topButton?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  updateTopButton();

  const sectionLinks = [...document.querySelectorAll('[data-section-nav] a[href^="#"]')];
  const sections = sectionLinks.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      sectionLinks.forEach((link) => {
        const active = link.getAttribute('href') === `#${visible.target.id}`;
        link.classList.toggle('active', active);
        if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
      });
    }, { rootMargin: '-18% 0px -62% 0px', threshold: [0, .2, .6] });
    sections.forEach((section) => observer.observe(section));
  }

  const filter = document.querySelector('[data-course-filter]');
  const rows = [...document.querySelectorAll('.table-wrap tbody tr')];
  const count = document.querySelector('[data-filter-count]');
  if (filter && rows.length) {
    const updateFilter = () => {
      const query = filter.value.trim().toLocaleLowerCase();
      let visible = 0;
      rows.forEach((row) => {
        const matches = !query || row.textContent.toLocaleLowerCase().includes(query);
        row.hidden = !matches;
        if (matches) visible += 1;
      });
      if (count) count.textContent = query ? `${visible} / ${rows.length}` : '';
    };
    filter.addEventListener('input', updateFilter);
  }
})();
