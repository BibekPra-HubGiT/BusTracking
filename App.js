// AppNavigation.js
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { NavigationContainer } from '@react-navigation/native';

// Import screens
import SplashScreen from './src/Screens/SplashScreen';
import SplashScreen1 from './src/Screens/SplashScreen1';
import SplashScreen2 from './src/Screens/SplashScreen2';
import SplashScreen3 from './src/Screens/SplashScreen3';
import LoginScreen from './src/Screens/LoginScreen';
import RegisterScreen from './src/Screens/RegisterScreen';
import UserDashboard from './src/Screens/UserDashboard';
import BusRoute from './src/Screens/BusRoute'
// import CustomerDrawerContent from './src/Screens/CustomDrawerContent'
import AccountScreen from './src/Screens/Account'

const Stack = createNativeStackNavigator();

const AppNavigation = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator 
        initialRouteName="SplashScreen"
        screenOptions={{ headerShown: false }} 
      >
        <Stack.Screen name="SplashScreen" component={SplashScreen} />
        <Stack.Screen name="SplashScreen1" component={SplashScreen1} />
        <Stack.Screen name="SplashScreen2" component={SplashScreen2} />
        <Stack.Screen name="SplashScreen3" component={SplashScreen3} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="UserDashboard" component={UserDashboard} />
        <Stack.Screen name="BusRoute" component={BusRoute}/>
        {/* <Stack.Screen name="CustomerDrawerContent" component={CustomerDrawerContent} /> */}
        <Stack.Screen name="AccountScreen" component={AccountScreen}/>
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigation;
