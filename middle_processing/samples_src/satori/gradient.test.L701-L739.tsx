  it('should support conic gradients', async () => {
    const box = (style) => (
      <div style={{ width: 70, height: 70, margin: 4, ...style }} />
    )
    const svg = await satori(
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          width: 240,
          height: 160,
          background: '#fff',
        }}
      >
        {box({
          backgroundImage:
            'conic-gradient(red, yellow, lime, aqua, blue, magenta, red)',
          borderRadius: 35,
        })}
        {box({
          backgroundImage: 'conic-gradient(from 45deg at 30% 40%, #f60, #0af)',
        })}
        {box({
          backgroundImage: 'repeating-conic-gradient(#999 0 25%, #fff 0 50%)',
          backgroundSize: '20px 20px',
        })}
        {box({
          background: 'conic-gradient(rgba(255,0,0,1), rgba(0,0,255,0)), #fc0',
        })}
        {box({ backgroundImage: 'conic-gradient(red, 20%, blue)' })}
        {box({
          background: '#0af',
          maskImage: 'conic-gradient(black, transparent)',
        })}
      </div>,
      { width: 240, height: 160, fonts }
    )
    expect(await toImage(svg, 240)).toMatchImageSnapshot()
  })
