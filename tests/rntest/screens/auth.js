/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react'
import { StyleSheet, Text, View, Button } from 'react-native'
import TouchID from 'react-native-touch-id'

export default class Auth extends Component<{}> {
  constructor(props) {
    super(props)
    this.state = { feedback: '' }
  }

  requestTouchId = () => {
    TouchID.authenticate('to test TouchId')
      .then(success => {
        this.setState({ feedback: 'TouchId success' })
      })
      .catch(error => {
        this.setState({ feedback: 'TouchId failure' })
      })
  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>TouchId/FaceId mobile tests</Text>
        <Text>{this.state.feedback}</Text>

        <Button
          accessibilityLabel="Request TouchId"
          title="Request TouchId"
          onPress={() => this.requestTouchId()}
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
