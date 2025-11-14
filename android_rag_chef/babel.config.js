module.exports = function(api) {
  api.cache(true);
  
  return {
    presets: ['module:metro-react-native-babel-preset'],
    plugins: [
      // Removido react-native-reanimated/plugin temporariamente
    ],
  };
};