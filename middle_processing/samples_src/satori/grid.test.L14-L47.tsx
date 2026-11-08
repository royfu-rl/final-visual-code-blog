const colors = [
  '#e11d48',
  '#2563eb',
  '#16a34a',
  '#9333ea',
  '#ea580c',
  '#0891b2',
]

function Cell({ i = 0, style, children }: any) {
  return (
    <div
      style={{
        background: colors[i % colors.length],
        color: 'white',
        fontSize: 14,
        padding: 4,
        ...style,
      }}
    >
      {children ?? String(i + 1)}
    </div>
  )
}

const cells = (count: number) =>
  Array.from({ length: count }, (_, i) => <Cell key={i} i={i} />)

describe('grid', () => {
  let fonts
  initFonts((f) => (fonts = f))

  const render = async (element: any, width = 200, height = 150) =>
    toImage(await satori(element, { width, height, fonts }), width)
