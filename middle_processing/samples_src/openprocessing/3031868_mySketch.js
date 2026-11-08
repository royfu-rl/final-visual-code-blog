// Cut gem in model space.
// Girdle sits in the xy plane. The crown is toward the camera (negative z)
// and the pavilion is away from it (positive z).
// Rotations are degrees.

let gems = []
let occupiedTriangles = []
let gemWeights = { regular: 1, irregular: 0 }
let gemLight
let painter

const SURFACE_PALETTE = [
  [214, 54, 78],
  [46, 116, 214],
  [242, 154, 46],
  [36, 168, 126],
  [142, 72, 196],
  [232, 92, 156],
  [48, 176, 196],
  [236, 206, 64],
]

const MAX_GEMS = 30
const MAX_POSITION_TRIES = 40
const POSITIONS_PER_GEM = 8
const MAX_FAILED_ROUNDS = 5

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL)
  brush.scaleBrushes(brushScale())
  startPainting()
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight)
  brush.scaleBrushes(brushScale())
  startPainting()
}

function startPainting() {
  layoutGems()
  painter = paintGems()
  loop()
}

function brushScale() {
  return 2.2 * (Math.min(width, height) / 800)
}

function draw() {
  ortho()
  translate(-width / 2, -height / 2)
  if (painter.next().done) noLoop()
}

function pickGemWeights() {
  const regular = random([0, 0.35, 0.65, 1])
  return { regular, irregular: 1 - regular }
}

function pickGemKind() {
  const total = gemWeights.regular + gemWeights.irregular
  if (random(total) < gemWeights.regular) return 'regular'
  return 'irregular'
}

function layoutGems() {
  gems = []
  occupiedTriangles = []
  gemWeights = pickGemWeights()
  gemLight = pickLight()

  let gemSize = Math.min(width, height) * 0.7
  const minSize = Math.min(width, height) * 0.075
  let failedRounds = 0

  while (gems.length < MAX_GEMS && gemSize >= minSize && failedRounds < MAX_FAILED_ROUNDS) {
    const placed = tryPlaceGem(gemSize)
    if (placed) {
      gems.push(placed)
      for (let i = 0; i < placed.triangles.length; i++) {
        occupiedTriangles.push(placed.triangles[i])
      }
      gemSize *= random(0.74, 0.86)
      failedRounds = 0
    } else {
      gemSize *= 0.8
      failedRounds += 1
    }
  }
}

function tryPlaceGem(targetSize) {
  const margin = 28
  for (let attempt = 0; attempt < MAX_POSITION_TRIES; attempt++) {
    const projected = projectRandomGem(pickGemKind())
    scaleFacesAboutCenter(projected.faces, targetSize * random(0.9, 1.06))
    const outline = convexHull(collectPoints(projected.faces))
    if (outline.length < 3) continue

    const bounds = pointBounds(outline)
    const roomX = width - margin * 2 - (bounds.maxX - bounds.minX)
    const roomY = height - margin * 2 - (bounds.maxY - bounds.minY)
    if (roomX < 0 || roomY < 0) continue

    for (let n = 0; n < POSITIONS_PER_GEM; n++) {
      const dx = margin - bounds.minX + random(roomX)
      const dy = margin - bounds.minY + random(roomY)
      const moved = []
      for (let i = 0; i < outline.length; i++) {
        moved.push([outline[i][0] + dx, outline[i][1] + dy])
      }
      const triangles = decomposeOutline(moved)
      if (triangles.length === 0 || overlapsOccupied(triangles)) continue
      translateFaces(projected.faces, dx, dy)
      return { faces: projected.faces, triangles }
    }
  }
  return null
}

function projectRandomGem(kind) {
  if (kind === 'regular') {
    return projectGem(randomCutGem(), [
      random(-28, 28),
      random(-28, 28),
      random(360),
    ])
  }
  return projectGem(randomIrregularGem(), [
    random(72, 105) * (random() < 0.5 ? -1 : 1),
    random(-24, 24),
    random(-18, 18),
  ])
}

function scaleFacesAboutCenter(faces, targetSize) {
  const bounds = faceBounds(faces)
  const span = Math.max(bounds.maxX - bounds.minX, bounds.maxY - bounds.minY) || 1
  const factor = targetSize / span
  const cx = (bounds.minX + bounds.maxX) / 2
  const cy = (bounds.minY + bounds.maxY) / 2
  for (let i = 0; i < faces.length; i++) {
    const pts = faces[i].points
    for (let k = 0; k < pts.length; k++) {
      pts[k][0] = (pts[k][0] - cx) * factor
      pts[k][1] = (pts[k][1] - cy) * factor
    }
  }
}

function translateFaces(faces, dx, dy) {
  for (let i = 0; i < faces.length; i++) {
    const pts = faces[i].points
    for (let k = 0; k < pts.length; k++) {
      pts[k][0] += dx
      pts[k][1] += dy
    }
  }
}

function collectPoints(faces) {
  const pts = []
  for (let i = 0; i < faces.length; i++) {
    const face = faces[i].points
    for (let k = 0; k < face.length; k++) pts.push(face[k])
  }
  return pts
}

