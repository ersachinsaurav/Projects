import React from 'react';

type ListProps<ListGenericsProps> = {
  items: ListGenericsProps[];
  onClick: (value: ListGenericsProps) => void;
};

// ListGenericsProps is an array of object and each object must have an id attribute
const List = <ListGenericsProps extends { id: number }>({
  items,
  onClick,
}: ListProps<ListGenericsProps>) => {
  return (
    <div>
      <h2>List of Items</h2>
      {items.map((item, index) => {
        return (
          <div key={index} onClick={() => onClick(item)}>
            {JSON.stringify(item)}
          </div>
        );
      })}
    </div>
  );
};

export default List;
