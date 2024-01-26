import React from 'react';

type ContainerProps = {
  styles: React.CSSProperties;
};

export default function Container(props: ContainerProps) {
  return <div style={props.styles}>Container</div>;
}
