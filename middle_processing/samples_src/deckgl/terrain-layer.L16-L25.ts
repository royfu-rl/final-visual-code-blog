const ELEVATION_DATA = '/test/data/terrain-tiles/{z}/{x}/{y}.png';
const TEXTURE = '/test/data/raster-tiles/{z}/{x}/{y}.png';
// https://www.mapzen.com/blog/terrain-tile-service/
// Exageration added for testing purpose
const DECODER = {
  rScaler: 256 * 4,
  gScaler: 1 * 4,
  bScaler: (1 / 256) * 4,
  offset: -32768 * 4
};
