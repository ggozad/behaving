import React, { Component } from 'react'
import { StyleSheet, Text, View, TextInput, ScrollView } from 'react-native'

export default class Scroll extends Component {
  state = {
    names: [
      'Ben',
      'Susan',
      'Robert',
      'Mary',
      'Daniel',
      'Laura',
      'John',
      'Debra',
      'Aron',
      'Emma',
      'Ann',
      'Steve',
      'Charlotte',
      'Ava',
      'Sophia',
      'Olivia',
    ],
  }
  render() {
    return (
      <ScrollView>
        {this.state.names.map((item, index) => (
          <View key={index}>
            <Text accessibilityId={item} style={styles.item}>
              {item}
            </Text>
          </View>
        ))}
      </ScrollView>
    )
  }
}

const styles = StyleSheet.create({
  item: {
    fontSize: 50,
  },
})
