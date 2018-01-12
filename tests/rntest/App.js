/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from "react";
import {
  Platform,
  StyleSheet,
  Text,
  View,
  Button,
  TouchableOpacity,
  TextInput
} from "react-native";

const instructions = Platform.select({
  ios: "Press Cmd+R to reload,\n" + "Cmd+D or shake for dev menu",
  android:
    "Double tap R on your keyboard to reload,\n" +
    "Shake or press menu button for dev menu"
});

export default class App extends Component<{}> {
  constructor(props) {
    super(props);
    this.state = { feedback: "" };
  }
  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>Behaving mobile tests</Text>
        <Text>{this.state.feedback}</Text>
        <TextInput
          style={styles.input}
          onChangeText={v => this.setState({ feedback: `You typed: ${v}` })}
          accessibilityLabel="Text Input"
        />

        <Button
          title="Normal button"
          onPress={() => {
            this.setState({ feedback: "Normal button pressed" });
          }}
        />
        <TouchableOpacity
          onPress={() => {
            this.setState({ feedback: "Touchable opacity pressed" });
          }}
          accessibilityLabel="Touchable opacity"
        >
          <Text>Touchable Opacity</Text>
        </TouchableOpacity>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#F5FCFF"
  },
  input: {
    borderColor: "gray",
    borderBottomWidth: 1,
    width: "80%"
  },
  welcome: {
    fontSize: 20,
    textAlign: "center",
    margin: 10
  },
  instructions: {
    textAlign: "center",
    color: "#333333",
    marginBottom: 5
  }
});
