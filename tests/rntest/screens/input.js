import React, { Component } from 'react'
import { StyleSheet, Text, View, TextInput } from 'react-native'

export default class App extends Component<{}> {
  constructor(props) {
    super(props)
    this.state = { feedback: '', inputValue: 'Default value' }
  }
  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>Input mobile tests</Text>
        <Text>{this.state.feedback}</Text>
        <TextInput
          style={styles.input}
          onChangeText={v => this.setState({ feedback: `You typed: ${v}` })}
          accessibilityLabel="Text Input"
          underlineColorAndroid="transparent"
        />
        <TextInput
          style={styles.input}
          value={this.state.inputValue}
          onChangeText={v =>
            this.setState({ feedback: `You typed: ${v}`, inputValue: v })
          }
          accessibilityLabel="Prefilled Input"
          underlineColorAndroid="transparent"
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
