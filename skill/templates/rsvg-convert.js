const fs = require("fs")
const path = require("path")
const { Resvg } = require("@resvg/resvg-js")

const args = process.argv.slice(2)
let width = null
let height = null
let output = null
let input = null

for (let index = 0; index < args.length; index += 1) {
  const value = args[index]
  if (value === "-w") width = Number(args[++index])
  else if (value === "-h") height = Number(args[++index])
  else if (value === "-o") output = args[++index]
  else if (!value.startsWith("-")) input = value
}

if (!input || !output) {
  process.stderr.write("usage: rsvg-convert [-w width] [-h height] input -o output\n")
  process.exit(2)
}

const fitTo = width ? { mode: "width", value: width } : height ? { mode: "height", value: height } : undefined
const renderer = new Resvg(fs.readFileSync(input), { fitTo })
const resourceRoot = path.dirname(path.resolve(input))
for (const href of renderer.imagesToResolve()) {
  if (path.isAbsolute(href) || /^[a-z][a-z0-9+.-]*:/i.test(href)) {
    throw new Error(`refusing non-relative SVG image resource: ${href}`)
  }
  const resource = path.resolve(resourceRoot, href)
  const relative = path.relative(resourceRoot, resource)
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error(`refusing SVG image resource outside its source directory: ${href}`)
  }
  renderer.resolveImage(href, fs.readFileSync(resource))
}
const png = renderer.render().asPng()
fs.mkdirSync(path.dirname(output), { recursive: true })
fs.writeFileSync(output, png)
