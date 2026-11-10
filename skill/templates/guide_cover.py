"""Measured, source-preserving pagination limited to the guide opening messages."""


COVER_SCRIPT = r"""
<script>
window.__coverReady = false;
window.__coverErrors = [];
(async () => {
  try {
    await document.fonts.ready;
    await Promise.all(Array.from(document.images, image => image.decode()));
    const first = document.querySelector('.cover');
    const original = first.querySelector('.message');
    const mm = 96 / 25.4;
    let current = first;
    let box = original;
    const bottom = () => current.querySelector('.base').getBoundingClientRect().top - 8 * mm;
    const fits = node => node.getBoundingClientRect().bottom <= bottom() + 0.1;
    const next = () => {
      const sheet = document.createElement('div');
      sheet.className = 'pg cover cover-continuation';
      const inner = document.createElement('div');
      inner.className = 'inner';
      const heading = document.createElement('div');
      heading.className = 'sys';
      heading.textContent = 'Brand message (continued)';
      inner.append(heading);
      box = original.cloneNode(false);
      inner.append(box, first.querySelector('.base').cloneNode(true), first.querySelector('.foot').cloneNode(true));
      sheet.append(inner);
      current.after(sheet);
      current = sheet;
    };
    if (original) {
      const roles = Array.from(original.children);
      original.replaceChildren();
      for (const role of roles) {
        let remainder = role.querySelector('[data-message-value]').textContent;
        let fragment = role;
        while (remainder.length) {
          const value = fragment.querySelector('[data-message-value]');
          value.textContent = remainder;
          box.append(fragment);
          if (fits(fragment)) break;
          if (box.children.length > 1) {
            fragment.remove();
            next();
            box.append(fragment);
            if (fits(fragment)) break;
          }
          // Keep whole words where possible, preserving every original separator.
          let units = remainder.match(/\S+\s*|\s+/gu) || [];
          const fitPrefix = parts => {
            let low = 0, high = parts.length;
            while (low < high) {
              const middle = Math.ceil((low + high) / 2);
              value.textContent = parts.slice(0, middle).join('');
              if (fits(fragment)) low = middle; else high = middle - 1;
            }
            return parts.slice(0, low).join('');
          };
          let prefix = fitPrefix(units);
          if (!prefix) prefix = fitPrefix(Array.from(remainder));
          if (!prefix) throw new Error('No readable message line fits in ' + fragment.dataset.messageRole);
          value.textContent = prefix;
          remainder = remainder.slice(prefix.length);
          if (remainder) {
            fragment = role.cloneNode(true);
            next();
          }
        }
      }
      const groups = new Map();
      for (const node of document.querySelectorAll('.cover [data-message-role]')) {
        const group = groups.get(node.dataset.messageRole) || [];
        group.push(node);
        groups.set(node.dataset.messageRole, group);
      }
      for (const group of groups.values()) {
        if (group.length > 1) group.forEach((node, index) => {
          node.dataset.messageFragment = String(index + 1);
          node.dataset.messageFragments = String(group.length);
        });
      }
    }
    document.querySelectorAll('.pg').forEach((page, index) => {
      const number = page.querySelector('.foot span:last-child');
      if (number) number.textContent = String(index + 1).padStart(2, '0');
    });
    window.__coverLayout = Array.from(document.querySelectorAll('.cover'), (sheet, index) => {
      const bounds = sheet.getBoundingClientRect();
      const base = sheet.querySelector('.base').getBoundingClientRect();
      const logo = sheet.querySelector('.lockup');
      let previous = logo ? logo.getBoundingClientRect().bottom : sheet.querySelector('.sys').getBoundingClientRect().bottom;
      const messages = Array.from(sheet.querySelectorAll('[data-message-role]'), node => {
        const value = node.querySelector('[data-message-value]');
        const rect = value.getBoundingClientRect();
        const style = getComputedStyle(value);
        const role = node.dataset.messageRole;
        if (rect.top < previous - 0.1 || rect.bottom > base.top - 8 * mm + 0.1 ||
            rect.left < bounds.left + 20 * mm - 0.1 || rect.right > bounds.right - 20 * mm + 0.1 ||
            value.scrollWidth > value.clientWidth + 1) window.__coverErrors.push('Message bounds: ' + role);
        previous = rect.bottom;
        return {role, fragment: node.dataset.messageFragment || '1',
          size_px: parseFloat(style.fontSize), line_height_px: parseFloat(style.lineHeight),
          family: style.fontFamily, weight: style.fontWeight,
          color: style.color, background: getComputedStyle(sheet).backgroundColor,
          x: rect.x - bounds.x, y: rect.y - bounds.y, width: rect.width, height: rect.height};
      });
      if (logo && logo.getBoundingClientRect().bottom > base.top - 8 * mm) window.__coverErrors.push('Logo bounds');
      return {page: index + 1, messages};
    });
  } catch (error) {
    window.__coverErrors.push(error.message);
  } finally {
    window.__coverReady = true;
  }
})();
</script>
"""
