import React from 'react';

type HeadingProps = {
  children: string;
};

export default function Heading(props: HeadingProps) {
  return (
    <div>
      <div>{props.children}</div>
    </div>
  );
}
