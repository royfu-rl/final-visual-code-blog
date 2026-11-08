  {
    name: 'terrain-layer',
    viewState: {
      longitude: -122.45,
      latitude: 37.75,
      zoom: 11.5,
      pitch: 60,
      bearing: 0
    },
    layers: [
      new TerrainLayer({
        elevationData: ELEVATION_DATA,
        texture: TEXTURE,
        elevationDecoder: DECODER
      })
    ],
    goldenImage: './test/render/golden-images/terrain-layer.png'
  },