function pointBounds(pts) {
  let minX = Infinity
  let maxX = -Infinity
  let minY = Infinity
  let maxY = -Infinity
  for (let i = 0; i < pts.length; i++) {
    const x = pts[i][0]
    const y = pts[i][1]
    if (x < minX) minX = x
    if (x > maxX) maxX = x
    if (y < minY) minY = y
    if (y > maxY) maxY = y
  }
  return { minX, maxX, minY, maxY }
}

function decomposeOutline(outline) {
  const points = []
  for (let i = 0; i < outline.length; i++) points.push([outline[i][0], outline[i][1]])
  decomp.makeCCW(points)
  let polygons = [points]
  if (decomp.isSimple(points)) polygons = decomp.quickDecomp(points)

  const triangles = []
  for (let i = 0; i < polygons.length; i++) {
    const parts = triangulate(polygons[i])
    for (let k = 0; k < parts.length; k++) triangles.push(parts[k])
  }
  return triangles
}

function overlapsOccupied(triangles) {
  for (let i = 0; i < triangles.length; i++) {
    for (let k = 0; k < occupiedTriangles.length; k++) {
      if (trianglesOverlap(triangles[i], occupiedTriangles[k])) return true
    }
  }
  return false
}

function randomCutGem() {
  const kind = random(['round', 'oval', 'pear', 'emerald', 'free'])
  const sides = kind === 'emerald' ? 8 : floor(random(5, 10))
  const radius = 150
  return makeGem({
    kind,
    sides,
    radius,
    crownHeight: radius * random(0.24, 0.42),
    pavilionHeight: radius * random(0.55, 0.9),
    tableScale: random(0.28, 0.55),
    culet: [radius * random(-0.08, 0.08), radius * random(-0.08, 0.08)],
    jitter: kind === 'free' ? random(0.12, 0.28) : 0,
  })
}

function makeGem({
  sides = 7,
  radius = 150,
  crownHeight = 48,
  pavilionHeight = 100,
  tableScale = 0.42,
  culet = [0, 0],
  kind = 'oval',
  jitter = 0,
} = {}) {
  const girdle = girdlePoints(kind, sides, radius, jitter)
  const count = girdle.length
  const vertices = girdle.slice()
  const tableIsPoint = tableScale <= 0.02
  const crownStart = vertices.length

  if (tableIsPoint) {
    vertices.push([culet[0] * 0.3, culet[1] * 0.3, -crownHeight])
  } else {
    for (let i = 0; i < count; i++) {
      vertices.push([
        girdle[i][0] * tableScale,
        girdle[i][1] * tableScale,
        -crownHeight,
      ])
    }
  }

  const culetIndex = vertices.length
  vertices.push([culet[0], culet[1], pavilionHeight])

  const faces = []
  for (let i = 0; i < count; i++) {
    const next = (i + 1) % count
    if (tableIsPoint) {
      faces.push({ indices: [i, crownStart, next], part: 'crown' })
    } else {
      faces.push({
        indices: [i, crownStart + i, crownStart + next, next],
        part: 'crown',
      })
    }
    faces.push({ indices: [i, next, culetIndex], part: 'pavilion' })
  }

  if (!tableIsPoint) {
    const table = []
    for (let i = count - 1; i >= 0; i--) table.push(crownStart + i)
    faces.push({ indices: table, part: 'crown' })
  }

  return { vertices, faces }
}

// Irregular crystal. Starts from a pointed cut, then shaves the convex
// mesh with shallow planes so the facets and the silhouette stop lining up.
function randomIrregularGem() {
  const radius = 150
  const tall = random() < 0.55
  return makeIrregularGem({
    radius,
    sides: floor(random(5, 9)),
    crownHeight: radius * (tall ? random(0.95, 1.4) : random(0.45, 0.85)),
    pavilionHeight: radius * (tall ? random(1.1, 1.7) : random(0.6, 1)),
    cuts: tall ? floor(random(6, 11)) : floor(random(8, 14)),
    jitter: random(0.28, 0.55),
    shear: random(0.22, 0.55) * (random() < 0.5 ? -1 : 1),
    squash: random(0.62, 0.95),
    keepBothTips: random() < 0.25,
  })
}

function makeIrregularGem({
  radius = 150,
  sides = 7,
  crownHeight = 160,
  pavilionHeight = 200,
  cuts = 7,
  jitter = 0.35,
  shear = 0.2,
  squash = 0.85,
  keepBothTips = true,
  culet = [0, 0],
} = {}) {
  const seed = makeGem({
    kind: 'free',
    sides,
    radius,
    crownHeight,
    pavilionHeight,
    tableScale: 0,
    culet,
    jitter,
  })

  const vertices = seed.vertices.map((xyz) => xyz.slice())
  for (let i = 0; i < vertices.length; i++) {
    vertices[i][0] += vertices[i][2] * shear
    vertices[i][1] *= squash
  }

  let faces = seed.faces.map((face) => face.indices.slice())
  let applied = 0
  let attempts = 0
  while (applied < cuts && attempts < cuts * 6) {
    attempts += 1
    const origin = vertexCentroid(vertices)
    const direction = cutDirection(vertices, origin)
    const clipped = clipConvexMesh(vertices, faces, direction, origin, {
      epsilon: radius * 1e-6,
      protectedIndices: protectedTips(vertices, keepBothTips),
    })
    if (!clipped) continue
    vertices.length = 0
    for (let i = 0; i < clipped.vertices.length; i++) vertices.push(clipped.vertices[i])
    faces = clipped.faces
    applied += 1
  }

  return {
    vertices,
    faces: faces.map((indices) => {
      let zSum = 0
      for (let i = 0; i < indices.length; i++) zSum += vertices[indices[i]][2]
      return { indices, part: zSum / indices.length < 0 ? 'crown' : 'pavilion' }
    }),
  }
}

