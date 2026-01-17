import { reactive } from 'vue';

const colorPalette = [
  'rgba(54, 162, 235, 0.8)',  // Blue
  'rgba(255, 99, 132, 0.8)',  // Pink/Red
  'rgba(75, 192, 192, 0.8)',  // Teal
  'rgba(255, 206, 86, 0.8)',  // Yellow
  'rgba(153, 102, 255, 0.8)', // Purple
  'rgba(255, 159, 64, 0.8)',  // Orange
  'rgba(83, 211, 87, 0.8)',   // Green
  'rgba(237, 100, 166, 0.8)', // Magenta
];

const categoryColorMap = reactive(new Map());

export function useColorPalette() {
  const precomputeColorsForAttribute = (data, attribute) => {
    categoryColorMap.clear();
    let values;
    if (attribute === 'Language') {
      values = data.map(item => {
        const rawValue = item.Language;
        if (!rawValue) return null;
        const firstVal = Array.isArray(rawValue) ? rawValue[0] : String(rawValue);
        return firstVal.split(/[,;]+/)[0].trim();
      }).filter(Boolean);
    } else {
        values = data.map(item => item[attribute]).flat().filter(Boolean);
    }
    const allValues = new Set(values);
    Array.from(allValues).sort().forEach((value, index) => {
        const colorIndex = index % colorPalette.length;
        categoryColorMap.set(value, colorPalette[colorIndex]);
    });
  };

  const getColorForCategory = (category) => {
    if (!categoryColorMap.has(category)) {
      // Fallback for categories that might not have been precomputed
      const colorIndex = categoryColorMap.size % colorPalette.length;
      categoryColorMap.set(category, colorPalette[colorIndex]);
    }
    return categoryColorMap.get(category);
  };

  const getBorderColor = (category) => {
    const bgColor = getColorForCategory(category);
    if (bgColor) {
      return bgColor.replace('0.8', '1'); // Full opacity for borders
    }
    return 'rgba(0,0,0,1)'; // Default border for un-colored categories
  };

  const resetColors = () => {
    categoryColorMap.clear();
  };

  return {
    getColorForCategory,
    getBorderColor,
    resetColors,
    colorPalette,
    precomputeColorsForAttribute,
    categoryColorMap
  };
}
