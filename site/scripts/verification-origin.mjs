const productionOrigin = 'https://brand.shruggie.tech';

export function selectVerificationOrigin(value) {
  const candidate = value?.trim();
  if (!candidate) return { kind: 'local', base: null };

  let url;
  try {
    url = new URL(candidate);
  } catch {
    throw new Error('SITE_VERIFY_BASE_URL must be a valid absolute URL');
  }

  if (url.protocol !== 'https:') {
    throw new Error('SITE_VERIFY_BASE_URL must use HTTPS');
  }

  if (
    url.origin !== productionOrigin
    || url.pathname !== '/'
    || url.search
    || url.hash
    || url.username
    || url.password
  ) {
    throw new Error(`SITE_VERIFY_BASE_URL must be exactly ${productionOrigin}`);
  }

  return { kind: 'remote', base: productionOrigin };
}

export function isCanonicalRedirect(status, location, base, sourcePath) {
  if (![301, 308].includes(status) || !location) return false;

  try {
    const actual = new URL(location, base);
    const expected = new URL(`${sourcePath}/`, base);
    return actual.origin === expected.origin
      && actual.pathname === expected.pathname
      && actual.search === ''
      && actual.hash === '';
  } catch {
    return false;
  }
}