function cutDirection(vertices, origin) {
  const corner = vertices[floor(random(vertices.length))]
  let direction = normalize3([
    corner[0] - origin[0],
    corner[1] - origin[1],
    corner[2] - origin[2],
  ])
  const wobble = random(0.4, 1.15)
  const spin = random(360)
  const tangent = perpendicular(direction)
  const bitangent = normalize3(cross3(direction, tangent))
  direction = normalize3([
    direction[0] + wobble * (degCos(spin) * tangent[0] + degSin(spin) * bitangent[0]),
    direction[1] + wobble * (degCos(spin) * tangent[1] + degSin(spin) * bitangent[1]),
    direction[2] + wobble * (degCos(spin) * tangent[2] + degSin(spin) * bitangent[2]),
  ])
  return direction
}

function protectedTips(vertices, keepBothTips) {
  let maxZ = 0
  let minZ = 0
  for (let i = 1; i < vertices.length; i++) {
    if (vertices[i][2] > vertices[maxZ][2]) maxZ = i
    if (vertices[i][2] < vertices[minZ][2]) minZ = i
  }
  return keepBothTips ? [maxZ, minZ] : [maxZ]
}

// Keeps the half-space that contains `origin`. Returns null when the cut is
// too deep, misses the mesh, or would slice off a protected tip.
function clipConvexMesh(vertices, faces, planeNormal, origin, options) {
  const epsilon = options.epsilon
  const depth = random(0.42, 0.72)
  let far = -Infinity
  let near = dot3(planeNormal, origin)
  const sides = []
  for (let i = 0; i < vertices.length; i++) {
    const signed = dot3(planeNormal, vertices[i])
    sides.push(signed)
    if (signed > far) far = signed
  }
  const offset = near + depth * (far - near)
  if (far - near < epsilon) return null

  let outside = 0
  for (let i = 0; i < sides.length; i++) {
    if (sides[i] > offset + epsilon) outside += 1
  }
  if (outside < 1 || outside > vertices.length * 0.5) return null

  const protectedIndices = options.protectedIndices || []
  for (let i = 0; i < protectedIndices.length; i++) {
    if (sides[protectedIndices[i]] > offset + epsilon) return null
  }

  const nextVertices = vertices.map((xyz) => xyz.slice())
  const edgePoint = new Map()

  function intersection(i, j) {
    const edgeKey = i < j ? i + ':' + j : j + ':' + i
    if (edgePoint.has(edgeKey)) return edgePoint.get(edgeKey)
    const si = sides[i] - offset
    const sj = sides[j] - offset
    const denom = si - sj
    const t = denom === 0 ? 0 : si / denom
    let index
    if (t <= 1e-6) index = i
    else if (t >= 1 - 1e-6) index = j
    else {
      const a = vertices[i]
      const b = vertices[j]
      index = nextVertices.length
      nextVertices.push([
        a[0] + (b[0] - a[0]) * t,
        a[1] + (b[1] - a[1]) * t,
        a[2] + (b[2] - a[2]) * t,
      ])
    }
    edgePoint.set(edgeKey, index)
    return index
  }

  const nextFaces = []
  for (let f = 0; f < faces.length; f++) {
    const indices = faces[f]
    const clipped = []
    for (let i = 0; i < indices.length; i++) {
      const a = indices[i]
      const b = indices[(i + 1) % indices.length]
      const aIn = sides[a] <= offset + epsilon
      const bIn = sides[b] <= offset + epsilon
      if (aIn && bIn) {
        clipped.push(b)
      } else if (aIn && !bIn) {
        clipped.push(intersection(a, b))
      } else if (!aIn && bIn) {
        clipped.push(intersection(a, b))
        clipped.push(b)
      }
    }
    const clean = []
    for (let i = 0; i < clipped.length; i++) {
      if (clean.length === 0 || clean[clean.length - 1] !== clipped[i]) clean.push(clipped[i])
    }
    if (clean.length >= 2 && clean[0] === clean[clean.length - 1]) clean.pop()
    const simplified = simplifyPolygon(nextVertices, clean)
    if (simplified.length >= 3) nextFaces.push(simplified)
  }

  const capIds = []
  const seen = new Set()
  for (const index of edgePoint.values()) {
    if (seen.has(index)) continue
    seen.add(index)
    capIds.push(index)
  }
  if (capIds.length < 3) return null

  const cap = orderOnPlane(nextVertices, capIds, planeNormal)
  if (cap.length >= 3) nextFaces.push(cap)
  if (nextFaces.length < 4) return null

  return compactMesh(nextVertices, nextFaces)
}

