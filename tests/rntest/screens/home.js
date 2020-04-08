import React, { Component } from 'react'
import { StyleSheet, View, Button } from 'react-native'

export default class Home extends Component {
  constructor(props) {
    super(props)
    this.state = { feedback: '' }
  }
  render() {
    const { navigate } = this.props.navigation
    return (
      <View style={styles.container}>
        <Button
          accessibilityLabel="Visibility"
          title="Visibility"
          onPress={() => navigate('Visibility')}
        />
        <Button
          accessibilityLabel="Touches"
          title="Touches"
          onPress={() => navigate('Touches')}
        />
        <Button
          accessibilityLabel="Input"
          title="Input"
          onPress={() => navigate('Input')}
        />
        <Button
          accessibilityLabel="Auth"
          title="Auth"
          onPress={() => navigate('Auth')}
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
    position: 'absolute',
    top: 100,
    width: 100,
    height: 100,
    backgroundColor: 'red',
  },
})
