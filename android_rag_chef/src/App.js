import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {createStackNavigator} from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialIcons';
import {StatusBar, StyleSheet} from 'react-native';

// Screens
import HomeScreen from './screens/HomeScreen';
import CameraScreen from './screens/CameraScreen';
import RecipesScreen from './screens/RecipesScreen';
import TimerScreen from './screens/TimerScreen';
import ProfileScreen from './screens/ProfileScreen';
import RecipeDetailScreen from './screens/RecipeDetailScreen';

// Services
import {APIService} from './services/APIService';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Main Tab Navigator
function MainTabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({route}) => ({
        tabBarIcon: ({focused, color, size}) => {
          let iconName;

          if (route.name === 'Home') {
            iconName = 'home';
          } else if (route.name === 'Camera') {
            iconName = 'camera-alt';
          } else if (route.name === 'Recipes') {
            iconName = 'restaurant';
          } else if (route.name === 'Timer') {
            iconName = 'timer';
          } else if (route.name === 'Profile') {
            iconName = 'person';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#FF6B35',
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: styles.tabBar,
        headerStyle: {
          backgroundColor: '#FF6B35',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}>
      <Tab.Screen 
        name="Home" 
        component={HomeScreen} 
        options={{title: 'Chef RAG'}}
      />
      <Tab.Screen 
        name="Camera" 
        component={CameraScreen} 
        options={{title: 'Capturar'}}
      />
      <Tab.Screen 
        name="Recipes" 
        component={RecipesScreen} 
        options={{title: 'Receitas'}}
      />
      <Tab.Screen 
        name="Timer" 
        component={TimerScreen} 
        options={{title: 'Timer'}}
      />
      <Tab.Screen 
        name="Profile" 
        component={ProfileScreen} 
        options={{title: 'Perfil'}}
      />
    </Tab.Navigator>
  );
}

// Root Stack Navigator
function App() {
  return (
    <NavigationContainer>
      <StatusBar barStyle="light-content" backgroundColor="#FF6B35" />
      <Stack.Navigator>
        <Stack.Screen 
          name="MainTabs" 
          component={MainTabNavigator} 
          options={{headerShown: false}}
        />
        <Stack.Screen 
          name="RecipeDetail" 
          component={RecipeDetailScreen}
          options={{
            title: 'Detalhes da Receita',
            headerStyle: {
              backgroundColor: '#FF6B35',
            },
            headerTintColor: '#fff',
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  tabBar: {
    backgroundColor: '#fff',
    borderTopColor: '#ddd',
    borderTopWidth: 1,
    paddingBottom: 5,
    paddingTop: 5,
    height: 60,
  },
});

export default App;