function orderOnPlane(vertices, indices, planeNormal) {
  const origin = vertexCentroid(indices.map((index) => vertices[index]))
  const tangent = perpendicular(planeNormal)
  const bitangent = normalize3(cross3(planeNormal, tangent))
  const sorted = indices.slice().sort((i, j) => {
    const ai = vertices[i]
    const aj = vertices[j]
    const angleA = Math.atan2(dot3(sub3(ai, origin), bitangent), dot3(sub3(ai, origin), tangent))
    const angleB = Math.atan2(dot3(sub3(aj, origin), bitangent), dot3(sub3(aj, origin), tangent))
    return angleA - angleB
  })
  const simplified = simplifyPolygon(vertices, sorted)
  if (simplified.length < 3) return simplified
  const winding = polygonOutward(simplified.map((index) => vertices[index]))
  if (dot3(winding, planeNormal) < 0) simplified.reverse()
  return simplified
}

function simplifyPolygon(vertices, indices) {
  if (indices.length <= 3) return indices.slice()
  const kept = []
  const count = indices.length
  for (let i = 0; i < count; i++) {
    const prev = vertices[indices[(i + count - 1) % count]]
    const curr = vertices[indices[i]]
    const next = vertices[indices[(i + 1) % count]]
    const ab = sub3(curr, prev)
    const bc = sub3(next, curr)
    const turn = cross3(ab, bc)
    const span = Math.hypot(ab[0], ab[1], ab[2]) * Math.hypot(bc[0], bc[1], bc[2])
    const area = Math.hypot(turn[0], turn[1], turn[2])
    if (span > 0 && area / span > 1e-3) kept.push(indices[i])
  }
  return kept.length >= 3 ? kept : indices.slice()
}

function compactMesh(vertices, faces) {
  const remap = new Map()
  const nextVertices = []
  const nextFaces = []
  for (let f = 0; f < faces.length; f++) {
    const face = []
    for (let i = 0; i < faces[f].length; i++) {
      const index = faces[f][i]
      if (!remap.has(index)) {
        remap.set(index, nextVertices.length)
        nextVertices.push(vertices[index].slice())
      }
      const mapped = remap.get(index)
      if (face.length === 0 || face[face.length - 1] !== mapped) face.push(mapped)
    }
    if (face.length >= 2 && face[0] === face[face.length - 1]) face.pop()
    if (face.length >= 3) nextFaces.push(face)
  }
  return { vertices: nextVertices, faces: nextFaces }
}

function vertexCentroid(vertices) {
  let x = 0
  let y = 0
  let z = 0
  for (let i = 0; i < vertices.length; i++) {
    x += vertices[i][0]
    y += vertices[i][1]
    z += vertices[i][2]
  }
  const count = vertices.length || 1
  return [x / count, y / count, z / count]
}

function perpendicular(direction) {
  const axis = Math.abs(direction[1]) < 0.8 ? [0, 1, 0] : [1, 0, 0]
  return normalize3(cross3(direction, axis))
}

function polygonOutward(points3d) {
  let x = 0
  let y = 0
  let z = 0
  for (let i = 0; i < points3d.length; i++) {
    const a = points3d[i]
    const b = points3d[(i + 1) % points3d.length]
    x += (a[1] - b[1]) * (a[2] + b[2])
    y += (a[2] - b[2]) * (a[0] + b[0])
    z += (a[0] - b[0]) * (a[1] + b[1])
  }
  return [x, y, z]
}

function dot3(a, b) {
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
}

function sub3(a, b) {
  return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
}

function cross3(a, b) {
  return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
}

function normalize3(xyz) {
  const span = Math.hypot(xyz[0], xyz[1], xyz[2]) || 1
  return [xyz[0] / span, xyz[1] / span, xyz[2] / span]
}

// Convex faces with more than 4 sides become a random mix of triangles and quads.
function splitLargeFaces(faces) {
  const split = []
  for (let i = 0; i < faces.length; i++) {
    const pieces = splitPolygon(faces[i].indices)
    for (let k = 0; k < pieces.length; k++) {
      split.push({ indices: pieces[k], part: faces[i].part })
    }
  }
  return split
}

function splitPolygon(indices) {
  if (indices.length <= 4) return [indices.slice()]

  let ring = indices.slice()
  const pieces = []
  while (ring.length > 4) {
    const start = floor(random(ring.length))
    const rotated = ring.slice(start).concat(ring.slice(0, start))
    const take = rotated.length > 5 && random() < 0.5 ? 4 : 3
    pieces.push(rotated.slice(0, take))
    ring = [rotated[0], rotated[take - 1]].concat(rotated.slice(take))
  }
  pieces.push(ring)
  return pieces
}

// Orthographic projection. Faces come back far to near (larger z first).
function projectGem(gem, rotation = [0, 0, 0]) {
  const vertices = gem.vertices.map((xyz) => rotatePoint(xyz, rotation))
  const faces = splitLargeFaces(gem.faces).map((face) => {
    const points3d = face.indices.map((index) => vertices[index])
    const outward = polygonOutward(points3d)
    let zSum = 0
    const points = []
    for (let i = 0; i < points3d.length; i++) {
      zSum += points3d[i][2]
      points.push([points3d[i][0], points3d[i][1]])
    }
    return {
      points,
      points3d,
      indices: face.indices,
      z: zSum / points3d.length,
      part: face.part,
      facing: outward[2] < 0 ? 'front' : 'back',
      swatch: SURFACE_PALETTE[floor(random(SURFACE_PALETTE.length))],
      outward,
    }
  })

  faces.sort((a, b) => b.z - a.z)
  return { vertices, faces }
}

