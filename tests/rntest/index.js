/**
 * @format
 */

import { AppRegistry } from 'react-native'
import { Home, Touches, Visibility, Input } from './screens'
import { name as appName } from './app.json'
import { createAppContainer } from 'react-navigation'
import { createStackNavigator } from 'react-navigation-stack'

const MainNavigator = createStackNavigator({
  Home: { screen: Home },
  Touches: { screen: Touches },
  Visibility: { screen: Visibility },
  Input: { screen: Input },
})

const App = createAppContainer(MainNavigator)
AppRegistry.registerComponent(appName, () => App)
