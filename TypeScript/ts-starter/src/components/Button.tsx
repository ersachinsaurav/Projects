import React from 'react';

type ButtonProps = {
  // handleClick: () => void;
  handleClick: (event: React.MouseEvent<HTMLButtonElement>, id: number) => void;
};

export default function Button(props: ButtonProps) {
  return (
    <div>
      <div>
        <button onClick={(event) => props.handleClick(event, 1)}>Button</button>
      </div>
    </div>
  );
}