function faceBounds(faces) {
  let minX = Infinity
  let maxX = -Infinity
  let minY = Infinity
  let maxY = -Infinity
  for (let i = 0; i < faces.length; i++) {
    const pts = faces[i].points
    for (let k = 0; k < pts.length; k++) {
      const x = pts[k][0]
      const y = pts[k][1]
      if (x < minX) minX = x
      if (x > maxX) maxX = x
      if (y < minY) minY = y
      if (y > maxY) maxY = y
    }
  }
  return { minX, maxX, minY, maxY }
}

function pickLight() {
  const primaries = [
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
  ]
  return {
    direction: normalize3([-0.45, -0.55, -1]),
    swatch: primaries[floor(random(primaries.length))],
  }
}

const pointGradient = {
  gap: 5,
  // gap: 18,
  mark: 2,
  // mark: 5,
  noiseAmplitude: 4,
  // noiseAmplitude: 0.65,
  // sway: 4,
  sway: 0.7,
  // stepJitter: 6,
  stepJitter: 0.85,
  // minStep: 0.45,
  minStep: 0.5,
  // rowShift: 0.3,
  rowShift: 0.5,
  drop: 0.12,
  shadowAlpha: 0.14,
  litAlpha: 0.64,
  toothMix: 0.25,
  minStrength: 0.55,
  incidenceGain: 0.45,
  rowNoiseScale: 0.08,
  stepNoiseScale: 0.12,
  swayNoiseScale: 0.2,
  toothNoiseScale: 0.4,
}

const brushGradient = {
  steps: 12,
  shadowOpacity: 28,
  litOpacity: 150,
  shadowBleed: 0.55,
  litBleed: 0.04,
  fadeToPaper: 0.4,
  minStrength: 0.55,
  incidenceGain: 0.45,
}

// Brush fills painted before yielding to the next frame.
// A face always finishes in the frame it starts.
const strokesPerFrame = 24

const cornerShade = {
  chance: 0.5,
  opacity: 70,
  minSplit: 0.2,
  maxSplit: 0.5,
  litThreshold: 0.45,
}

function* paintGems() {
  background(248)
  let strokes = 0
  for (let g = 0; g < gems.length; g++) {
    const faces = gems[g].faces
    for (let i = 0; i < faces.length; i++) {
      strokes += paintFace(faces[i])
      if (strokes >= strokesPerFrame) {
        strokes = 0
        yield
      }
    }
  }
}

function paintFace(face) {
  const shade = faceShade(face, gemLight.direction)
  const strokes = drawBrushGradient(face, shade, brushGradient)
  drawCornerShade(face, shade)
  drawPointGradient(face, shade, pointGradient)
  drawFaceLines(face.points)
  return strokes
}

// Triangle tucked into one corner of the facet.
// M sits partway along the edge that leaves the chosen corner.
function drawCornerShade(face, shade) {
  const pts = face.points
  if (pts.length < 3 || random() >= cornerShade.chance) return

  const corner = floor(random(pts.length))
  const prev = (corner + pts.length - 1) % pts.length
  const next = (corner + 1) % pts.length
  const along = random(cornerShade.minSplit, cornerShade.maxSplit)
  const mx = pts[corner][0] + (pts[next][0] - pts[corner][0]) * along
  const my = pts[corner][1] + (pts[next][1] - pts[corner][1]) * along
  const lit = shade.incidence >= cornerShade.litThreshold

  noStroke()
  fill(lit ? 255 : 0, cornerShade.opacity)
  beginShape()
  vertex(pts[prev][0], pts[prev][1])
  vertex(pts[corner][0], pts[corner][1])
  vertex(mx, my)
  endShape(CLOSE)
}

// Lambert term plus the light direction projected onto the face.
// The gradient runs from the shadowed side of the facet to the lit side.
function faceShade(face, lightDir) {
  const n = normalize3(face.outward)
  const incidence = Math.abs(dot3(n, lightDir))
  const along = dot3(n, lightDir)
  const axis = [lightDir[0] - n[0] * along, lightDir[1] - n[1] * along]
  const span = Math.hypot(axis[0], axis[1])
  if (span < 1e-4) return { incidence, flat: true }

  const ux = axis[0] / span
  const uy = axis[1] / span
  const pts = face.points
  let minC = Infinity
  let maxC = -Infinity
  let cx = 0
  let cy = 0
  for (let i = 0; i < pts.length; i++) {
    const coord = pts[i][0] * ux + pts[i][1] * uy
    if (coord < minC) minC = coord
    if (coord > maxC) maxC = coord
    cx += pts[i][0]
    cy += pts[i][1]
  }
  cx /= pts.length
  cy /= pts.length
  const mid = cx * ux + cy * uy
  return {
    incidence,
    flat: false,
    x0: cx + ux * (minC - mid),
    y0: cy + uy * (minC - mid),
    x1: cx + ux * (maxC - mid),
    y1: cy + uy * (maxC - mid),
  }
}

