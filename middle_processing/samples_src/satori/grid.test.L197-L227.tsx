  it('should place items in named areas', async () => {
    const image = await render(
      <div
        style={{
          display: 'grid',
          width: '100%',
          height: '100%',
          gridTemplateAreas: '"header header" "sidebar main" "footer footer"',
          gridTemplateColumns: '60px 1fr',
          gridTemplateRows: '30px 1fr 24px',
          gap: 4,
          padding: 4,
          background: '#eee',
        }}
      >
        <Cell i={5} style={{ gridArea: 'footer' }}>
          footer
        </Cell>
        <Cell i={0} style={{ gridArea: 'header' }}>
          header
        </Cell>
        <Cell i={1} style={{ gridArea: 'main' }}>
          main
        </Cell>
        <Cell i={2} style={{ gridArea: 'sidebar' }}>
          sidebar
        </Cell>
      </div>
    )
    expect(image).toMatchImageSnapshot()
  })
