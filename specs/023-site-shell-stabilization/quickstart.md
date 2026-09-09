# Quickstart: Verify S023

## Source and type checks

```powershell
pnpm --dir site lint
```

## Static site build

```powershell
pnpm --dir site build
```

If the Windows environment denies the Turbopack child process, use the repository-supported webpack path after content preparation:

```powershell
pnpm --dir site prepare:content
pnpm --dir site exec next build --webpack
```

## Rendered site contract

```powershell
pnpm --dir site test
```

Expected result: source-policy tests pass, every generated route is reachable, WCAG 2.1 AA reports zero violations, exact homepage/navigation/footer contracts pass, and cross-route measurements remain within one CSS pixel with no horizontal overflow.

## Aggregate repository gate

```powershell
python scripts/build_all.py
```

Expected result: every production kit reports zero verification problems and zero glyph failures, the site rebuild and checks pass, and repository hygiene reports no generated artifacts or machine-local Spec Kit state staged for commit.

## Encoding and change review

```powershell
git diff --check
git status --short
```

Confirm all authored text is UTF-8 without BOM, LF-only, free of mojibake, and contains no unnecessary em dash.