function drawBrushGradient(face, shade, {
  steps = 6,
  shadowOpacity = 28,
  litOpacity = 150,
  shadowBleed = 0.55,
  litBleed = 0.04,
  fadeToPaper = 0.4,
  minStrength = 0.55,
  incidenceGain = 0.45,
} = {}) {
  const pts = face.points
  const [r, g, b] = face.swatch
  const axis = gradientAxis(pts, shade)
  const ax = axis.x
  const ay = axis.y
  let minAlong = Infinity
  let maxAlong = -Infinity
  for (let i = 0; i < pts.length; i++) {
    const along = (pts[i][0] - axis.originX) * ax + (pts[i][1] - axis.originY) * ay
    if (along < minAlong) minAlong = along
    if (along > maxAlong) maxAlong = along
  }
  const span = maxAlong - minAlong || 1
  const strength = minStrength + incidenceGain * shade.incidence
  const ink = color(r, g, b)
  const paper = color(248)

  brush.noStroke()
  brush.noHatch()
  brush.noMass()

  let strokes = 0
  for (let bandIndex = 0; bandIndex < steps; bandIndex++) {
    const t0 = bandIndex / steps
    const t1 = (bandIndex + 1) / steps
    const t = (t0 + t1) / 2
    const overlap = (t1 - t0) * 0.35
    const band = clipBand(
      pts,
      ax,
      ay,
      axis.originX,
      axis.originY,
      minAlong + span * Math.max(0, t0 - overlap),
      minAlong + span * Math.min(1, t1 + overlap),
    )
    if (band.length < 3) continue

    const opacity = (shadowOpacity + (litOpacity - shadowOpacity) * t) * strength
    const bleed = shadowBleed + (litBleed - shadowBleed) * t
    brush.fill(lerpColor(ink, paper, (1 - t) * fadeToPaper), opacity)
    brush.fillBleed(bleed, bleed > 0.15 ? 'out' : undefined)
    brush.fillTexture(0.35, 0.08, false)
    brush.polygon(band)
    strokes++
  }
  brush.noFill()
  return strokes
}

function drawFaceLines(pts) {
  stroke(40, 90)
  strokeWeight(1)
  noFill()
  for (let i = 0; i < pts.length; i++) {
    const a = pts[i]
    const b = pts[(i + 1) % pts.length]
    line(a[0], a[1], b[0], b[1])
  }
}

function clipBand(pts, ax, ay, originX, originY, along0, along1) {
  let band = []
  for (let i = 0; i < pts.length; i++) band.push([pts[i][0], pts[i][1]])
  band = clipHalfPlane(band, ax, ay, originX, originY, along1, false)
  band = clipHalfPlane(band, ax, ay, originX, originY, along0, true)
  return band
}

function clipHalfPlane(poly, ax, ay, originX, originY, limit, keepGreater) {
  if (poly.length === 0) return []
  const side = (p) => (p[0] - originX) * ax + (p[1] - originY) * ay
  const out = []
  for (let i = 0; i < poly.length; i++) {
    const a = poly[i]
    const b = poly[(i + 1) % poly.length]
    const sa = side(a)
    const sb = side(b)
    const aIn = keepGreater ? sa >= limit - 1e-6 : sa <= limit + 1e-6
    const bIn = keepGreater ? sb >= limit - 1e-6 : sb <= limit + 1e-6
    if (aIn && bIn) {
      out.push(b)
    } else if (aIn !== bIn) {
      const denom = sb - sa
      const t = denom === 0 ? 0 : (limit - sa) / denom
      out.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
      if (bIn) out.push(b)
    }
  }
  return out
}

