  {
    name: 'h3-hexagon-layer',
    viewState: {
      latitude: 37.78,
      longitude: -122.45,
      zoom: 11,
      pitch: 30,
      bearing: 0
    },
    layers: [
      new H3HexagonLayer({
        data: gridDisk('882830829bfffff', 4),
        opacity: 0.8,
        getHexagon: d => d,
        getFillColor: (d, {index}) => [255, index * 5, 0],
        getElevation: (d, {index}) => index * 100
      })
    ],
    goldenImage: './test/render/golden-images/h3-hexagon.png'
  },
