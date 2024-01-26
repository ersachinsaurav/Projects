import React from 'react';

type CounterProps = {
  message: string;
};

type CounterState = {
  count: number;
};

export class CCounter extends React.Component<CounterProps, CounterState> {
  state = { count: 0 };

  handleClick = () => {
    this.setState((previousState) => ({ count: previousState.count + 1 }));
  };

  render() {
    return (
      <div>
        <button onClick={this.handleClick}>Increment</button>
        {this.props.message} {this.state.count}
      </div>
    );
  }
}