// Sparse marks along the light axis, drawn over the watercolor.
// Noise sets the gap between them, so the fade is uneven.
function drawPointGradient(face, shade, {
  gap = 10,
  mark = 2,
  noiseAmplitude = 0.65,
  sway = 0.7,
  stepJitter = 0.85,
  minStep = 1,
  rowShift = 0.5,
  drop = 0.12,
  shadowAlpha = 0.14,
  litAlpha = 0.64,
  toothMix = 0.25,
  minStrength = 0.55,
  incidenceGain = 0.45,
  rowNoiseScale = 0.08,
  stepNoiseScale = 0.12,
  swayNoiseScale = 0.2,
  toothNoiseScale = 0.4,
} = {}) {
  const pts = face.points
  const [r, g, b] = face.swatch
  const axis = gradientAxis(pts, shade)
  const ax = axis.x
  const ay = axis.y
  const px = -ay
  const py = ax

  let minAlong = Infinity
  let maxAlong = -Infinity
  let minAcross = Infinity
  let maxAcross = -Infinity
  for (let i = 0; i < pts.length; i++) {
    const dx = pts[i][0] - axis.originX
    const dy = pts[i][1] - axis.originY
    const along = dx * ax + dy * ay
    const across = dx * px + dy * py
    if (along < minAlong) minAlong = along
    if (along > maxAlong) maxAlong = along
    if (across < minAcross) minAcross = across
    if (across > maxAcross) maxAcross = across
  }
  const alongSpan = maxAlong - minAlong || 1
  const strength = minStrength + incidenceGain * shade.incidence
  const half = mark / 2

  push()
  // beginClip only rasterizes the mask when a fill is active. Face outlines
  // call noFill(), so without this the mask is empty after the first face.
  fill(255)
  beginClip()
  beginShape()
  for (let k = 0; k < pts.length; k++) vertex(pts[k][0], pts[k][1])
  endShape(CLOSE)
  endClip()

  noFill()

  strokeWeight(1.1)
  for (let across = minAcross; across <= maxAcross; across += gap) {
    const rowNoise = noise(across * rowNoiseScale, 1.3)
    let along = minAlong - gap * rowShift * rowNoise
    while (along <= maxAlong + gap) {
      const stepNoise = noise(along * stepNoiseScale, across * stepNoiseScale, 4.1)
      const place = along + (stepNoise - 0.5) * gap * noiseAmplitude
      const swayOffset = (noise(along * swayNoiseScale, across * swayNoiseScale, 6.2) - 0.5) * sway
      const x = axis.originX + ax * place + px * (across + swayOffset)
      const y = axis.originY + ay * place + py * (across + swayOffset)
      const t = Math.min(1, Math.max(0, (place - minAlong) / alongSpan))
      const tooth = noise(x * toothNoiseScale, y * toothNoiseScale, 9.1)
      if (tooth > drop) {
        const fade = shadowAlpha + (litAlpha - shadowAlpha) * t
        const markAlpha = fade * (1 - toothMix + toothMix * tooth) * strength
        stroke(r, g, b, markAlpha * 255)
        // line(x - ax * half, y - ay * half, x + ax * half, y + ay * half)
        let m = mark * random(0.5, 1)
        ellipse(x, y, m*3, m)
      }
      along += gap * (minStep + stepNoise * stepJitter)
    }
  }
  pop()
}

function gradientAxis(pts, shade) {
  if (!shade.flat) {
    const dx = shade.x1 - shade.x0
    const dy = shade.y1 - shade.y0
    const span = Math.hypot(dx, dy) || 1
    return { x: dx / span, y: dy / span, originX: shade.x0, originY: shade.y0 }
  }
  const bounds = pointBounds(pts)
  return { x: 1, y: 0, originX: bounds.minX, originY: (bounds.minY + bounds.maxY) / 2 }
}

function girdlePoints(kind, sides, radius, jitter) {
  if (kind === 'emerald') return emeraldGirdle(radius)

  const count = kind === 'free' ? Math.max(sides, 8) : sides
  const pts = []
  for (let i = 0; i < count; i++) {
    const angle = (i / count) * 360
    let r = radius
    if (kind === 'pear') r *= 0.75 + 0.25 * degCos(angle)
    if (jitter) r *= 1 + random(-jitter, jitter)
    let x = r * degCos(angle)
    let y = r * degSin(angle)
    if (kind === 'oval' || kind === 'pear') y *= 0.72
    pts.push([x, y])
  }

  let outline = pts
  if (kind === 'free') {
    const hull = convexHull(pts)
    if (hull.length >= 3) outline = hull
  }
  return outline.map((p) => [p[0], p[1], 0])
}

function emeraldGirdle(radius) {
  const halfW = radius
  const halfH = radius * 0.72
  const cut = radius * 0.28
  return [
    [halfW, halfH - cut],
    [halfW - cut, halfH],
    [-halfW + cut, halfH],
    [-halfW, halfH - cut],
    [-halfW, -halfH + cut],
    [-halfW + cut, -halfH],
    [halfW - cut, -halfH],
    [halfW, -halfH + cut],
  ].map((p) => [p[0], p[1], 0])
}

function convexHull(points) {
  const sorted = points.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1])
  if (sorted.length <= 2) return sorted.slice()

  const turn = (o, a, b) =>
    (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

  const lower = []
  for (let i = 0; i < sorted.length; i++) {
    while (
      lower.length >= 2 &&
      turn(lower[lower.length - 2], lower[lower.length - 1], sorted[i]) <= 0
    ) {
      lower.pop()
    }
    lower.push(sorted[i])
  }

  const upper = []
  for (let i = sorted.length - 1; i >= 0; i--) {
    while (
      upper.length >= 2 &&
      turn(upper[upper.length - 2], upper[upper.length - 1], sorted[i]) <= 0
    ) {
      upper.pop()
    }
    upper.push(sorted[i])
  }

  lower.pop()
  upper.pop()
  return lower.concat(upper)
}

function outwardNormal(points3d) {
  const a = points3d[0]
  const b = points3d[1]
  const c = points3d[2]
  const ux = b[0] - a[0]
  const uy = b[1] - a[1]
  const uz = b[2] - a[2]
  const vx = c[0] - a[0]
  const vy = c[1] - a[1]
  const vz = c[2] - a[2]
  return [uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx]
}

function rotatePoint(xyz, rotation) {
  let x = xyz[0]
  let y = xyz[1]
  let z = xyz[2]
  ;[x, y, z] = rotateAboutZ(x, y, z, rotation[2])
  ;[x, y, z] = rotateAboutY(x, y, z, rotation[1])
  ;[x, y, z] = rotateAboutX(x, y, z, rotation[0])
  return [x, y, z]
}

