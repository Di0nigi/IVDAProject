import { reactive } from 'vue';

const colorPalette = [
  'rgba(54, 162, 235, 0.8)',  // Blue
  'rgba(255, 99, 132, 0.8)',  // Pink/Red
  'rgba(75, 192, 192, 0.8)',  // Teal
  'rgba(255, 206, 86, 0.8)',  // Yellow
  'rgba(153, 102, 255, 0.8)', // Purple
  'rgba(255, 159, 64, 0.8)',  // Orange
  'rgba(201, 203, 207, 0.8)', // Grey
  'rgba(83, 211, 87, 0.8)',   // Green
  'rgba(237, 100, 166, 0.8)', // Magenta
];

const categoryColorMap = reactive(new Map());

export function useColorPalette() {
  const getColorForCategory = (category) => {
    if (!categoryColorMap.has(category)) {
      const colorIndex = categoryColorMap.size % colorPalette.length;
      categoryColorMap.set(category, colorPalette[colorIndex]);
    }
    return categoryColorMap.get(category);
  };

  const getBorderColor = (category) => {
    const bgColor = getColorForCategory(category);
    return bgColor.replace('0.8', '1'); // Full opacity for borders
  };

  const resetColors = () => {
    categoryColorMap.clear();
  };

  return {
    getColorForCategory,
    getBorderColor,
    resetColors,
    colorPalette
  };
}
