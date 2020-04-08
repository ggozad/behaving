/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react'
import {
  StyleSheet,
  Text,
  View,
  Button,
  TouchableOpacity,
  Switch,
  TextInput,
} from 'react-native'

export default class Touches extends Component<{}> {
  constructor(props) {
    super(props)
    this.state = { feedback: '' }
  }
  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>Touch mobile tests</Text>
        <Text>{this.state.feedback}</Text>

        <TouchableOpacity
          onPress={ev => {
            this.setState({
              feedback: `Tap at ${ev.nativeEvent.locationX}, ${ev.nativeEvent.locationY}`,
            })
          }}
          style={styles.touchableBox}
        />
        <Button
          title="Normal button"
          onPress={() => {
            this.setState({ feedback: 'Normal button pressed' })
          }}
        />
        <TouchableOpacity
          onPress={() => {
            this.setState({ feedback: 'Touchable opacity pressed' })
          }}
          accessibilityLabel="TouchableOpacity"
        >
          <Text>Touchable opacity with accessibilityLabel</Text>
        </TouchableOpacity>
        <Switch
          value={false}
          accessibilityLabel="switch"
          onValueChange={val => {
            this.setState({ feedback: 'Switch pressed' })
          }}
        />
      </View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  touchableBox: {
    width: 100,
    height: 100,
    backgroundColor: 'red',
  },
  input: {
    borderColor: 'gray',
    borderBottomWidth: 1,
    width: '80%',
    marginBottom: 10,
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
})