function rotateAboutX(x, y, z, angle) {
  const c = degCos(angle)
  const s = degSin(angle)
  return [x, c * y - s * z, s * y + c * z]
}

function rotateAboutY(x, y, z, angle) {
  const c = degCos(angle)
  const s = degSin(angle)
  return [c * x + s * z, y, -s * x + c * z]
}

function rotateAboutZ(x, y, z, angle) {
  const c = degCos(angle)
  const s = degSin(angle)
  return [c * x - s * y, s * x + c * y, z]
}

function degCos(angle) {
  return Math.cos((angle * Math.PI) / 180)
}

function degSin(angle) {
  return Math.sin((angle * Math.PI) / 180)
}

function triangulate(polygon) {
  const triangles = []
  if (polygon.length < 3) return triangles
  const remaining = polygon.slice()
  let index = 0
  let guard = remaining.length * remaining.length

  while (remaining.length > 3 && guard > 0) {
    guard -= 1
    const a = remaining[index % remaining.length]
    const b = remaining[(index + 1) % remaining.length]
    const c = remaining[(index + 2) % remaining.length]
    if (isConvexCorner(a, b, c) && !pointInEar(remaining, index)) {
      triangles.push([a, b, c])
      remaining.splice((index + 1) % remaining.length, 1)
      index = 0
    } else {
      index += 1
    }
  }

  if (remaining.length >= 3) triangles.push([remaining[0], remaining[1], remaining[2]])
  return triangles
}

function isConvexCorner(a, b, c) {
  return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0
}

function pointInEar(polygon, index) {
  const count = polygon.length
  const a = polygon[index % count]
  const b = polygon[(index + 1) % count]
  const c = polygon[(index + 2) % count]
  for (let i = 0; i < count; i++) {
    if (i === index % count || i === (index + 1) % count || i === (index + 2) % count) continue
    if (isPointInTriangle(polygon[i], a, b, c)) return true
  }
  return false
}

function isPointInTriangle(p, a, b, c) {
  const c1 = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
  const c2 = (c[0] - b[0]) * (p[1] - b[1]) - (c[1] - b[1]) * (p[0] - b[0])
  const c3 = (a[0] - c[0]) * (p[1] - c[1]) - (a[1] - c[1]) * (p[0] - c[0])
  const hasNeg = c1 < -1e-8 || c2 < -1e-8 || c3 < -1e-8
  const hasPos = c1 > 1e-8 || c2 > 1e-8 || c3 > 1e-8
  return !(hasNeg && hasPos)
}

function trianglesOverlap(triA, triB) {
  const [a1, b1, c1] = triA
  const [a2, b2, c2] = triB
  const minAx = Math.min(a1[0], b1[0], c1[0])
  const maxAx = Math.max(a1[0], b1[0], c1[0])
  const minBx = Math.min(a2[0], b2[0], c2[0])
  const maxBx = Math.max(a2[0], b2[0], c2[0])
  const minAy = Math.min(a1[1], b1[1], c1[1])
  const maxAy = Math.max(a1[1], b1[1], c1[1])
  const minBy = Math.min(a2[1], b2[1], c2[1])
  const maxBy = Math.max(a2[1], b2[1], c2[1])
  if (maxAx < minBx || maxBx < minAx || maxAy < minBy || maxBy < minAy) return false

  if (
    isPointInTriangle(a1, a2, b2, c2) ||
    isPointInTriangle(b1, a2, b2, c2) ||
    isPointInTriangle(c1, a2, b2, c2) ||
    isPointInTriangle(a2, a1, b1, c1) ||
    isPointInTriangle(b2, a1, b1, c1) ||
    isPointInTriangle(c2, a1, b1, c1)
  ) {
    return true
  }

  const edgesA = [[a1, b1], [b1, c1], [c1, a1]]
  const edgesB = [[a2, b2], [b2, c2], [c2, a2]]
  for (let i = 0; i < edgesA.length; i++) {
    for (let k = 0; k < edgesB.length; k++) {
      if (segmentsIntersect(edgesA[i][0], edgesA[i][1], edgesB[k][0], edgesB[k][1])) return true
    }
  }
  return false
}

function segmentsIntersect(p1, q1, p2, q2) {
  const o1 = orientation(p1, q1, p2)
  const o2 = orientation(p1, q1, q2)
  const o3 = orientation(p2, q2, p1)
  const o4 = orientation(p2, q2, q1)
  if (o1 !== o2 && o3 !== o4) return true
  if (o1 === 0 && onSegment(p1, p2, q1)) return true
  if (o2 === 0 && onSegment(p1, q2, q1)) return true
  if (o3 === 0 && onSegment(p2, p1, q2)) return true
  if (o4 === 0 && onSegment(p2, q1, q2)) return true
  return false
}

function orientation(p, q, r) {
  const val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
  if (Math.abs(val) < 1e-8) return 0
  return val > 0 ? 1 : 2
}

function onSegment(p, q, r) {
  return (
    q[0] <= Math.max(p[0], r[0]) &&
    q[0] >= Math.min(p[0], r[0]) &&
    q[1] <= Math.max(p[1], r[1]) &&
    q[1] >= Math.min(p[1], r[1])
  )
}

