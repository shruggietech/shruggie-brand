import { extname } from 'node:path';

const contentTypes = {
  '.ico': ['image/x-icon', 'image/vnd.microsoft.icon'],
  '.json': ['application/json'],
  '.pdf': ['application/pdf'],
  '.png': ['image/png'],
  '.svg': ['image/svg+xml'],
  '.txt': ['text/plain'],
  '.webmanifest': ['application/manifest+json', 'application/json'],
  '.xml': ['application/xml', 'text/xml'],
  '.zip': ['application/zip', 'application/x-zip-compressed'],
};

function decodeUtf8(body) {
  return new TextDecoder('utf-8', { fatal: true }).decode(body);
}

function hasIcoDirectory(body) {
  if (body.length < 6 || !body.subarray(0, 4).equals(Buffer.from([0, 0, 1, 0]))) return false;
  const count = body.readUInt16LE(4);
  if (!count || body.length < 6 + count * 16) return false;
  for (let index = 0; index < count; index += 1) {
    const entry = 6 + index * 16;
    const length = body.readUInt32LE(entry + 8);
    const offset = body.readUInt32LE(entry + 12);
    if (!length || offset < 6 + count * 16 || offset + length > body.length) return false;
  }
  return true;
}

export function payloadFailures(pathname, rawContentType, rawBody) {
  const failures = [];
  const body = Buffer.isBuffer(rawBody) ? rawBody : Buffer.from(rawBody ?? []);
  const extension = extname(new URL(pathname, 'https://local.invalid').pathname).toLowerCase();
  const allowedTypes = contentTypes[extension];
  if (!allowedTypes) return ['has unsupported payload type'];

  const contentType = (rawContentType ?? '').split(';', 1)[0].trim().toLowerCase();
  if (!allowedTypes.includes(contentType)) failures.push(`has content type ${contentType || '(missing)'}, expected ${allowedTypes.join(' or ')}`);
  if (!body.length) {
    failures.push('body is empty');
    return failures;
  }

  try {
    if (extension === '.pdf') {
      if (!body.subarray(0, 5).equals(Buffer.from('%PDF-')) || !body.subarray(-1024).includes(Buffer.from('%%EOF'))) failures.push('lacks a valid PDF signature and trailer');
    } else if (extension === '.png') {
      if (body.length <= 8 || !body.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))) failures.push('lacks a valid PNG signature');
    } else if (extension === '.ico') {
      if (!hasIcoDirectory(body)) failures.push('lacks a valid ICO signature and directory');
    } else if (extension === '.svg') {
      const text = decodeUtf8(body).trim();
      if (!/<svg(?:\s|>)/i.test(text) || !/<\/svg>\s*$/i.test(text) || /<html(?:\s|>)/i.test(text)) failures.push('is not a complete SVG document');
    } else if (extension === '.json' || extension === '.webmanifest') {
      const value = JSON.parse(decodeUtf8(body));
      if (value === null || typeof value !== 'object' || Array.isArray(value)) failures.push('must contain a JSON object');
    } else if (extension === '.xml') {
      const text = decodeUtf8(body).trim();
      if (!/<urlset(?:\s|>)/i.test(text) || !/<\/urlset>\s*$/i.test(text) || /<html(?:\s|>)/i.test(text)) failures.push('is not a complete XML urlset document');
    } else if (extension === '.zip') {
      if (body.length < 22 || !body.subarray(0, 4).equals(Buffer.from([80, 75, 3, 4])) || !body.subarray(-65557).includes(Buffer.from([80, 75, 5, 6]))) failures.push('lacks a valid ZIP signature and end record');
    } else if (extension === '.txt') {
      const text = decodeUtf8(body);
      if (!/^User-agent:/im.test(text) || !/^Sitemap:\s+https:\/\//im.test(text)) failures.push('does not contain the required robots directives');
    }
  } catch (error) {
    if (extension === '.json' || extension === '.webmanifest') failures.push(`is not valid JSON: ${error.message}`);
    else failures.push(`cannot be decoded as valid UTF-8 ${extension.slice(1).toUpperCase()}: ${error.message}`);
  }

  return failures;
}
