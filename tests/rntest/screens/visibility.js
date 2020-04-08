import React, { Component } from 'react'
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native'

export default class Visibility extends Component<{}> {
  constructor(props) {
    super(props)
    this.state = { feedback: '' }
  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>Visibility mobile tests</Text>
        <TouchableOpacity
          onPress={() => {
            this.setState({ feedback: 'Touchable opacity pressed' })
          }}
          accessibilityLabel="TouchableOpacity"
        >
          <Text>Touchable opacity with accessibilityLabel</Text>
        </TouchableOpacity>
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
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
})
