import React from 'react';

type TextOwnProps<customElement extends React.ElementType> = {
  size?: 'sm' | 'md' | 'lg';
  color?: 'primary' | 'secondary';
  children: React.ReactNode;
  as?: customElement;
};

type TextProps<customElement extends React.ElementType> =
  TextOwnProps<customElement> &
    Omit<
      React.ComponentProps<customElement>,
      keyof TextOwnProps<customElement>
    >;

const Text = <customElement extends React.ElementType = 'div'>({
  size,
  color,
  children,
  as,
}: TextProps<customElement>) => {
  const HtmlElement = as || 'div';

  return (
    <HtmlElement className={`class-with-${size}-${color}`}>
      {children}
    </HtmlElement>
  );
};

export default Text;
