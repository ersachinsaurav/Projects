import React from 'react';

type OscarProps = {
  children: React.ReactNode;
};

export default function Oscar(props: OscarProps) {
  return <div>{props.children}</div>;
}
