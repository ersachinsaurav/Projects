import React from 'react';

type CustomInputProps = React.ComponentProps<'input'>;

const CustomInput = (props: CustomInputProps) => {
  return <input {...props} />;
};

export default CustomInput;
