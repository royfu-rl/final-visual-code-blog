  {
    name: 'arc-lnglat-3d',
    viewState: {
      latitude: 37.788,
      longitude: -122.45,
      zoom: 13,
      pitch: 60,
      bearing: 0
    },
    layers: [
      new ArcLayer({
        id: 'arc-lnglat-3d',
        data: [
          {source: [-122.46, 37.77, -150], target: [-122.44, 37.77, 450], height: 0.5},
          {source: [-122.46, 37.77, -150], target: [-122.44, 37.77, 450], height: 1},
          {source: [-122.46, 37.77, -150], target: [-122.44, 37.77, 450], height: 2},
          {source: [-122.46, 37.78, 600], target: [-122.44, 37.78, 0], height: 0.5},
          {source: [-122.46, 37.78, 600], target: [-122.44, 37.78, 0], height: 1},
          {source: [-122.46, 37.78, 600], target: [-122.44, 37.78, 0], height: 2}
        ],
        opacity: 0.8,
        getWidth: 4,
        getSourcePosition: d => d.source,
        getTargetPosition: d => d.target,
        getHeight: d => d.height,
        getSourceColor: [255, 255, 0],
        getTargetColor: [255, 0, 0]
      })
    ],
    goldenImage: './test/render/golden-images/arc-lnglat-3d.png'
  },
