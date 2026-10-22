/* ============================================================
   Portfolio runtime — smooth scroll, preloader, hero intro,
   reveals, marquees, counters, hover previews, custom cursor,
   filters, contact form.
   ============================================================ */

(function () {
  'use strict';

  document.documentElement.classList.add('js');

  var gsap = window.gsap;
  var ScrollTrigger = window.ScrollTrigger;
  var SplitText = window.SplitText;
  var Lenis = window.Lenis;

  if (!gsap) {
    // No animation library: show everything and bail out gracefully.
    document.documentElement.classList.remove('js');
    var pl = document.querySelector('.preloader');
    if (pl) pl.remove();
    return;
  }

  gsap.registerPlugin(ScrollTrigger, SplitText);

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var FINE_POINTER = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------- Smooth scroll ---------- */
  var lenis = null;
  if (Lenis) {
    lenis = new Lenis({ lerp: 0.085, wheelMultiplier: 1, anchors: { offset: -40 } });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
  }

  /* ---------- Local clock ---------- */
  function initClock() {
    var els = $$('[data-clock]');
    if (!els.length) return;
    var fmt = new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
    var tick = function () {
      var now = fmt.format(new Date());
      els.forEach(function (el) { el.textContent = now; });
    };
    tick();
    setInterval(tick, 1000);
  }

  /* ---------- Header + mobile menu ---------- */
  function initHeader() {
    var header = $('[data-header]');
    if (!header) return;

    var last = 0;
    var hero = $('[data-hero]');
    var update = function (y) {
      header.classList.toggle('is-hidden', y > 160 && y > last && !document.body.classList.contains('menu-open'));
      header.classList.toggle('is-scrolled', y > 40);
      header.classList.toggle('is-transparent', !!hero && y < hero.offsetHeight - header.offsetHeight);
      last = y;
    };
    update(window.scrollY);
    if (lenis) lenis.on('scroll', function (e) { update(e.scroll); });
    else window.addEventListener('scroll', function () { update(window.scrollY); }, { passive: true });

    var toggle = $('[data-menu-toggle]');
    var menu = $('[data-menu]');
    if (!toggle || !menu) return;

    $$('a', menu).forEach(function (a) {
      a.addEventListener('click', function () {
        if (toggle.getAttribute('aria-expanded') === 'true') toggle.click();
      });
    });

    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.classList.toggle('menu-open', open);
      if (open) {
        menu.hidden = false;
        requestAnimationFrame(function () { menu.classList.add('is-open'); });
        if (lenis) lenis.stop();
        gsap.fromTo($$('.menu__link', menu),
          { yPercent: 100, opacity: 0 },
          { yPercent: 0, opacity: 1, duration: 1, ease: 'expo.out', stagger: 0.06, delay: 0.25 });
      } else {
        menu.classList.remove('is-open');
        if (lenis) lenis.start();
        setTimeout(function () { menu.hidden = true; }, 800);
      }
    });
  }

  /* ---------- Custom cursor ---------- */
  function initCursor() {
    var cursor = $('[data-cursor-el]');
    if (!cursor || !FINE_POINTER) return;
    document.documentElement.classList.add('has-cursor');

    var dot = $('.cursor__dot', cursor);
    var ring = $('.cursor__ring', cursor);
    var label = $('[data-cursor-label]', cursor);
    var name = $('[data-cursor-name]', cursor);

    var orbit = function (text) {
      var unit = text.toUpperCase() + ' • ';
      return unit.repeat(Math.max(1, Math.floor(34 / unit.length)));
    };

    var dx = gsap.quickTo(dot, 'x', { duration: 0.1 });
    var dy = gsap.quickTo(dot, 'y', { duration: 0.1 });
    var rx = gsap.quickTo(ring, 'x', { duration: 0.5, ease: 'power3' });
    var ry = gsap.quickTo(ring, 'y', { duration: 0.5, ease: 'power3' });

    window.addEventListener('pointermove', function (e) {
      dx(e.clientX); dy(e.clientY); rx(e.clientX); ry(e.clientY);
    });

    document.addEventListener('pointerover', function (e) {
      var target = e.target.closest ? e.target.closest('[data-cursor="view"]') : null;
      cursor.classList.toggle('is-view', !!target);
      if (target) label.textContent = target.dataset.cursorLabel || 'View';
      var projectName = target && target.dataset.cursorName;
      cursor.classList.toggle('has-name', !!projectName);
      if (name && projectName && name.dataset.for !== projectName) {
        name.textContent = orbit(projectName);
        name.dataset.for = projectName;
      }
    });

    document.addEventListener('pointerleave', function () { gsap.to(cursor, { opacity: 0, duration: 0.3 }); });
    document.addEventListener('pointerenter', function () { gsap.to(cursor, { opacity: 1, duration: 0.3 }); });
  }

  /* ---------- Hero intro + preloader ---------- */
  function initHeroIntro() {
    var hero = $('[data-hero]');
    if (!hero) return;

    var chars = [];
    $$('[data-hero-line]', hero).forEach(function (line) {
      var split = new SplitText(line, { type: 'chars', charsClass: 'char' });
      chars.push.apply(chars, split.chars);
    });

    var fades = $$('[data-hero-fade]', hero);
    var pills = $$('[data-pill]', hero);
    var rotators = $$('[data-rotate]', hero);
    var preloader = $('.preloader');

    gsap.set(chars, { yPercent: 115 });
    gsap.set(fades, { opacity: 0, y: 16 });
    gsap.set(pills, { yPercent: 115 });
    gsap.set(rotators, { yPercent: 115 });

    var intro = gsap.timeline({ paused: true, defaults: { ease: 'expo.out' } });
    intro
      .to(chars, { yPercent: 0, duration: 1.4, stagger: 0.022 })
      .to(rotators, { yPercent: 0, duration: 1.4 }, 0.12)
      .to(pills, { yPercent: 0, duration: 1.4 }, 0.18)
      .to(fades, { opacity: 1, y: 0, duration: 1.2, stagger: 0.08 }, 0.6);

    pills.forEach(function (pill) {
      var img = pill.querySelector('img');
      if (!img) return;
      var mark = function () { img.classList.add('is-loaded'); };
      if (img.complete && img.naturalWidth) mark();
      else if (img.decode) img.decode().then(mark, mark);
      else img.addEventListener('load', mark);
    });

    var seen = sessionStorage.getItem('pm-intro');
    if (!preloader || seen) {
      if (preloader) preloader.remove();
      intro.play(0.1);
      return;
    }

    sessionStorage.setItem('pm-intro', '1');
    if (lenis) lenis.stop();

    var count = $('[data-count]', preloader);
    var bar = $('.preloader__bar span', preloader);
    var value = { v: 0 };

    gsap.timeline()
      .to(value, {
        v: 100, duration: 1.8, ease: 'power3.inOut',
        onUpdate: function () { count.textContent = String(Math.round(value.v)).padStart(3, '0'); }
      })
      .to(bar, { scaleX: 1, duration: 1.8, ease: 'power3.inOut' }, 0)
      .to(preloader, {
        clipPath: 'inset(0 0 100% 0)', duration: 1.1, ease: 'expo.inOut',
        onStart: function () { intro.play(0); },
        onComplete: function () { preloader.remove(); if (lenis) lenis.start(); }
      });
  }

  /* ---------- Hero scroll parallax ---------- */
  function initHeroParallax() {
    var hero = $('[data-hero]');
    if (!hero) return;

    var bg = $('[data-hero-bg]', hero);
    if (bg) {
      gsap.to(bg, {
        yPercent: 18, scale: 1.08, ease: 'none',
        scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true }
      });
    }

    var title = $('[data-hero-title]', hero);
    if (title) {
      gsap.to(title, {
        yPercent: -20, opacity: 0.2, ease: 'none',
        scrollTrigger: { trigger: hero, start: 'center center', end: 'bottom top', scrub: true }
      });
    }
  }

  /* ---------- Rotating words ---------- */
  function initRotate() {
    $$('[data-rotate]').forEach(function (el) {
      var words = JSON.parse(el.dataset.rotate || '[]');
      if (words.length < 2) return;

      var i = 0;
      el.innerHTML = '<span class="roll"><span class="roll__cur"></span><span class="roll__next"></span></span>';
      var roll = el.firstElementChild;
      var cur = roll.children[0];
      var next = roll.children[1];
      cur.textContent = words[0];

      var step = function () {
        i = (i + 1) % words.length;
        next.textContent = words[i];
        gsap.fromTo(roll, { yPercent: 0 }, {
          yPercent: -140, duration: 0.8, ease: 'expo.out',
          onComplete: function () {
            cur.textContent = words[i];
            gsap.set(roll, { yPercent: 0 });
          }
        });
      };

      setTimeout(function () { setInterval(step, 2600); }, 1200);
    });
  }

  /* ---------- Reveals + split headings ---------- */
  function initReveals() {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px' });

    $$('[data-reveal]').forEach(function (el) { io.observe(el); });

    $$('[data-split]').forEach(function (el) {
      if (el.closest('[data-hero]')) return;
      var lines = $$('.line-mask > span', el);
      gsap.set(lines, { yPercent: 110 });
      ScrollTrigger.create({
        trigger: el, start: 'top 85%', once: true,
        onEnter: function () {
          gsap.to(lines, { yPercent: 0, duration: 1.3, ease: 'expo.out', stagger: 0.08 });
        }
      });
    });
  }

  /* ---------- Lazy video autoplay ---------- */
  function initAutoplay() {
    var videos = $$('video[data-autoplay]');
    if (!videos.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var v = entry.target;
        if (entry.isIntersecting) {
          if (v.preload === 'none') v.preload = 'auto';
          var p = v.play();
          if (p && p.catch) p.catch(function () {});
        } else {
          v.pause();
        }
      });
    }, { rootMargin: '200px 0px' });
    videos.forEach(function (v) { io.observe(v); });
  }

  /* ---------- Marquees ---------- */
  function shuffleMarquee(el) {
    var track = el.querySelector('[data-marquee-track]');
    var groups = track ? Array.prototype.slice.call(track.children) : [];
    if (!groups.length) return;

    var order = Array.prototype.slice.call(groups[0].children).map(function (_, i) { return i; });
    for (var i = order.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = order[i]; order[i] = order[j]; order[j] = tmp;
    }
    groups.forEach(function (group) {
      var kids = Array.prototype.slice.call(group.children);
      order.forEach(function (idx) { group.appendChild(kids[idx]); });
    });
  }

  function initMarquees() {
    $$('[data-shuffle]').forEach(shuffleMarquee);

    $$('[data-marquee]').forEach(function (el) {
      var track = $('[data-marquee-track]', el);
      if (!track) return;

      var reverse = el.dataset.marquee === 'reverse';
      var tween = gsap.fromTo(track,
        { xPercent: reverse ? -50 : 0 },
        { xPercent: reverse ? 0 : -50, duration: Number(el.dataset.duration || 38), ease: 'none', repeat: -1 });

      if (!el.hasAttribute('data-no-pause')) {
        el.addEventListener('pointerenter', function () { tween.pause(); });
        el.addEventListener('pointerleave', function () { tween.resume(); });
      }

      ScrollTrigger.create({
        trigger: el, start: 'top bottom', end: 'bottom top',
        onUpdate: function (self) {
          var scale = 1 + Math.min(Math.abs(self.getVelocity()) / 400, 6);
          gsap.killTweensOf(tween);
          gsap.timeline()
            .to(tween, { timeScale: scale, duration: 0.2 })
            .to(tween, { timeScale: 1, duration: 1.2, ease: 'power2.out' });
        }
      });
    });
  }

  /* ---------- Word-by-word scrub ---------- */
  function initScrubWords() {
    $$('[data-scrub-words]').forEach(function (el) {
      var split = new SplitText(el, { type: 'words', wordsClass: 'word' });
      gsap.fromTo(split.words, { opacity: 0.14 }, {
        opacity: 1, ease: 'none', stagger: 0.1,
        scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 45%', scrub: true }
      });
    });
  }

  /* ---------- Number counters ---------- */
  function initCounters() {
    $$('[data-counter]').forEach(function (el) {
      var raw = el.dataset.counter != null ? el.dataset.counter : (el.textContent || '');
      var match = raw.match(/^(\D*)(\d+)(\D*)$/);
      if (!match) return;

      var prefix = match[1], digits = match[2], suffix = match[3];
      var target = Number(digits);
      var value = { v: 0 };

      el.textContent = prefix + '0'.padStart(digits.length, '0') + suffix;
      ScrollTrigger.create({
        trigger: el, start: 'top 90%', once: true,
        onEnter: function () {
          gsap.to(value, {
            v: target, duration: 2, ease: 'expo.out',
            onUpdate: function () {
              el.textContent = prefix + String(Math.round(value.v)).padStart(digits.length, '0') + suffix;
            }
          });
        }
      });
    });
  }

  /* ---------- Work index hover preview ---------- */
  function initIndexPreview() {
    var index = $('[data-index]');
    var preview = $('[data-index-preview]');
    if (!index || !preview || !FINE_POINTER) return;

    var items = $$('[data-preview-item]', preview);
    var px = gsap.quickTo(preview, 'x', { duration: 0.7, ease: 'power3' });
    var py = gsap.quickTo(preview, 'y', { duration: 0.7, ease: 'power3' });
    var pr = gsap.quickTo(preview, 'rotation', { duration: 0.9, ease: 'power3' });
    var lastX = 0;

    index.addEventListener('pointermove', function (e) {
      px(e.clientX); py(e.clientY);
      pr(gsap.utils.clamp(-8, 8, (e.clientX - lastX) * 0.6));
      lastX = e.clientX;
    });
    index.addEventListener('pointerenter', function () {
      gsap.to(preview, { opacity: 1, scale: 1, duration: 0.6, ease: 'expo.out' });
    });
    index.addEventListener('pointerleave', function () {
      gsap.to(preview, { opacity: 0, scale: 0.85, duration: 0.5, ease: 'expo.out' });
    });

    $$('[data-index-row]', index).forEach(function (row, i) {
      row.addEventListener('pointerenter', function () {
        items.forEach(function (item, n) {
          gsap.to(item, {
            clipPath: n === i ? 'inset(0% 0% 0% 0%)' : 'inset(0% 0% 100% 0%)',
            scale: n === i ? 1 : 1.15,
            duration: 0.8, ease: 'expo.out'
          });
        });
      });
    });
  }

  /* ---------- Project hero pin + expand ---------- */
  function initProjectHero() {
    var hero = $('[data-project-hero]');
    if (!hero) return;

    var media = $('[data-ph-media]', hero);
    var left = $('[data-ph-left]', hero);
    var right = $('[data-ph-right]', hero);
    var fades = $$('[data-ph-fade]', hero);
    if (!media) return;

    gsap.from([left, right], {
      xPercent: function (i) { return i === 0 ? -40 : 40; },
      opacity: 0, duration: 1.6, ease: 'expo.out', delay: 0.15
    });
    gsap.from(fades, { opacity: 0, y: 20, duration: 1.2, ease: 'expo.out', stagger: 0.08, delay: 0.5 });

    gsap.matchMedia().add('(min-width: 901px)', function () {
      var items = $$('[data-ph-fade]', hero);
      var base = { width: media.offsetWidth, height: media.offsetHeight };
      var ease = 'expo.inOut';

      var expand = function () {
        gsap.to(media, { width: '100vw', height: '100vh', duration: 1.1, ease: ease, overwrite: 'auto' });
        gsap.to(left, { xPercent: -60, opacity: 0, duration: 1.1, ease: ease, overwrite: 'auto' });
        gsap.to(right, { xPercent: 60, opacity: 0, duration: 1.1, ease: ease, overwrite: 'auto' });
        gsap.to(items, { opacity: 0, y: 0, duration: 0.4, overwrite: 'auto' });
      };
      var collapse = function () {
        gsap.to(media, {
          width: base.width, height: base.height, duration: 0.9, ease: ease, overwrite: 'auto',
          onComplete: function () { gsap.set(media, { clearProps: 'width,height' }); }
        });
        gsap.to([left, right], { xPercent: 0, opacity: 1, duration: 0.9, ease: ease, overwrite: 'auto' });
        gsap.to(items, { opacity: 1, y: 0, duration: 0.6, delay: 0.3, overwrite: 'auto' });
      };

      var expanded = false;
      var st = ScrollTrigger.create({
        trigger: hero, start: 'top top', end: '+=60%', pin: true,
        onUpdate: function (self) {
          if (!expanded && self.direction === 1 && self.progress > 0.01) {
            expanded = true; expand();
            if (lenis) lenis.scrollTo(self.end + 1, { duration: 1.1, lock: true, force: true });
          } else if (expanded && self.direction === -1 && self.progress < 0.99) {
            expanded = false; collapse();
            if (lenis) lenis.scrollTo(self.start, { duration: 1, lock: true, force: true });
          }
        },
        onEnterBack: function () {
          if (expanded) {
            expanded = false; collapse();
            if (lenis) lenis.scrollTo(st.start, { duration: 1, lock: true, force: true });
          }
        }
      });

      var onScroll = function (e) {
        if (expanded && e.scroll <= st.start + 2) { expanded = false; collapse(); }
      };
      if (lenis) lenis.on('scroll', onScroll);

      return function () {
        st.kill();
        if (lenis) lenis.off('scroll', onScroll);
      };
    });
  }

  /* ---------- Generic parallax ---------- */
  function initParallax() {
    $$('[data-parallax]').forEach(function (el) {
      var amount = Number(el.dataset.parallax || 10);
      gsap.fromTo(el, { yPercent: -amount }, {
        yPercent: amount, ease: 'none',
        scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true }
      });
    });
  }

  /* ---------- Fit-to-width text ---------- */
  function initFitText() {
    var els = $$('[data-fit]');
    if (!els.length) return;
    var fit = function () {
      els.forEach(function (el) {
        var parent = el.parentElement;
        var cs = getComputedStyle(parent);
        var avail = parent.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
        el.style.fontSize = '100px';
        var w = el.scrollWidth;
        el.style.fontSize = (100 * avail * 0.99 / w) + 'px';
      });
    };
    fit();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    window.addEventListener('resize', fit);
  }

  /* ---------- Award / certification rows ---------- */
  function initAwardRows() {
    $$('[data-award-row]').forEach(function (row, i) {
      gsap.from(row, {
        opacity: 0, y: 24, duration: 1, ease: 'expo.out', delay: (i % 10) * 0.05,
        scrollTrigger: { trigger: row, start: 'top 92%', once: true }
      });
    });
  }

  /* ---------- Work filters ---------- */
  function initFilters() {
    var bar = $('[data-filters]');
    if (!bar) return;
    var cards = $$('[data-tags]');

    $$('button[data-filter]', bar).forEach(function (btn) {
      btn.addEventListener('click', function () {
        var key = btn.dataset.filter;
        $$('button[data-filter]', bar).forEach(function (b) {
          b.setAttribute('aria-pressed', String(b === btn));
        });

        var shown = cards.filter(function (c) {
          return key === 'all' || c.dataset.tags.split('|').indexOf(key) !== -1;
        });
        var hidden = cards.filter(function (c) { return shown.indexOf(c) === -1; });

        gsap.to(hidden, {
          opacity: 0, scale: 0.96, duration: 0.4, ease: 'power3.out',
          onComplete: function () { hidden.forEach(function (c) { c.hidden = true; }); }
        });
        shown.forEach(function (c) { c.hidden = false; });
        gsap.fromTo(shown, { opacity: 0, y: 30 }, {
          opacity: 1, y: 0, scale: 1, duration: 0.9, ease: 'expo.out', stagger: 0.05, delay: 0.35,
          onComplete: function () { ScrollTrigger.refresh(); }
        });
      });
    });
  }

  /* ---------- Back to top ---------- */
  function initToTop() {
    $$('[data-to-top]').forEach(function (el) {
      el.addEventListener('click', function () {
        if (lenis) lenis.scrollTo(0, { duration: 1.6 });
        else window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });
  }

  /* ---------- Protect media ---------- */
  function initMediaGuards() {
    document.addEventListener('contextmenu', function (e) {
      if (!e.target.closest('input, textarea')) e.preventDefault();
    });
    document.addEventListener('dragstart', function (e) {
      if (e.target.closest && e.target.closest('img, video, canvas')) e.preventDefault();
    });
  }

  /* ---------- Contact form ---------- */
  function initContactForm() {
    var form = $('[data-contact-form]');
    if (!form) return;

    var status = $('[data-form-status]', form);
    var split = null;

    var say = function (state, text) {
      if (split) { split.revert(); split = null; }
      status.dataset.state = state;
      status.textContent = text;
      if (state !== 'sending') {
        split = new SplitText(status, { type: 'words', mask: 'words' });
        gsap.from(split.words, { yPercent: 110, opacity: 0, duration: 0.8, ease: 'expo.out', stagger: 0.035 });
      }
    };

    // Readable text for the error codes POST /api/contact can return.
    var MESSAGES = {
      name_required: 'Please add your name.',
      email_required: 'Please add your email.',
      message_required: 'Please add a message.',
      email_invalid: "That email address doesn't look right.",
      name_too_long: 'That name is too long.',
      email_too_long: 'That email address is too long.',
      company_too_long: 'That company name is too long.',
      message_too_long: 'That message is too long — 5000 characters max.'
    };

    // Last resort: hand the message to the visitor's own mail client, so a
    // missing API key or a dead provider never costs an enquiry.
    var mailtoFallback = function (data) {
      var body = 'Name: ' + (data.get('name') || '') +
                 '\nEmail: ' + (data.get('email') || '') +
                 '\nCompany: ' + (data.get('company') || '') +
                 '\n\n' + (data.get('message') || '');
      say('sent', 'Opening your mail app so you can send it directly — thank you!');
      window.location.href = 'mailto:pradeepmaurya2002@gmail.com' +
        '?subject=' + encodeURIComponent('Portfolio enquiry from ' + (data.get('name') || 'website')) +
        '&body=' + encodeURIComponent(body);
    };

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var submit = $('button[type=submit]', form);
      var endpoint = form.getAttribute('action');
      var data = new FormData(form);

      if (!endpoint || endpoint === '#') return mailtoFallback(data);

      submit.disabled = true;
      say('sending', 'Sending…');
      try {
        var res = await fetch(endpoint, {
          method: 'POST',
          body: data,
          headers: { Accept: 'application/json' }
        });
        var json = await res.json().catch(function () { return {}; });

        if (res.ok) {
          form.reset();
          form.classList.add('is-sent');
          say('sent', "Thanks for your message. I'll get back to you within 24 hours.");
          return;
        }

        // 400 is the visitor's input — tell them what to fix. Anything else
        // is our problem, so don't make them retype it.
        if (res.status === 400 && MESSAGES[json.error]) {
          say('error', MESSAGES[json.error]);
          return;
        }
        mailtoFallback(data);
      } catch (err) {
        mailtoFallback(data);   // offline, blocked, CORS — still recoverable
      } finally {
        submit.disabled = false;
      }
    });
  }

  /* ---------- Radiating data streams ----------
     Strands of glowing dots flowing outward from the centre along gently
     waving paths, growing and brightening as they travel toward the viewer.

     Per-canvas attributes:
       data-streams="<density>"   1 = default strand count, scales from there
  */
  function initStreams() {
    var canvases = $$('canvas[data-streams]');
    if (!canvases.length) return;

    var STILL = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var ACCENT = '226,35,86';
    var PALE = '255,206,218';

    canvases.forEach(function (canvas) {
      var ctx = canvas.getContext('2d');
      if (!ctx) return;

      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var density = Number(canvas.dataset.streams) || 1;

      var w = 0, h = 0, cx = 0, cy = 0, ex = 0, ey = 0;
      var resize = function () {
        var r = canvas.getBoundingClientRect();
        w = Math.max(r.width, 1);
        h = Math.max(r.height, 1);
        canvas.width = Math.round(w * dpr);
        canvas.height = Math.round(h * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        cx = w / 2;
        cy = h * 0.5;
        // Elliptical field — wider than tall, so strands spread sideways
        // across a wide hero instead of piling up top and bottom.
        ex = w * 0.74;
        ey = h * 0.95;
      };
      resize();
      if (window.ResizeObserver) new ResizeObserver(resize).observe(canvas);
      else window.addEventListener('resize', resize);

      // Thin the field on narrow screens — the hero is short there and a
      // full-density fan sits right on top of the body copy.
      var strandCount = Math.round(30 * density * (w < 700 ? 0.5 : 1));
      var DOTS = 34;
      var strands = [];
      var perSide = Math.max(1, Math.floor(strandCount / 2) - 1);
      for (var s = 0; s < strandCount; s++) {
        // Fan left and right rather than evenly around the circle — the hero
        // is wide, and sideways strands read as flow, not as a starburst.
        var side = (s % 2) ? 0 : Math.PI;
        var lane = Math.floor(s / 2) / perSide;
        strands.push({
          base: side + (lane - 0.5) * 1.8 + (Math.random() - 0.5) * 0.12,
          amp: 0.16 + Math.random() * 0.3,
          freq: 1.6 + Math.random() * 3.2,
          phase: Math.random() * Math.PI * 2,
          speed: 0.05 + Math.random() * 0.06,
          depth: 0.55 + Math.random() * 0.8,
          hot: Math.random() < 0.3,
          seed: Math.random()
        });
      }

      var bokeh = [];
      for (var b = 0; b < 8; b++) {
        bokeh.push({
          x: Math.random(), y: Math.random(),
          rad: 14 + Math.random() * 44,
          alpha: 0.03 + Math.random() * 0.05,
          vx: (Math.random() - 0.5) * 0.00016,
          vy: (Math.random() - 0.5) * 0.00016
        });
      }

      var visible = true;
      new IntersectionObserver(function (e) { visible = e[0].isIntersecting; },
        { rootMargin: '120px' }).observe(canvas);

      var t = 0;

      var draw = function () {
        var bg = ctx.createLinearGradient(0, 0, 0, h);
        bg.addColorStop(0, '#190f15');
        bg.addColorStop(1, '#141414');
        ctx.fillStyle = bg;
        ctx.fillRect(0, 0, w, h);

        ctx.globalCompositeOperation = 'lighter';

        // Core glow the strands appear to pour out of
        var pulse = 0.22 + 0.06 * Math.sin(t * 0.8);
        var core = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.min(w, h) * 0.62);
        core.addColorStop(0, 'rgba(' + ACCENT + ',' + pulse.toFixed(3) + ')');
        core.addColorStop(0.4, 'rgba(' + ACCENT + ',0.07)');
        core.addColorStop(1, 'rgba(' + ACCENT + ',0)');
        ctx.fillStyle = core;
        ctx.fillRect(0, 0, w, h);

        for (var i = 0; i < strandCount; i++) {
          var st = strands[i];
          var rgb = st.hot ? ACCENT : PALE;
          for (var d = 0; d < DOTS; d++) {
            var p = (d / DOTS + t * st.speed + st.seed) % 1;
            // Start clear of the centre and space the dots fairly evenly, so
            // each strand reads as a chain rather than a blob at the core.
            var rp = 0.1 + 0.9 * Math.pow(p, 1.25);
            var ang = st.base + Math.sin(p * st.freq + t * 0.55 + st.phase) * st.amp;
            var x = cx + Math.cos(ang) * rp * ex;
            var y = cy + Math.sin(ang) * rp * ey;

            var fade = Math.min(p * 5, 1) * (1 - p * p * p);
            var alpha = fade * st.depth * 0.95;
            if (alpha < 0.015) continue;
            var rad = (0.5 + p * 2.9) * st.depth;

            ctx.fillStyle = 'rgba(' + rgb + ',' + alpha.toFixed(3) + ')';
            ctx.beginPath();
            ctx.arc(x, y, rad, 0, Math.PI * 2);
            ctx.fill();

            // A soft halo on the nearest dots, for the bloom in the reference
            if (p > 0.6 && st.depth > 1.15) {
              var halo = ctx.createRadialGradient(x, y, 0, x, y, rad * 3);
              halo.addColorStop(0, 'rgba(' + rgb + ',' + (alpha * 0.3).toFixed(3) + ')');
              halo.addColorStop(1, 'rgba(' + rgb + ',0)');
              ctx.fillStyle = halo;
              ctx.beginPath();
              ctx.arc(x, y, rad * 3, 0, Math.PI * 2);
              ctx.fill();
            }
          }
        }

        bokeh.forEach(function (bp) {
          bp.x += bp.vx; bp.y += bp.vy;
          if (bp.x < -0.1 || bp.x > 1.1) bp.vx *= -1;
          if (bp.y < -0.1 || bp.y > 1.1) bp.vy *= -1;
          var bx = bp.x * w, by = bp.y * h;
          var g = ctx.createRadialGradient(bx, by, 0, bx, by, bp.rad);
          g.addColorStop(0, 'rgba(' + PALE + ',' + bp.alpha + ')');
          g.addColorStop(1, 'rgba(' + PALE + ',0)');
          ctx.fillStyle = g;
          ctx.beginPath();
          ctx.arc(bx, by, bp.rad, 0, Math.PI * 2);
          ctx.fill();
        });

        ctx.globalCompositeOperation = 'source-over';
      };

      if (STILL) { draw(); return; }

      var frame = function () {
        requestAnimationFrame(frame);
        if (!visible) return;
        t += 0.0065;
        draw();
      };
      requestAnimationFrame(frame);
    });
  }
  /* ---------- Plexus network background ----------
     A 3D point cloud joined by proximity lines, perspective-projected and
     slowly rotating, lit by volumetric rays from one off-canvas corner.
     Tuned to the site accent rather than the usual cyan.

     Per-canvas attributes:
       data-plexus="<density>"  1 = default node count, scales from there
       data-plexus-ray="<deg>"  direction the light rays travel, default 150
  */
  function initPlexus() {
    var canvases = $$('canvas[data-plexus]');
    if (!canvases.length) return;

    var STILL = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var LINE = '236,146,170';   // light rose — the mesh itself
    var ACCENT = '226,35,86';   // brand accent — nodes, rays, glow
    var LINK = 0.40;            // join nodes closer than this in model space
    var FOV = 2.4;
    var DEPTH = 0.8;            // half-depth of the cloud, in model units

    canvases.forEach(function (canvas) {
      var ctx = canvas.getContext('2d');
      if (!ctx) return;

      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var density = Number(canvas.dataset.plexus) || 1;
      var rayAngle = (Number(canvas.dataset.plexusRay) || 150) * Math.PI / 180;

      var w = 0, h = 0, cx = 0, cy = 0, spreadX = 0, spreadY = 0;
      var srcX = 0, srcY = 0, rayLen = 0;
      var resize = function () {
        var r = canvas.getBoundingClientRect();
        w = Math.max(r.width, 1);
        h = Math.max(r.height, 1);
        canvas.width = Math.round(w * dpr);
        canvas.height = Math.round(h * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        cx = w / 2;
        cy = h / 2;
        // The cloud stays a cube in model space — stretching it there would
        // let the Y-rotation swing points past the camera. The canvas aspect
        // is applied here instead, purely at projection time.
        spreadX = w * 0.60;
        spreadY = h * 0.80;
        srcX = w * 0.86;          // rays originate just off the top-right
        srcY = -h * 0.12;
        rayLen = Math.max(w, h) * 1.7;
      };
      resize();
      // The hero is sized by its content, so it grows after webfonts land.
      // Watch the element, not just the window, or the buffer ends up a
      // different size from the box and the whole scene renders stretched.
      if (window.ResizeObserver) new ResizeObserver(resize).observe(canvas);
      else window.addEventListener('resize', resize);

      // Nodes drift inside x,y:[-1,1] z:[-DEPTH,DEPTH]. Rotation preserves
      // distance, so link tests can use the unrotated model coords.
      var count = Math.round(Math.min(Math.max(w * h / 5200, 70), 185) * density);
      var nodes = [];
      for (var i = 0; i < count; i++) {
        nodes.push({
          x: Math.random() * 2 - 1,
          y: Math.random() * 2 - 1,
          z: (Math.random() * 2 - 1) * DEPTH,
          vx: (Math.random() - 0.5) * 0.0009,
          vy: (Math.random() - 0.5) * 0.0009,
          vz: (Math.random() - 0.5) * 0.0006,
          hot: Math.random() < 0.2
        });
      }

      var rays = [];
      for (var r = 0; r < 16; r++) {
        rays.push({
          off: (r / 15 - 0.5) * 0.62,          // fan spread, radians
          near: 4 + Math.random() * 16,
          far: 90 + Math.random() * 190,
          alpha: 0.03 + Math.random() * 0.055,
          drift: 0.1 + Math.random() * 0.35,
          phase: Math.random() * Math.PI * 2
        });
      }

      var bokeh = [];
      for (var b = 0; b < 7; b++) {
        bokeh.push({
          x: Math.random(), y: Math.random(),
          rad: 8 + Math.random() * 26,
          alpha: 0.035 + Math.random() * 0.055,
          vx: (Math.random() - 0.5) * 0.00018,
          vy: (Math.random() - 0.5) * 0.00018
        });
      }

      var px = new Float32Array(count);
      var py = new Float32Array(count);
      var pk = new Float32Array(count);

      var visible = true;
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
      }, { rootMargin: '120px' }).observe(canvas);

      var t = 0;

      var draw = function () {
        // --- ground + corner glow -------------------------------------
        var bg = ctx.createLinearGradient(0, 0, 0, h);
        bg.addColorStop(0, '#191117');
        bg.addColorStop(1, '#141414');
        ctx.fillStyle = bg;
        ctx.fillRect(0, 0, w, h);

        ctx.globalCompositeOperation = 'lighter';

        var glow = ctx.createRadialGradient(srcX, srcY, 0, srcX, srcY, Math.max(w, h) * 0.95);
        glow.addColorStop(0, 'rgba(' + ACCENT + ',0.30)');
        glow.addColorStop(0.35, 'rgba(' + ACCENT + ',0.09)');
        glow.addColorStop(1, 'rgba(' + ACCENT + ',0)');
        ctx.fillStyle = glow;
        ctx.fillRect(0, 0, w, h);

        // --- volumetric rays ------------------------------------------
        rays.forEach(function (ray) {
          var a = rayAngle + ray.off + Math.sin(t * ray.drift + ray.phase) * 0.012;
          ctx.save();
          ctx.translate(srcX, srcY);
          ctx.rotate(a);
          var g = ctx.createLinearGradient(0, 0, rayLen, 0);
          var pulse = ray.alpha * (0.72 + 0.28 * Math.sin(t * 0.55 + ray.phase));
          g.addColorStop(0, 'rgba(' + ACCENT + ',' + pulse.toFixed(4) + ')');
          g.addColorStop(0.45, 'rgba(' + ACCENT + ',' + (pulse * 0.45).toFixed(4) + ')');
          g.addColorStop(1, 'rgba(' + ACCENT + ',0)');
          ctx.fillStyle = g;
          ctx.beginPath();
          ctx.moveTo(0, -ray.near / 2);
          ctx.lineTo(rayLen, -ray.far / 2);
          ctx.lineTo(rayLen, ray.far / 2);
          ctx.lineTo(0, ray.near / 2);
          ctx.closePath();
          ctx.fill();
          ctx.restore();
        });

        // --- project the cloud ----------------------------------------
        var ry = t * 0.055;
        var rx = Math.sin(t * 0.035) * 0.22;
        var cosY = Math.cos(ry), sinY = Math.sin(ry);
        var cosX = Math.cos(rx), sinX = Math.sin(rx);

        for (var i = 0; i < count; i++) {
          var n = nodes[i];
          n.x += n.vx; n.y += n.vy; n.z += n.vz;
          if (n.x < -1 || n.x > 1) n.vx *= -1;
          if (n.y < -1 || n.y > 1) n.vy *= -1;
          if (n.z < -DEPTH || n.z > DEPTH) n.vz *= -1;

          var x1 = n.x * cosY - n.z * sinY;
          var z1 = n.x * sinY + n.z * cosY;
          var y2 = n.y * cosX - z1 * sinX;
          var z2 = n.y * sinX + z1 * cosX;

          var k = FOV / (FOV + z2);
          px[i] = cx + x1 * k * spreadX;
          py[i] = cy + y2 * k * spreadY;
          pk[i] = k;
        }

        // --- mesh ------------------------------------------------------
        // Depth maps k (0.75 near the back .. 1.5 at the front) onto 0..1 so
        // far links recede instead of flattening the whole web.
        ctx.lineWidth = 1;
        var LINK2 = LINK * LINK;
        for (var a1 = 0; a1 < count; a1++) {
          var na = nodes[a1];
          for (var b1 = a1 + 1; b1 < count; b1++) {
            var nb = nodes[b1];
            var dx = na.x - nb.x;
            if (dx > LINK || dx < -LINK) continue;        // cheap reject
            var dy = na.y - nb.y, dz = na.z - nb.z;
            var d2 = dx * dx + dy * dy + dz * dz;
            if (d2 > LINK2) continue;
            var depthL = ((pk[a1] + pk[b1]) * 0.5 - 0.60) / 0.75;
            if (depthL <= 0) continue;
            var alpha = (1 - Math.sqrt(d2) / LINK) * Math.min(depthL, 1) * 0.95;
            if (alpha < 0.012) continue;
            ctx.strokeStyle = 'rgba(' + LINE + ',' + alpha.toFixed(4) + ')';
            ctx.beginPath();
            ctx.moveTo(px[a1], py[a1]);
            ctx.lineTo(px[b1], py[b1]);
            ctx.stroke();
          }
        }

        // --- nodes -----------------------------------------------------
        for (var j = 0; j < count; j++) {
          var depth = Math.min((pk[j] - 0.60) / 0.75, 1);
          if (depth <= 0) continue;
          var rad = 0.6 + depth * 1.9;
          ctx.fillStyle = nodes[j].hot
            ? 'rgba(' + ACCENT + ',' + Math.min(depth * 1.3, 1).toFixed(3) + ')'
            : 'rgba(255,228,236,' + Math.min(depth * 1.1, 0.95).toFixed(3) + ')';
          ctx.beginPath();
          ctx.arc(px[j], py[j], rad, 0, Math.PI * 2);
          ctx.fill();
        }

        // --- bokeh -----------------------------------------------------
        bokeh.forEach(function (p) {
          p.x += p.vx; p.y += p.vy;
          if (p.x < -0.1 || p.x > 1.1) p.vx *= -1;
          if (p.y < -0.1 || p.y > 1.1) p.vy *= -1;
          var bx = p.x * w, by = p.y * h;
          var bg2 = ctx.createRadialGradient(bx, by, 0, bx, by, p.rad);
          bg2.addColorStop(0, 'rgba(255,200,215,' + p.alpha + ')');
          bg2.addColorStop(1, 'rgba(255,200,215,0)');
          ctx.fillStyle = bg2;
          ctx.beginPath();
          ctx.arc(bx, by, p.rad, 0, Math.PI * 2);
          ctx.fill();
        });

        ctx.globalCompositeOperation = 'source-over';
      };

      if (STILL) { draw(); return; }

      var frame = function () {
        requestAnimationFrame(frame);
        if (!visible) return;
        t += 0.006;
        draw();
      };
      requestAnimationFrame(frame);
    });
  }

  /* ---------- Animated hero background ---------- */
  function initHeroCanvas() {
    var canvases = $$('canvas[data-flow]');
    if (!canvases.length) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    canvases.forEach(function (canvas) {
      var ctx = canvas.getContext('2d');
      if (!ctx) return;

      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = 0, h = 0;
      var density = Number(canvas.dataset.flow || 1);

      var resize = function () {
        var rect = canvas.getBoundingClientRect();
        w = Math.max(rect.width, 1);
        h = Math.max(rect.height, 1);
        canvas.width = Math.round(w * dpr);
        canvas.height = Math.round(h * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      };
      resize();
      window.addEventListener('resize', resize);

      // Drifting network of nodes — abstract, code-adjacent motion.
      var count = Math.round(Math.min(Math.max(w * h / 26000, 26), 90) * density);
      var nodes = [];
      for (var i = 0; i < count; i++) {
        nodes.push({
          x: Math.random(), y: Math.random(),
          vx: (Math.random() - 0.5) * 0.00022,
          vy: (Math.random() - 0.5) * 0.00022,
          r: 0.6 + Math.random() * 1.5
        });
      }

      var t = 0;
      var visible = true;
      var io = new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
      }, { rootMargin: '100px' });
      io.observe(canvas);

      var frame = function () {
        requestAnimationFrame(frame);
        if (!visible) return;
        t += 0.0032;

        ctx.clearRect(0, 0, w, h);

        // Soft moving glow
        var g = ctx.createRadialGradient(
          w * (0.5 + Math.sin(t * 0.7) * 0.22),
          h * (0.42 + Math.cos(t * 0.55) * 0.18),
          0,
          w * 0.5, h * 0.5, Math.max(w, h) * 0.75
        );
        g.addColorStop(0, 'rgba(226,35,86,0.30)');
        g.addColorStop(0.45, 'rgba(40,40,52,0.35)');
        g.addColorStop(1, 'rgba(20,20,20,1)');
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, w, h);

        // Grid
        ctx.strokeStyle = 'rgba(255,255,255,0.045)';
        ctx.lineWidth = 1;
        var step = 72;
        var offset = (t * 36) % step;
        for (var gx = -step + offset; gx < w + step; gx += step) {
          ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, h); ctx.stroke();
        }
        for (var gy = -step + offset; gy < h + step; gy += step) {
          ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(w, gy); ctx.stroke();
        }

        // Nodes + links
        for (var a = 0; a < nodes.length; a++) {
          var n = nodes[a];
          n.x += n.vx; n.y += n.vy;
          if (n.x < 0 || n.x > 1) n.vx *= -1;
          if (n.y < 0 || n.y > 1) n.vy *= -1;

          for (var b = a + 1; b < nodes.length; b++) {
            var m = nodes[b];
            var ddx = (n.x - m.x) * w, ddy = (n.y - m.y) * h;
            var dist = Math.sqrt(ddx * ddx + ddy * ddy);
            if (dist < 150) {
              ctx.strokeStyle = 'rgba(255,255,255,' + (0.12 * (1 - dist / 150)).toFixed(3) + ')';
              ctx.beginPath();
              ctx.moveTo(n.x * w, n.y * h);
              ctx.lineTo(m.x * w, m.y * h);
              ctx.stroke();
            }
          }

          ctx.fillStyle = a % 7 === 0 ? 'rgba(226,35,86,0.85)' : 'rgba(255,255,255,0.45)';
          ctx.beginPath();
          ctx.arc(n.x * w, n.y * h, n.r, 0, Math.PI * 2);
          ctx.fill();
        }
      };
      requestAnimationFrame(frame);
    });
  }

  /* ---------- Boot ---------- */
  function boot() {
    initClock();
    initHeader();
    initCursor();
    initHeroCanvas();
    initPlexus();
    initStreams();
    initHeroIntro();
    initHeroParallax();
    initRotate();
    initReveals();
    initAutoplay();
    initMarquees();
    initScrubWords();
    initCounters();
    initIndexPreview();
    initProjectHero();
    initParallax();
    initFitText();
    initAwardRows();
    initFilters();
    initToTop();
    initContactForm();
    initMediaGuards();
    window.addEventListener('load', function () { ScrollTrigger.refresh(); });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
